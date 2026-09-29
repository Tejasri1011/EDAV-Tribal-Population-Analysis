import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Tribal Population Analysis",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# SIMPLE STYLING
# =========================================================
st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    font-size: 17px;
    color: #888888;
    margin-bottom: 20px;
}

.section-title {
    font-size: 25px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv("analysis_data.csv")


df = load_data().copy()


# =========================================================
# CLEAN DATA
# =========================================================
if "Tribe" in df.columns:
    df = df[
        df["Tribe"].astype(str).str.strip() != "All Schedule Tribes"
    ].copy()


numeric_columns = [
    "Population",
    "Male_Population",
    "Female_Population",
    "Literacy_Rate",
    "Sex_Ratio",
    "Total_Workers"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">'
    '📊 Demographic Analysis of Tribal Population'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of demographic and socio-economic indicators '
    'for selected tribal population data in India.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.title("🔎 Explore Data")

st.sidebar.caption(
    "Use the filters below to explore demographic patterns."
)

st.sidebar.divider()

st.sidebar.subheader("Geographic Filters")


# -----------------------------
# Region
# -----------------------------
regions = ["All"]

if "Region" in df.columns:
    regions += sorted(
        df["Region"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)


# Start with complete dataset
filtered_df = df.copy()


# Apply region filter
if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"].astype(str) == selected_region
    ]


# -----------------------------
# State
# -----------------------------
states = ["All"]

if "State" in filtered_df.columns:
    states += sorted(
        filtered_df["State"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_state = st.sidebar.selectbox(
    "Select State",
    states
)


# Apply state filter
if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["State"].astype(str) == selected_state
    ]


# -----------------------------
# Tribe
# -----------------------------
tribes = ["All"]

if "Tribe" in filtered_df.columns:
    tribes += sorted(
        filtered_df["Tribe"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_tribe = st.sidebar.selectbox(
    "Select Tribe",
    tribes
)


# Apply tribe filter
if selected_tribe != "All":
    filtered_df = filtered_df[
        filtered_df["Tribe"].astype(str) == selected_tribe
    ]


# -----------------------------
# Current selection
# -----------------------------
st.sidebar.divider()

st.sidebar.markdown("### Current Selection")

st.sidebar.write(f"**Region:** {selected_region}")
st.sidebar.write(f"**State:** {selected_state}")
st.sidebar.write(f"**Tribe:** {selected_tribe}")

st.sidebar.metric(
    "Records",
    f"{len(filtered_df):,}"
)


# =========================================================
# KEY DEMOGRAPHIC INDICATORS
# =========================================================
st.markdown(
    '<div class="section-title">'
    '📌 Key Demographic Indicators'
    '</div>',
    unsafe_allow_html=True
)


if filtered_df.empty:

    st.warning("No records match the selected filters.")

else:

    total_population = (
        filtered_df["Population"].sum()
        if "Population" in filtered_df.columns
        else 0
    )

    average_literacy = (
        filtered_df["Literacy_Rate"].mean()
        if "Literacy_Rate" in filtered_df.columns
        else None
    )

    average_sex_ratio = (
        filtered_df["Sex_Ratio"].mean()
        if "Sex_Ratio" in filtered_df.columns
        else None
    )

    total_workers = (
        filtered_df["Total_Workers"].sum()
        if "Total_Workers" in filtered_df.columns
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "👥 Population",
            f"{total_population:,.0f}"
        )


    with col2:
        if pd.notna(average_literacy):
            st.metric(
                "📚 Avg. Literacy Rate",
                f"{average_literacy:.2f}%"
            )
        else:
            st.metric(
                "📚 Avg. Literacy Rate",
                "N/A"
            )


    with col3:
        if pd.notna(average_sex_ratio):
            st.metric(
                "⚖️ Avg. Sex Ratio",
                f"{average_sex_ratio:.2f}"
            )
        else:
            st.metric(
                "⚖️ Avg. Sex Ratio",
                "N/A"
            )


    with col4:
        st.metric(
            "👷 Total Workers",
            f"{total_workers:,.0f}"
        )


st.divider()


# =========================================================
# REGIONAL ANALYSIS
# =========================================================
st.markdown(
    '<div class="section-title">'
    '📊 Regional Analysis'
    '</div>',
    unsafe_allow_html=True
)


if not filtered_df.empty:

    regional_summary = (
        filtered_df
        .groupby("Region")
        .agg(
            Population=("Population", "sum"),
            Literacy_Rate=("Literacy_Rate", "mean"),
            Sex_Ratio=("Sex_Ratio", "mean")
        )
        .reset_index()
    )


    chart1, chart2, chart3 = st.columns(3)


    with chart1:
        st.write("**Total Population by Region**")

        st.bar_chart(
            regional_summary.set_index("Region")["Population"]
        )


    with chart2:
        st.write("**Average Literacy Rate by Region**")

        st.bar_chart(
            regional_summary.set_index("Region")["Literacy_Rate"]
        )


    with chart3:
        st.write("**Average Sex Ratio by Region**")

        st.bar_chart(
            regional_summary.set_index("Region")["Sex_Ratio"]
        )

else:

    st.info("Regional analysis is not available.")


st.divider()


# =========================================================
# STATE-LEVEL ANALYSIS
# =========================================================
st.markdown(
    '<div class="section-title">'
    '🏛️ State-level Population Analysis'
    '</div>',
    unsafe_allow_html=True
)


if not filtered_df.empty:

    state_summary = (
        filtered_df
        .groupby("State")["Population"]
        .sum()
        .reset_index()
    )

    if not state_summary.empty:
        st.bar_chart(
            state_summary.set_index("State")["Population"]
        )
    else:
        st.info("No state population data available.")

else:

    st.info("No state-level data available.")


st.divider()


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================
st.markdown(
    '<div class="section-title">'
    '💡 Key Insights'
    '</div>',
    unsafe_allow_html=True
)


if not filtered_df.empty:

    # Highest population state
    state_population = (
        filtered_df
        .groupby("State")["Population"]
        .sum()
        .sort_values(ascending=False)
    )

    if not state_population.empty:
        highest_population_state = state_population.index[0]
        highest_population_value = state_population.iloc[0]
    else:
        highest_population_state = "N/A"
        highest_population_value = 0


    # Highest literacy region
    region_literacy = (
        filtered_df
        .groupby("Region")["Literacy_Rate"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )

    if not region_literacy.empty:
        highest_literacy_region = region_literacy.index[0]
        highest_literacy_value = region_literacy.iloc[0]
    else:
        highest_literacy_region = "N/A"
        highest_literacy_value = 0


    # Highest sex ratio region
    region_sex_ratio = (
        filtered_df
        .groupby("Region")["Sex_Ratio"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )

    if not region_sex_ratio.empty:
        highest_sex_ratio_region = region_sex_ratio.index[0]
        highest_sex_ratio_value = region_sex_ratio.iloc[0]
    else:
        highest_sex_ratio_region = "N/A"
        highest_sex_ratio_value = 0


    insight1, insight2, insight3 = st.columns(3)


    with insight1:
        st.info(
            f"🏛️ **Highest Population State**\n\n"
            f"**{highest_population_state}**\n\n"
            f"Population: {highest_population_value:,.0f}"
        )


    with insight2:
        st.info(
            f"📚 **Highest Average Literacy Rate**\n\n"
            f"**{highest_literacy_region}**\n\n"
            f"Literacy Rate: {highest_literacy_value:.2f}%"
        )


    with insight3:
        st.info(
            f"⚖️ **Highest Average Sex Ratio**\n\n"
            f"**{highest_sex_ratio_region}**\n\n"
            f"Sex Ratio: {highest_sex_ratio_value:.2f}"
        )

else:

    st.info("No data available for generating insights.")


st.divider()


# =========================================================
# POPULATION VS LITERACY RATE
# =========================================================
st.markdown(
    '<div class="section-title">'
    '📈 Population vs Literacy Rate'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "This chart shows the relationship between population size "
    "and literacy rate for the selected records."
)


if not filtered_df.empty:

    scatter_data = filtered_df[
        [
            "Population",
            "Literacy_Rate",
            "Region",
            "State",
            "Tribe"
        ]
    ].dropna(
        subset=[
            "Population",
            "Literacy_Rate"
        ]
    )


    if not scatter_data.empty:

        st.scatter_chart(
            scatter_data,
            x="Population",
            y="Literacy_Rate"
        )

        st.caption(
            "Each point represents a tribal record. "
            "Population is shown on the x-axis and "
            "Literacy Rate on the y-axis."
        )

    else:

        st.info(
            "No valid Population/Literacy Rate data available."
        )

else:

    st.info("No data available for the scatter plot.")


st.divider()


# =========================================================
# DATA EXPLORER
# =========================================================
st.markdown(
    '<div class="section-title">'
    '📋 Data Explorer'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    f"Showing **{len(filtered_df):,}** records "
    "based on the selected filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD
# =========================================================
csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="tribal_filtered_data.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "EDAV Project • Demographic Analysis of Tribal Population Data"
)