# 02_📖_بكالوريوس القراءات.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
from pages.utils.github_helpers import get_github_file_content, get_available_years, get_available_reports

st.set_page_config(
    page_title="بكالوريوس القراءات",
    page_icon="📖",
    layout="wide"
)

st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    unsafe_allow_html=True
)
st.markdown("""
<style>
    .stApp { direction: rtl; text-align: right; }
    h1, h2, h3, h4, h5, h6 { text-align: right; }
    .dataframe { text-align: right; }
    button, input, select, textarea, .stButton>button, .stTextInput>div>div>input { text-align: right; }
    .stMarkdown { text-align: right; }
    .css-1inwz65 { text-align: right; }
    .plotly { direction: ltr; }
    @media only screen and (max-width: 600px) {
        .stDataFrame, .stPlotlyChart, .streamlit-pdf-viewer { width: 100% !important; }
        [data-testid="stBlock"] > .row-widget.stColumns { flex-direction: column !important; }
        [data-testid="stSidebar"] { display: none; }
        .block-container { padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("📖 بكالوريوس القراءات")

program_code = "bachelor_readings"
available_years, data_file_map = get_available_years(program_code)
available_reports = get_available_reports(program_code)

st.sidebar.header("تصفية البيانات")

if available_years:
    year_key = f'selected_year_{program_code}'
    if year_key not in st.session_state:
        st.session_state[year_key] = available_years[0]

    selected_year = st.sidebar.selectbox(
        "اختر السنة:",
        available_years,
        key=f'selectbox_{year_key}',
        index=available_years.index(st.session_state[year_key])
    )
    st.session_state[year_key] = selected_year

    if selected_year in data_file_map:
        st.header(f"بيانات عام {selected_year}")
        df = get_github_file_content(data_file_map[selected_year])
        if isinstance(df, pd.DataFrame):
            st.dataframe(df, use_container_width=True)
            if "النسبة المئوية" in df.columns and "الهدف" in df.columns and "المعيار" in df.columns:
                st.subheader("مقارنة النسب المئوية بالأهداف")
                fig = px.bar(
                    df,
                    x="المعيار",
                    y=["النسبة المئوية", "الهدف"],
                    barmode="group",
                    title=f"مؤشرات الأداء لعام {selected_year}",
                    labels={"value": "النسبة المئوية", "variable": ""}
                )
                st.plotly_chart(fig, use_container_width=True)
                if selected_year != available_years[-1]:
                    st.subheader("تطور المؤشرات خلال السنوات")
                    trend_data = []
                    for year in available_years:
                        if year >= selected_year:
                            year_df = get_github_file_content(data_file_map[year])
                            if isinstance(year_df, pd.DataFrame):
                                for _, row in year_df.iterrows():
                                    trend_data.append({
                                        "العام": str(year),
                                        "المعيار": row["المعيار"],
                                        "النسبة المئوية": row["النسبة المئوية"]
                                    })
                    if trend_data:
                        trend_df = pd.DataFrame(trend_data)
                        fig_trend = px.line(
                            trend_df,
                            x="العام",
                            y="النسبة المئوية",
                            color="المعيار",
                            markers=True,
                            title="تطور النسب المئوية للمؤشرات"
                        )
                        st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.error("تعذر تحميل البيانات")
else:
    st.sidebar.warning("لا توجد بيانات سنوية متاحة لهذا البرنامج")

if available_reports:
    st.sidebar.header("التقارير والمستندات")
    report_key = f'selected_report_{program_code}'

    annual_reports = {k: v for k, v in available_reports.items() if k.startswith('تقرير_')}
    desc_files = {k: v for k, v in available_reports.items() if k.startswith('توصيف_')}

    if desc_files:
        with st.expander("توصيف البرنامج", expanded=False):
            desc_name = list(desc_files.keys())[0]
            desc_content = get_github_file_content(desc_files[desc_name])
            if desc_content:
                st.markdown(desc_content)

    if annual_reports:
        report_names = list(annual_reports.keys())
        if report_key not in st.session_state:
            st.session_state[report_key] = report_names[0]

        selected_report = st.sidebar.selectbox(
            "اختر تقريرًا:",
            report_names,
            key=f'selectbox_{report_key}',
            index=report_names.index(st.session_state[report_key]) if st.session_state[report_key] in report_names else 0
        )
        st.session_state[report_key] = selected_report

        if selected_report:
            st.header(f"تقرير: {selected_report.replace('.md', '')}")
            report_content = get_github_file_content(annual_reports[selected_report])
            if report_content:
                if selected_report.endswith('.md'):
                    st.markdown(report_content)
                elif selected_report.endswith('.pdf'):
                    pdf_viewer(st.session_state[f'pdf_data_{selected_report}'])
else:
    st.sidebar.warning("لا توجد تقارير متاحة لهذا البرنامج")
