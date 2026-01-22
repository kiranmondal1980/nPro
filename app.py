import streamlit as st
import zipfile
import io
import json
from datetime import datetime
from jinja2 import Template

# --- 1. APP CONFIGURATION & UI AESTHETIC ---
st.set_page_config(page_title="Kaydiem Titan v13.0 | Platinum Architect", layout="wide", page_icon="💎")

# Apply the original "Titan" Dark Theme to the Streamlit UI
st.markdown("""
    <style>
    .main { background: #0b0f1a; color: white; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8; font-weight: bold; font-size: 1rem; }
    .stTabs [aria-selected="true"] { color: #fbbf24 !important; border-bottom-color: #fbbf24 !important; }
    div[data-testid="stExpander"] { background: #161e2e; border: 1px solid #1e293b; border-radius: 12px; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 4.5em; 
        background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); 
        color: black; font-weight: 900; border: none; font-size: 1.5rem;
        box-shadow: 0 15px 45px rgba(217, 119, 6, 0.3); transition: all 0.4s;
    }
    .stButton>button:hover { transform: translateY(-5px); box-shadow: 0 20px 50px rgba(217, 119, 6, 0.5); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DESIGN STUDIO (FULLY RESTORED & EXPANDED) ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=60)
    st.title("Titan v13.0 Studio")
    
    with st.expander("🎭 1. Layout & DNA", expanded=True):
        layout_dna = st.selectbox("Design DNA", ["Industrial Titan", "Glass-Tech", "Modern Royal", "Brutalist", "Corporate Elite"])
        p_color = st.color_picker("Primary Brand Color", "#4A0E0E")
        s_color = st.color_picker("Accent/CTA Color", "#D4AF37")
        bg_color = st.color_picker("Site Background", "#FFFFFF")
        border_rad = st.select_slider("Corner Roundness", options=["0px", "4px", "12px", "24px", "40px", "60px"], value="40px")

    with st.expander("✍️ 2. Typography Studio", expanded=True):
        h_font = st.selectbox("Heading Font", ["Playfair Display", "Oswald", "Montserrat", "Syncopate", "Inter", "Bebas Neue"])
        b_font = st.selectbox("Body Font", ["Montserrat", "Inter", "Roboto", "Open Sans"])
        h_weight = st.select_slider("Heading Weight", options=["300", "400", "700", "900"], value="700")
        ls = st.select_slider("Letter Spacing", options=["-0.05em", "-0.02em", "0em", "0.05em", "0.1em", "0.2em"], value="0.05em")

    with st.expander("🚀 3. Pro Features (NEW)", expanded=False):
        use_aos = st.checkbox("Enable Scroll Animations (AOS)", value=True)
        use_dark_mode = st.checkbox("Force Dark Theme Site", value=False)
        preloader = st.checkbox("Enable Site Preloader", value=True)

    gsc_tag = st.text_input("GSC Verification Tag")
    st.info("Titan Engine: v13.0 Platinum Edition")

st.title("🏗️ Kaydiem Titan Supreme v13.0")

# --- MULTI-TAB DATA COLLECTION (RESTORED) ---
tabs = st.tabs(["📍 Identity", "🏗️ Content & SEO", "📸 Asset Manager", "⚡ Live E-com", "🌟 Social Proof", "⚖️ Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "Red Hippo (The Planners)")
        biz_phone = st.text_input("Verified Phone", "+91 84540 02711")
        biz_email = st.text_input("Business Email", "events@redhippoplanners.in")
    with c2:
        biz_cat = st.text_input("Category", "Luxury Wedding Planner")
        biz_hours = st.text_input("Hours", "Mon-Sun: 10:00 - 19:00")
        prod_url = st.text_input("Production URL (for Sitemap/SEO)", "https://kani201012.github.io/site/")
    biz_logo = st.text_input("Logo URL (Transparent PNG recommended)")
    biz_addr = st.text_area("Full Maps Address")
    biz_areas = st.text_area("Service Areas (Comma separated)", "Vasant Kunj, Chhatarpur, South Delhi")
    map_iframe = st.text_area("Map Embed HTML Code (From Google Maps)")

with tabs[1]:
    hero_h = st.text_input("Hero Headline", "Crafting Dream Weddings: New Delhi's Premier Luxury Decorators")
    seo_d = st.text_area("Meta Description (SEO)", "Luxury wedding planning and decor services in Delhi. Certified planners for elite events.")
    biz_key = st.text_input("SEO Keywords", "wedding planner delhi, luxury decor, event management")
    biz_serv = st.text_area("Services Listing (One per line)", "Floral Design\nLighting Production\nCatering Management\nGuest Concierge")
    about_txt = st.text_area("Our Story / Detailed About", height=250)

with tabs[2]:
    st.header("📸 Asset Manager")
    custom_hero = st.text_input("Hero Background URL")
    custom_feat = st.text_input("Feature Section Image URL")
    custom_gall = st.text_input("About Section Image URL")
    og_image = st.text_input("Social Share Image URL (OG:Image)")

with tabs[3]:
    st.header("🛒 Live Showroom (Google Sheets)")
    st.warning("FORMAT: Name | Price | Description | ImageURL")
    sheet_url = st.text_input("Published CSV Link")

with tabs[4]:
    testi_txt = st.text_area("Testimonials (Name | Quote)")
    faq_txt = st.text_area("FAQ (Question? ? Answer)")

with tabs[5]:
    st.header("⚖️ Legal Hub")
    priv_body = st.text_area("Privacy Policy Content", height=200)
    terms_body = st.text_area("Terms Content", height=200)

# --- THE SUPREME GENERATION ENGINE ---

if st.button("🚀 DEPLOY 100% MARKET-DOMINATING ASSET"):
    
    # Logic Processing
    wa_clean = "".join(filter(str.isdigit, biz_phone))
    a_list = [a.strip() for a in biz_areas.split(",")]
    s_areas_json = json.dumps(a_list)
    
    # Asset Defaults
    img_h = custom_hero or "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=1600"
    img_f = custom_feat or "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=800"
    img_g = custom_gall or "https://images.unsplash.com/photo-1532712938310-34cb3982ef74?auto=format&fit=crop&q=80&w=1600"

    # --- HTML CSS MASTER ENGINE ---
    theme_css = f"""
    :root {{ 
        --p: {p_color}; --s: {s_color}; --radius: {border_rad}; 
        --bg: {'#0f172a' if use_dark_mode else bg_color};
        --text: {'#ffffff' if use_dark_mode else '#0f172a'};
    }}
    * {{ box-sizing: border-box; outline: none; }}
    body {{ 
        font-family: '{b_font}', sans-serif; background: var(--bg); color: var(--text); 
        margin: 0; line-height: 1.6; overflow-x: hidden;
    }}
    h1, h2, h3 {{ 
        font-family: '{h_font}', sans-serif; font-weight: {h_weight}; 
        letter-spacing: {ls}; text-transform: uppercase; 
    }}
    .hero-mask {{ 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{img_h}'); 
        background-size: cover; background-position: center; background-attachment: fixed;
        min-height: 90vh; display: flex; align-items: center; justify-content: center; text-align: center;
        padding: 20px;
    }}
    .btn-accent {{ 
        background: var(--s); color: white !important; padding: 1.2rem 3rem; 
        border-radius: var(--radius); font-weight: 900; transition: all 0.4s; 
        display: inline-block; text-decoration:none; text-transform: uppercase; 
        letter-spacing: 0.2em; font-size: 13px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .btn-accent:hover {{ transform: scale(1.05); filter: brightness(1.1); box-shadow: 0 15px 40px var(--s); }}
    
    .glass-nav {{ 
        background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); 
        position: fixed; top: 0; width: 100%; z-index: 1000; border-bottom: 1px solid rgba(0,0,0,0.05);
    }}
    {'.glass-nav { background: rgba(15,23,42,0.9); border-bottom: 1px solid rgba(255,255,255,0.1); }' if use_dark_mode else ''}

    .product-card {{ 
        background: {'#1e293b' if use_dark_mode else '#ffffff'}; 
        border-radius: var(--radius); padding: 2rem; transition: 0.4s; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    .product-card:hover {{ transform: translateY(-10px); box-shadow: 0 30px 60px rgba(0,0,0,0.1); }}

    #preloader {{ 
        position: fixed; inset: 0; background: var(--bg); z-index: 999999; 
        display: flex; align-items: center; justify-content: center; transition: 0.5s;
    }}
    """

    # --- HTML LAYOUT GENERATOR ---
    def generate_html(title_tag, content, is_index=False):
        aos_init = '<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script><script>AOS.init({duration:1000, once:true});</script>' if use_aos else ""
        aos_css = '<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">' if use_aos else ""
        
        preloader_html = '<div id="preloader"><div class="w-16 h-16 border-4 border-t-transparent rounded-full animate-spin" style="border-color:var(--p); border-top-color:transparent;"></div></div><script>window.onload=()=>document.getElementById("preloader").style.opacity="0";setTimeout(()=>document.getElementById("preloader").remove(),500);</script>' if preloader else ""

        # Dynamic JS for Inventory
        dynamic_js = ""
        if is_index and sheet_url:
            dynamic_js = f"""
            <script>
            let currentProducts = [];
            async function fetchInventory() {{
                try {{
                    const res = await fetch('{sheet_url}');
                    const text = await res.text();
                    const rows = text.split('\\n').slice(1);
                    const container = document.getElementById('inventory-grid');
                    container.innerHTML = "";
                    rows.forEach((row, i) => {{
                        const p = row.split('|');
                        if(p.length >= 2) {{
                            const item = {{ name: p[0].trim(), price: p[1].trim(), desc: (p[2]||"").trim(), img: (p[3]||"{img_f}").trim() }};
                            currentProducts.push(item);
                            container.innerHTML += `
                                <div class="product-card" onclick="openModal(${{i}})" data-aos="fade-up">
                                    <img src="${{item.img}}" class="w-full h-64 object-cover rounded-[2rem] mb-6">
                                    <h3 class="text-xl font-black mb-2">${{item.name}}</h3>
                                    <p class="text-primary font-bold mb-4" style="color:var(--p)">${{item.price}}</p>
                                    <span class="text-[10px] font-black uppercase tracking-widest opacity-50 underline">View Details</span>
                                </div>`;
                        }}
                    }});
                }} catch(e) {{ console.log("CORS/Fetch error"); }}
            }}
            function openModal(id) {{
                const p = currentProducts[id];
                document.getElementById('m-title').innerText = p.name;
                document.getElementById('m-price').innerText = p.price;
                document.getElementById('m-desc').innerText = p.desc;
                document.getElementById('m-img').src = p.img;
                document.getElementById('m-wa').href = "https://wa.me/{wa_clean}?text=Inquiry: " + encodeURIComponent(p.name);
                document.getElementById('site-modal').style.display = 'flex';
            }}
            window.onload = () => {{ fetchInventory(); { 'AOS.init();' if use_aos else '' } }};
            </script>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title_tag} | {biz_name}</title>
            <meta name="description" content="{seo_d}"><meta name="keywords" content="{biz_key}">
            <meta property="og:title" content="{biz_name}"><meta property="og:image" content="{og_image}">
            <link rel="canonical" href="{prod_url}">
            {f'<meta name="google-site-verification" content="{gsc_tag}">' if gsc_tag else ""}
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700;900&family={b_font.replace(' ','+')}&display=swap" rel="stylesheet">
            {aos_css}
            <style>{theme_css}</style>
        </head>
        <body>
            {preloader_html}
            <nav class="glass-nav py-4 px-8">
                <div class="max-w-7xl mx-auto flex justify-between items-center">
                    <a href="index.html" class="text-2xl font-black uppercase tracking-tighter" style="color:var(--p)">{biz_name}</a>
                    <div class="hidden md:flex space-x-8 text-[11px] font-black uppercase tracking-widest">
                        <a href="index.html">Home</a><a href="about.html">About</a><a href="contact.html">Contact</a>
                        <a href="tel:{biz_phone}" class="text-primary" style="color:var(--p)">{biz_phone}</a>
                    </div>
                </div>
            </nav>
            <main>{content}</main>
            <footer class="py-20 px-8 bg-black text-white text-center">
                <div class="max-w-4xl mx-auto">
                    <h2 class="text-3xl font-black mb-8">{biz_name}</h2>
                    <p class="opacity-50 mb-10">{biz_addr}</p>
                    <div class="flex justify-center space-x-6 text-xs font-bold uppercase tracking-widest">
                        <a href="privacy.html">Privacy</a><a href="terms.html">Terms</a>
                    </div>
                    <p class="mt-12 text-[10px] opacity-20 uppercase tracking-[0.5em]">Architected by Kaydiem Titan</p>
                </div>
            </footer>
            
            <!-- Modal System -->
            <div id="site-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.9); z-index:2000; align-items:center; justify-content:center; padding:20px;" onclick="if(event.target==this)this.style.display='none'">
                <div class="bg-white text-black max-w-4xl w-full rounded-[2.5rem] overflow-hidden grid md:grid-cols-2">
                    <img id="m-img" class="h-full w-full object-cover">
                    <div class="p-12">
                        <h2 id="m-title" class="text-4xl font-black mb-4"></h2>
                        <p id="m-price" class="text-2xl font-bold mb-6 text-amber-600"></p>
                        <p id="m-desc" class="text-gray-600 mb-10"></p>
                        <a id="m-wa" href="#" class="btn-accent w-full text-center">Confirm Interest</a>
                        <button onclick="document.getElementById('site-modal').style.display='none'" class="mt-6 text-xs font-bold uppercase opacity-30 w-full text-center">Close Window</button>
                    </div>
                </div>
            </div>

            {dynamic_js}
            {aos_init}
        </body>
        </html>
        """

    # --- CONTENT BUILDERS ---
    # Index Content
    s_cards = "".join([f'<div class="p-10 border rounded-[2rem] bg-white/5" data-aos="fade-up"><h3 class="text-2xl font-black mb-4">{s.strip()}</h3><p class="opacity-60 text-sm">Professional solution tailored for your specific needs by {biz_name}.</p></div>' for s in biz_serv.splitlines() if s.strip()])
    
    index_content = f"""
    <section class="hero-mask text-white">
        <div data-aos="zoom-in">
            <h1 class="text-6xl md:text-9xl font-black mb-8 leading-none tracking-tighter">{hero_h}</h1>
            <p class="text-xl md:text-2xl opacity-80 mb-12 max-w-3xl mx-auto font-light">{seo_d}</p>
            <a href="#inventory" class="btn-accent">View Collection</a>
        </div>
    </section>
    <section class="py-32 px-8 max-w-7xl mx-auto">
        <h2 class="text-5xl font-black mb-20 text-center" data-aos="fade-up">Core Expertise</h2>
        <div class="grid md:grid-cols-3 gap-10">{s_cards}</div>
    </section>
    <section id="inventory" class="py-32 px-8 bg-gray-50">
        <div class="max-w-7xl mx-auto">
            <h2 class="text-5xl font-black mb-20 text-center" style="color:var(--text)">Exclusive Catalog</h2>
            <div id="inventory-grid" class="grid md:grid-cols-3 gap-10">
                <p class="col-span-full text-center opacity-30">Connecting to Live Data...</p>
            </div>
        </div>
    </section>
    """

    # --- ZIP OUTPUT GENERATION ---
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "w") as zf:
        zf.writestr("index.html", generate_html("Home", index_content, True))
        zf.writestr("about.html", generate_html("About", f"<section class='py-40 px-8 max-w-4xl mx-auto'><h1 class='text-7xl font-black mb-12' data-aos='fade-right'>Our Heritage</h1><div class='text-xl leading-relaxed opacity-70 mb-20'>{about_txt}</div><img src='{img_g}' class='rounded-[3rem] w-full shadow-2xl'></section>"))
        zf.writestr("contact.html", generate_html("Contact", f"<section class='py-40 px-8 max-w-7xl mx-auto grid md:grid-cols-2 gap-20'><div data-aos='fade-up'><h1 class='text-7xl font-black mb-10'>Contact Hub</h1><p class='text-4xl font-bold text-primary mb-4' style='color:var(--p)'>{biz_phone}</p><p class='text-xl opacity-60 mb-10'>{biz_addr}</p><a href='https://wa.me/{wa_clean}' class='btn-accent'>Chat on WhatsApp</a></div><div class='rounded-[3rem] overflow-hidden shadow-2xl h-[500px]'>{map_iframe}</div></section>"))
        zf.writestr("privacy.html", generate_html("Privacy", f"<div class='py-40 px-8 max-w-3xl mx-auto'><h1 class='text-4xl font-black mb-10'>Privacy Policy</h1><div class='opacity-70 whitespace-pre-wrap'>{priv_body}</div></div>"))
        zf.writestr("terms.html", generate_html("Terms", f"<div class='py-40 px-8 max-w-3xl mx-auto'><h1 class='text-4xl font-black mb-10'>Terms & Conditions</h1><div class='opacity-70 whitespace-pre-wrap'>{terms_body}</div></div>"))
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}sitemap.xml")
        zf.writestr("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}index.html</loc></url></urlset>')

    st.balloons()
    st.success("💎 TITAN PLATINUM v13.0 DEPLOYED SUCCESSFULLY")
    st.download_button("📥 DOWNLOAD COMPLETE SUPREME PACKAGE", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_v13_platinum.zip")
