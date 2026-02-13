import streamlit as st

from data_loader import load_data
from analyzer import prepare_summary
from ai_analysis import generate_insight

st.set_page_config(
    page_title="Printing Cost Dashboard",
    layout="wide"
)

st.title("Dashboard Biaya Printing")

uploaded_file = st.file_uploader(
    "Upload file Excel", type=["xlsx", "xls"]
)

if uploaded_file:
    df = load_data(uploaded_file)

    st.subheader("Mapping Kolom")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        col_month = st.selectbox(
            "Kolom Bulan", df.columns
        )
    with col2:
        col_dept = st.selectbox(
            "Kolom Departemen", df.columns
        )
    with col3:
        col_bw = st.selectbox(
            "Kolom BW Pages", df.columns
        )
    with col4:
        col_color = st.selectbox(
            "Kolom Color Pages", df.columns
        )

    st.subheader("Harga per Halaman")

    h1, h2 = st.columns(2)
    with h1:
        bw_price = st.number_input(
            "Harga BW / halaman", value=110
        )
    with h2:
        color_price = st.number_input(
            "Harga Color / halaman", value=1300
        )

    raw_df, monthly, dept = prepare_summary(
        df,
        col_month,
        col_dept,
        col_bw,
        col_color,
        bw_price,
        color_price
    )

    st.subheader("Ringkasan Utama")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Pages", f"{int(monthly['TOTAL_PAGES'].sum()):,}")
    k2.metric("BW Pages", f"{int(monthly['BW_PAGES'].sum()):,}")
    k3.metric("Color Pages", f"{int(monthly['COLOR_PAGES'].sum()):,}")
    k4.metric("Total Cost", f"Rp{int(monthly['TOTAL_COST'].sum()):,}")
    
    st.subheader("Cost Trend per Month")
    st.line_chart(
        monthly.set_index("PERIOD")[
            ["BW_COST", "COLOR_COST", "TOTAL_COST"]
        ]
    )

    st.subheader("Halaman yang digunakan perbulan")
    st.bar_chart(
        monthly.set_index("PERIOD")["January","February","March","April","Mey","June","July","August","September","October","November","Desember"
            ["BW_PAGES", "COLOR_PAGES"]
        ]
    )

    st.subheader("Ringkasan Bulanan")
    st.dataframe(monthly)

    st.subheader("Analisis Departemen")

    top_dept = (
        dept.sort_values("TOTAL_COST", ascending=False)
        .set_index("DEPARTMENT")
    )

    st.bar_chart(top_dept["TOTAL_COST"])
    st.dataframe(dept)

    st.subheader("Insight & Recommendation")

    for text in generate_insight(monthly, dept):
        st.markdown(f"- {text}")

