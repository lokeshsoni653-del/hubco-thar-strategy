import folium
from folium.plugins import HeatMap, Fullscreen, Draw
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="HUBCO Thar Strategy | Lokesh Kumar", page_icon="🏜️", layout="wide")

# --- CUSTOM CSS & BRANDING ---
st.markdown("""
    <style>
    .main-header {font-size: 2.6rem; font-weight: 800; color: #b35900; letter-spacing: -1px;}
    .sub-header {font-size: 1.2rem; color: #4a4a4a; margin-bottom: 5px;}
    .architect-tag {font-size: 0.95rem; font-weight: 600; color: #D4AF37; background: #05112F; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 20px;}
    .esg-box {background-color: #f7f3e; padding: 15px; border-radius: 10px; border-left: 5px solid #d4af37; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="main-header">🏜️ HUBCO Thar Plant: BD & CSR Strategy Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Spatial Optimization for Corporate Social Responsibility (CSR) Infrastructure in Tharparkar.</div>', unsafe_allow_html=True)
st.markdown('<div class="architect-tag">Architected by Lokesh Kumar • Native Context: Mithi, Sindh</div>', unsafe_allow_html=True)

# --- DATA SIMULATION (Tharparkar Coordinates: Block II, Islamkot, Mithi region) ---
@st.cache_data
def load_thar_data():
    np.random.seed(42)
    # Coordinates roughly around Islamkot and Mithi
    lats = np.random.uniform(24.7000, 24.9000, 80)
    lons = np.random.uniform(69.7500, 70.3500, 80)
    water_scarcity = np.random.randint(50, 100, 80) # High means severe lack of water
    population = np.random.randint(500, 5000, 80)  
    
    return pd.DataFrame({'Latitude': lats, 'Longitude': lons, 'Water_Scarcity_Index': water_scarcity, 'Village_Population': population})

df = load_thar_data()

# Key HUBCO Landmarks
landmarks = {
    "HUBCO Thar Energy Ltd (TEL)": [24.7977, 70.2808],
    "Mithi (Regional Hub)": [24.7370, 69.7971],
    "Islamkot": [24.7946, 70.1804]
}

# --- SIDEBAR: CONTROLS & BD BUDGET ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Hubco_Logo.svg/1200px-Hubco_Logo.svg.png", width=150)
    
    st.markdown("### 📈 BD & CSR Budget (FY-26)")
    csr_budget = st.slider("Total Allocation (Millions PKR)", 50, 500, 150) * 1000000
    
    st.markdown("### 🏗️ Infrastructure Costs")
    cost_ro_plant = st.number_input("Cost per RO Water Plant", value=8000000, step=500000)
    cost_solar = st.number_input("Cost per Solar Microgrid", value=12000000, step=500000)
    
    st.markdown("### 🎯 Intervention Targeting")
    min_scarcity = st.slider("Target Minimum Water Scarcity", 0, 100, 75)
    min_pop = st.slider("Target Minimum Population", 500, 5000, 1500)
    
    st.divider()
    st.caption("Strategic Focus: Block II & Surrounding Communities")

# --- ALGORITHM LOGIC ---
# Filter villages needing intervention
target_villages = df[(df['Water_Scarcity_Index'] >= min_scarcity) & (df['Village_Population'] >= min_pop)].copy()

# Allocate RO plants to the most scarce, Solar to the rest
target_villages = target_villages.sort_values(by='Water_Scarcity_Index', ascending=False)
target_villages['Project_Type'] = np.where(target_villages['Water_Scarcity_Index'] > 85, "RO Water Plant", "Solar Microgrid")
target_villages['Project_Cost'] = np.where(target_villages['Project_Type'] == "RO Water Plant", cost_ro_plant, cost_solar)

# Budget Constraint Logic
target_villages['Cumulative_Cost'] = target_villages['Project_Cost'].cumsum()
target_villages['Status'] = np.where(target_villages['Cumulative_Cost'] <= csr_budget, "Approved (Funded)", "Waitlisted")

# Metrics
funded_projects = target_villages[target_villages['Status'] == "Approved (Funded)"]
total_capex = funded_projects['Project_Cost'].sum()
lives_impacted = funded_projects['Village_Population'].sum()
ro_count = len(funded_projects[funded_projects['Project_Type'] == "RO Water Plant"])
solar_count = len(funded_projects[funded_projects['Project_Type'] == "Solar Microgrid"])

# --- ENTERPRISE TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Regional Deployment", "📊 CSR Financials", "🤝 Community Dynamics", "📸 Field Audits", "🛡️ Fleet Safety"])

with tab1:
    st.markdown("### Tharparkar Block II Intervention Map")
    
    # REVERTED: Back to the clean, light-mode corporate map
    m = folium.Map(location=[24.7977, 70.1804], zoom_start=11, tiles="CartoDB positron")
    
    # Kept the Planners' Fullscreen & Drawing tools
    Fullscreen(position='topright').add_to(m)
    Draw(export=True, position='topleft', draw_options={'polyline':False, 'circlemarker':False}).add_to(m)
    
    # Scarcity Heatmap
    heat_data = [[row['Latitude'], row['Longitude'], row['Water_Scarcity_Index']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=10, gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}).add_to(m)

    # Plot Landmarks
    for name, coords in landmarks.items():
        folium.Marker(coords, popup=f"<b>{name}</b>", icon=folium.Icon(color="black", icon="building", prefix='fa')).add_to(m)

    # Plot Projects with Formal Executive Popups
    for idx, row in target_villages.iterrows():
        color = "lightgray" if row['Status'] == "Waitlisted" else ("blue" if row['Project_Type'] == "RO Water Plant" else "orange")
        icon_type = "tint" if row['Project_Type'] == "RO Water Plant" else "sun"
        
        # UPGRADE: Formal HTML Data Table for the Popup
        html_card = f"""
        <div style="font-family: Arial, sans-serif; width: 220px;">
            <h4 style="margin-top: 0; margin-bottom: 8px; color: #0056b3; border-bottom: 2px solid #ccc; padding-bottom: 5px;">Site Intervention Audit</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #333;">
                <tr><td style="padding: 4px 0; font-weight: bold; width: 45%;">Project Type:</td><td style="padding: 4px 0;">{row['Project_Type']}</td></tr>
                <tr><td style="padding: 4px 0; font-weight: bold;">Est. Population:</td><td style="padding: 4px 0;">{row['Village_Population']}</td></tr>
                <tr><td style="padding: 4px 0; font-weight: bold;">Scarcity Index:</td><td style="padding: 4px 0;">{row['Water_Scarcity_Index']}/100</td></tr>
                <tr><td style="padding: 4px 0; font-weight: bold;">Funding Status:</td><td style="padding: 4px 0;">{row['Status']}</td></tr>
                <tr><td style="padding: 4px 0; font-weight: bold;">CAPEX Reqd:</td><td style="padding: 4px 0;">Rs. {row['Project_Cost']/1000000:.1f} M</td></tr>
            </table>
        </div>
        """
        
        iframe = folium.IFrame(html=html_card, width=250, height=180)
        formal_popup = folium.Popup(iframe, max_width=260)
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']], 
            popup=formal_popup, 
            tooltip=row['Project_Type'], 
            icon=folium.Icon(color=color, icon=icon_type, prefix='fa')
        ).add_to(m)

    st_folium(m, width=1200, height=500)

with tab2:
    st.markdown("### Business Development: CSR Allocation & ROI")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Villages Funded", value=len(funded_projects))
    c2.metric(label="Total Lives Impacted", value=f"{lives_impacted:,}")
    c3.metric(label="Total CAPEX Utilized", value=f"Rs. {total_capex / 1000000:.1f} M")
    
    if not funded_projects.empty:
        fig1 = px.pie(funded_projects, names='Project_Type', values='Project_Cost', hole=0.5, 
                      title='CSR Fund Distribution', color='Project_Type', 
                      color_discrete_map={"RO Water Plant": "#0056b3", "Solar Microgrid": "#ffc107"})
        st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown(f"""
    <div class="esg-box">
        <h4>🌱 Thar Foundation Impact Statement</h4>
        <p>By deploying <b>{ro_count} RO Plants</b> and <b>{solar_count} Solar Microgrids</b>, HUBCO directly elevates the living standards of <b>{lives_impacted:,}</b> residents in the Thar Coal Block II radius, securing vital community goodwill and fulfilling corporate ESG mandates.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🗣️ Local Dynamics: Dhatki Multilingual AI (PoC)")
    st.write("A Proof of Concept demonstrating how incoming SMS grievances from local communities can be auto-translated for English-speaking management and Chinese CPEC engineering teams.")
    
    st.markdown("#### 📥 Live SMS Grievance Inbox (Simulated)")
    
    # UPGRADE: Added Mandarin Chinese translations with Pinyin
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
    
    selected_phrase = st.selectbox("Select incoming SMS (Dhatki/Roman Script):", list(mock_dhatki_data.keys()))
    
    # UPGRADE: Target Language Toggle
    target_lang = st.radio("Select Target Output Language:", ["🇬🇧 English", "🇨🇳 Mandarin Chinese (CPEC Teams)"], horizontal=True)
    
    if st.button("🧠 Process via NLP Translation Engine"):
        with st.spinner(f"Routing through Dhatki-to-{target_lang.split(' ')[1]} translation pipeline..."):
            import time
            time.sleep(1.5) 
            
            result = mock_dhatki_data[selected_phrase]
            
            st.success("✅ Translation and Intent Extraction Complete")
            
            colX, colY = st.columns(2)
            with colX:
                # Dynamically display the correct language based on the toggle
                translation_text = result['english'] if "English" in target_lang else result['chinese']
                st.markdown(f"**Translated Output:**\n> *{translation_text}*")
                st.markdown(f"**Auto-Categorized As:** `{result['category']}`")
            with colY:
                st.markdown(f"**System Priority:** {result['priority']}")
                st.markdown(f"**Recommended Action:** {result['action']}")
                
    st.divider()
    st.info("💡 **Architecture Note:** This UI currently runs on simulated rule-based data. The architecture is designed to seamlessly integrate with a live Multilingual LLM API once the Dhatki dataset is fully compiled.")

with tab4:
    st.markdown("### 📸 Field Operations (Mithi / Islamkot Hub)")
    st.write("Field engineers can capture pre-deployment site audits (e.g., groundwater drilling sites) directly into the BD system.")
    site_photo = st.camera_input("Capture Audit Image")
    if site_photo:
        st.success("✅ Audit image verified from field location.")
        st.download_button("💾 Save to CSR Report", data=site_photo, file_name="Thar_Audit.png", mime="image/png")

with tab5:
    st.markdown("### 🛡️ Fleet Safety & Inclusion Hub")
    st.write("Dedicated monitoring and emergency response interface for the Women Dump Truck Drivers initiative at Thar Coal Block II.")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Active Female Drivers", "42", "+3 this month")
    col_b.metric("Current Shift", "Night Shift (18:00 - 06:00)", "High Alert")
    col_c.metric("SOS Incidents (Last 30 Days)", "0", "-1", delta_color="inverse")
    
    st.markdown("#### 🚨 Emergency Dispatch Simulation")
    st.info("In a live environment, this dashboard receives SOS signals triggered via physical panic buttons installed in the dump truck cabins.")
    
    # Simulated incoming SOS
    sos_active = st.checkbox("Simulate Incoming SOS Alert")
    
    if sos_active:
        st.error("**⚠️ URGENT SOS RECEIVED**")
        st.markdown("""
        * **Driver:** Samina B. (ID: T-409)
        * **Vehicle:** 60-Ton Dump Truck #42
        * **Location:** Block II, Sector 4, Decline Ramp
        * **Trigger Type:** Cabin Panic Button
        """)
        
        if st.button("Dispatch Rapid Response Team"):
            with st.spinner("Pinging nearest security vehicle..."):
                import time
                time.sleep(1)
                st.success("✅ Response Team Alpha dispatched. ETA: 3 Minutes. Live GPS tracking enabled.")
    else:
        st.success("All fleet operations are currently reporting normal status. No active SOS signals.")

    st.divider()
    st.markdown("#### 📱 Proposed Mobile Interface (Driver Side)")
    st.write("A companion mobile app for the drivers would feature:")
    st.markdown("- **One-Tap SOS:** Instant alert to this HQ dashboard with GPS coordinates.")
    st.markdown("- **Dhatki/Sindhi Voice Commands:** 'Help' triggered via voice recognition if hands are occupied.")
    st.markdown("- **Route Hazards:** Live alerts about unstable terrain or severe weather in the mining pit.")
