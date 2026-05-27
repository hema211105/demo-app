import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Region Analysis",
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

st.title("Region Wise Sales Analysis")
st.write("Analyze sales, profit, quantity, and trends by region.")

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
    if "Region" in df.columns:
        selected_region = st.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )
    else:
        selected_region = []

with filter_col2:
    if "Category" in df.columns:
        selected_category = st.multiselect(
            "Select Category",
            options=df["Category"].dropna().unique(),
            default=df["Category"].dropna().unique()
        )
    else:
        selected_category = []

with filter_col3:
    if "Segment" in df.columns:
        selected_segment = st.multiselect(
            "Select Segment",
            options=df["Segment"].dropna().unique(),
            default=df["Segment"].dropna().unique()
        )
    else:
        selected_segment = []

filtered_df = df.copy()

if "Region" in filtered_df.columns and selected_region:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_region)
    ]

if "Category" in filtered_df.columns and selected_category:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_category)
    ]

if "Segment" in filtered_df.columns and selected_segment:
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(selected_segment)
    ]

st.subheader("Key Metrics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Sales",
        f"{filtered_df['Sales'].sum():,.2f}"
    )

with kpi2:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with kpi3:
    st.metric(
        "Total Quantity",
        int(filtered_df["Quantity"].sum())
    )

with kpi4:
    st.metric(
        "Total Orders",
        filtered_df["Order ID"].nunique()
    )

st.subheader("Region Wise Sales")

region_sales = filtered_df.groupby(
    "Region",
    as_index=False
)["Sales"].sum()

fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    text_auto=True,
    color="Region",
    title="Region Wise Sales"
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

st.subheader("Region Wise Quantity")

region_quantity = filtered_df.groupby(
    "Region",
    as_index=False
)["Quantity"].sum()

fig3 = px.bar(
    region_quantity,
    x="Region",
    y="Quantity",
    text_auto=True,
    color="Region",
    title="Region Wise Quantity Sold"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Region vs Category Sales")

region_category = filtered_df.groupby(
    ["Region", "Category"],
    as_index=False
)["Sales"].sum()

fig4 = px.bar(
    region_category,
    x="Region",
    y="Sales",
    color="Category",
    barmode="group",
    text_auto=True,
    title="Region vs Category Sales"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Monthly Region Sales Trend")

if "Year Month" in filtered_df.columns:

    region_trend = filtered_df.groupby(
        ["Year Month", "Region"],
        as_index=False
    )["Sales"].sum()

    fig5 = px.line(
        region_trend,
        x="Year Month",
        y="Sales",
        color="Region",
        markers=True,
        title="Monthly Region Sales Trend"
    )

    st.plotly_chart(fig5, use_container_width=True)

st.subheader("Profit vs Sales by Region")

profit_sales = filtered_df.groupby(
    "Region",
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum"
})

fig6 = px.scatter(
    profit_sales,
    x="Sales",
    y="Profit",
    size="Sales",
    color="Region",
    text="Region",
    title="Profit vs Sales by Region"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("Region Summary Table")

summary_table = filtered_df.groupby(
    "Region",
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum",
    "Discount": "mean",
    "Order ID": "nunique"
})

summary_table = summary_table.rename(
    columns={
        "Order ID": "Total Orders",
        "Discount": "Average Discount"
    }
)

st.dataframe(summary_table, use_container_width=True)

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Region Analysis Data",
    data=csv,
    file_name="region_analysis_data.csv",
    mime="text/csv"
)