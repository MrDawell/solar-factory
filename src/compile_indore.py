import os
import json
import time
import datetime
from compiler import compile_website_data
from indexer import add_batch_to_index

def compile_indore_leads():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    leads_json_path = "/home/mryhain_well/indore-solar-leads.json"
    
    batch_date = "2026-06-06"
    batch_dir = os.path.join(base_dir, 'data', batch_date)
    template_dir = os.path.join(base_dir, 'src', 'templates')
    template_name = 'template.html'
    
    if not os.path.exists(leads_json_path):
        print(f"Error: Indore leads file not found at: {leads_json_path}")
        return
        
    with open(leads_json_path, 'r', encoding='utf-8') as f:
        leads_data = json.load(f)
        
    print(f"Found {len(leads_data)} Indore business records. Starting compilation...")
    
    batch_index_entries = {}
    success_count = 0
    start_time = time.time()
    
    for idx, biz_data in enumerate(leads_data, start=1):
        unique_id = biz_data.get("business_id") or f"SLR-{batch_date.replace('-', '')}-{idx:03d}"
        biz_name = biz_data["business_name"]
        
        # Ensure ID format matches SLR-YYYYMMDD-XXX
        if not unique_id.startswith("SLR-"):
            unique_id = f"SLR-{batch_date.replace('-', '')}-{idx:03d}"
            biz_data["business_id"] = unique_id
            
        try:
            biz_dir = os.path.join(batch_dir, unique_id)
            os.makedirs(biz_dir, exist_ok=True)
            
            json_out = os.path.join(biz_dir, "business.json")
            html_out = os.path.join(biz_dir, "index.html")
            meta_out = os.path.join(biz_dir, "metadata.json")
            
            # Save the enriched business.json
            with open(json_out, 'w', encoding='utf-8') as f:
                json.dump(biz_data, f, indent=4, ensure_ascii=False)
                
            # Compile the website
            compile_website_data(biz_data, template_dir, template_name, html_out)
            
            # Save metadata.json
            timestamp = datetime.datetime.now().isoformat()
            metadata = {
                "business_id": unique_id,
                "business_name": biz_name,
                "slug": biz_data.get("slug", "indore-solar"),
                "lead_source": "indore-solar-leads.json",
                "date_created": timestamp,
                "template_version": template_name,
                "status": {
                    "enrichment": "SUCCESS",
                    "compilation": "SUCCESS",
                    "whatsapp_outreach": "PENDING"
                },
                "history": [
                    {
                        "timestamp": timestamp,
                        "action": "IMPORT_LEAD",
                        "details": "Imported Indore enriched JSON"
                    },
                    {
                        "timestamp": timestamp,
                        "action": "COMPILE_WEBSITE",
                        "details": "Compiled index.html using template.html"
                    }
                ]
            }
            with open(meta_out, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
                
            # Save to global search index map
            batch_index_entries[unique_id] = {
                "business_name": biz_name,
                "city": biz_data["location"]["city"],
                "state": biz_data["location"]["state"],
                "batch_date": batch_date,
                "status": "SUCCESS",
                "path": f"data/{batch_date}/{unique_id}"
            }
            
            success_count += 1
            print(f"Compiled [{success_count}/{len(leads_data)}]: {unique_id} ({biz_name})")
            
        except Exception as e:
            print(f"Error compiling {unique_id} ({biz_name}): {e}")
            
    if batch_index_entries:
        print("Registering all Indore entries in Global Index...")
        add_batch_to_index(batch_index_entries, base_dir)
        
    duration = time.time() - start_time
    print("=" * 60)
    print(f"Indore Compilation finished in {duration:.4f} seconds!")
    print(f"Total compiled successfully: {success_count}/{len(leads_data)}")
    print("=" * 60)

if __name__ == "__main__":
    compile_indore_leads()
