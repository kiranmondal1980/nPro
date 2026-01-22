import streamlit as st
import zipfile
import io
import json
from datetime import datetime
from jinja2 import Template
import validators

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="Titan v13.0 | Architect Pro",
    page_icon="💎",
    layout="wide"
)

# App Styling
st.markdown("""
    <style>
    .stApp { background: #0a0a0c; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #facc15 !important; border-bottom-color: #facc15 !important; }
    div[data-testid="stExpander"] { background: #16161a; border-radius: 12px; border: 1px solid #2d2d33; }
    .main-btn { 
        background: linear-gradient(90deg, #facc15 0%, #eab308 100%); 
        color: black !important; font-weight: bold; border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE MASTER JINJA2 TEMPLATE ---
# This is the "Engine Room" that generates the professional HTML code.
MASTER_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | {{ biz_name }}</title>
    <meta name="description" content="{{ meta_desc }}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family={{ h_font }}:wght@700;900&family={{ b_font }}:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root { --p: {{ p_color }}; --s: {{ s_color }}; --radius: {{ border_rad }}; }
        body { font-family: '{{ b_font }}', sans-serif; color: #1a1a1a; scroll-behavior: smooth; }
        h1, h2, h3 { font-family: '{{ h_font }}', sans-serif; text-transform: uppercase; letter-spacing: {{ ls }}; }
        .bg-primary { background-color: var(--p); }
        .text-primary { color: var(--p); }
        .btn-main { background: var(--p); color: white; padding: 1rem 2rem; border-radius: var(--radius); transition: all 0.3s ease; font-weight: bold; text-align: center; display: inline-block; }
        .btn-main:hover { filter: brightness(1.1); transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .glass { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        [x-cloak] { display: none !important; }
    </style>
</head>
<body x-data="{ openModal: false, activeProduct: {} }">
    <nav class="glass fixed w-full z-50 border-b border-gray-100">
        <div class="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-black tracking-tighter text-primary">{{ biz_name }}</a>
            <div class="hidden md:flex space-x-8 text-xs font-bold uppercase tracking-widest">
                <a href="index.html" class="hover:text-primary">Home</a>
                <a href="about.html" class="hover:text-primary">About</a>
                <a href="contact.html" class="hover:text-primary">Contact</a>
                <a href="tel:{{ biz_phone }}" class="text-primary border-2 border-primary px-4 py-2 rounded-full">Call Now</a>
            </div>
        </div>
    </nav>

    <main class="min-h-screen pt-20">
        {{ content | safe }}
    </main>

    <footer class="bg-gray-950 text-white py-20">
        <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-3 gap-12">
            <div>
                <h3 class="text-xl font-bold mb-6">{{ biz_name }}</h3>
                <p class="text-gray-400 text-sm leading-relaxed">{{ biz_addr }}</p>
            </div>
            <div>
                <h4 class="text-xs font-bold uppercase tracking-widest mb-6">Quick Links</h4>
                <ul class="text-gray-400 space-y-4 text-sm">
                    <li><a href="privacy.html">Privacy Policy</a></li>
                    <li><a href="terms.html">Terms & Conditions</a></li>
                </ul>
            </div>
            <div class="md:text-right">
                <h4 class="text-xs font-bold uppercase tracking-widest mb-6">Connect</h4>
                <p class="text-xl font-bold">{{ biz_phone }}</p>
                <p class="text-gray-400">{{ biz_email }}</p>
            </div>
        </div>
    </footer>

    <!-- WhatsApp Float -->
    <a href="https://wa.me/{{ wa_clean }}" class="fixed bottom-8 right-8 bg-[#25d366] p-4 rounded-full shadow-2xl transition hover:scale-110 z-50">
        <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg>
    </a>

    <!-- Modal System -->
    <div x-show="openModal" x-cloak class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/90" @click.self="openModal = false">
        <div class="bg-white max-w-4xl w-full rounded-3xl overflow-hidden shadow-2xl">
            <div class="grid md:grid-cols-2">
                <div class="h-96 md:h-full">
                    <img :src="activeProduct.img" class="w-full h-full object-cover">
                </div>
                <div class="p-12">
                    <h2 class="text-4xl font-black mb-4 text-primary" x-text="activeProduct.name"></h2>
                    <p class="text-2xl font-bold text-gray-400 mb-6" x-text="activeProduct.price"></p>
                    <p class="text-gray-600 mb-8 leading-relaxed" x-text="activeProduct.desc"></p>
                    <a :href="'https://wa.me/{{ wa_clean }}?text=Interested in ' + activeProduct.name" class="btn-main w-full">Inquire Now</a>
                    <button @click="openModal = false" class="mt-4 text-xs uppercase tracking-widest opacity-50 w-full">Close Window</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- 3. HELPER FUNCTIONS ---
def get_wa_clean(phone):
    return "".join(filter(str.isdigit, phone))

def build_index_content(hero_h, seo_d, services, sheet_url, img_hero):
    service_cards = "".join([f"""
        <div class="p-8 border border-gray-100 rounded-3xl hover:shadow-xl transition group bg-white">
            <h3 class="text-xl font-black mb-4 group-hover:text-primary">{s.strip()}</h3>
            <p class="text-gray-500 text-sm uppercase font-bold tracking-tighter italic">Professional Grade Expertise</p>
        </div>
    """ for s in services.splitlines() if s.strip()])

    inventory_js = ""
    if sheet_url:
        inventory_js = f"""
        <section class="py-24 bg-gray-50 px-6">
            <div class="max-w-7xl mx-auto">
                <h2 class="text-5xl font-black mb-16 text-center">Exclusive Collection</h2>
                <div id="product-grid" class="grid md:grid-cols-3 gap-10">
                    <!-- Loaded via JS -->
                </div>
            </div>
            <script>
                async function loadInventory() {{
                    try {{
                        const res = await fetch('{sheet_url}');
                        const text = await res.text();
                        const rows = text.split('\\n').slice(1);
                        const grid = document.getElementById('product-grid');
                        rows.forEach(row => {{
                            const cols = row.split('|');
                            if(cols.length >= 2) {{
                                const p = {{ name: cols[0], price: cols[1], desc: cols[2]||'', img: cols[3]||'https://images.unsplash.com/photo-1519741497674-611481863552' }};
                                const card = document.createElement('div');
                                card.className = "bg-white p-6 rounded-[2rem] shadow-sm hover:scale-[1.02] transition cursor-pointer border border-gray-100";
                                card.onclick = () => {{ 
                                    const scope = document.querySelector('[x-data]').__x.$data;
                                    scope.activeProduct = p;
                                    scope.openModal = true;
                                }};
                                card.innerHTML = `<img src="${{p.img}}" class="w-full h-64 object-cover rounded-2xl mb-6"><h3 class="text-xl font-bold text-primary uppercase">${{p.name}}</h3><p class="text-gray-400 font-bold">${{p.price}}</p>`;
                                grid.appendChild(card);
                            }}
                        }});
                    }} catch(e) {{ console.error("Sheet Load Error", e); }}
                }}
                window.addEventListener('DOMContentLoaded', loadInventory);
            </script>
        </section>
        """

    return f"""
    <section class="relative h-[90vh] flex items-center justify-center text-white overflow-hidden">
        <img src="{img_hero}" class="absolute inset-0 w-full h-full object-cover brightness-50">
        <div class="relative z-10 text-center px-6">
            <h1 class="text-6xl md:text-9xl font-black mb-8 leading-none tracking-tighter animate-in slide-in-from-bottom duration-1000">{hero_h}</h1>
            <p class="text-xl md:text-2xl max-w-3xl mx-auto font-light opacity-90 mb-12">{seo_d}</p>
            <div class="flex flex-col md:flex-row gap-4 justify-center">
                <a href="#services" class="btn-main px-12">Our Expertise</a>
                <a href="contact.html" class="bg-white text-black px-12 py-4 rounded-full font-bold hover:bg-gray-100 transition">Get Quote</a>
            </div>
        </div>
    </section>

    <section id="services" class="py-24 px-6 max-w-7xl mx-auto">
        <div class="grid md:grid-cols-3 gap-12">{service_cards}</div>
    </section>

    {inventory_js}

    <section class="py-24 bg-primary text-white text-center px-6">
        <h2 class="text-4xl md:text-6xl font-black mb-8 uppercase tracking-tighter">Ready to Begin?</h2>
        <a href="tel:{get_wa_clean(biz_phone)}" class="bg-white text-primary px-16 py-6 rounded-full font-black text-xl hover:scale-105 transition inline-block">CALL US NOW</a>
    </section>
    """

# --- 4. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("💎 Titan v13.0")
    st.caption("Platinum High-Performance Engine")
    
    with st.expander("🎨 Brand DNA", expanded=True):
        p_color = st.color_picker("Primary Color", "#000000")
        s_color = st.color_picker("Accent Color", "#facc15")
        h_font = st.selectbox("Heading Font", ["Playfair Display", "Syncopate", "Montserrat", "Oswald"])
        b_font = st.selectbox("Body Font", ["Inter", "Roboto", "Open Sans"])
        radius = st.select_slider("Corner Radius", ["0px", "12px", "24px", "40px"], value="24px")

    with st.expander("📸 Asset Manager"):
        h_img = st.text_input("Hero Background URL", "https://images.unsplash.com/photo-1519741497674-611481863552?q=80&w=2000")
        f_img = st.text_input("Feature Image URL", "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=1200")

    st.success("Target: High-Conversion Static Site")

# --- 5. MAIN INTERFACE ---
tabs = st.tabs(["📍 Identity", "🏗️ Content", "🛒 Inventory", "⚖️ Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "Red Hippo Planners")
        biz_phone = st.text_input("Official Phone", "+91 84540 02711")
        biz_email = st.text_input("Email", "events@redhippoplanners.in")
    with c2:
        biz_addr = st.text_area("Full Address", "Vasant Kunj, South Delhi, India")
        gsc_tag = st.text_input("GSC Verification Tag (Optional)")

with tabs[1]:
    hero_h = st.text_input("Main Hero Headline", "Luxury Events Engineered to Perfection")
    meta_d = st.text_area("Short SEO Description", "The premier luxury wedding and event planner in New Delhi.")
    services = st.text_area("Services (One per line)", "Wedding Decor\nCorporate Galas\nBoutique Catering")

with tabs[2]:
    st.info("💡 Format: Product Name | Price | Description | ImageURL")
    sheet_csv = st.text_input("Published CSV Link (Google Sheets)")

with tabs[3]:
    p_policy = st.text_area("Privacy Policy", "We value your privacy...")
    t_terms = st.text_area("Terms of Service", "Standard business terms apply...")

# --- 6. GENERATION ENGINE ---
if st.button("🚀 DEPLOY TITAN SUPREME ASSET", use_container_width=True, type="primary"):
    
    # Template Configuration
    config = {
        "biz_name": biz_name,
        "biz_phone": biz_phone,
        "biz_email": biz_email,
        "biz_addr": biz_addr,
        "wa_clean": get_wa_clean(biz_phone),
        "p_color": p_color,
        "s_color": s_color,
        "h_font": h_font,
        "b_font": b_font,
        "border_rad": radius,
        "ls": "0.05em",
        "meta_desc": meta_d
    }

    # Generate Pages
    template = Template(MASTER_LAYOUT)
    
    idx_html = template.render(title="Home", content=build_index_content(hero_h, meta_d, services, sheet_csv, h_img), **config)
    abt_html = template.render(title="About", content=f"<section class='py-32 max-w-4xl mx-auto px-6'><h1 class='text-6xl font-black mb-12'>Our Story</h1><p class='text-xl leading-relaxed text-gray-600'>{meta_d}</p><img src='{f_img}' class='mt-12 rounded-[3rem] w-full'></section>", **config)
    con_html = template.render(title="Contact", content=f"<section class='py-32 max-w-4xl mx-auto px-6 text-center'><h1 class='text-6xl font-black mb-12'>Get In Touch</h1><p class='text-3xl font-bold text-primary mb-6'>{biz_phone}</p><p class='text-xl text-gray-500'>{biz_addr}</p></section>", **config)
    pri_html = template.render(title="Privacy", content=f"<section class='py-32 max-w-3xl mx-auto px-6'><h1 class='text-4xl font-bold mb-10'>Privacy Policy</h1><div class='prose'>{p_policy}</div></section>", **config)
    trm_html = template.render(title="Terms", content=f"<section class='py-32 max-w-3xl mx-auto px-6'><h1 class='text-4xl font-bold mb-10'>Terms & Conditions</h1><div class='prose'>{t_terms}</div></section>", **config)

    # ZIP Logic
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("index.html", idx_html)
        zf.writestr("about.html", abt_html)
        zf.writestr("contact.html", con_html)
        zf.writestr("privacy.html", pri_html)
        zf.writestr("terms.html", trm_html)
        # SEO
        zf.writestr("robots.txt", "User-agent: *\nAllow: /")
        # Schema.org Integration
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": biz_name,
            "telephone": biz_phone,
            "address": {"@type": "PostalAddress", "streetAddress": biz_addr}
        }
        zf.writestr("schema.json", json.dumps(schema))

    st.balloons()
    st.success("💎 SITE ARCHITECTURE COMPLETE")
    st.download_button(
        "📥 DOWNLOAD TITAN V13.0 ZIP", 
        zip_buffer.getvalue(), 
        f"{biz_name.lower().replace(' ','_')}_platinum.zip",
        "application/zip"
    )
