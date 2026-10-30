
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AgriNova | Rwanda Agricultural Intelligence",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 AgriNova")
st.caption(
    "Rwanda Agricultural Intelligence Platform | "
    "HAICO — NISR Big Data Hackathon 2026"
)

st.warning(
    "DEMO MODE: This dataset contains synthetic demonstration data. "
    "Do not present its values as official NISR statistics."
)

DATA_PATH = (
    Path(__file__).parent / "data" / "agriculture_demo_data.csv"
)


REQUIRED_COLUMNS = [
    "province",
    "district",
    "season",
    "crop",
    "cultivated_area_ha",
    "production_tonnes",
    "data_status",
]

NUMERIC_COLUMNS = [
    "cultivated_area_ha",
    "production_tonnes",
]


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


# 1. Load and validate the dataset
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.info(
        "Check that agriculture_demo_data.csv is inside "
        "your project's data folder."
    )
    st.stop()
except (pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(f"The CSV file could not be read: {error}")
    st.stop()

missing_columns = [
    column for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# Work on a copy so the loaded source data is not modified
df = df.copy()

# Convert measurements to numbers.
# Invalid text becomes NaN and is reported below.
for column in NUMERIC_COLUMNS:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 2. Identify data-quality problems
missing_cells = int(df[REQUIRED_COLUMNS].isna().sum().sum())

missing_area = df["cultivated_area_ha"].isna()
missing_production = df["production_tonnes"].isna()

missing_yield = pd.Series(True, index=df.index)

invalid_area = (
    df["cultivated_area_ha"].notna()
    & (df["cultivated_area_ha"] <= 0)
)

negative_production = (
    df["production_tonnes"].notna()
    & (df["production_tonnes"] < 0)
)

# Yield is calculated by AgriNova, not read from the CSV.
negative_yield = pd.Series(False, index=df.index)

# Check exact duplicate rows and repeated geographic/crop keys.
exact_duplicate_count = int(df.duplicated().sum())

record_key = ["province", "district", "season", "crop"]
complete_keys = df[record_key].notna().all(axis=1)

duplicate_key_count = int(
    df.loc[complete_keys].duplicated(
        subset=record_key, keep=False
    ).sum()
)

# 3. Recalculate yield only when area and production are valid
valid_measurements = (
    df["cultivated_area_ha"].notna()
    & (df["cultivated_area_ha"] > 0)
    & df["production_tonnes"].notna()
    & (df["production_tonnes"] >= 0)
)

df["yield_tonnes_per_ha"] = float("nan")

df.loc[valid_measurements, "yield_tonnes_per_ha"] = (
    df.loc[valid_measurements, "production_tonnes"]
    / df.loc[valid_measurements, "cultivated_area_ha"]
)

# 4. Display quality report
st.subheader("Data quality report")

quality_metrics = st.columns(4)

quality_metrics[0].metric(
    "Rows loaded", f"{len(df):,}"
)

quality_metrics[1].metric(
    "Missing cells", f"{missing_cells:,}"
)

quality_metrics[2].metric(
    "Invalid area rows", f"{int(invalid_area.sum()):,}"
)

quality_metrics[3].metric(
    "Negative production rows",
    f"{int(negative_production.sum()):,}"
)

with st.expander("View all validation checks"):
    st.write(
        "Rows with missing area:",
        int(missing_area.sum()),
    )
    st.write(
        "Rows with missing production:",
        int(missing_production.sum()),
    )
    st.write(
        "Rows with missing recorded yield:",
        int(missing_yield.sum()),
    )
    st.write(
        "Rows with invalid area:",
        int(invalid_area.sum()),
    )
    st.write(
        "Rows with negative production:",
        int(negative_production.sum()),
    )
    st.write(
        "Exact duplicate rows:",
        exact_duplicate_count,
    )
    st.write(
        "Duplicate district-season-crop records:",
        duplicate_key_count,
    )

    st.write(
        "Rows with negative yield:",
        int(negative_yield.sum()),
    )

    st.write("Exact duplicate rows:", exact_duplicate_count)
    st.write(
        "Rows involved in repeated province/district/season/crop keys:",
        duplicate_key_count,
    )

    if (
        missing_cells
        or invalid_area.any()
        or negative_production.any()
        or negative_yield.any()
        or exact_duplicate_count
        or duplicate_key_count
    ):
        st.warning(
            "Review the reported issues before using the data. "
            "Duplicate keys are flagged for review, not automatically removed."
        )
    else:
        st.success("All configured data-quality checks passed.")

# 5. Exclude rows with unusable measurements or missing filter fields.
# Keep the original df for inspection; use analysis_df for metrics.
required_for_analysis = [
    "province",
    "district",
    "season",
    "crop",
    "cultivated_area_ha",
    "production_tonnes",
]

usable_rows = (
    df[required_for_analysis].notna().all(axis=1)
    & (df["cultivated_area_ha"] > 0)
    & (df["production_tonnes"] >= 0)
)

analysis_df = df.loc[usable_rows].copy()

excluded_count = int((~usable_rows).sum())

if excluded_count:
    st.warning(
        f"{excluded_count} row(s) excluded from dashboard calculations "
        "because required fields or measurements are invalid."
    )

if analysis_df.empty:
    st.error(
        "No valid records remain for analysis. "
        "Check the dataset and the data-quality report."
    )
    st.stop()

# 6. Filters
with st.sidebar:
    st.header("Explore data")

    provinces = sorted(analysis_df["province"].unique().tolist())
    selected_provinces = st.multiselect(
        "Province", provinces, default=provinces
    )

    seasons = sorted(analysis_df["season"].unique().tolist())
    selected_seasons = st.multiselect(
        "Season", seasons, default=seasons
    )

    crops = sorted(analysis_df["crop"].unique().tolist())
    selected_crops = st.multiselect(
        "Crop", crops, default=crops
    )

filtered = analysis_df[
    analysis_df["province"].isin(selected_provinces)
    & analysis_df["season"].isin(selected_seasons)
    & analysis_df["crop"].isin(selected_crops)
].copy()

if filtered.empty:
    st.info(
        "No rows match these filters. Select at least one "
        "province, season, and crop."
    )
    st.stop()

# 7. Correct calculations
# Yield = production / cultivated area
filtered["yield_tonnes_per_ha"] = (
    filtered["production_tonnes"]
    / filtered["cultivated_area_ha"]
)

total_area = filtered["cultivated_area_ha"].sum()
total_production = filtered["production_tonnes"].sum()

weighted_yield = (
    total_production / total_area if total_area > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records in view", f"{len(filtered):,}")
c2.metric("Cultivated area (ha)", f"{total_area:,.0f}")
c3.metric("Production (tonnes)", f"{total_production:,.0f}")
c4.metric("Overall yield (t/ha)", f"{weighted_yield:,.2f}")

# 8. Production by district
st.subheader("Production by district")

district_prod = (
    filtered.groupby("district", as_index=False)["production_tonnes"]
    .sum()
    .sort_values("production_tonnes", ascending=False)
)

fig1 = px.bar(
    district_prod,
    x="district",
    y="production_tonnes",
    title="Production by selected district",
    labels={
        "district": "District",
        "production_tonnes": "Production (tonnes)",
    },
)
st.plotly_chart(fig1, use_container_width=True)

left, right = st.columns(2)

with left:
    by_crop = (
        filtered.groupby("crop", as_index=False)["production_tonnes"]
        .sum()
    )
    fig2 = px.pie(
        by_crop,
        names="crop",
        values="production_tonnes",
        title="Share of production by crop",
    )
    st.plotly_chart(fig2, use_container_width=True)

with right:
    by_season = (
        filtered.groupby("season", as_index=False)["production_tonnes"]
        .sum()
    )
    fig3 = px.bar(
        by_season,
        x="season",
        y="production_tonnes",
        title="Production by season",
        labels={
            "season": "Season",
            "production_tonnes": "Production (tonnes)",
        },
    )
    st.plotly_chart(fig3, use_container_width=True)

# 9. Insights
st.subheader("AgriNova Insights")

best = district_prod.iloc[0]

st.write(
    f"Within the selected demonstration data, **{best['district']}** "
    f"has the highest recorded production "
    f"({best['production_tonnes']:,.0f} tonnes). "
    "This is a descriptive comparison only and does not explain causation."
)

st.caption(
    "Data status: synthetic demonstration records. "
    "Verify source, reference period, units, and geographic coverage "
    "before using real data."
)

# 10. Filtered data and CSV download
st.subheader("Filtered data")

st.dataframe(filtered, use_container_width=True, hide_index=True)

st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="agrinova_filtered_data.csv",
    mime="text/csv",
)
