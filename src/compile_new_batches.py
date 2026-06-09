import os
import json
import time
import datetime
from compiler import compile_website_data
from indexer import add_batch_to_index

def compile_leads(file_path, start_idx, city_name, batch_date):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    batch_dir = os.path.join(base_dir, 'data', batch_date)
    template_dir = os.path.join(base_dir, 'src', 'templates')
    template_name = 'template.html'
    
    if not os.path.exists(file_path):
        print(f"Error: file not found at: {file_path}")
        return {}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        leads_data = json.load(f)
        
    print(f"Processing {len(leads_data)} {city_name} leads starting from index {start_idx:03d}...")
    
    batch_index_entries = {}
    success_count = 0
    
    for idx, biz_data in enumerate(leads_data):
        current_idx = start_idx + idx
        unique_id = f"SLR-{batch_date.replace('-', '')}-{current_idx:03d}"
        biz_data["business_id"] = unique_id
        biz_name = biz_data["business_name"]
        
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
                "slug": biz_data.get("slug", f"{city_name.lower()}-solar"),
                "lead_source": os.path.basename(file_path),
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
                        "details": f"Imported {city_name} enriched JSON"
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
            
        except Exception as e:
            print(f"Error compiling {unique_id} ({biz_name}): {e}")
            
    print(f"Successfully compiled {success_count}/{len(leads_data)} {city_name} leads.")
    return batch_index_entries

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    batch_date = "2026-06-10"
    
    jodhpur_entries = compile_leads(os.path.join(base_dir, "jodhpur-solar-leads.json"), 1, "Jodhpur", batch_date)
    pratapgarh_entries = compile_leads(os.path.join(base_dir, "pratapgarh-solar-leads.json"), 101, "Pratapgarh", batch_date)
    
    all_entries = {}
    all_entries.update(jodhpur_entries)
    all_entries.update(pratapgarh_entries)
    
    if all_entries:
        print("Registering all entries in Global Index...")
        add_batch_to_index(all_entries, base_dir)
        print("Done!")

if __name__ == "__main__":
    main()
