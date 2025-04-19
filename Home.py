import streamlit as st
import pandas as pd
import plotly.express as px
from pages.utils.github_helpers import get_github_file_content

st.set_page_config(
    page_title="لوحة مؤشرات البرامج الأكاديمية",
    page_icon="📊",
    layout="wide"
)

st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")

st.sidebar.success("اختر برنامجًا من القائمة أعلاه لعرض تفاصيله.")

@st.cache_data(ttl=3600)
def load_department_summary():
    return get_github_file_content("data/department_summary.csv")

try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_faculty = dept_data["أعضاء هيئة التدريس"].sum()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("إجمالي عدد الطلاب", f"{total_students:,}")
    with col2:
        st.metric("إجمالي أعضاء هيئة التدريس", f"{total_faculty:,}")
    st.divider()
except Exception as e:
    st.error(f"خطأ في تحميل بيانات القسم: {e}")
