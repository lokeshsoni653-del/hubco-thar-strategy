import folium
from folium.plugins import HeatMap, Fullscreen, Draw
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
 
# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HUBCO Thar Strategy | Lokesh Kumar",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ═══════════════════════════════════════════════════════════════
#  DESIGN TOKENS & GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
 
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
 
/* ── Root Variables ── */
:root {
    --navy-950:  #030B1A;
    --navy-900:  #05112F;
    --navy-800:  #081840;
    --navy-700:  #0D2255;
    --slate-800: #1A2035;
    --slate-700: #212840;
    --slate-600: #2A3350;
    --slate-300: #6B7594;
    --slate-100: #B8BFD4;
    --slate-50:  #E2E5F0;
    --amber-500: #D4700A;
    --amber-400: #E8830A;
    --amber-300: #F5A623;
    --gold:      #D4AF37;
    --gold-dim:  #9E8120;
    --teal-500:  #0D9488;
    --teal-300:  #2DD4BF;
    --red-500:   #DC2626;
    --red-300:   #F87171;
    --green-500: #16A34A;
    --green-300: #4ADE80;
    --text-pri:  #E8EAF2;
    --text-sec:  #9BA3BF;
    --text-mut:  #5C6480;
    --border:    rgba(255,255,255,0.07);
    --border-md: rgba(255,255,255,0.12);
    --r-xl: 14px;
    --r-lg: 10px;
    --r-md: 7px;
    --shadow: 0 4px 24px rgba(0,0,0,0.45), 0 1px 4px rgba(0,0,0,0.3);
}
 
/* ── App Background ── */
.stApp {
    background: linear-gradient(160deg, #040d20 0%, #060f28 40%, #040b1c 100%);
    font-family: 'DM Sans', system-ui, sans-serif;
}
 
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #05112F 0%, #040d1f 100%) !important;
    border-right: 1px solid var(--border-md) !important;
}
[data-testid="stSidebar"] * { color: var(--text-sec) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--text-pri) !important; }
[data-testid="stSidebar"] .stSlider > label,
[data-testid="stSidebar"] .stNumberInput > label { color: var(--text-sec) !important; font-size: 0.78rem !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stSidebar"] hr { border-color: var(--border-md) !important; }
 
/* ── Slider thumb amber ── */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--gold) !important;
    box-shadow: 0 0 8px rgba(212,175,55,0.6) !important;
}
 
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-bottom: 1px solid var(--border-md) !important;
    border-radius: var(--r-lg) var(--r-lg) 0 0 !important;
    padding: 0 6px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.80rem !important;
    font-weight: 600 !important;
    color: var(--text-mut) !important;
    padding: 10px 18px !important;
    border-radius: var(--r-md) var(--r-md) 0 0 !important;
    letter-spacing: 0.02em !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    background: rgba(212,175,55,0.07) !important;
    border-bottom: 2px solid var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-xl) var(--r-xl) !important;
    padding: 24px !important;
}
 
/* ── Plotly charts transparent bg ── */
.js-plotly-plot .plotly { background: transparent !important; }
 
/* ── Metrics override ── */
[data-testid="stMetric"] {
    background: var(--slate-800) !important;
    border: 1px solid var(--border-md) !important;
    border-radius: var(--r-xl) !important;
    padding: 18px 20px !important;
    box-shadow: var(--shadow) !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--amber-500), var(--gold));
}
[data-testid="stMetricLabel"] > div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: var(--text-mut) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}
[data-testid="stMetricValue"] > div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-pri) !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] > div {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
}
 
/* ── st.info / st.success / st.error ── */
[data-testid="stInfo"] {
    background: rgba(13,148,136,0.08) !important;
    border: 1px solid rgba(45,212,191,0.2) !important;
    border-radius: var(--r-lg) !important;
    color: var(--teal-300) !important;
}
[data-testid="stAlert"][kind="success"] {
    background: rgba(22,163,74,0.10) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: var(--r-lg) !important;
    color: var(--green-300) !important;
}
[data-testid="stAlert"][kind="error"] {
    background: rgba(220,38,38,0.10) !important;
    border: 1px solid rgba(248,113,113,0.25) !important;
    border-radius: var(--r-lg) !important;
}
 
/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--amber-500), var(--gold)) !important;
    color: #05112F !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 10px 22px !important;
    box-shadow: 0 2px 12px rgba(212,175,55,0.35) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    box-shadow: 0 4px 22px rgba(212,175,55,0.55) !important;
    transform: translateY(-1px) !important;
}
 
/* ── Selectbox / Radio ── */
[data-testid="stSelectbox"] > div,
[data-testid="stSelectbox"] select {
    background: var(--slate-700) !important;
    border: 1px solid var(--border-md) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-pri) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stRadio"] label { color: var(--text-sec) !important; font-size: 0.83rem !important; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] { color: var(--text-sec) !important; }
 
/* ── Camera input ── */
[data-testid="stCameraInput"] {
    border: 1px solid var(--border-md) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
}
 
/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(212,175,55,0.12) !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    color: var(--gold) !important;
    border-radius: var(--r-md) !important;
}
 
/* ── Checkboxes ── */
[data-testid="stCheckbox"] label { color: var(--text-sec) !important; }
[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] { color: var(--text-sec) !important; }
 
/* ── Markdown text in main area ── */
.main [data-testid="stMarkdownContainer"] h1,
.main [data-testid="stMarkdownContainer"] h2,
.main [data-testid="stMarkdownContainer"] h3,
.main [data-testid="stMarkdownContainer"] h4 { color: var(--text-pri) !important; }
.main [data-testid="stMarkdownContainer"] p,
.main [data-testid="stMarkdownContainer"] li { color: var(--text-sec) !important; }
.main [data-testid="stMarkdownContainer"] strong { color: var(--text-pri) !important; }
.main [data-testid="stMarkdownContainer"] code {
    background: rgba(212,175,55,0.1) !important;
    color: var(--gold) !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82em !important;
    padding: 2px 6px !important;
}
 
/* ── Divider ── */
hr { border-color: var(--border-md) !important; }
 
/* ── Caption text ── */
[data-testid="stCaptionContainer"] { color: var(--text-mut) !important; font-size: 0.75rem !important; }
 
/* ── Column gaps ── */
[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  PLOTLY THEME HELPER
# ═══════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    font_family="DM Sans, system-ui, sans-serif",
    font_color="#9BA3BF",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.04)",
        bordercolor="rgba(255,255,255,0.10)",
        borderwidth=1,
        font=dict(color="#B8BFD4", size=11),
    ),
    title_font=dict(size=13, color="#E8EAF2", family="DM Sans"),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#5C6480", size=10),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#5C6480", size=10),
    ),
    colorway=["#D4AF37", "#3B82F6", "#F5A623", "#2DD4BF", "#F87171"],
)
AMBER  = "#D4AF37"
BLUE   = "#3B82F6"
ORANGE = "#F5A623"
TEAL   = "#2DD4BF"
 
# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(212,175,55,0.08) 0%, rgba(5,17,47,0.6) 100%);
    border: 1px solid rgba(212,175,55,0.15);
    border-left: 4px solid #D4AF37;
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 24px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 12px;
">
    <div>
        <div style="font-family:'DM Sans',sans-serif; font-size:1.75rem; font-weight:800;
                    color:#E8EAF2; letter-spacing:-0.03em; line-height:1.15; margin-bottom:5px;">
            🏜️ HUBCO Thar Plant: BD &amp; CSR Strategy Engine
        </div>
        <div style="font-family:'DM Sans',sans-serif; font-size:0.9rem; color:#9BA3BF; line-height:1.5;">
            Spatial Optimization for Corporate Social Responsibility (CSR) Infrastructure in Tharparkar.
        </div>
    </div>
    <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
        <span style="
            font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:700;
            color:#4ADE80; background:rgba(22,163,74,0.12); border:1px solid rgba(74,222,128,0.25);
            padding:5px 13px; border-radius:99px; text-transform:uppercase; letter-spacing:.08em;
            display:flex; align-items:center; gap:5px;">
            <span style="width:6px;height:6px;background:#4ADE80;border-radius:50%;
                         box-shadow:0 0 6px #4ADE80;display:inline-block"></span>
            Live Prototype
        </span>
        <span style="
            font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:700;
            color:#D4AF37; background:rgba(212,175,55,0.10); border:1px solid rgba(212,175,55,0.25);
            padding:5px 13px; border-radius:99px; letter-spacing:.04em;">
            🏗️ Architected by Lokesh Kumar &nbsp;·&nbsp; Native Context: Mithi, Sindh
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  DATA SIMULATION (unchanged logic, seed=42)
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_thar_data():
    np.random.seed(42)
    lats = np.random.uniform(24.7000, 24.9000, 80)
    lons = np.random.uniform(69.7500, 70.3500, 80)
    water_scarcity = np.random.randint(50, 100, 80)
    population = np.random.randint(500, 5000, 80)
    return pd.DataFrame({
        'Latitude': lats, 'Longitude': lons,
        'Water_Scarcity_Index': water_scarcity, 'Village_Population': population
    })
 
df = load_thar_data()
 
landmarks = {
    "HUBCO Thar Energy Ltd (TEL)": [24.7977, 70.2808],
    "Mithi (Regional Hub)":        [24.7370, 69.7971],
    "Islamkot":                    [24.7946, 70.1804]
}
 
# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo area
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 16px;">
        <div style="font-size:2.4rem; margin-bottom:6px;">🏜️</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:1.0rem; font-weight:800;
                    color:#E8EAF2; letter-spacing:-0.01em;">HUBCO Thar</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:0.68rem; font-weight:700;
                    color:#D4AF37; text-transform:uppercase; letter-spacing:.12em;">Strategy Engine</div>
        <div style="margin-top:10px; padding:4px 12px; border-radius:99px;
                    background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.2);
                    display:inline-block; font-size:0.68rem; font-weight:600; color:#F5A623;">
            Block II · Tharparkar
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin: 0 0 16px;">
    """, unsafe_allow_html=True)
 
    st.markdown("### 📈 BD & CSR Budget (FY-26)")
    csr_budget = st.slider("Total Allocation (Millions PKR)", 50, 500, 150) * 1_000_000
 
    st.markdown("### 🏗️ Infrastructure Costs")
    cost_ro_plant = st.number_input("Cost per RO Water Plant (PKR)", value=8_000_000, step=500_000)
    cost_solar    = st.number_input("Cost per Solar Microgrid (PKR)", value=12_000_000, step=500_000)
 
    st.markdown("### 🎯 Intervention Targeting")
    min_scarcity = st.slider("Target Minimum Water Scarcity", 0, 100, 75)
    min_pop      = st.slider("Target Minimum Population", 500, 5000, 1500)
 
    st.divider()
 
    # Developer card
    st.markdown("""
    <div style="
        background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.15);
        border-radius:10px; padding:12px 14px; margin-top:4px;
    ">
        <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:700;
                    color:#D4AF37; text-transform:uppercase; letter-spacing:.08em; margin-bottom:5px;">
            Developer
        </div>
        <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; font-weight:600;
                    color:#E8EAF2;">Lokesh Kumar</div>
        <div style="font-size:0.72rem; color:#9BA3BF; margin-top:2px;">
            Native Context: Mithi, Sindh
        </div>
    </div>
    <div style="font-family:'DM Sans',sans-serif; font-size:0.7rem; color:#5C6480;
                margin-top:10px; padding-left:2px;">
        Strategic Focus: Block II &amp; Surrounding Communities
    </div>
    """, unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  ALGORITHM LOGIC (unchanged)
# ═══════════════════════════════════════════════════════════════
target_villages = df[
    (df['Water_Scarcity_Index'] >= min_scarcity) &
    (df['Village_Population']   >= min_pop)
].copy()
 
target_villages = target_villages.sort_values('Water_Scarcity_Index', ascending=False)
target_villages['Project_Type'] = np.where(
    target_villages['Water_Scarcity_Index'] > 85, "RO Water Plant", "Solar Microgrid"
)
target_villages['Project_Cost'] = np.where(
    target_villages['Project_Type'] == "RO Water Plant", cost_ro_plant, cost_solar
)
target_villages['Cumulative_Cost'] = target_villages['Project_Cost'].cumsum()
target_villages['Status'] = np.where(
    target_villages['Cumulative_Cost'] <= csr_budget, "Approved (Funded)", "Waitlisted"
)
 
funded_projects = target_villages[target_villages['Status'] == "Approved (Funded)"]
total_capex      = funded_projects['Project_Cost'].sum()
lives_impacted   = funded_projects['Village_Population'].sum()
ro_count         = len(funded_projects[funded_projects['Project_Type'] == "RO Water Plant"])
solar_count      = len(funded_projects[funded_projects['Project_Type'] == "Solar Microgrid"])
budget_pct       = int((total_capex / csr_budget) * 100) if csr_budget else 0
 
# ═══════════════════════════════════════════════════════════════
#  TOP-LEVEL KPI STRIP (above tabs)
# ═══════════════════════════════════════════════════════════════
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("🏘️ Villages Funded",     len(funded_projects),            f"of {len(target_villages)} targeted")
with kpi2:
    st.metric("👥 Lives Impacted",       f"{lives_impacted:,}",           "↑ ESG milestone")
with kpi3:
    st.metric("💰 CAPEX Utilized",       f"Rs. {total_capex/1e6:.1f} M",  f"{budget_pct}% of budget")
with kpi4:
    st.metric("⚡ Projects Deployed",    f"{ro_count} RO · {solar_count} Solar", "Active CSR footprint")
 
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  SECTION LABEL HELPER
# ═══════════════════════════════════════════════════════════════
def section_label(text):
    st.markdown(f"""
    <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:700;
                color:#5C6480; text-transform:uppercase; letter-spacing:.10em;
                margin:0 0 12px; padding-left:2px;">
        {text}
    </div>""", unsafe_allow_html=True)
 
def card_header(title, subtitle=""):
    sub = f"<div style='font-size:.78rem;color:#5C6480;margin-top:2px'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"""
    <div style="font-family:'DM Sans',sans-serif; font-size:.85rem; font-weight:700;
                color:#E8EAF2; letter-spacing:.02em; margin-bottom:14px;">
        {title}{sub}
    </div>""", unsafe_allow_html=True)
 
def esg_box(html_content):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(212,175,55,0.07), rgba(5,17,47,0.4));
        border: 1px solid rgba(212,175,55,0.2); border-left: 3px solid #D4AF37;
        border-radius: 10px; padding: 16px 20px; margin-top: 16px;
        font-family: 'DM Sans', sans-serif;
    ">
        {html_content}
    </div>""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  ENTERPRISE TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  Regional Deployment",
    "📊  CSR Financials",
    "🤝  Community Dynamics",
    "📸  Field Audits",
    "🛡️  Fleet Safety"
])
 
# ───────────────────────────────────────────────────────────────
#  TAB 1 — REGIONAL DEPLOYMENT
# ───────────────────────────────────────────────────────────────
with tab1:
    section_label("Tharparkar Block II · Intervention Deployment Map")
 
    st.markdown("""
    <div style="
        display:flex; gap:20px; margin-bottom:16px; flex-wrap:wrap;
    ">
        <div style="display:flex;align-items:center;gap:6px;font-size:.78rem;color:#9BA3BF">
            <span style="width:10px;height:10px;border-radius:50%;background:#3B82F6;display:inline-block"></span>
            RO Water Plant (Funded)
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:.78rem;color:#9BA3BF">
            <span style="width:10px;height:10px;border-radius:50%;background:#F5A623;display:inline-block"></span>
            Solar Microgrid (Funded)
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:.78rem;color:#9BA3BF">
            <span style="width:10px;height:10px;border-radius:50%;background:#9CA3AF;display:inline-block"></span>
            Waitlisted
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:.78rem;color:#9BA3BF">
            <span style="width:10px;height:10px;border-radius:50%;background:#D4AF37;border:2px solid #fff;display:inline-block"></span>
            Key Landmark
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    m = folium.Map(location=[24.7977, 70.1804], zoom_start=11, tiles="CartoDB positron")
    Fullscreen(position='topright').add_to(m)
    Draw(export=True, position='topleft', draw_options={'polyline': False, 'circlemarker': False}).add_to(m)
 
    heat_data = [[row['Latitude'], row['Longitude'], row['Water_Scarcity_Index']]
                 for _, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=10,
            gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}).add_to(m)
 
    for name, coords in landmarks.items():
        folium.Marker(
            coords, popup=f"<b style='color:#0056b3'>{name}</b>",
            icon=folium.Icon(color="black", icon="building", prefix='fa')
        ).add_to(m)
 
    for idx, row in target_villages.iterrows():
        color     = "lightgray" if row['Status'] == "Waitlisted" else ("blue" if row['Project_Type'] == "RO Water Plant" else "orange")
        icon_type = "tint" if row['Project_Type'] == "RO Water Plant" else "sun"
        html_card = f"""
        <div style="font-family:'DM Sans',Arial,sans-serif; width:220px;">
            <h4 style="margin:0 0 8px; color:#0056b3; font-size:12px;
                       border-bottom:2px solid #e5e7eb; padding-bottom:5px;">
                Site Intervention Audit
            </h4>
            <table style="width:100%;border-collapse:collapse;font-size:11.5px;color:#374151;">
                <tr><td style="padding:4px 0;font-weight:600;width:45%">Project Type:</td>
                    <td style="padding:4px 0">{row['Project_Type']}</td></tr>
                <tr><td style="padding:4px 0;font-weight:600">Est. Population:</td>
                    <td style="padding:4px 0">{row['Village_Population']:,}</td></tr>
                <tr><td style="padding:4px 0;font-weight:600">Scarcity Index:</td>
                    <td style="padding:4px 0">{row['Water_Scarcity_Index']}/100</td></tr>
                <tr><td style="padding:4px 0;font-weight:600">Funding Status:</td>
                    <td style="padding:4px 0">{row['Status']}</td></tr>
                <tr><td style="padding:4px 0;font-weight:600">CAPEX Reqd:</td>
                    <td style="padding:4px 0">Rs. {row['Project_Cost']/1e6:.1f} M</td></tr>
            </table>
        </div>"""
        iframe = folium.IFrame(html=html_card, width=250, height=180)
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(iframe, max_width=260),
            tooltip=row['Project_Type'],
            icon=folium.Icon(color=color, icon=icon_type, prefix='fa')
        ).add_to(m)
 
    st_folium(m, width="100%", height=500)
 
# ───────────────────────────────────────────────────────────────
#  TAB 2 — CSR FINANCIALS
# ───────────────────────────────────────────────────────────────
with tab2:
    section_label("Business Development · CSR Allocation & ROI")
 
    col_left, col_right = st.columns([1.1, 1], gap="large")
 
    with col_left:
        card_header("CSR Fund Distribution by Type", "CAPEX breakdown across intervention categories")
        if not funded_projects.empty:
            fig_donut = px.pie(
                funded_projects, names='Project_Type', values='Project_Cost',
                hole=0.58,
                color='Project_Type',
                color_discrete_map={"RO Water Plant": BLUE, "Solar Microgrid": ORANGE}
            )
            fig_donut.update_traces(
                textposition='outside', textinfo='percent+label',
                marker=dict(line=dict(color='rgba(0,0,0,0.3)', width=2)),
                hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}<br>%{percent}<extra></extra>"
            )
            fig_donut.update_layout(
                **PLOTLY_LAYOUT,
                showlegend=False,
                title=None,
                height=300,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No funded projects match the current filter criteria.")
 
    with col_right:
        card_header("Budget Utilization Breakdown", "Funded vs. available allocation")
 
        # Budget progress bar visual
        ro_capex    = ro_count    * cost_ro_plant
        solar_capex = solar_count * cost_solar
        ro_pct      = min(int((ro_capex    / csr_budget) * 100), 100) if csr_budget else 0
        solar_pct   = min(int((solar_capex / csr_budget) * 100), 100) if csr_budget else 0
        total_pct   = min(budget_pct, 100)
 
        def progress_row(label, pct, color, val_text):
            st.markdown(f"""
            <div style="margin-bottom:14px">
                <div style="display:flex;justify-content:space-between;
                            font-size:.78rem;margin-bottom:5px;">
                    <span style="color:#9BA3BF;font-weight:500">{label}</span>
                    <span style="color:#D4AF37;font-weight:600;font-family:'DM Mono',monospace">{val_text}</span>
                </div>
                <div style="height:6px;background:rgba(255,255,255,0.08);border-radius:99px;overflow:hidden">
                    <div style="height:100%;width:{pct}%;background:{color};border-radius:99px;
                                transition:width .5s ease"></div>
                </div>
            </div>""", unsafe_allow_html=True)
 
        progress_row("RO Water Plants",  ro_pct,    f"linear-gradient(90deg,{BLUE},{TEAL})",   f"Rs. {ro_capex/1e6:.1f}M")
        progress_row("Solar Microgrids", solar_pct, f"linear-gradient(90deg,{ORANGE},{AMBER})",f"Rs. {solar_capex/1e6:.1f}M")
        progress_row("Total Budget Used",total_pct, f"linear-gradient(90deg,#DC2626,{ORANGE})",f"{total_pct}%")
 
       cost_per_life = int(total_capex / lives_impacted) if lives_impacted else 0
        esg_box(f"""
<div style="font-size:.72rem;font-weight:700;color:#D4AF37;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">
    📌 Cost per Life Impacted
</div>
<div style="font-size:1.6rem;font-weight:700;color:#F5A623;margin-bottom:4px">
    Rs. {cost_per_life:,}
</div>
<div style="font-size:.75rem;color:#9BA3BF">
    PKR per beneficiary &nbsp;·&nbsp; World Bank ESG threshold: &lt; Rs. 15,000
</div>
""")
 
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
 
    # Cumulative CAPEX line chart
    if not target_villages.empty:
        section_label("Cumulative CAPEX vs. Budget Ceiling")
        target_sorted = target_villages.copy().reset_index(drop=True)
        target_sorted['Site #'] = target_sorted.index + 1
 
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=target_sorted['Site #'],
            y=target_sorted['Cumulative_Cost'] / 1e6,
            mode='lines', name='Cumulative CAPEX',
            line=dict(color=ORANGE, width=2.5),
            fill='tozeroy', fillcolor='rgba(245,166,35,0.07)',
            hovertemplate='Site %{x}<br>Rs. %{y:.1f}M<extra></extra>'
        ))
        fig_line.add_hline(
            y=csr_budget / 1e6, line_dash='dash',
            line_color='#DC2626', line_width=1.8,
            annotation_text=f"Budget: Rs. {csr_budget/1e6:.0f}M",
            annotation_font_color='#F87171', annotation_font_size=10
        )
        fig_line.update_layout(
            **PLOTLY_LAYOUT, height=250,
            xaxis_title="Site Priority Rank",
            yaxis_title="Cumulative Cost (Rs. M)",
            showlegend=False,
        )
        st.plotly_chart(fig_line, use_container_width=True)
 
    esg_box(f"""
        <h4 style="margin:0 0 6px;font-size:.9rem;color:#D4AF37;">🌱 Thar Foundation Impact Statement</h4>
        <p style="margin:0;font-size:.85rem;color:#9BA3BF;line-height:1.65">
            By deploying <b style="color:#F5A623">{ro_count} RO Plants</b> and
            <b style="color:#F5A623">{solar_count} Solar Microgrids</b>, HUBCO directly elevates the living
            standards of <b style="color:#F5A623">{lives_impacted:,}</b> residents in the Thar Coal Block II
            radius, securing vital community goodwill and fulfilling corporate ESG mandates.
        </p>""")
 
# ───────────────────────────────────────────────────────────────
#  TAB 3 — COMMUNITY DYNAMICS
# ───────────────────────────────────────────────────────────────
with tab3:
    section_label("Local Dynamics · Dhatki Multilingual AI (PoC)")
    st.markdown("""
    <p style="color:#9BA3BF;font-size:.85rem;margin-bottom:18px;line-height:1.65">
        A Proof of Concept demonstrating how incoming SMS grievances from local communities can be
        auto-translated for English-speaking management and Chinese CPEC engineering teams.
    </p>""", unsafe_allow_html=True)
 
    col_inbox, col_output = st.columns([1, 1], gap="large")
 
    mock_dhatki_data = {
        "Maaye gaon mein paani ko maslo hai, RO plant kharab hai.": {
            "english": "There is a water problem in our village, the RO plant is broken.",
            "chinese": "我们的村庄供水出现问题，反渗透水处理设备坏了。 (Wǒmen de cūnzhuāng gōngshuǐ chūxiàn wèntí...)",
            "category": "Maintenance - RO Plant",
            "priority": "🔴 High",
            "action": "Dispatch technician to Islamkot Block II"
        },
        "Solar panel ri battery charge koni pyi they.": {
            "english": "The solar panel battery is not charging.",
            "chinese": "太阳能电池板的电池无法充电。 (Tàiyángnéng diànchí bǎn de diànchí wúfǎ chōngdiàn.)",
            "category": "Maintenance - Solar",
            "priority": "🟡 Medium",
            "action": "Schedule battery replacement assessment"
        },
        "School mein master koni aayo aaj.": {
            "english": "The teacher did not come to the school today.",
            "chinese": "今天老师没有来学校。 (Jīntiān lǎoshī méiyǒu lái xuéxiào.)",
            "category": "CSR - Education",
            "priority": "🟢 Low",
            "action": "Log for monthly Thar Foundation review"
        }
    }
 
    with col_inbox:
        card_header("📥 Live SMS Grievance Inbox", "Simulated · Dhatki / Roman Script")
        selected_phrase = st.selectbox(
            "Select incoming SMS:", list(mock_dhatki_data.keys()), label_visibility="collapsed"
        )
        target_lang = st.radio(
            "Output Language:", ["🇬🇧 English", "🇨🇳 Mandarin Chinese (CPEC Teams)"],
            horizontal=True
        )
        process_btn = st.button("🧠 Process via NLP Translation Engine")
 
    with col_output:
        card_header("Translation Output", "Intent extraction + priority routing")
        if process_btn:
            with st.spinner(f"Routing through Dhatki-to-{target_lang.split(' ')[1]} pipeline..."):
                import time; time.sleep(1.5)
            result = mock_dhatki_data[selected_phrase]
            translation_text = result['english'] if "English" in target_lang else result['chinese']
            st.success("✅ Translation and Intent Extraction Complete")
            st.markdown(f"""
            <div style="background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.15);
                        border-radius:10px;padding:14px 16px;margin-bottom:10px">
                <div style="font-size:.7rem;font-weight:700;color:#D4AF37;
                            text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px">
                    Translated Output
                </div>
                <div style="font-size:.88rem;color:#E8EAF2;line-height:1.6;font-style:italic">
                    {translation_text}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                            border-radius:8px;padding:12px 14px">
                    <div style="font-size:.68rem;font-weight:700;color:#5C6480;
                                text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Category</div>
                    <div style="font-size:.82rem;color:#F5A623;font-weight:600">{result['category']}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                            border-radius:8px;padding:12px 14px">
                    <div style="font-size:.68rem;font-weight:700;color:#5C6480;
                                text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Priority</div>
                    <div style="font-size:.82rem;color:#E8EAF2;font-weight:600">{result['priority']}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                            border-radius:8px;padding:12px 14px;grid-column:span 2">
                    <div style="font-size:.68rem;font-weight:700;color:#5C6480;
                                text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">
                        Recommended Action
                    </div>
                    <div style="font-size:.82rem;color:#2DD4BF;font-weight:600">{result['action']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display:flex;align-items:center;justify-content:center;
                        height:200px;flex-direction:column;gap:10px;
                        border:1px dashed rgba(255,255,255,0.1);border-radius:10px">
                <div style="font-size:2rem">🤖</div>
                <div style="font-size:.82rem;color:#5C6480">
                    Select a grievance and click Process
                </div>
            </div>""", unsafe_allow_html=True)
 
    st.divider()
    st.info("💡 **Architecture Note:** This UI currently runs on simulated rule-based data. The architecture is designed to seamlessly integrate with a live Multilingual LLM API once the Dhatki dataset is fully compiled.")
 
# ───────────────────────────────────────────────────────────────
#  TAB 4 — FIELD AUDITS
# ───────────────────────────────────────────────────────────────
with tab4:
    section_label("Field Operations · Mithi / Islamkot Hub")
 
    col_cam, col_info = st.columns([1, 1], gap="large")
    with col_cam:
        card_header("📸 Site Audit Camera", "Capture groundwater drilling site audits")
        st.write("Field engineers can capture pre-deployment site audits directly into the BD system.")
        site_photo = st.camera_input("Capture Audit Image")
        if site_photo:
            st.success("✅ Audit image verified from field location.")
            st.download_button("💾 Save to CSR Report", data=site_photo,
                               file_name="Thar_Audit.png", mime="image/png")
 
    with col_info:
        card_header("📋 Audit Protocol", "Standard pre-deployment site checklist")
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:8px">
        """, unsafe_allow_html=True)
        checks = [
            ("🌊", "Groundwater Depth Assessment",   "Measure drilling depth and yield"),
            ("📍", "GPS Coordinate Confirmation",     "Match with Block II grid reference"),
            ("👥", "Community Representative Present","Village elder or council member"),
            ("🔧", "Site Accessibility Check",        "Road access for equipment transport"),
            ("📋", "Environmental Impact Flag",        "EPA compliance pre-check"),
        ]
        for icon, title, sub in checks:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:12px">
                <span style="font-size:1.2rem">{icon}</span>
                <div>
                    <div style="font-size:.82rem;font-weight:600;color:#E8EAF2">{title}</div>
                    <div style="font-size:.72rem;color:#5C6480;margin-top:1px">{sub}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
 
# ───────────────────────────────────────────────────────────────
#  TAB 5 — FLEET SAFETY
# ───────────────────────────────────────────────────────────────
with tab5:
    section_label("Fleet Safety & Inclusion Hub")
    st.markdown("""
    <p style="color:#9BA3BF;font-size:.85rem;margin-bottom:18px">
        Dedicated monitoring and emergency response interface for the
        <b style="color:#E8EAF2">Women Dump Truck Drivers Initiative</b> at Thar Coal Block II.
    </p>""", unsafe_allow_html=True)
 
    # Fleet KPIs with custom styling
    fa, fb, fc = st.columns(3)
    with fa:
        st.metric("Active Female Drivers",      "42",                     "+3 this month")
    with fb:
        st.metric("Current Shift",              "Night (18:00–06:00)",    "High Alert")
    with fc:
        st.metric("SOS Incidents (Last 30 Days)", "0",                    "-1", delta_color="inverse")
 
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
 
    col_sos, col_mobile = st.columns([1, 1], gap="large")
 
    with col_sos:
        card_header("🚨 Emergency Dispatch Simulation")
        st.info("In a live environment, this dashboard receives SOS signals triggered via physical panic buttons installed in the dump truck cabins.")
        sos_active = st.checkbox("Simulate Incoming SOS Alert")
 
        if sos_active:
            st.markdown("""
            <div style="
                background:rgba(220,38,38,0.10);border:1px solid rgba(248,113,113,0.3);
                border-radius:10px;padding:18px 20px;animation: pulse 2s infinite;
            ">
                <div style="font-size:.95rem;font-weight:800;color:#F87171;
                            margin-bottom:12px;display:flex;align-items:center;gap:8px">
                    ⚠️ URGENT SOS RECEIVED — ACTIVE INCIDENT
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                    <div><div style="font-size:.68rem;color:#5C6480;margin-bottom:2px">Driver</div>
                         <div style="font-size:.85rem;color:#E8EAF2;font-weight:600">Samina B. (ID: T-409)</div></div>
                    <div><div style="font-size:.68rem;color:#5C6480;margin-bottom:2px">Vehicle</div>
                         <div style="font-size:.85rem;color:#E8EAF2;font-weight:600">60-Ton Dump Truck #42</div></div>
                    <div><div style="font-size:.68rem;color:#5C6480;margin-bottom:2px">Location</div>
                         <div style="font-size:.85rem;color:#E8EAF2;font-weight:600">Block II, Sector 4, Decline Ramp</div></div>
                    <div><div style="font-size:.68rem;color:#5C6480;margin-bottom:2px">Trigger Type</div>
                         <div style="font-size:.85rem;color:#F87171;font-weight:600">Cabin Panic Button</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
 
            if st.button("🚑 Dispatch Rapid Response Team"):
                with st.spinner("Pinging nearest security vehicle..."):
                    import time; time.sleep(1)
                st.success("✅ Response Team Alpha dispatched. ETA: 3 Minutes. Live GPS tracking enabled.")
        else:
            st.success("✅ All fleet operations are currently reporting normal status. No active SOS signals.")
 
    with col_mobile:
        card_header("📱 Proposed Mobile Interface (Driver Side)", "Companion app feature set")
        features = [
            ("🆘", "One-Tap SOS",                 "Instant alert to HQ dashboard with GPS coordinates."),
            ("🎙️", "Dhatki/Sindhi Voice Commands", "'Help' triggered via voice recognition if hands are occupied."),
            ("⚠️", "Route Hazard Alerts",          "Live alerts about unstable terrain or severe weather in the mining pit."),
            ("📍", "GPS Breadcrumbing",            "Continuous location sync to this HQ dashboard for dispatch."),
        ]
        for icon, title, desc in features:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-radius:8px;padding:12px 14px;margin-bottom:8px;
                        display:flex;align-items:flex-start;gap:12px">
                <span style="font-size:1.3rem;margin-top:1px">{icon}</span>
                <div>
                    <div style="font-size:.85rem;font-weight:700;color:#E8EAF2;margin-bottom:2px">{title}</div>
                    <div style="font-size:.78rem;color:#9BA3BF;line-height:1.5">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
