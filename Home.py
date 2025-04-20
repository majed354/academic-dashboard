import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="لوحة مؤشرات البرامج الأكاديمية",
    page_icon="📊",
    layout="wide"
)

# --- قراءة ملف الخط وتحويله إلى Base64 ---
with open("static/fonts/Mj_TunisiaLt.ttf", "rb") as font_file:
    font_base64 = base64.b64encode(font_file.read()).decode("utf-8")

# تضمين meta viewport وCSS للخطّ المخصص
st.markdown(
    f"""
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        @font-face {{
            font-family: 'Mj Tunisia Lt';
            src: url(data:font/ttf;base64,{font_base64}) format('truetype');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }}
        html, body, [class*="css"], .stApp, .stMarkdown {{
            font-family: 'Mj Tunisia Lt', sans-serif;
        }}
        /* دعم RTL */
        .stApp {{ direction: rtl; text-align: right; }}
        h1 {{
            color: #1e88e5;
            padding-bottom: 15px;
            border-bottom: 2px solid #1e88e5;
            margin-bottom: 30px;
            font-weight: 700;
        }}
        h2, h3 {{
            color: #1e88e5;
            margin-top: 30px;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        .metric-card, .chart-container, .faculty-card, .achievement-item {{
            font-weight: 400;
        }}
        @media only screen and (max-width: 600px) {{
            .stDataFrame, .stPlotlyChart, .streamlit-pdf-viewer {{ width: 100% !important; }}
            [data-testid="stBlock"] > .row-widget.stColumns {{ flex-direction: column !important; }}
            [data-testid="stSidebar"] {{ display: none; }}
            .block-container {{ padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- الترويسة ----
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
    st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
with col2:
    today = datetime.now().strftime("%Y/%m/%d")
    st.markdown(f"<div style='text-align: left;'>التاريخ: {today}</div>", unsafe_allow_html=True)

# رسالة ترحيبية
st.sidebar.success("اختر برنامجًا من القائمة أعلاه لعرض تفاصيله.")

# ---- تحميل البيانات ----
@st.cache_data(ttl=3600)
def load_department_summary():
    try:
        return get_github_file_content("data/department_summary.csv")
    except:
        data = {
            "البرنامج": [
                "بكالوريوس في القرآن وعلومه",
                "بكالوريوس القراءات",
                "ماجستير الدراسات القرآنية المعاصرة",
                "ماجستير القراءات",
                "دكتوراه علوم القرآن",
                "دكتوراه القراءات"
            ],
            "عدد الطلاب": [210, 180, 150, 200, 120, 140],
            "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6]
        }
        return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_yearly_data():
    years = list(range(2020, 2025))
    data = []
    programs = [
        "بكالوريوس في القرآن وعلومه",
        "بكالوريوس القراءات",
        "ماجستير الدراسات القرآنية المعاصرة",
        "ماجستير القراءات",
        "دكتوراه علوم القرآن",
        "دكتوراه القراءات"
    ]
    import hashlib
    for year in years:
        for program in programs:
            ph = int(hashlib.md5(program.encode()).hexdigest(), 16) % 100
            data.append({
                "العام": year,
                "البرنامج": program,
                "عدد الطلاب": 100 + (year - 2020) * 10 + ph,
                "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + ph % 10),
                "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + (ph // 2) % 10)
            })
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_faculty_achievements():
    achievements = [
        {"العضو": "د. محمد أحمد", "الإنجاز": "نشر بحث في مجلة عالمية", "التاريخ": "2025-04-15", "النقاط": 50, "البرنامج": "بكالوريوس في القرآن وعلومه"},
        {"العضو": "د. عائشة سعد", "الإنجاز": "إطلاق مبادرة تعليمية", "التاريخ": "2025-04-10", "النقاط": 40, "البرنامج": "دكتوراه علوم القرآن"},
        {"العضو": "د. عبدالله محمد", "الإنجاز": "المشاركة في مؤتمر دولي", "التاريخ": "2025-04-05", "النقاط": 35, "البرنامج": "بكالوريوس القراءات"},
        {"العضو": "د. فاطمة علي", "الإنجاز": "تطوير مقرر دراسي", "التاريخ": "2025-04-01", "النقاط": 30, "البرنامج": "ماجستير الدراسات القرآنية المعاصرة"},
        {"العضو": "د. خالد إبراهيم", "الإنجاز": "تقديم ورشة عمل", "التاريخ": "2025-03-25", "النقاط": 25, "البرنامج": "ماجستير القراءات"}
    ]
    return pd.DataFrame(achievements)

@st.cache_data(ttl=3600)
def load_top_faculty():
    top_faculty = [
        {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"},
        {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"},
        {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"}
    ]
    return pd.DataFrame(top_faculty)

try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_faculty = dept_data["أعضاء هيئة التدريس"].sum()
    yearly_data = load_yearly_data()
    latest_year_data = yearly_data[yearly_data["العام"] == 2024]
    faculty_achievements = load_faculty_achievements()
    top_faculty = load_top_faculty()
except Exception as e:
    st.error(f"خطأ في تحميل البيانات: {e}")
    st.warning("سيتم استخدام بيانات تجريبية لأغراض العرض.")
    total_students = 1000
    total_faculty = 50

# المؤشرات الرئيسية
st.subheader("المؤشرات الرئيسية")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("إجمالي عدد الطلاب", f"{total_students:,}", "+5% منذ العام الماضي")
with c2:
    st.metric("إجمالي أعضاء هيئة التدريس", f"{total_faculty:,}", "+2 عضو جديد")
with c3:
    st.metric("معدل النجاح الإجمالي", "87%", "+3% منذ العام الماضي")
with c4:
    st.metric("متوسط رضا الطلاب", "92%", "+4% منذ العام الماضي")

# الرسومات
st.subheader("تحليل البرامج الأكاديمية")
tabs = st.tabs(["توزيع الطلاب", "مقارنة المؤشرات", "التطور السنوي"])

with tabs[0]:
    col1, col2 = st.columns([1, 1])
    with col1:
        fig_pie = px.pie(
            latest_year_data,
            values="عدد الطلاب",
            names="البرنامج",
            title="توزيع الطلاب بين البرامج",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(
            latest_year_data,
            y="البرنامج",
            x="عدد الطلاب",
            title="#"")]}
