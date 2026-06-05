import os
import csv
import json
import re

def slugify(text):
    """Generate a URL-friendly slug from text."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def calculate_solar_metrics(avg_bill_inr):
    """
    Calculate realistic solar metrics for Indian properties.
    """
    try:
        bill = float(avg_bill_inr)
    except (ValueError, TypeError):
        bill = 6000.0

    monthly_units = bill / 8.0
    capacity_kw = round((monthly_units / 120.0) * 2) / 2
    if capacity_kw < 1.0:
        capacity_kw = 1.0
        
    panels_needed_min = int(capacity_kw * 2)
    panels_needed_max = int(capacity_kw * 3)
    
    monthly_savings = bill * 0.85
    annual_savings = monthly_savings * 12
    system_cost = capacity_kw * 65000
    
    if capacity_kw >= 3.0:
        subsidy = 78000
    elif capacity_kw == 2.0:
        subsidy = 60000
    else:
        subsidy = 30000 * capacity_kw
        
    net_cost = max(system_cost - subsidy, 30000)
    payback_years = round(net_cost / annual_savings, 1)
    
    if payback_years < 2.5:
        payback_years = 2.5
    elif payback_years > 6.0:
        payback_years = 5.2

    return {
        "annual_savings": f"₹{int(annual_savings):,}",
        "monthly_savings": f"₹{int(monthly_savings):,}",
        "payback": f"{payback_years} Yrs",
        "size": f"{capacity_kw} kW",
        "panels": f"{panels_needed_min} - {panels_needed_max}"
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

def improve_headline(biz_name, city):
    """
    Transforms dry lead parameters into high-converting headlines.
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

def get_hash_theme(business_name):
    """Deterministically select a color palette based on business name."""
    # Curated premium Tailwind HSL color themes mapping to primary, secondary, primary-container, etc.
    THEMES = [
        # Tech Silicon Blue & Solar Amber (Tesla Energy Look)
        {
            "primary": "#0b2e4f", "secondary": "#f59e0b", 
            "primary_container": "#061a30", "secondary_container": "#fffbeb",
            "background": "#f8fafc", "surface": "#ffffff"
        },
        # Sky Blue & Solar Orange (Enphase Look)
        {
            "primary": "#0284c7", "secondary": "#ea580c", 
            "primary_container": "#0369a1", "secondary_container": "#ffedd5",
            "background": "#f8fafc", "surface": "#ffffff"
        },
        # Clean Emerald & Sun Gold
        {
            "primary": "#059669", "secondary": "#d97706", 
            "primary_container": "#047857", "secondary_container": "#fef3c7",
            "background": "#fafaf9", "surface": "#ffffff"
        },
        # Deep Royal Slate & Bright Amber
        {
            "primary": "#0f172a", "secondary": "#eab308", 
            "primary_container": "#0b1220", "secondary_container": "#fef9c3",
            "background": "#f8fafc", "surface": "#ffffff"
        },
        # Cyber-Tech Space Slate & Orange
        {
            "primary": "#1e293b", "secondary": "#ea580c", 
            "primary_container": "#0f172a", "secondary_container": "#ffedd5",
            "background": "#f8fafc", "surface": "#ffffff"
        }
    ]
    theme_index = abs(hash(business_name)) % len(THEMES)
    return THEMES[theme_index]

def enrich_lead(row, unique_id):
    """Convert a row of lead data into a complete production business.json configuration."""
    biz_name = row.get("Business Name", "Local Solar Solutions").strip()
    owner_name = row.get("Owner Name", "Our Expert Team").strip()
    city = row.get("City", "India").strip()
    state = row.get("State", "India").strip()
    address = row.get("Address", f"Main Market Road, {city}, {state}").strip()
    phone = row.get("Phone", "").strip()
    email = row.get("Email", "").strip()
    whatsapp = row.get("WhatsApp", phone).strip().replace("+", "").replace(" ", "")
    
    # Calculate branding colors and theme
    colors = get_hash_theme(biz_name)
    primary_color = row.get("Primary Color", "").strip()
    secondary_color = row.get("Secondary Color", "").strip()
    if primary_color:
        colors["primary"] = primary_color
    if secondary_color:
        colors["secondary"] = secondary_color
        
    logo_parts = biz_name.split()
    logo_text = " ".join(logo_parts[:2]) if len(logo_parts) >= 2 else biz_name
    logo_svg = generate_svg_logo(biz_name, colors["primary"], colors["secondary"])
    
    # Generate slug
    slug = slugify(biz_name)
    
    # Set default values for calculator config
    calc_config = {
        "residential_factor": 1200,
        "commercial_factor": 1000,
        "factory_factor": 800
    }
    if city == "Raipur":
        calc_config = {
            "residential_factor": 1200,
            "commercial_factor": 1000,
            "factory_factor": 800
        }
        
    # Testimonials/Suburbs for local city
    local_suburbs = {
        "Raipur": ["Shankar Nagar", "Tatibandh", "Devendra Nagar", "Samta Colony"],
        "Jaipur": ["Vaishali Nagar", "Malviya Nagar", "C-Scheme", "Mansarovar"],
        "Pune": ["Kothrud", "Baner", "Hinjawadi", "Aundh"],
        "Ahmedabad": ["Satellite", "Vastrapur", "Prahlad Nagar", "Bodakdev"],
        "Amritsar": ["Mall Road", "Ranjit Avenue", "Golden Temple Chowk", "Putligarh"]
    }
    suburbs = local_suburbs.get(city, ["Sector 4", "Main Market Area", "Subhash Nagar", "Nehru Bazaar"])
    sub1, sub2 = suburbs[0], suburbs[1]
    
    # Calculations for plans
    # 2-3 BHK Flat
    flat_metrics = calculate_solar_metrics(4000)
    # Independent House
    house_metrics = calculate_solar_metrics(8000)
    # Small Shop
    shop_metrics = calculate_solar_metrics(15000)
    
    # Custom improved headline
    headline = improve_headline(biz_name, city)

    # Build production JSON structure matching template.html 1-to-1
    business_json = {
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
            "email": email or f"contact@{slug}.in",
            "business_hours": "Mon - Sat: 10:00 AM - 7:00 PM"
        },
        "location": {
            "city": city,
            "state": state,
            "address": address,
            "map_query": f"{biz_name}, {city}, {state}".replace(" ", "%20")
        },
        "branding": {
            "logo_svg": logo_svg,
            "colors": colors,
            "hero_image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCGYM46nI_IzuF_YX3nN6kxxxhFLnQ4e7WZ0JpgIc9ld0iiZa6XGCfX6r94OHr7mkbe13lrzvew5gRG91dATiC2kCXTlWLmiZn9cEMpZhGuqiIfj5MbVYu455uhmoicVGp9dABF3q5Q1UEFDAEKh2y2Uol-gWoX9owzRjWhQOZVizZckWYMSTlYBWQe_X95tATKLmHDOXAqC-rXo5ROfPjFJe5IrU0q--z3sahOqLniaG9lk8MocwlXHdUcq7yZwVbbPT3OuU93FrV3"
        },
        "hero": {
            "badge": "MNRE Approved Partner",
            "headline": headline,
            "subheadline": f"Premium solar systems with government subsidy support. Expert installation serving {city}, {sub1}, and surrounding areas.",
            "background_image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCGYM46nI_IzuF_YX3nN6kxxxhFLnQ4e7WZ0JpgIc9ld0iiZa6XGCfX6r94OHr7mkbe13lrzvew5gRG91dATiC2kCXTlWLmiZn9cEMpZhGuqiIfj5MbVYu455uhmoicVGp9dABF3q5Q1UEFDAEKh2y2Uol-gWoX9owzRjWhQOZVizZckWYMSTlYBWQe_X95tATKLmHDOXAqC-rXo5ROfPjFJe5IrU0q--z3sahOqLniaG9lk8MocwlXHdUcq7yZwVbbPT3OuU93FrV3",
            "image_alt": f"Rooftop solar installation in {city}"
        },
        "trust_signals": [
            {
                "icon": "solar_power",
                "headline": "100+ Systems Installed",
                "description": f"Proven track record of powering homes and businesses across {state}."
            },
            {
                "icon": "workspace_premium",
                "headline": "5+ Years Experience",
                "description": "Deep technical expertise in MNRE guidelines and local net-metering processes."
            },
            {
                "icon": "support_agent",
                "headline": "Local Service Team",
                "description": f"Based in {city} for lightning-fast maintenance and on-site support."
            }
        ],
        "plans": [
            {
                "title": "2-3 BHK Flat",
                "original_bill": "₹4,000",
                "new_bill": "₹1,600",
                "savings_pct": 60,
                "features": ["3kW System Capacity", "Net Metering Paperwork Included", "Central Subsidy Assistance"],
                "cta_text": "Enquire Now",
                "popular": False
            },
            {
                "title": "Independent House",
                "original_bill": "₹8,000",
                "new_bill": "₹2,400",
                "savings_pct": 70,
                "features": [f"5kW - 8kW System sizing for {city}", "Whole House Power Backup Integration", "Mobile System Monitoring App Support"],
                "cta_text": "Get Best Deal",
                "popular": True
            },
            {
                "title": "Small Shop",
                "original_bill": "₹15,000",
                "new_bill": "₹7,500",
                "savings_pct": 50,
                "features": ["10kW High-Efficiency Array", "Commercial Grid Tie Approvals", "Projected Payback in 3.5 Years"],
                "cta_text": "Commercial Quote",
                "popular": False
            }
        ],
        "services_section": {
            "headline": "Tailored Solar Solutions",
            "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDYc8O--WnGs6bwpYRp2Tq0JiFbtfSVbwIk6hWhqu0BnfJ9IeZnvknZLvdq_YKQRpQdxfqtEpQ4DdFmpFRQ6p2ZCdAPhTdYOsTH9Qk_a_XMuTqlwjHvpAtzbwRT3HejKxhyHHraMfsXr1WO_kBEFCiOtFMLh930awQdlpGlHwaJr_rtQBI8TFfRGJik2go9Jg3JLgwbDLfL-xpByu7498gVym1eGkeArnW0nZt1ETPWTaV6lrFgxMg4sL28CjWtMsH-ZpUNaeseBJrp",
            "image_alt": f"Solar EPC service array inspection in {city}"
        },
        "services": [
            {
                "title": "Home Solar",
                "description": f"Maximize your roof space with high-efficiency residential systems designed for {city} properties."
            },
            {
                "title": "Commercial Solar",
                "description": f"Reduce operational costs for offices, warehouses, and shopping complexes across {state}."
            },
            {
                "title": "School/Clinic Solar",
                "description": "Reliable uninterrupted power for essential community services with zero noise and pollution."
            },
            {
                "title": "Annual Maintenance",
                "description": "Regular cleaning, shading reports, and technical diagnostics to ensure peak annual generation."
            }
        ],
        "projects": [
            {
                "title": f"{sub1} Residence Project",
                "subtitle": f"5kW Residential System • Monthly Savings: {flat_metrics['monthly_savings']}",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBtz5ZHKM1VLtQYXYsR8eSj41P8R8j765GVpFkcsV3-kcfAdOWCiarC2mx9BVtpFKWvAAo3GsmvpIky8PgaC2_iZMEXejLIQ4NoB6AeBjjra-ciCYICIM3nroKB9Wja7B0wP40kN9k9br1YUhuRuEchrscfuJgnLEzWvNfN3nRr3EhGRby0pUVhowfZegf3UeQH1Z3mvdeLLiS9S9Wg-J6SDftFiQmrbHuSqpmgDPGN7xl1jHa9YnhrZPqsTjciFkemrwgbNbAO9Bhm"
            },
            {
                "title": f"{sub2} Commercial installation",
                "subtitle": f"10kW Shop System • Monthly Savings: {shop_metrics['monthly_savings']}",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAOTiyARPLwS66rRHbgxgHTnrB6ldirzmQyamKlgY8ixmzHIxZT6lHEnvw4Tsbrl7bqsvn1LQ2_UTyQ_Gm2sFLUTrFASfbCDqyQUQ1L3oMDLr8OuNkr_jwE4vZW0GRZ1SsUfepdRK7g5g5W2ZXV7PuJIha90wE-oZJBrtKQFjy5GKVsuTc0_VZHfODdPf-xD4jaOC05zyT_8T-YkIoQPx7KXoGLS1EISeOAV81K5veV5P5pWAovMgGX2eSc7LyGY3Y-Jj3y_hYJmOvB"
            }
        ],
        "faq": [
            {
                "question": "How much subsidy can I get?",
                "answer": f"Under the PM-Surya Ghar Muft Bijli Yojana, residential consumers in {city} can get up to ₹78,000 subsidy for a 3kW system. Our team handles 100% of the net-metering and subsidy applications."
            },
            {
                "question": "What is the cost of installation?",
                "answer": "Costs vary based on system size and panel quality. Typically, a 3kW system starts from ₹1.5 Lakhs (before subsidy) in Chhattisgarh. We offer easy zero-cost EMI options."
            },
            {
                "question": "Do solar panels work in rainy season?",
                "answer": f"Yes! Panels generate power from solar light, not heat. While generation is lower on heavy cloudy days, modern Tier-1 monocrystalline panels generate substantial power in the monsoon seasons of {state}."
            }
        ],
        "reputation": {
            "rating": "4.9",
            "reviews_count": "150+"
        },
        "calculator_config": calc_config
    }
    
    return business_json
