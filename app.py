import streamlit as st
import zipfile
import io
import json
from datetime import datetime

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Kaydiem Titan v12.3 | Flawless Platinum Architect", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: #0f172a; color: white; }
    .stTabs [data-baseweb="tab"] { color: white; font-weight: bold; font-size: 1.1rem; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
        color: white; font-weight: 900; border: none; font-size: 1.4rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); filter: brightness(1.2); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DESIGN STUDIO ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=50)
    st.title("Titan v12.3 Studio")
    
    with st.expander("🎭 1. Layout & DNA", expanded=True):
        layout_dna = st.selectbox("Design DNA", ["Industrial Titan", "Classic Royal", "Soft-UI", "Glass-Tech", "Brutalist", "Corporate Elite"])
        p_color = st.color_picker("Primary Brand Color", "#4A0E0E")
        s_color = st.color_picker("Accent/CTA Color", "#D4AF37")
        border_rad = st.select_slider("Corner Roundness", options=["0px", "12px", "24px", "60px"], value="24px")

    with st.expander("✍️ 2. Typography Studio", expanded=True):
        h_font = st.selectbox("Heading Font", ["Playfair Display", "Oswald", "Montserrat", "Syncopate", "Inter"])
        b_font = st.selectbox("Body Font", ["Montserrat", "Inter", "Roboto", "Open Sans"])
        h_weight = st.select_slider("Heading Weight", options=["300", "400", "700", "900"], value="700")
        ls = st.select_slider("Letter Spacing", options=["-0.05em", "-0.02em", "0em", "0.05em", "0.1em"], value="0.05em")

    gsc_tag_input = st.text_input("GSC Verification Tag")
    st.info("Technical Authority: Kaydiem Script Lab")

st.title("🏗️ Kaydiem Titan Supreme v12.3")

# --- 2. MULTI-TAB DATA COLLECTION ---
tabs = st.tabs(["📍 Identity", "🏗️ Content & SEO", "🖼️ Photo Manager", "⚡ Live E-com", "🌟 Social Proof", "⚖️ Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name (NAP)", "Red Hippo (The Planners)")
        biz_phone = st.text_input("Verified Phone", "+91 84540 02711")
        biz_email = st.text_input("Business Email", "events@redhippoplanners.in")
    with c2:
        biz_cat = st.text_input("Category", "Luxury Wedding Planner")
        biz_hours = st.text_input("Hours", "Mon-Sun: 10:00 - 19:00")
        prod_url = st.text_input("Production URL", "https://kani201012.github.io/site/")
    biz_logo = st.text_input("Logo Image URL")
    biz_addr = st.text_area("Full Maps Physical Address")
    biz_areas = st.text_area("Service Areas", "Vasant Kunj, Chhatarpur, South Delhi")
    map_iframe = st.text_area("Map Embed HTML Code")

with tabs[1]:
    hero_h = st.text_input("Hero Headline", "Crafting Dream Weddings: New Delhi's Premier Luxury Decorators")
    seo_d = st.text_input("Meta Description (160 Chars)")
    biz_key = st.text_input("SEO Keywords")
    biz_serv = st.text_area("Services Listing (One per line)")
    about_txt = st.text_area("Our Story (800+ Words for E-E-A-T)", height=250)

with tabs[2]:
    st.header("📸 Premium Asset Manager")
    custom_hero = st.text_input("Hero Background URL")
    custom_feat = st.text_input("Feature Image URL")
    custom_gall = st.text_input("About Image URL")

with tabs[3]:
    st.header("🛒 Live E-commerce Data")
    sheet_url = st.text_input("Published CSV Link")

with tabs[4]:
    testi_txt = st.text_area("Testimonials (Name | Quote)")
    faq_txt = st.text_area("FAQ (Question? ? Answer)")

with tabs[5]:
    st.header("⚖️ Legal Hub")
    priv_body = st.text_area("Privacy Policy Content", height=300)
    terms_body = st.text_area("Terms Content", height=300)

# --- 3. THE SUPREME ENGINE V12.3 ---

if st.button("🚀 DEPLOY 100% STABLE PLATINUM ASSET"):
    
    # Setup Image logic
    img_h = custom_hero if custom_hero else "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=1600"
    img_f = custom_feat if custom_feat else "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=800"
    img_g = custom_gall if custom_gall else "https://images.unsplash.com/photo-1532712938310-34cb3982ef74?auto=format&fit=crop&q=80&w=1600"

    logo_display = f'<img src="{biz_logo}" alt="{biz_name}" class="h-10 md:h-16 w-auto object-contain">' if biz_logo else f'<span class="text-xl md:text-3xl font-black tracking-tighter uppercase" style="color:var(--p)">{biz_name}</span>'
    
    wa_clean = biz_phone.replace(" ", "").replace("+", "")
    wa_base_url = f"https://wa.me/{wa_clean}?text="
    
    a_list = [a.strip() for a in biz_areas.split(",")]
    s_areas_json = json.dumps(a_list)

    theme_css = f"""
    :root {{ --p: {p_color}; --s: {s_color}; --radius: {border_rad}; }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; width: 100%; overflow-x: hidden; position: relative; scroll-behavior: smooth; }}
    body {{ font-family: '{b_font}', sans-serif; color: #0f172a; line-height: 1.7; background: #fff; }}
    
    /* RECTIFIED TYPOGRAPHY: FORCES WORDS TO WRAP ON MOBILE */
    h1, h2, h3 {{ 
        font-family: '{h_font}', sans-serif; 
        font-weight: {h_weight}; 
        letter-spacing: {ls}; 
        text-transform: uppercase; 
        line-height: 1.1; 
        overflow-wrap: break-word;
        word-break: break-word;
        hyphens: auto;
    }}
    
    .hero-title {{ font-size: clamp(1.4rem, 8vw, 95px); text-shadow: 0 4px 20px rgba(0,0,0,0.4); line-height: 1; }}
    .section-title {{ font-size: clamp(1.6rem, 6vw, 75px); color: var(--p); }}
    
    .btn-p {{ background: var(--p); color: white !important; padding: 0.9rem 2.2rem; border-radius: var(--radius); font-weight: 900; transition: all 0.4s; display: inline-block; text-align: center; border:none; text-decoration:none; text-transform: uppercase; font-size: 11px; }}
    .btn-accent {{ background: var(--s); color: white !important; padding: 1rem 2.5rem; border-radius: var(--radius); font-weight: 900; transition: all 0.4s; display: inline-block; text-align: center; border:none; box-shadow: 0 10px 20px -5px var(--s); text-decoration:none; cursor: pointer; text-transform: uppercase; letter-spacing: 0.1em; font-size: 12px; }}
    .btn-accent:hover {{ transform: translateY(-3px); filter: brightness(1.1); box-shadow: 0 20px 40px -5px var(--s); }}
    
    .glass-nav {{ background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(0,0,0,0.05); width: 100%; z-index: 9999; position: fixed; top: 0; left: 0; }}
    
    .hero-mask {{ 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.5)), url('{img_h}'); 
        background-size: cover; background-position: center; 
        min-height: 85vh; display: flex; align-items: center; justify-content: center; 
        width: 100%; margin: 0; padding: 140px 20px 60px 20px;
    }}
    
    .product-card {{ background: white; border-radius: var(--radius); padding: 2rem; border: 1px solid #f1f5f9; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); transition: 0.3s; cursor: pointer; height: 100%; }}
    
    /* RECTIFIED MODAL ARCHITECTURE */
    #modal {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 100000; padding: 1rem; align-items: center; justify-content: center; overflow-y: auto; }}
    .modal-content {{ background: white; max-width: 1100px; width: 100%; border-radius: var(--radius); overflow: hidden; position: relative; }}
    
    .legal-text {{ white-space: pre-wrap; word-wrap: break-word; font-size: 1.1rem; color: #334155; line-height: 1.9; padding: 20px 0; }}
    .legal-bold-title {{ font-weight: 900; font-size: clamp(2.2rem, 6vw, 4.5rem); color: var(--p); margin-bottom: 2rem; text-transform: uppercase; line-height: 1; }}
    .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; color: white; width: 60px; height: 60px; border-radius: 50px; display: flex; align-items: center; justify-content: center; z-index: 99999; box-shadow: 0 10px 20px rgba(0,0,0,0.2); transition: 0.3s ease; text-decoration:none; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(37,211,102,0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(37,211,102,0); }} 100% {{ box-shadow: 0 0 0 0 rgba(37,211,102,0); }} }}
    """

    def get_layout(title_tag, desc_tag, body_html, is_h=False):
        v_tag = f'<meta name="google-site-verification" content="{gsc_tag_input}">' if (is_h and gsc_tag_input) else ""
        
        # --- RECTIFIED DYNAMIC INJECTION SCRIPT ---
        # Note: Doubled curly braces used for literal JavaScript braces
        dynamic_script = ""
        if is_h and sheet_url:
            dynamic_script = f"""
            <script>
            let currentProducts = [];
            async function fetchLiveData() {{
                try {{
                    const response = await fetch('{sheet_url}');
                    const csvText = await response.text();
                    if (csvText.includes("<!DOCTYPE")) return;
                    
                    const rows = csvText.split('\\n').map(row => row.split('|')).slice(1);
                    const container = document.getElementById('live-data-container');
                    container.innerHTML = "";
                    
                    rows.forEach((parts, idx) => {{
                        if (parts.length >= 2) {{
                            const p = {{ 
                                id: idx, name: parts[0].trim(), price: parts[1].trim(), desc: (parts[2] || "").trim(), 
                                img1: (parts[3] || "{img_f}").trim(), img2: (parts[4] || "").trim(), img3: (parts[5] || "").trim() 
                            }};
                            currentProducts.push(p);
                            container.innerHTML += `
                            <div onclick="openProduct(${{idx}})" class="product-card flex flex-col justify-between transition-all hover:scale-[1.03]">
                                <img src="${{p.img1}}" class="w-full h-56 object-cover mb-6 rounded-[2.5rem] bg-slate-50" onerror="this.src='{img_f}'">
                                <div>
                                    <h3 class="text-2xl font-black mb-2 uppercase" style="color:var(--p)">${{p.name}}</h3>
                                    <p class="font-black text-2xl mb-4 text-s" style="color:var(--s)">${{p.price}}</p>
                                    <p class="text-slate-400 text-[10px] font-black uppercase tracking-widest italic underline decoration-slate-100 underline-offset-4">Click to Open →</p>
                                </div>
                            </div>`;
                        }}
                    }});
                }} catch (e) {{ console.log("Fail"); }}
            }}
            function openProduct(id) {{
                const p = currentProducts[id];
                document.getElementById('m-title').innerText = p.name;
                document.getElementById('m-price').innerText = p.price;
                document.getElementById('m-desc').innerText = p.desc;
                document.getElementById('m-main-img').src = p.img1;
                document.getElementById('m-wa').href = "{wa_base_url}" + encodeURIComponent("I am interested in " + p.name + " (" + p.price + ")");
                document.getElementById('modal').style.display = 'flex';
                document.body.style.overflow = 'hidden';
            }}
            function closeModal() {{ 
                document.getElementById('modal').style.display='none'; 
                document.body.style.overflow='auto'; 
            }}
            window.onload = fetchLiveData;
            </script>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    {v_tag}
    <title>{title_tag} | {biz_name}</title>
    <meta name="description" content="{desc_tag}"><meta name="keywords" content="{biz_key}">
    <link rel="canonical" href="{prod_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@700;900&family={b_font.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
    <style>{theme_css}</style>
</head>
<body class="bg-white">
    <nav class="glass-nav p-4 md:p-6 shadow-sm">
        <div class="max-w-[1440px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <a href="index.html" class="no-underline">{logo_display}</a>
            <div class="flex items-center space-x-6 md:space-x-12 text-[10px] md:text-xs font-black uppercase tracking-widest text-slate-600">
                <a href="index.html" class="hover:text-blue-600 no-underline">Home</a> <a href="about.html" class="hover:text-blue-600 no-underline">About</a> <a href="contact.html" class="hover:text-blue-600 no-underline">Contact</a>
                <a href="tel:{biz_phone}" class="btn-accent" style="padding: 0.5rem 1.5rem; font-size: 10px;">CALL NOW</a>
            </div>
        </div>
    </nav>
    <main class="flex-grow pt-24 md:pt-0">{body_html}</main>
    
    <div id="modal" onclick="if(event.target == this) closeModal()">
        <div class="modal-content shadow-2xl animate-in zoom-in duration-300">
            <div class="grid md:grid-cols-2">
                <div class="p-4 bg-slate-50">
                    <img id="m-main-img" class="w-full h-48 md:h-80 object-cover rounded-[1.5rem] shadow-xl">
                </div>
                <div class="p-6 md:p-12 flex flex-col justify-center text-left">
                    <h2 id="m-title" class="text-2xl md:text-4xl font-black mb-2 uppercase text-p" style="color:var(--p)"></h2>
                    <p id="m-price" class="text-xl md:text-3xl font-black mb-4 text-s" style="color:var(--s)"></p>
                    <p id="m-desc" class="text-slate-600 mb-6 leading-relaxed text-xs md:text-lg"></p>
                    <a id="m-wa" href="#" target="_blank" class="btn-accent w-full uppercase tracking-widest shadow-2xl py-3 md:py-4">Confirm Booking</a>
                    <button onclick="closeModal()" class="text-xs font-black uppercase tracking-widest opacity-30 mt-6 underline no-underline">Close Window</button>
                </div>
            </div>
        </div>
    </div>
    <a href="https://wa.me/{wa_clean}" class="wa-float" target="_blank"><svg style="width:38px;height:38px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></a>

    <footer class="bg-slate-950 text-slate-400 py-24 px-10 border-t border-slate-900">
        <div class="max-w-[1440px] mx-auto grid md:grid-cols-3 gap-16">
            <div>
                {logo_display.replace('h-10 md:h-16', 'h-8 mb-6 opacity-70')}
                <p class="text-sm leading-relaxed mb-10 max-w-md">{biz_addr}</p>
                <p class="text-[10px] opacity-30 font-black uppercase tracking-widest italic tracking-widest underline decoration-white underline-offset-8 decoration-2 text-white">Architected By Kaydiem Script Lab</p>
            </div>
            <div>
                <h4 class="text-white font-bold mb-8 uppercase text-xs tracking-widest">Legal Hub</h4>
                <ul class="space-y-4 text-sm font-bold uppercase list-none p-0 tracking-widest">
                    <li><a href="privacy.html" class="hover:text-white transition no-underline">Privacy Policy</a></li>
                    <li><a href="terms.html" class="hover:text-white transition no-underline">Terms & Conditions</a></li>
                </ul>
            </div>
            <div class="md:text-right">
                <h4 class="text-white font-bold mb-8 uppercase text-xs text-brand tracking-widest underline decoration-blue-600 decoration-4 underline-offset-8 uppercase tracking-widest" style="color:var(--s)">Direct Connect</h4>
                <p class="text-xl mt-4 font-black text-white">{biz_phone}</p>
                <p class="text-xs mt-2 text-slate-500">{biz_email}</p>
            </div>
        </div>
    </footer>
    {dynamic_script}
</body></html>"""

    # --- INDEX ---
    serv_final_html = "".join([f'<div class="bg-slate-50 p-12 rounded-[2.5rem] border border-slate-100 shadow-xl hover:scale-[1.02] transition-transform"><h3 class="text-2xl font-black mb-4 uppercase text-brand" style="color:var(--p)">{s.strip()}</h3><p class="text-slate-500 text-sm leading-relaxed font-bold uppercase tracking-tight italic">Verified technical solution for {biz_name}.</p></div>' for s in biz_serv.splitlines() if s.strip()])
    t_cards = "".join([f'<div class="p-10 bg-slate-50 rounded-[3rem] border border-slate-100 italic text-xl shadow-inner mb-8" style="color:var(--p)">"{t.split("|")[1].strip()}"<br><span class="font-black not-italic text-sm block mt-6 uppercase tracking-widest text-brand" style="color:var(--p)">— {t.split("|")[0].strip()} <span class="text-emerald-500 font-black ml-2 text-xs">● Partner</span></span></div>' for t in testi_txt.splitlines() if "|" in t])
    f_cards = "".join([f'<details class="mb-6 bg-white p-6 rounded-2xl border border-slate-100 cursor-pointer shadow-sm"><summary class="font-black text-lg uppercase tracking-tight">{f.split("?")[0].strip()}?</summary><p class="mt-4 text-slate-600 leading-relaxed font-medium text-sm">{f.split("?")[1].strip()}</p></details>' for f in faq_txt.splitlines() if "?" in f])

    dynamic_section = f"""<section id="inventory" class="py-32 px-6 max-w-[1440px] mx-auto text-center border-b"><h2 class="section-title mb-20 uppercase tracking-tighter" style="color:var(--p)">Exclusive Collection</h2><div id="live-data-container" class="grid grid-cols-1 md:grid-cols-4 gap-10 text-left"><p class="p-20 text-center text-slate-400 font-bold animate-pulse uppercase tracking-widest">Opening Data Hub...</p></div></section>""" if sheet_url else ""

    idx_content = f"""
    <section class="hero-mask px-6 text-center text-white">
        <div class="max-w-[1200px] mx-auto">
            <h1 class="hero-title mb-10 uppercase tracking-tighter leading-none">{hero_h}</h1>
            <p class="text-lg md:text-3xl font-light mb-16 max-w-4xl mx-auto opacity-90 leading-tight">{seo_d}</p>
            <a href="#inventory" class="btn-accent uppercase tracking-[0.4em] text-[10px] md:text-sm shadow-2xl">Discover Packages</a>
        </div>
    </section>
    
    <section class="max-w-[1440px] mx-auto py-24 px-6 text-center border-b">
        <h2 class="section-title mb-20 uppercase tracking-tighter" style="color:var(--p)">Our Expertise</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-left">{serv_final_html}</div>
    </section>
    {dynamic_section}
    <section class="bg-slate-50 py-32 px-6 border-y text-left">
        <div class="max-w-[1440px] mx-auto grid md:grid-cols-2 gap-24 items-center">
            <img src="{img_f}" class="shadow-2xl" style="border-radius: var(--radius)">
            <div>
                <h2 class="text-5xl font-black mb-12 uppercase tracking-tighter leading-none" style="color:var(--p)">Verified Heritage</h2>
                <p class="text-2xl text-slate-600 mb-12 leading-relaxed italic">"Supplying the engineering foundation for the 2026 city landscape. Precision execution, certified safety, and direct quality oversight."</p>
                <a href="about.html" class="btn-p">Read Full Story</a>
            </div>
        </div>
    </section>
    <section class="py-32 px-6 max-w-7xl mx-auto text-center"><div class="grid md:grid-cols-2 gap-24 text-left"><div><h2 class="text-4xl font-black mb-16 uppercase tracking-tighter" style="color:var(--p)">Success Stories</h2>{t_cards}</div><div><h2 class="text-4xl font-black mb-16 uppercase tracking-tighter" style="color:var(--p)">Expert Insights</h2>{f_cards}</div></div></section>
    """

    # --- ZIP OUTPUT ---
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as z_f:
        z_f.writestr("index.html", get_layout("Home", seo_d, idx_content, True))
        z_f.writestr("about.html", get_layout("About", "History", f"<section class='max-w-7xl mx-auto py-32 px-6'><h1 class='legal-bold-title uppercase tracking-tighter text-brand' style='color:var(--p)'>About Our Heritage</h1><div class='text-xl md:text-2xl leading-relaxed text-slate-700 legal-text'>{about_txt}</div><img src='{img_g}' class='mt-20 w-full h-[600px] object-cover shadow-2xl' style='border-radius: var(--radius)'></section>"))
        z_f.writestr("contact.html", get_layout("Contact", "Location", f"<section class='max-w-[1440px] mx-auto py-32 px-6 text-center'><h1 class='legal-bold-title uppercase tracking-tighter text-brand' style='color:var(--p)'>Technical Hub</h1><div class='grid md:grid-cols-2 gap-16 text-left'><div class='bg-slate-950 p-12 md:p-24 text-white' style='border-radius: var(--radius)'><p class='text-4xl font-black mb-8 text-white'>{biz_phone}</p><p class='text-2xl mb-12 opacity-80'>{biz_addr}</p><a href='tel:{biz_phone}' class='btn-accent w-full no-underline uppercase tracking-widest font-black'>Book Consultation</a></div><div class='rounded-[3rem] overflow-hidden border shadow-2xl bg-slate-100' style='min-height:300px'>{map_iframe}</div></div></section>"))
        z_f.writestr("privacy.html", get_layout("Privacy", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10'><h1 class='legal-bold-title uppercase tracking-tighter text-brand' style='color:var(--p)'>Privacy Policy</h1><div class='text-lg legal-text'>{priv_body}</div></div>"))
        z_f.writestr("terms.html", get_layout("Terms", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10'><h1 class='legal-bold-title uppercase tracking-tighter text-brand' style='color:var(--p)'>Terms & Conditions</h1><div class='text-lg legal-text'>{terms_body}</div></div>"))
        z_f.writestr("404.html", get_layout("404", "Not Found", "<div class='py-64 text-center'><h1 class='text-[120px] font-black uppercase text-slate-200 tracking-widest'>404</h1></div>"))
        z_f.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}sitemap.xml")
        z_f.writestr("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}index.html</loc></url><url><loc>{prod_url}about.html</loc></url></urlset>')

    st.success("💎 TITAN SUPREME v12.3 FINAL PLATINUM DEPLOYED. Fixed Modal & Variable Names.")
    st.download_button("📥 DOWNLOAD COMPLETE BIZ PACKAGE", z_b.getvalue(), f"{biz_name.lower().replace(' ', '_')}_v12_3.zip")
