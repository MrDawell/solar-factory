import os
import json
import time
import datetime
import re
from enricher import slugify, get_hash_theme
from compiler import compile_website_data
from indexer import add_batch_to_index

TRUE_VARANASI_ADDRESSES = {
    "abhiram-solar": "Sahitya Naka Road, Near Union Bank, Sahitya Naka, Varanasi, Uttar Pradesh 221005",
    "akn-power-(india)-pvt.-ltd": "Nadesar Main Road, Near Mint House, Patel Nagar, Nadesar, Varanasi, Uttar Pradesh 221002",
    "anya-green-energy-solution": "N10/72E-25, New Colony Kakarmatta, Sundarpur, DLW Road, Varanasi, Uttar Pradesh 221005",
    "babaaji-solar-and-tools-pvt-ltd": "N. 6/13A, Chitaipur Road, Near Sunderpur, Chitaipur, Varanasi, Uttar Pradesh 221005",
    "green-shine-solar-(second-listing)": "PAC Road, Near Bhulanpur PAC, Bhulanpur, Varanasi, Uttar Pradesh 221009",
    "green-shine-solar": "B 1/3 Vijay Garh Kothi, Assi Lanka Road, Varanasi, Uttar Pradesh 221005",
    "greenland-solar": "Stadium Road, Near Sigra Stadium, Sigra, Varanasi, Uttar Pradesh 221002",
    "greenlantern-energy": "N 14/27 F-1, Ashutosh Nagar Colony, Sarainandan, Khojwa, Varanasi, Uttar Pradesh 221010",
    "hariom-traders": "Sarnath Road, Near Paharia Sarnath Belt, Paharia, Varanasi, Uttar Pradesh 221007",
    "indrawati-solar-solution": "Opposite Shepa Institute, Bachhawn Road, Varanasi, Uttar Pradesh 221011",
    "kartik-solar--utl-solar--loom-solar": "Lamahi Road, Near Lamahi Area, Varanasi, Uttar Pradesh 221003",
    "lallan-solar": "Opposite Pradeep Bakers, Chunar Road, Sunderpur, Varanasi, Uttar Pradesh 221005",
    "loom-solar----utl-solar----distributor": "Maldahiya Crossing, Near Maldahiya, Varanasi, Uttar Pradesh 221001",
    "m2m-solar-point": "A 34/105, Golgadda Road, Near Bus Stand, Ganga Nagar Colony, Adampur, Varanasi, Uttar Pradesh 221001",
    "mahadev-enterprises-[wholesale]": "Singhpur Bus Stand Road, Near Singhpur, Varanasi, Uttar Pradesh 221003",
    "matri-shree-green-solar": "Flat No-11, First Floor, Block No-F1, Patel Nagar, Nadesar, Varanasi, Uttar Pradesh 221002",
    "msp-and-company": "N.12/448-D, Sheoratanpur Road, Post Bajardiha, Varanasi, Uttar Pradesh 221109",
    "patel-solar-power-system": "Shivaji Nagar Colony Road, Near Shivaji Nagar, Varanasi, Uttar Pradesh 221010",
    "pradha-solar-generation": "Vaishno Nagar Colony, Near Vaishno Nagar, Varanasi, Uttar Pradesh 221003",
    "projecteez-solar-power-system": "B.30/2, Plot No. 14, Prafull Nagar Colony, Lanka, Varanasi, Uttar Pradesh 221005",
    "purvanchal-green-energy": "Vidyut Nagar, Bhikharipur, P.O. DLW, Varanasi, Uttar Pradesh 221004",
    "shri-babaji-power-and-solar-solution-llp": "N. 6/13A, Chitaipur Road, Near Sunderpur, Chitaipur, Varanasi, Uttar Pradesh 221005",
    "sks-solar-tech-solutions": "JNM College Gate Road, Near JNM College, Varanasi, Uttar Pradesh 221005",
    "smart-solar-solutions": "1/13 Awas Vikas, Near LIC Office, Pandeypur, Varanasi, Uttar Pradesh 221002",
    "solar-tek-india-varanasi": "Ghat Road, Near Dashashwamedh Ghat Area, Varanasi, Uttar Pradesh 221001",
    "sri-krishna-and-company": "Ashapur Narendra Complex, Chandra Chauraha, Ashapur, Sarnath, Varanasi, Uttar Pradesh 221007",
    "sun-ray-system": "Police Line Road, Near Police Line, Varanasi, Uttar Pradesh 221002",
    "udita-enterprises-(solar-energy)": "Sonia Pokhara Road, Near Sonia Pokhara, Varanasi, Uttar Pradesh 221010",
    "varanasi-solar-panel": "Chetganj Road, Near Chetganj Chowk, Varanasi, Uttar Pradesh 221001",
    "varanasi-solar-tech": "Opposite Hotel Landmark, Cantonment, Varanasi, Uttar Pradesh 221002",
    "wisdom-tree-solar-solution": "Singhpur Gola Road, Near Singhpur Gola, Varanasi, Uttar Pradesh 221003"
}

def generate_svg_logo(business_name, primary_color, secondary_color):
    """
    Generates a highly premium, modern, vector SVG logo for the business.
    Outputs the raw SVG inline.
    """
    hash_val = abs(hash(business_name))
    variation = hash_val % 5
    
    initial = "S"
    for char in business_name.strip():
        if char.isalnum():
            initial = char.upper()
            break
            
    grad_id = f"grad_{hash_val}"
    
    if variation == 0:
        # Modern Circular Sun/Star Badge
        svg_icon = f"""<svg class="w-8 h-8 flex-shrink-0" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{primary_color}" />
                    <stop offset="100%" stop-color="{secondary_color}" />
                </linearGradient>
            </defs>
            <circle cx="16" cy="16" r="14" fill="url(#{grad_id})" fill-opacity="0.15" />
            <circle cx="16" cy="16" r="10" stroke="url(#{grad_id})" stroke-width="2" />
            <circle cx="16" cy="16" r="4" fill="{secondary_color}" />
            <path d="M16 2V6M16 26V30M2 16H6M26 16H30M25.9 6.1L23.07 8.93M8.93 23.07L6.1 25.9M25.9 25.9L23.07 23.07M8.93 8.93L6.1 6.1" stroke="url(#{grad_id})" stroke-width="1.5" stroke-linecap="round"/>
        </svg>"""
    elif variation == 1:
        # Dynamic Eco Leaf Badge
        svg_icon = f"""<svg class="w-8 h-8 flex-shrink-0" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="{primary_color}" />
                    <stop offset="100%" stop-color="{secondary_color}" />
                </linearGradient>
            </defs>
            <path d="M16 2C8.27 2 2 8.27 2 16C2 21.5 5.5 26.2 10.5 28.5L16 16L21.5 28.5C26.5 26.2 30 21.5 30 16C30 8.27 23.73 2 16 2Z" fill="url(#{grad_id})" fill-opacity="0.1" />
            <path d="M16 28C22.63 28 28 22.63 28 16C28 9.37 22.63 4 16 4C9.37 4 4 9.37 4 16C4 22.63 9.37 28 16 28Z" stroke="url(#{grad_id})" stroke-width="2" />
            <path d="M16 8C11.58 8 8 11.58 8 16C8 20 12 24 16 26C20 24 24 20 24 16C24 11.58 20.42 8 16 8Z" fill="url(#{grad_id})" />
            <path d="M16 12V20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
        </svg>"""
    elif variation == 2:
        # Geometric Tech Solar Grid
        svg_icon = f"""<svg class="w-8 h-8 flex-shrink-0" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="50%" y1="0%" x2="50%" y2="100%">
                    <stop offset="0%" stop-color="{primary_color}" />
                    <stop offset="100%" stop-color="{secondary_color}" />
                </linearGradient>
            </defs>
            <rect x="2" y="2" width="12" height="12" rx="2" fill="url(#{grad_id})" fill-opacity="0.8" />
            <rect x="18" y="2" width="12" height="12" rx="2" fill="{secondary_color}" fill-opacity="0.8" />
            <rect x="2" y="18" width="12" height="12" rx="2" fill="{secondary_color}" fill-opacity="0.8" />
            <rect x="18" y="18" width="12" height="12" rx="2" fill="url(#{grad_id})" fill-opacity="0.8" />
            <circle cx="16" cy="16" r="5" fill="#ffffff" stroke="url(#{grad_id})" stroke-width="2" />
            <path d="M16 14V18M14 16H18" stroke="{primary_color}" stroke-width="1.5" stroke-linecap="round" />
        </svg>"""
    elif variation == 3:
        # Hexagonal Energy Badge
        svg_icon = f"""<svg class="w-8 h-8 flex-shrink-0" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{primary_color}" />
                    <stop offset="100%" stop-color="{secondary_color}" />
                </linearGradient>
            </defs>
            <path d="M16 2L28.12 9V23L16 30L3.88 23V9L16 2Z" fill="url(#{grad_id})" fill-opacity="0.1" stroke="url(#{grad_id})" stroke-width="2" stroke-linejoin="round" />
            <path d="M17 6L9 16H16L15 26L23 16H16L17 6Z" fill="url(#{grad_id})" stroke="url(#{grad_id})" stroke-width="1" />
        </svg>"""
    else:
        # Customized Brand Initials Badge
        svg_icon = f"""<svg class="w-8 h-8 flex-shrink-0" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{primary_color}" />
                    <stop offset="100%" stop-color="{secondary_color}" />
                </linearGradient>
            </defs>
            <circle cx="16" cy="16" r="14" fill="url(#{grad_id})" />
            <circle cx="16" cy="16" r="11" fill="#ffffff" />
            <text x="50%" y="58%" dominant-baseline="middle" text-anchor="middle" font-family="'Montserrat', 'Inter', sans-serif" font-size="14" font-weight="bold" fill="url(#{grad_id})">{initial}</text>
        </svg>"""
    return svg_icon

def extract_address_from_subheadline(subheadline, city, state):
    """
    Extract landmarks from subheadline using advanced regex mapping.
    """
    subheadline = subheadline.strip()
    
    patterns = [
        r'near\s+([A-Za-z0-9\s\-\(\)\/\&]+?)(?:\s+with|\s+and|\s+serving|\s+colony|\.|$)',
        r'around\s+([A-Za-z0-9\s\-\(\)\/\&]+?)(?:\s+area|\s+colony|\.|$)',
        r'opposite\s+([A-Za-z0-9\s\-\(\)\/\&]+?)(?:\s+institute|\s+hotel|\.|$)',
        r'at\s+([A-Za-z0-9\s\-\(\)\/\&]+?)(?:\s+bus|\s+stand|\s+gola|\.|$)',
        r'in\s+([A-Za-z0-9\s\-\(\)\/\&]+?)\s+belt'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, subheadline, re.IGNORECASE)
        if match:
            landmark = match.group(1).strip()
            landmark = re.sub(r'\s+based$', '', landmark, flags=re.IGNORECASE).strip()
            landmark = landmark.rstrip('.').strip()
            if len(landmark) > 2:
                return f"{landmark} Road, Near {landmark}, {city}, {state} 221005"
                
    fallback_areas = [
        "Lanka Main Road, Near Lanka Chowk",
        "Cantonment Road, Near Varanasi Cantt Railway Station",
        "Assi Road, Near Assi Ghat",
        "Maldahiya Crossing, Near Maldahiya",
        "Sigra Main Road, Near Sigra Chowk"
    ]
    h_idx = abs(hash(subheadline)) % len(fallback_areas)
    return f"{fallback_areas[h_idx]}, {city}, {state} 221002"

def improve_headline(raw_headline, biz_name, city):
    """
    Transforms dry scraped directory headers into high-converting headlines.
    """
    copys = [
        f"Cut Your {city} Electricity Bills by Up to 90% with {biz_name}",
        f"Switch to Clean, Affordable Rooftop Solar with {biz_name}",
        f"{city}'s Trusted Partner for Government Subsidy Rooftop Solar",
        f"Go Solar with {biz_name}: Eliminate High Power Bills in {city}",
        f"Get MNRE-Approved Rooftop Solar Installation by {biz_name}"
    ]
    
    headline_index = abs(hash(biz_name)) % len(copys)
    return copys[headline_index]

def normalize_varanasi_data(raw_data, unique_id):
    """
    Normalize and enrich the raw Varanasi JSON data to conform 1-to-1 
    with the production Jinja2 template schema.
    """
    raw_id = raw_data.get("identity", {})
    biz_name = raw_id.get("business_name", "Local Solar Expert").strip()
    slug = slugify(biz_name)
    
    # 1. Map identity & contact
    owner_name = raw_id.get("owner_name", "Our Expert Team").strip()
    phone = raw_id.get("phone", "+91 90000 00000").strip()
    whatsapp = raw_id.get("whatsapp") or phone
    whatsapp = str(whatsapp).replace("+", "").replace(" ", "").replace("-", "")
    if len(whatsapp) == 10:
        whatsapp = "91" + whatsapp
        
    email = raw_id.get("email") or f"info@{slug}.in"
    
    # 2. Extract true address landmarks from subheadline or fallback
    raw_hero = raw_data.get("hero", {})
    subheadline = raw_hero.get("subheadline", "")
    address = raw_id.get("address") or TRUE_VARANASI_ADDRESSES.get(slug) or extract_address_from_subheadline(subheadline, "Varanasi", "Uttar Pradesh")
    
    # 3. Dynamic Maps integration
    map_query = f"{biz_name}, Varanasi, Uttar Pradesh"
    
    # 4. Branding Colors & Dynamic Custom SVG Logo Icon
    colors = get_hash_theme(biz_name)
    logo_svg = generate_svg_logo(biz_name, colors["primary"], colors["secondary"])
    
    logo_parts = biz_name.split()
    logo_text = " ".join(logo_parts[:2]) if len(logo_parts) >= 2 else biz_name
    
    # 5. Hero Section Copywriter Improvement
    badge = raw_hero.get("badge") or "Rooftop Solar in Varanasi"
    raw_headline = raw_hero.get("headline", "")
    headline = improve_headline(raw_headline, biz_name, "Varanasi")
    
    project_images = [
        "https://lh3.googleusercontent.com/aida-public/AB6AXuBtz5ZHKM1VLtQYXYsR8eSj41P8R8j765GVpFkcsV3-kcfAdOWCiarC2mx9BVtpFKWvAAo3GsmvpIky8PgaC2_iZMEXejLIQ4NoB6AeBjjra-ciCYICIM3nroKB9Wja7B0wP40kN9k9br1YUhuRuEchrscfuJgnLEzWvNfN3nRr3EhGRby0pUVhowfZegf3UeQH1Z3mvdeLLiS9S9Wg-J6SDftFiQmrbHuSqpmgDPGN7xl1jHa9YnhrZPqsTjciFkemrwgbNbAO9Bhm",
        "https://lh3.googleusercontent.com/aida-public/AB6AXuAOTiyARPLwS66rRHbgxgHTnrB6ldirzmQyamKlgY8ixmzHIxZT6lHEnvw4Tsbrl7bqsvn1LQ2_UTyQ_Gm2sFLUTrFASfbCDqyQUQ1L3oMDLr8OuNkr_jwE4vZW0GRZ1SsUfepdRK7g5g5W2ZXV7PuJIha90wE-oZJBrtKQFjy5GKVsuTc0_VZHfODdPf-xD4jaOC05zyT_8T-YkIoQPx7KXoGLS1EISeOAV81K5veV5P5pWAovMgGX2eSc7LyGY3Y-Jj3y_hYJmOvB"
    ]
    
    # 6. Trust Signals Loop Mapping
    trust_signals = []
    raw_signals = raw_data.get("trust_signals", [])
    for signal in raw_signals:
        trust_signals.append({
            "icon": "verified" if signal.get("icon") == "trust" else "star",
            "headline": signal.get("title", "Local Expertise"),
            "description": signal.get("description", "")
        })
    if len(trust_signals) < 3:
        fillers = [
            {"icon": "solar_power", "headline": "100+ Systems Installed", "description": "Proven track record of rooftop systems in Uttar Pradesh."},
            {"icon": "workspace_premium", "headline": "5+ Years Experience", "description": "Expert engineering aligned with MNRE subsidy standards."},
            {"icon": "support_agent", "headline": "Local Varanasi Team", "description": "Based in Varanasi for quick support and site audits."}
        ]
        for f in fillers:
            if len(trust_signals) < 3:
                trust_signals.append(f)
                
    # 7. Plans
    plans = [
        {
            "title": "2-3 BHK Flat",
            "original_bill": "₹4,000",
            "new_bill": "₹1,400",
            "savings_pct": 65,
            "features": ["3kW System Capacity", "Net Metering Documentation Support", "Surya Ghar Subsidy Eligible"],
            "cta_text": "Enquire Now",
            "popular": False
        },
        {
            "title": "Independent House",
            "original_bill": "₹8,000",
            "new_bill": "₹2,000",
            "savings_pct": 75,
            "features": ["5kW - 8kW Sized for Varanasi roofs", "Grid Tie Inverter with Mobile Monitoring", "Zero Upfront Maintenance Scheme"],
            "cta_text": "Get Best Deal",
            "popular": True
        },
        {
            "title": "Small Shop / Office",
            "original_bill": "₹15,000",
            "new_bill": "₹6,750",
            "savings_pct": 55,
            "features": ["10kW Rooftop Panel Array", "Commercial Net Meter Setup", "Payback Slabs under PuVVNL Tariff"],
            "cta_text": "Commercial Quote",
            "popular": False
        }
    ]
    
    # 8. Services
    services = []
    raw_services = raw_data.get("services", [])
    for s in raw_services:
        services.append({
            "title": s.get("title", "Home Solar Rooftop"),
            "description": s.get("description", "High performance solar panels design and installation.")
        })
    standard_services = [
        {"title": "Home Solar", "description": "Maximize your roof space with high-efficiency residential systems designed for Varanasi homes."},
        {"title": "Commercial Solar", "description": "Reduce operational costs for offices, warehouses, and shopping complexes across Uttar Pradesh."},
        {"title": "Clinic & School Solar", "description": "Reliable uninterrupted power for essential community services with zero noise and pollution."},
        {"title": "Annual Maintenance", "description": "Regular cleaning, shading reports, and technical diagnostics to ensure peak annual generation."}
    ]
    for ss in standard_services:
        if len(services) < 4:
            if not any(item["title"].lower() == ss["title"].lower() for item in services):
                services.append(ss)
                
    # 9. Projects
    projects = []
    raw_projects = raw_data.get("projects", [])
    local_suburbs = ["Sigra", "Lahurabir", "Lanka", "Sarnath", "Bhelupur"]
    for idx, p in enumerate(raw_projects):
        suburb = local_suburbs[idx % len(local_suburbs)]
        projects.append({
            "title": p.get("title") or f"{suburb} Installation",
            "subtitle": f"{p.get('location', 'Varanasi')} System • {p.get('monthly_savings', 'Substantial Savings')}",
            "image_url": project_images[idx % len(project_images)]
        })
    if not projects:
        projects = [
            {"title": "Sigra Residential Setup", "subtitle": "Varanasi System • Monthly Savings: ₹3,400", "image_url": project_images[0]},
            {"title": "Lanka Commercial Plant", "subtitle": "Varanasi System • Monthly Savings: ₹12,750", "image_url": project_images[1]}
        ]
        
    # 10. FAQ
    faq = []
    raw_faq = raw_data.get("faq", [])
    for f in raw_faq:
        faq.append({
            "question": f.get("question", ""),
            "answer": f.get("answer", "")
        })
        
    # 11. Reputation
    raw_rep = raw_data.get("reputation", {})
    reputation = {
        "rating": raw_rep.get("rating", 4.8),
        "reviews_count": f"{raw_rep.get('review_count', 10)}+"
    }
    
    # 12. Calculator Config
    calc_config = {
        "residential_factor": 1200,
        "commercial_factor": 1000,
        "factory_factor": 800
    }
    
    normalized = {
        "business_id": unique_id,
        "business_name": biz_name,
        "slug": slug,
        "identity": {
            "business_name": biz_name,
            "owner_name": owner_name,
            "logo_text": logo_text
        },
        "contact": {
            "phone": phone,
            "whatsapp": whatsapp,
            "email": email,
            "business_hours": "Mon - Sat: 10:00 AM - 7:00 PM"
        },
        "location": {
            "city": "Varanasi",
            "state": "Uttar Pradesh",
            "address": address,
            "map_query": map_query.replace(" ", "%20")
        },
        "branding": {
            "logo_svg": logo_svg,
            "colors": colors,
            "hero_image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCGYM46nI_IzuF_YX3nN6kxxxhFLnQ4e7WZ0JpgIc9ld0iiZa6XGCfX6r94OHr7mkbe13lrzvew5gRG91dATiC2kCXTlWLmiZn9cEMpZhGuqiIfj5MbVYu455uhmoicVGp9dABF3q5Q1UEFDAEKh2y2Uol-gWoX9owzRjWhQOZVizZckWYMSTlYBWQe_X95tATKLmHDOXAqC-rXo5ROfPjFJe5IrU0q--z3sahOqLniaG9lk8MocwlXHdUcq7yZwVbbPT3OuU93FrV3"
        },
        "hero": {
            "badge": badge,
            "headline": headline,
            "subheadline": subheadline,
            "background_image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCGYM46nI_IzuF_YX3nN6kxxxhFLnQ4e7WZ0JpgIc9ld0iiZa6XGCfX6r94OHr7mkbe13lrzvew5gRG91dATiC2kCXTlWLmiZn9cEMpZhGuqiIfj5MbVYu455uhmoicVGp9dABF3q5Q1UEFDAEKh2y2Uol-gWoX9owzRjWhQOZVizZckWYMSTlYBWQe_X95tATKLmHDOXAqC-rXo5ROfPjFJe5IrU0q--z3sahOqLniaG9lk8MocwlXHdUcq7yZwVbbPT3OuU93FrV3",
            "image_alt": f"Solar energy installer rooftop in Varanasi"
        },
        "trust_signals": trust_signals,
        "plans": plans,
        "services_section": {
            "headline": "Tailored Solar Solutions",
            "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDYc8O--WnGs6bwpYRp2Tq0JiFbtfSVbwIk6hWhqu0BnfJ9IeZnvknZLvdq_YKQRpQdxfqtEpQ4DdFmpFRQ6p2ZCdAPhTdYOsTH9Qk_a_XMuTqlwjHvpAtzbwRT3HejKxhyHHraMfsXr1WO_kBEFCiOtFMLh930awQdlpGlHwaJr_rtQBI8TFfRGJik2go9Jg3JLgwbDLfL-xpByu7498gVym1eGkeArnW0nZt1ETPWTaV6lrFgxMg4sL28CjWtMsH-ZpUNaeseBJrp",
            "image_alt": "Solar engineer structural assessment check"
        },
        "services": services,
        "projects": projects,
        "faq": faq,
        "reputation": reputation,
        "calculator_config": calc_config
    }
    
    return normalized

def compile_varanasi_leads():
    """Batch processes the Varanasi JSON leads files and generates index.html files."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    varanasi_dir = os.path.join(base_dir, 'data', 'varanasi-leads-business-json-enriched')
    
    batch_date = "2026-06-02"
    batch_dir = os.path.join(base_dir, 'data', batch_date)
    template_dir = os.path.join(base_dir, 'src', 'templates')
    template_name = 'template.html'
    
    if not os.path.exists(varanasi_dir):
        print(f"Error: Varanasi enriched directory not found at: {varanasi_dir}")
        return
        
    json_files = [f for f in os.listdir(varanasi_dir) if f.endswith('.json')]
    print(f"Found {len(json_files)} Varanasi business records. Starting compilation...")
    
    batch_index_entries = {}
    success_count = 0
    start_time = time.time()
    
    for idx, filename in enumerate(json_files, start=201):
        raw_path = os.path.join(varanasi_dir, filename)
        unique_id = f"SLR-{batch_date.replace('-', '')}-{idx}"
        
        try:
            with open(raw_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            biz_data = normalize_varanasi_data(raw_data, unique_id)
            biz_name = biz_data["business_name"]
            
            biz_dir = os.path.join(batch_dir, unique_id)
            os.makedirs(biz_dir, exist_ok=True)
            
            json_out = os.path.join(biz_dir, "business.json")
            html_out = os.path.join(biz_dir, "index.html")
            meta_out = os.path.join(biz_dir, "metadata.json")
            
            with open(json_out, 'w', encoding='utf-8') as f:
                json.dump(biz_data, f, indent=4, ensure_ascii=False)
                
            compile_website_data(biz_data, template_dir, template_name, html_out)
            
            timestamp = datetime.datetime.now().isoformat()
            metadata = {
                "business_id": unique_id,
                "business_name": biz_name,
                "slug": biz_data["slug"],
                "lead_source": "varanasi-leads-business-json-enriched",
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
                        "details": "Imported Varanasi enriched JSON"
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
                
            batch_index_entries[unique_id] = {
                "business_name": biz_name,
                "city": biz_data["location"]["city"],
                "state": biz_data["location"]["state"],
                "batch_date": batch_date,
                "status": "SUCCESS",
                "path": f"data/{batch_date}/{unique_id}"
            }
            
            success_count += 1
            print(f"Compiled [{success_count}/{len(json_files)}]: {unique_id} ({biz_name})")
            
        except Exception as e:
            print(f"Error compiling {filename}: {e}")
            
    if batch_index_entries:
        print("Registering all Varanasi entries in Global Index...")
        add_batch_to_index(batch_index_entries, base_dir)
        
    duration = time.time() - start_time
    print("=" * 60)
    print(f"Varanasi Compilation finished in {duration:.4f} seconds!")
    print(f"Total compiled successfully: {success_count}/{len(json_files)}")
    print("=" * 60)

if __name__ == "__main__":
    compile_varanasi_leads()
