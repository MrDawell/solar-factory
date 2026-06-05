import os
import argparse
import datetime
import json
import time
from indexer import search_index, load_index
from compiler import compile_website_data

def search_command(query, base_dir):
    """Execute search on the index and display results."""
    results = search_index(query, base_dir)
    if not results:
        print(f"No businesses found matching: '{query}'")
        return
        
    print(f"Found {len(results)} matching business(es):")
    print("-" * 100)
    print(f"{'ID':<18} | {'Business Name':<30} | {'City':<15} | {'Date':<12} | {'Status':<8}")
    print("-" * 100)
    for r in results:
        print(f"{r['business_id']:<18} | {r['business_name'][:30]:<30} | {r['city'][:15]:<15} | {r['batch_date']:<12} | {r['status']:<8}")
    print("-" * 100)

def compile_by_id(business_id, base_dir, template_dir, template_name):
    """Regenerate a single business website by ID."""
    index = load_index(base_dir)
    entry = index.get(business_id)
    if not entry:
        print(f"Error: Business ID '{business_id}' not found in index.")
        return False
        
    # Standard path resolution
    # entry['path'] is 'data/YYYY-MM-DD/SLR-YYYYMMDD-XXX'
    biz_dir = os.path.join(base_dir, entry['path'].replace('/', os.sep))
    json_path = os.path.join(biz_dir, "business.json")
    html_path = os.path.join(biz_dir, "index.html")
    meta_path = os.path.join(biz_dir, "metadata.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Single source of truth 'business.json' not found at: {json_path}")
        return False
        
    # Read business data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Regenerating website for: {business_id} ({data['business_name']})...")
    
    # Re-render HTML template
    compile_start = time.time()
    compile_website_data(data, template_dir, template_name, html_path)
    compile_duration = time.time() - compile_start
    
    # Read, update and write metadata
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    else:
        meta = {
            "business_id": business_id,
            "business_name": data["business_name"],
            "slug": data.get("slug"),
            "lead_source": "REGENERATED",
            "date_created": datetime.datetime.now().isoformat(),
            "status": {}
        }
        
    meta["template_version"] = template_name
    meta["status"]["compilation"] = "SUCCESS"
    
    timestamp = datetime.datetime.now().isoformat()
    if "history" not in meta:
        meta["history"] = []
    meta["history"].append({
        "timestamp": timestamp,
        "action": "COMPILE_REGENERATE",
        "details": f"Regenerated index.html using template {template_name} in {compile_duration:.4f}s"
    })
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Compiled website written to: {html_path}")
    return True

def compile_by_date(batch_date, base_dir, template_dir, template_name):
    """Regenerate all business websites processed under a specific batch date."""
    index = load_index(base_dir)
    
    # Find all business IDs belonging to this date
    matching_ids = [biz_id for biz_id, entry in index.items() if entry.get("batch_date") == batch_date]
    
    if not matching_ids:
        print(f"No business records found in the index for batch date: {batch_date}")
        return False
        
    print(f"Found {len(matching_ids)} businesses for batch {batch_date}. Starting regeneration batch...")
    successes = 0
    
    for biz_id in matching_ids:
        if compile_by_id(biz_id, base_dir, template_dir, template_name):
            successes += 1
            
    print(f"Batch compilation finished: {successes}/{len(matching_ids)} succeeded.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solar Website Factory Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Management commands")
    
    # Search Command
    search_parser = subparsers.add_parser("search", help="Search global index of solar businesses")
    search_parser.add_argument("query", type=str, help="Search query (ID, Name, City, State, etc.)")
    
    # Compile Command
    compile_parser = subparsers.add_parser("compile", help="Regenerate static website HTML files")
    group = compile_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", type=str, help="Unique Business ID (e.g. SLR-20260602-001)")
    group.add_argument("--date", type=str, help="Batch date in YYYY-MM-DD format")
    
    args = parser.parse_args()
    
    # Establish project directories
    src_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(src_dir)
    template_dir = os.path.join(src_dir, 'templates')
    template_name = 'template.html'
    
    if args.command == "search":
        search_command(args.query, base_dir)
    elif args.command == "compile":
        if args.id:
            compile_by_id(args.id, base_dir, template_dir, template_name)
        elif args.date:
            compile_by_date(args.date, base_dir, template_dir, template_name)
    else:
        parser.print_help()
