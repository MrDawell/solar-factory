import os
import argparse
import datetime
import time
import json
import logging
import csv
from enricher import enrich_lead
from compiler import compile_website_data
from indexer import add_batch_to_index

def setup_logger(log_dir):
    """Set up file and stream logging for the batch run."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'pipeline.log')
    
    logger = logging.getLogger('PipelineOrchestrator')
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        logger.handlers.clear()
        
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger, log_file

def run_pipeline(batch_date, base_dir, template_dir, template_name):
    """Orchestrate the entire batch pipeline for a specific date using unique business folders."""
    batch_dir = os.path.join(base_dir, 'data', batch_date)
    
    # Support both new YYYY-MM-DD/leads/leads.csv and backward compatible YYYY-MM-DD/leads.csv
    leads_csv_new = os.path.join(batch_dir, 'leads', 'leads.csv')
    leads_csv_old = os.path.join(batch_dir, 'leads.csv')
    
    if os.path.exists(leads_csv_new):
        leads_csv = leads_csv_new
    elif os.path.exists(leads_csv_old):
        leads_csv = leads_csv_old
    else:
        print(f"Error: Leads file not found for date {batch_date}.")
        print(f"Expected at: {leads_csv_new} or {leads_csv_old}")
        return False
        
    logs_dir = os.path.join(batch_dir, 'logs')
    logger, log_file_path = setup_logger(logs_dir)
    logger.info(f"Starting Solar Website Factory Pipeline for batch: {batch_date}")
    logger.info(f"Leads CSV source: {leads_csv}")
    
    pipeline_start = time.time()
    date_compact = batch_date.replace('-', '')
    
    # Read leads
    leads = []
    with open(leads_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Business Name", "").strip():
                leads.append(row)
                
    total_leads = len(leads)
    logger.info(f"Found {total_leads} leads to process.")
    
    batch_index_entries = {}
    success_count = 0
    
    for i, row in enumerate(leads, start=1):
        # Generate Unique ID SLR-YYYYMMDD-XXX
        unique_id = f"SLR-{date_compact}-{i:03d}"
        business_name = row.get("Business Name", "Local Solar Solutions").strip()
        logger.info(f"[{i}/{total_leads}] Processing: {unique_id} ({business_name})")
        
        # 1. Create dedicated folder
        biz_dir = os.path.join(batch_dir, unique_id)
        os.makedirs(biz_dir, exist_ok=True)
        
        # Filename targets
        json_path = os.path.join(biz_dir, "business.json")
        html_path = os.path.join(biz_dir, "index.html")
        meta_path = os.path.join(biz_dir, "metadata.json")
        
        try:
            # 2. Enrich Lead
            enrich_start = time.time()
            business_data = enrich_lead(row, unique_id)
            enrich_duration = time.time() - enrich_start
            
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(business_data, jf, indent=4, ensure_ascii=False)
                
            # 3. Compile Website
            compile_start = time.time()
            compile_website_data(business_data, template_dir, template_name, html_path)
            compile_duration = time.time() - compile_start
            
            # 4. Generate Metadata
            lead_source = os.path.basename(leads_csv)
            timestamp_now = datetime.datetime.now().isoformat()
            
            metadata = {
                "business_id": unique_id,
                "business_name": business_name,
                "slug": business_data.get("slug"),
                "lead_source": lead_source,
                "date_created": timestamp_now,
                "template_version": template_name,
                "status": {
                    "enrichment": "SUCCESS",
                    "compilation": "SUCCESS",
                    "whatsapp_outreach": "PENDING"
                },
                "history": [
                    {
                        "timestamp": timestamp_now,
                        "action": "IMPORT_LEAD",
                        "details": f"Imported lead from {lead_source}"
                    },
                    {
                        "timestamp": timestamp_now,
                        "action": "ENRICH_DATA",
                        "details": f"Successfully enriched data in {enrich_duration:.4f}s"
                    },
                    {
                        "timestamp": timestamp_now,
                        "action": "COMPILE_WEBSITE",
                        "details": f"Compiled index.html in {compile_duration:.4f}s"
                    }
                ]
            }
            
            with open(meta_path, 'w', encoding='utf-8') as mf:
                json.dump(metadata, mf, indent=4, ensure_ascii=False)
                
            # 5. Save to batch index mapping (to write to global index.json)
            batch_index_entries[unique_id] = {
                "business_name": business_name,
                "city": business_data["location"]["city"],
                "state": business_data["location"]["state"],
                "batch_date": batch_date,
                "status": "SUCCESS",
                "path": f"data/{batch_date}/{unique_id}"
            }
            
            success_count += 1
            logger.info(f"Successfully generated website for {unique_id}")
            
        except Exception as e:
            logger.error(f"Failed to process {unique_id}: {e}", exc_info=True)
            # Add failed status to batch index
            batch_index_entries[unique_id] = {
                "business_name": business_name,
                "city": row.get("City", "Unknown"),
                "state": row.get("State", "Unknown"),
                "batch_date": batch_date,
                "status": "FAILED",
                "path": f"data/{batch_date}/{unique_id}"
            }
            
    # Update global index.json once at the end of the batch
    logger.info("Updating Global Search Index...")
    add_batch_to_index(batch_index_entries, base_dir)
    
    total_duration = time.time() - pipeline_start
    
    # Save overall summary
    summary = {
        "batch_date": batch_date,
        "run_timestamp": datetime.datetime.now().isoformat(),
        "leads_processed": total_leads,
        "websites_compiled": success_count,
        "timings": {
            "total_pipeline_seconds": round(total_duration, 4)
        },
        "average_speed_per_site_seconds": round(total_duration / max(success_count, 1), 4),
        "status": "SUCCESS" if (success_count == total_leads and total_leads > 0) else "PARTIAL_SUCCESS"
    }
    
    summary_path = os.path.join(logs_dir, 'run_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as sf:
        json.dump(summary, sf, indent=4)
        
    logger.info("=" * 60)
    logger.info(f"Pipeline finished in {total_duration:.4f} seconds!")
    logger.info(f"Total Leads Processed: {total_leads}")
    logger.info(f"Total Websites Generated: {success_count}")
    logger.info(f"Logs: {log_file_path}")
    logger.info("=" * 60)
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solar Website Factory Batch Pipeline")
    parser.add_argument(
        "--date", 
        type=str, 
        default=datetime.date.today().strftime("%Y-%m-%d"),
        help="Batch date in YYYY-MM-DD format (default: today)"
    )
    
    args = parser.parse_args()
    
    src_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(src_dir)
    template_dir = os.path.join(src_dir, 'templates')
    template_name = 'template.html'
    
    success = run_pipeline(
        batch_date=args.date,
        base_dir=base_dir,
        template_dir=template_dir,
        template_name=template_name
    )
    
    import sys
    if not success:
        sys.exit(1)
