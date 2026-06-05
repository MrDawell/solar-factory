import os
import json

def get_index_path(base_dir):
    """Return the absolute path to the global index.json file."""
    return os.path.join(base_dir, 'data', 'index.json')

def load_index(base_dir):
    """Load the global index or return an empty dict if it doesn't exist."""
    index_path = get_index_path(base_dir)
    if not os.path.exists(index_path):
        return {}
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load global index ({e}). Initializing empty index.")
        return {}

def save_index(index, base_dir):
    """Save the index dict to the global index.json file."""
    index_path = get_index_path(base_dir)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    try:
        # Atomic write by writing to a temp file first, then renaming
        temp_path = index_path + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=4, ensure_ascii=False)
        if os.path.exists(index_path):
            os.remove(index_path)
        os.rename(temp_path, index_path)
    except Exception as e:
        print(f"Error saving global index: {e}")

def add_or_update_index(business_id, entry_details, base_dir):
    """Add or update a business entry in the global index."""
    index = load_index(base_dir)
    index[business_id] = entry_details
    save_index(index, base_dir)

def add_batch_to_index(entries_dict, base_dir):
    """Add multiple entries to the index in one write operation to save disk I/O."""
    index = load_index(base_dir)
    index.update(entries_dict)
    save_index(index, base_dir)

def search_index(query, base_dir):
    """
    Search the index by business name, city, state, or ID.
    Returns a list of matching entries (each with a business_id key).
    """
    index = load_index(base_dir)
    query = query.lower().strip()
    
    results = []
    for biz_id, details in index.items():
        name = details.get('business_name', '').lower()
        city = details.get('city', '').lower()
        state = details.get('state', '').lower()
        status = details.get('status', '').lower()
        lead_source = details.get('lead_source', '').lower()
        
        if (query in biz_id.lower() or
            query in name or
            query in city or
            query in state or
            query in status or
            query in lead_source):
            
            # Append biz_id to the output result
            match = details.copy()
            match['business_id'] = biz_id
            results.append(match)
            
    return results
