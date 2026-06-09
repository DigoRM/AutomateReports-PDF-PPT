---
title: OptimaReports Restaurant AI VideoAnalytics
emoji: 📊
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# OptimaReports · Enterprise AI Video Analytics & Reporting Platform

### 🚀 Live Web Application: [https://mr-marcolino-optimareports-restaurant-ai-videoanalytics.hf.space](https://mr-marcolino-optimareports-restaurant-ai-videoanalytics.hf.space)

OptimaReports is a premium, enterprise-grade data compilation and visualization platform designed to transform complex raw operational data from AI-driven video audits into highly standardized, interactive, and client-ready reporting dashboards and deliverables.

Historically, analysts spent hundreds of hours every week manually parsing, cleaning, and formatting spreadsheets to generate weekly performance reports for restaurant franchises. **OptimaReports automates this entire pipeline into a single click**, ensuring total standardization and enabling scalable company growth with strict data privacy.

---

## ⚡ The Value Proposition

* **Massive Time Savings**: Complex, multi-store weekly analysis that took hours is processed and compiled in under **3 seconds**.
* **Total Standardization**: Guarantees total consistency across analysts, report layouts, metrics, and client deliverables.
* **Scalable Business Model**: Allows analysts to handle 10x more clients by automating document creation (PDF & PPTX exports).
* **Bilingual/Trilingual Capability**: Instant real-time language toggling (Portuguese, Spanish, English) across the entire application interface, charts, and metrics.
* **Strict LGPD/GDPR Privacy Compliance**: Core parsing architecture anonymizes operational store locations on-the-fly (e.g. `Store 01`, `Store 02`) to ensure data separation between distinct franchises.

---

## 🚀 Key Features

### 1. Interactive AI Executive Dashboard
* **Dynamic Charting**: Built with **Chart.js**, showing KBP (Key Business Process) distributions, Area alerts, and rankings.
* **Master totalizer UI**: Visually distinct "Total KBP" card styled as the master accumulator, making it clear how components sum up to the total.
* **Theme Customization**: Real-time toggling between dark mode (for interactive review) and light mode (designed for high-contrast presentation exports).

### 2. Multi-Tab Granular Operational Analysis
Granular breakdown tabs tailored to critical restaurant operation segments:
* **CE (Customer Experience)**: Metrics on queue times, order times, unattended clients, and complaint rates.
* **RC (Cost Reduction)**: Cost leakages like open cash drawers, staff away from registers, incorrect PIN pad usage, and early closures.
* **CO (Operational Compliance)**: Audits on uniforms, caps, refrigerator stocking, and delivery driver wait times.
* **Channel Specific Performance**: Dedicated views for **Delivery**, **Drive Thru**, and **Cam Check** (camera status audits).

### 3. Server-Side Automated Report Export
* **PDF Report Generator**: Uses an integrated headless **Playwright** engine to render the interactive dashboard into a clean, A4-landscape print publication.
* **PowerPoint (PPTX) Deck Exporter**: Generates slide decks automatically by rendering and compiling layout snapshots into fully editable presentation templates.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.9 / Flask (Lightweight and robust WSGI app server)
* **Frontend**: HTML5 / Vanilla CSS3 / Javascript (ES6)
* **Visualizations**: Chart.js 4.4 / Chart.js Datalabels plugin
* **Report Compiling**: python-pptx / Playwright Headless Chromium / html2pdf
* **Infrastructure**: Docker / Gunicorn / Hugging Face Spaces SDK

---

## 📦 Local Installation & Run

### Prerequisites
* Python 3.9+
* Docker (Optional, for containerized run)

### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/DigoRM/AutomateReports-PDF-PPT.git
   cd AutomateReports-PDF-PPT/IceCream\ Co._ReportsAuto/optimareports-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   playwright install-deps chromium
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000`.

### Running with Docker
1. Build the image:
   ```bash
   docker build -t optimareports .
   ```

2. Run the container:
   ```bash
   docker run -p 7860:7860 optimareports
   ```
   Open your browser at `http://127.0.0.1:7860`.
