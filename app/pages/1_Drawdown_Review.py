import os

import streamlit as st
import pandas as pd
import plotly.express as px

from common import dirFiles

# Set up the Streamlit app
st.title("Emission Reduction Solutions Data Explorer")
st.write("Units are in Total CO2-eq (Gt) Reduced/Sequestered (2020–2050)")


# File upload
@st.cache_data
def load_data():
    uploaded_file = os.path.join(dirFiles,"dd02.csv")
    df = pd.read_csv(uploaded_file)
    df = df[~df["Sector"].str.endswith("Total")]
    df.columns = ["Sector", "Subgroup", "Solution", "Scenario 1", "Scenario 2"]
    df = df.dropna(subset=["Scenario 1", "Scenario 2"])
    return df

df = load_data()


# Sidebar filters
st.sidebar.header("Filter Data")

st.write("### Sector and Subgroup CO2 Reduction - Scenario 1")
chart_data = df.groupby(["Sector", "Subgroup"])["Scenario 1"].sum().reset_index()
chart_dataPct = chart_data.copy()
chart_dataPct["Contribution"] = (chart_dataPct["Scenario 1"] / chart_dataPct["Scenario 1"].sum() * 100).round(1)

#main data visualisation
cols = st.columns([2,3])
figPie = px.sunburst(chart_data, path=["Sector", "Subgroup"], values="Scenario 1",
                    #  title="CO2 Reduction by Sector and Subgroup",
                     )
cols[0].plotly_chart(figPie, use_container_width=True)

cols[1].dataframe(chart_dataPct.set_index("Sector").sort_values("Contribution"), use_container_width=True)


# Filter by Sector
sector_options = df["Sector"].unique()
selected_sectors = st.sidebar.multiselect("Select Sector(s):", sector_options, default=sector_options)

# Filter by Subgroup
subgroup_options = df["Subgroup"].unique()
selected_subgroups = st.sidebar.multiselect("Select Subgroup(s):", subgroup_options, default=subgroup_options)


# Apply filters
filtered_df = df[(df["Sector"].isin(selected_sectors)) & (df["Subgroup"].isin(selected_subgroups))]

# # Display filtered data
# st.write("### Filtered Data", filtered_df)

# Sorting options
st.sidebar.header("Sort Data")
sort_column = st.sidebar.selectbox("Select column to sort by:", df.columns, index=3)  # Default to sorting by the 4th column
sort_ascending = st.sidebar.radio("Sort order:", ["Ascending", "Descending"]) == "Ascending"

# Apply sorting
sorted_df = filtered_df.sort_values(by=sort_column, ascending=sort_ascending)

# Display sorted data
st.markdown("---")
cols = st.columns(2)
cols[0].write("### Filtered and Sorted Data")
cols[0].dataframe(sorted_df.set_index("Sector"), use_container_width=True)

TOP_N = 10
filtered_top = filtered_df.nlargest(TOP_N, sort_column)
cols[1].write(f"### Top {TOP_N} Solutions in Filtered Data")
figTop = px.bar(
    filtered_top,
    x="Solution",
    y=sort_column,
    color="Sector",
    barmode="group",
    hover_data=["Subgroup", sort_column],
)  # title=f"Top {TOP_N} CO2 Reduction by Sector and Subgroup"
figTop.update_layout(showlegend=True, legend=dict(orientation="h", x=0.5, xanchor="center", y=1.2))
cols[1].plotly_chart(figTop, use_container_width=True)
