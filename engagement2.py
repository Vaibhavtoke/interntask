import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Supplier Engagement Dashboard", page_icon=":package:", layout="wide")

# ---- READ EXCEL (CSV format inside an Excel sheet) ----
@st.cache_data
def get_data_from_excel():
    # Read the sheet that contains the CSV-like data
    df = pd.read_excel(
        io="supplier_engagement.xlsx",  # Update with your Excel file path
        engine="openpyxl",
        sheet_name="m16j_supplier_analytics (2).csv",  # Update sheet name if necessary
        skiprows=0,  # Adjust if needed, depending on your file's header
        usecols="A:C",  # Assuming Supplier Name, Company Name, and Product Name are in columns A, B, and C
        nrows=50000,
    )
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

# Default is no selection
supplier = st.sidebar.multiselect(
    "Select the Supplier:",
    options=df["Supplier Name"].unique(),
    default=[]  # No default selection
)

company = st.sidebar.multiselect(
    "Select the Company:",
    options=df["Company Name"].unique(),
    default=[]  # No default selection
)

product = st.sidebar.multiselect(
    "Select the Product:",
    options=df["Product Name"].unique(),
    default=[]  # No default selection
)

# ---- Search Button ----
search_button = st.sidebar.button("Search")

# Only proceed if "Search" is clicked
if search_button:
    # Apply filter logic that allows for partial selections:
    query_string = ""
    if supplier:
        query_string += "`Supplier Name` == @supplier"
    if company:
        if query_string:
            query_string += " & "
        query_string += "`Company Name` == @company"
    if product:
        if query_string:
            query_string += " & "
        query_string += "`Product Name` == @product"

    # Apply the query only if there's a filter; otherwise, display the whole dataframe
    if query_string:
        df_selection = df.query(query_string)
    else:
        df_selection = df  # No filter applied; show all data

    # Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  # This will halt the app from further execution.

    # ---- MAINPAGE ----
    st.title(":package: Supplier Engagement Dashboard")
    st.markdown("##")

    # TOP KPI's (Engagement Metrics or Basic Data Counts)
    total_engagements = int(df_selection.shape[0])  # Assuming each row represents an engagement/transaction

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Engagements:")
        st.subheader(f"{total_engagements:,}")

    st.markdown("""---""")

    # ENGAGEMENTS BY SUPPLIER [BAR CHART]
    engagement_by_supplier = df_selection.groupby(by=["Supplier Name"]).size()
    fig_supplier_engagement = px.bar(
        engagement_by_supplier,
        x=engagement_by_supplier.index,
        y=engagement_by_supplier.values,
        title="<b>Engagements by Supplier</b>",
        color_discrete_sequence=["#0083B8"] * len(engagement_by_supplier),
        template="plotly_white",
    )
    fig_supplier_engagement.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )

    # ENGAGEMENTS BY COMPANY [BAR CHART]
    engagement_by_company = df_selection.groupby(by=["Company Name"]).size()
    fig_company_engagement = px.bar(
        engagement_by_company,
        x=engagement_by_company.index,
        y=engagement_by_company.values,
        title="<b>Engagements by Company</b>",
        color_discrete_sequence=["#0083B8"] * len(engagement_by_company),
        template="plotly_white",
    )
    fig_company_engagement.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_supplier_engagement, use_container_width=True)
    right_column.plotly_chart(fig_company_engagement, use_container_width=True)

    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # ---- CUSTOM STYLE FOR DARK BLUE BACKGROUND ----
    page_bg_style = """
        <style>
        body {
            background-color: #0B3D91;
            color: white;
        }
        </style>
        """
    st.markdown(page_bg_style, unsafe_allow_html=True)
else:
    st.info("Please select your filters and click 'Search' to see the data.")

