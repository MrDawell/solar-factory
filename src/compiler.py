import os
import json
import time
from jinja2 import Environment, FileSystemLoader, select_autoescape

def compile_website_data(data, template_dir, template_name, output_path):
    """
    Compile a website using the provided data dictionary and template, writing to output_path.
    """
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load template
    template = env.get_template(template_name)
    
    # Render template with JSON data
    rendered_html = template.render(**data)
    
    # Write rendered HTML to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def compile_website(json_path, template_dir, template_name, output_dir=None):
    """
    Compile a single website from a business.json file.
    If output_dir is not provided, it writes index.html in the same directory as the JSON.
    """
    # Read the business JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Set output folder and file path
    if output_dir is None:
        output_dir = os.path.dirname(json_path)
        
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")
    
    compile_website_data(data, template_dir, template_name, output_path)
    return output_path

def compile_batch(json_dir, template_dir, template_name, output_dir):
    """
    Backward-compatible batch compiler. Compiles all JSONs in json_dir
    into the output_dir. (Outputs as slug.html or index.html)
    """
    if not os.path.exists(json_dir):
        raise FileNotFoundError(f"JSON directory not found: {json_dir}")
        
    os.makedirs(output_dir, exist_ok=True)
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    compiled_count = 0
    start_time = time.time()
    
    for filename in json_files:
        json_path = os.path.join(json_dir, filename)
        try:
            # For backward compatibility, compile to [slug].html in output_dir
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            slug = data.get('slug')
            out_file = os.path.join(output_dir, f"{slug}.html")
            compile_website_data(data, template_dir, template_name, out_file)
            compiled_count += 1
        except Exception as e:
            print(f"Error compiling {filename}: {e}")
            
    elapsed = time.time() - start_time
    return compiled_count, elapsed

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        # If compiled from a single json_path
        json_p = sys.argv[1]
        temp_d = sys.argv[2]
        temp_n = sys.argv[3]
        out_d = sys.argv[4] if len(sys.argv) > 4 else None
        
        print(f"Compiling single website from {json_p}...")
        path = compile_website(json_p, temp_d, temp_n, out_d)
        print(f"Successfully compiled: {path}")
    else:
        print("Usage: python compiler.py <json_path> <template_dir> <template_name> [output_dir]")
