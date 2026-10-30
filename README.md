# 🌱 AgriNova

### Rwanda Agricultural Intelligence Platform
**HAICO — NISR Big Data Hackathon 2026**

## 1. Project Overview

AgriNova is an interactive agricultural intelligence platform designed to make agricultural data easier to explore and understand in Rwanda.

It allows users to examine agricultural indicators across provinces, seasons, and crops through an interactive dashboard. The platform presents cultivated area, agricultural production, productivity indicators, and visual insights.

AgriNova aims to support better understanding of agricultural patterns and encourage data-informed decision-making.

## 2. Problem Statement

Agricultural information is often distributed across reports, tables, and datasets. This can make it difficult to compare agricultural production and productivity across different locations, seasons, and crops.

AgriNova addresses this challenge by bringing agricultural information into one accessible and interactive platform.

## 3. Main Features

- Interactive filtering by province, season, and crop.
- Agricultural cultivated-area indicators.
- Total agricultural production indicators.
- Overall yield calculation in tonnes per hectare.
- Interactive charts for exploring agricultural production.
- Data-quality checks for missing values, invalid cultivated area, and negative production.
- Download filtered agricultural data as CSV.
- Agricultural insights based on the displayed dataset.

## 4. Technologies Used

- **Python** — Application programming.
- **Streamlit** — Interactive web dashboard.
- **Pandas** — Data processing and analysis.
- **Plotly** — Interactive data visualisation.

## 5. Dataset and Data Quality

**Important data notice:** The dataset currently included in this project contains synthetic demonstration data. It is used to demonstrate AgriNova's functionality and must not be interpreted as official NISR agricultural statistics.

The application includes data-quality checks to help identify missing values and invalid measurements.

Yield is calculated using:

**Yield (tonnes per hectare) = Total Production (tonnes) ÷ Total Cultivated Area (hectares)**

Integration of verified and properly cited official NISR agricultural datasets is a future improvement.

## 6. Project Structure

```text
AgriNova_Submission_Package/
│
├── app.py
├── README.md
├── requirements.txt
├── AgriNova_NISR_2026_Hackathon_Project_Documentation.docx
│
└── data/
    ├── agriculture_demo_data.csv
    └── Data_dictionary
```

## 7. How to Install and Run

### Requirements

- Python 3 installed.
- Internet connection for installing dependencies.

### Install dependencies

Open a terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 8. Future Improvements

- Integration of verified official NISR agricultural statistics.
- More detailed agricultural trend analysis.
- Additional agricultural indicators.
- Expanded visualisation and analytical capabilities.

## 9. Project Goal

AgriNova demonstrates how agricultural data can be organised, analysed, and visualised through an accessible platform to support agricultural information exploration in Rwanda.

---

**AgriNova — Turning agricultural data into accessible insights for Rwanda.**
