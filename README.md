# AgriNova — Rwanda Agricultural Intelligence Platform

**Team:** HAICO — Harvest Analytics, Innovation, Climate & Opportunity  
**Competition:** NISR Big Data Hackathon 2026 — Track 1: Agricultural Productivity

## Important data note
The CSV included in this starter package contains **synthetic demonstration data** created only to demonstrate the dashboard. These values are not official NISR statistics. Before final submission, replace `data/agriculture_demo_data.csv` with an authorised, verified NISR dataset and update the source citation in the app and documentation.

## Run the application
1. Install Python 3.10 or newer.
2. Open a terminal/command prompt in this folder.
3. Create and activate a virtual environment (recommended).
4. Install packages: `pip install -r requirements.txt`
5. Start the dashboard: `streamlit run app.py`
6. The app should open in your browser. Use the sidebar filters to explore province, season, and crop.

## Files
- `app.py` — Streamlit dashboard source code.
- `data/agriculture_demo_data.csv` — synthetic demonstration data; replace before final evaluation.
- `requirements.txt` — Python dependencies.
- `README.md` — run instructions and project notes.

## Dashboard features
- Filters for province, season, and crop.
- Summary indicators for record count, cultivated area, production, and overall yield.
- Charts for district production, crop share, and seasonal production.
- A descriptive insight based on the selected records.
- A table and CSV download of filtered data.

## Method notes
- Yield is calculated as total production divided by total cultivated area for the currently selected records, where area is non-zero.
- The insight describes a pattern in the displayed records; it does not claim that one factor caused another.
- Replace the demo dataset with verified source data and validate definitions, units, missing values, geographic coverage, and published totals before reporting results.

## Official data citation
Add the exact title, year, publisher, and direct URL for every official dataset used. The project documentation identifies NISR's Seasonal Agricultural Survey (SAS) and relevant annual/seasonal publications as intended sources, but the exact dataset used must be recorded after it has been obtained and checked.

## Screen-recording checklist
Record your actual dashboard using desktop screen-recording software (not a phone camera). Show the dashboard, change the filters, explain one chart and one insight, and show the data table. Export as `.webm` or `.gif`; keep the recording at or under 3 minutes. The video must be recorded on your own computer after running the app.
