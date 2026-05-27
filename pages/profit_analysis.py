import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Profit Analysis",
    layout="wide"
)

@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    return df

df = read_excel("data/sales.xls")

df.columns = df.columns.str.strip()

if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

st.title("Profit Analysis Dashboard")
st.write("Analyze profit performance by category, region, segment, and time.")

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Total Records", len(df))

st.dataframe(df.head(), use_container_width=True)

st.subheader("Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    selected_region = st.multiselect(
        "Select Region",
        options=df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )

with filter_col2:
    selected_category = st.multiselect(
        "Select Category",
        options=df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )

with filter_col3:
    selected_segment = st.multiselect(
        "Select Segment",
        options=df["Segment"].dropna().unique(),
        default=df["Segment"].dropna().unique()
    )

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_region)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_category)
]

filtered_df = filtered_df[
    filtered_df["Segment"].isin(selected_segment)
]

st.subheader("Profit Metrics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with kpi2:
    st.metric(
        "Average Profit",
        f"{filtered_df['Profit'].mean():,.2f}"
    )

with kpi3:
    st.metric(
        "Maximum Profit",
        f"{filtered_df['Profit'].max():,.2f}"
    )

with kpi4:
    st.metric(
        "Minimum Profit",
        f"{filtered_df['Profit'].min():,.2f}"
    )

st.subheader("Category Wise Profit")

category_profit = filtered_df.groupby(
    "Category",
    as_index=False
)["Profit"].sum()

fig1 = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Category",
    text_auto=True,
    title="Category Wise Profit"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby(
    "Region",
    as_index=False
)["Profit"].sum()

fig2 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region Wise Profit Share"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Segment Wise Profit")

segment_profit = filtered_df.groupby(
    "Segment",
    as_index=False
)["Profit"].sum()

fig3 = px.bar(
    segment_profit,
    x="Segment",
    y="Profit",
    color="Segment",
    text_auto=True,
    title="Segment Wise Profit"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Monthly Profit Trend")

monthly_profit = filtered_df.groupby(
    "Year Month",
    as_index=False
)["Profit"].sum()

fig4 = px.line(
    monthly_profit,
    x="Year Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Sales vs Profit")

fig5 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_data=["Region", "Segment"],
    title="Sales vs Profit Analysis"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Discount vs Profit")

fig6 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    title="Discount Impact on Profit"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("Profit Summary Table")

summary_table = filtered_df.groupby(
    ["Region", "Category"],
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum",
    "Discount": "mean"
})

summary_table = summary_table.rename(
    columns={
        "Discount": "Average Discount"
    }
)

st.dataframe(summary_table, use_container_width=True)

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Profit Analysis Data",
    data=csv,
    file_name="profit_analysis.csv",
    mime="text/csv"
)