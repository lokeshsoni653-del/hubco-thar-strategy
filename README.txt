# 🏜️ HUBCO Thar Plant: BD & CSR Strategy Engine

**Architected by:** Lokesh Kumar  
**Native Context:** Mithi, Sindh, Pakistan  
**Live Prototype:** [View the Enterprise Dashboard](https://appco-thar-strategy-t8kcbxrgjyg8unakk2xqhu.streamlit.app/)

## 📖 Project Overview
The HUBCO Thar Strategy Engine is an enterprise-grade spatial optimization and Corporate Social Responsibility (CSR) dashboard tailored for the Thar Coal Block II project. Designed to bridge the gap between corporate governance and community impact, this platform enables data-driven decision-making for infrastructure deployment, financial allocation, and community grievance management.

Recently upgraded with a custom dark-mode UI/UX architecture, the application mimics a production-ready SaaS environment, moving beyond standard data visualization into comprehensive public policy and ESG (Environmental, Social, and Governance) analytics.

## ✨ Key Enterprise Features
* **🗺️ Regional Deployment Mapping:** Interactive spatial mapping (via Folium) targeting villages based on Water Scarcity Indexes and population density to optimize the placement of RO Water Plants and Solar Microgrids.
* **📊 CSR Financial Analytics:** Dynamic Plotly visualizations tracking CAPEX utilization against the FY-26 CSR budget, calculating real-time "Cost per Life Impacted" metrics.
* **🤝 Dhatki Multilingual AI (PoC):** A simulated NLP pipeline demonstrating how localized SMS grievances (in Dhatki/Roman Sindhi) can be auto-translated and routed to English and Mandarin-speaking (CPEC) management teams.
* **📸 Field Audit Protocols:** Integrated camera inputs for engineers to capture and verify groundwater drilling site audits directly from the field.
* **🛡️ Fleet Safety Hub:** A live monitoring simulation for the Women Dump Truck Drivers Initiative, featuring instant SOS dispatch routing and hazard alerts.

## 🛠️ Technical Stack
* **Frontend/UI:** Streamlit (with aggressive custom CSS injection for enterprise styling)
* **Data Processing:** Python 3.11, Pandas, NumPy
* **Geospatial Mapping:** Folium, Streamlit-Folium
* **Data Visualization:** Plotly Express, Plotly Graph Objects

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/hubco-thar-strategy.git](https://github.com/your-username/hubco-thar-strategy.git)
   cd hubco-thar-strategy
