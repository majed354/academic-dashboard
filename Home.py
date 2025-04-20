import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime

# إعدادات الصفحة - تغيير العنوان وإضافة أيقونة البيت
st.set_page_config(
    page_title="الرئيسية",
    page_icon="🏠",
    layout="wide"
)

# CSS مخصص لدعم اللغة العربية والتخطيط وتعديل الخط مع استجابة للشاشات المختلفة
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
    /* تطبيق الخط على جميع العناصر */
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    /* تعديلات عامة لدعم RTL */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق العنوان الرئيسي */
    h1 {
        color: #1e88e5;
        padding-bottom: 15px;
        border-bottom: 2px solid #1e88e5;
        margin-bottom: 30px;
        font-weight: 700;
        font-size: calc(1.2rem + 1vw);
    }
    
    /* تنسيق العناوين الفرعية */
    h2, h3 {
        color: #1e88e5;
        margin-top: 30px;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: calc(1rem + 0.5vw);
    }
    
    /* تنسيق البطاقات */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* تنسيق الرسم البياني */
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        width: 100%;
    }
    
    /* تنسيق البطاقات للأعضاء المميزين */
    .faculty-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e6f0 100%);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* تنسيق الإنجازات */
    .achievement-item {
        padding: 10px;
        border-right: 3px solid #1e88e5;
        margin-bottom: 10px;
        background-color: rgba(30, 136, 229, 0.05);
    }
    
    /* تحسين مظهر عناصر التحكم */
    .stSelectbox label, .stMultiselect label {
        font-weight: 500;
    }
    
    /* تحسين النصوص */
    p, div, span {
        font-size: calc(0.85rem + 0.2vw);
        line-height: 1.6;
    }
    
    /* تعديل الشريط الجانبي */
    .css-1d391kg, .css-1inwz65 {
        font-family: 'Tajawal', sans-serif !important;
    }

    /* جعل الجداول قابلة للتمرير أفقيًا */
    .stDataFrame, .stTable {
        overflow-x: auto;
    }

    /* تحسين مؤشرات metric */
    div[data-testid="stMetricValue"] {
        font-size: calc(1rem + 0.5vw) !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: calc(0.7rem + 0.2vw) !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: calc(0.6rem + 0.1vw) !important;
    }

    /* استعلامات الوسائط لتكيف دقيق */

    /* أجهزة الهواتف الصغيرة (iPhone portrait & landscape) */
    @media (max-width: 480px) {
        h1 { font-size: 1.4rem; margin-bottom: 10px; padding-bottom: 8px; }
        h2, h3 { font-size: 1rem; margin-top: 10px; margin-bottom: 8px; }
        .metric-card { padding: 8px; margin-bottom: 8px; }
        .chart-container { padding: 6px; margin-bottom: 15px; }
        text { font-size: 9px !important; }
    }

    /* الأجهزة متوسطة الحجم (iPhone Plus / small tablets) */
    @media (min-width: 481px) and (max-width: 768px) {
        h1 { font-size: 1.6rem; }
        h2, h3 { font-size: 1.1rem; }
        .metric-card { padding: 10px; }
        .chart-container { padding: 8px; }
    }

    /* أجهزة الآيباد portrait */
    @media (min-width: 769px) and (max-width: 1024px) and (orientation: portrait) {
        h1 { font-size: 1.8rem; }
        h2, h3 { font-size: 1.3rem; }
        .metric-card { padding: 12px; }
        .chart-container { padding: 10px; }
    }

    /* أجهزة الآيباد landscape */
    @media (min-width: 769px) and (max-width: 1366px) and (orientation: landscape) {
        h1 { font-size: 2rem; }
        h2, h3 { font-size: 1.4rem; }
        .metric-card { padding: 14px; }
        .chart-container { padding: 12px; }
    }

    /* الشاشات الكبيرة */
    @media (min-width: 1367px) {
        /* استخدام القيم الافتراضية */
    }

    /* تعديلات خاصة بالعناصر التفاعلية */
    button, .stButton>button {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
</style>
""", unsafe_allow_html=True)

# دالة مساعدة (تبقى للاستخدام المحتمل مستقبلاً)
def is_mobile():
    return False  # نعتمد تماماً على CSS الآن

# ---- الترويسة ----
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏠 الرئيسية")
    st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
with col2:
    today = datetime.now().strftime("%Y/%m/%d")
    st.markdown(f"<div style='text-align: left;'>التاريخ: {today}</div>", unsafe_allow_html=True)

# رسالة ترحيبية في الشريط الجانبي
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
    for year in years:
        for program in programs:
            import hashlib
            program_hash = int(hashlib.md5(program.encode()).hexdigest(), 16) % 100
            data.append({
                "العام": year,
                "البرنامج": program,
                "عدد الطلاب": 100 + (year - 2020) * 10 + program_hash % 100,
                "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + program_hash % 10),
                "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + (program_hash // 2) % 10)
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

# ---- مؤشرات رئيسية ----
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

# ---- الرسومات البيانية ----
st.subheader("تحليل البرامج الأكاديمية")
tabs = st.tabs(["توزيع الطلاب", "مقارنة المؤشرات", "التطور السنوي"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            latest_year_data, values="عدد الطلاب", names="البرنامج",
            title="توزيع الطلاب بين البرامج", color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(margin=dict(t=50, b=0), height=400, font=dict(family="Tajawal"))
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(
            latest_year_data, y="البرنامج", x="عدد الطلاب",
            title="عدد الطلاب في كل برنامج", orientation='h',
            color="عدد الطلاب", color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(xaxis_title="عدد الطلاب", yaxis={'categoryorder':'total ascending'}, height=400, font=dict(family="Tajawal"))
        st.plotly_chart(fig_bar, use_container_width=True)

with tabs[1]:
    fig_indicators = px.bar(
        latest_year_data, x="البرنامج", y=["نسبة النجاح", "معدل الرضا"],
        barmode="group", title="مقارنة المؤشرات بين البرامج",
        labels={"value": "النسبة المئوية", "variable": "المؤشر"},
        color_discrete_sequence=["#1e88e5", "#27AE60"]
    )
    fig_indicators.update_layout(xaxis_title="البرنامج", yaxis_title="النسبة المئوية", legend_title="المؤشر", height=500, font=dict(family="Tajawal"))
    st.plotly_chart(fig_indicators, use_container_width=True)

with tabs[2]:
    selected_program = st.selectbox("اختر البرنامج لعرض تطوره السنوي:", options=yearly_data["البرنامج"].unique())
    program_data = yearly_data[yearly_data["البرنامج"] == selected_program]
    fig_trend = px.line(
        program_data, x="العام", y=["عدد الطلاب", "نسبة النجاح", "معدل الرضا"],
        title=f"تطور مؤشرات برنامج {selected_program} (2020-2024)",
        labels={"value": "القيمة", "variable": "المؤشر"}, markers=True
    )
    fig_trend.update_layout(xaxis_title="السنة", yaxis_title="القيمة", legend_title="المؤشر", height=500, font=dict(family="Tajawal"))
    st.plotly_chart(fig_trend, use_container_width=True)

# ---- أعضاء هيئة التدريس والإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    for _, member in top_faculty.iterrows():
        st.markdown(f"""
        <div class='faculty-card'>
            <h3>{member['الشارة']} {member['الاسم']}</h3>
            <p><strong>اللقب:</strong> {member['اللقب']}</p>
            <p><strong>البرنامج:</strong> {member['البرنامج']}</p>
            <p><strong>النقاط:</strong> {member['النقاط']}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("[عرض جميع أعضاء هيئة التدريس](http://localhost:8501/هيئة_التدريس)")
with col2:
    st.markdown("### 🌟 أحدث الإنجازات")
    for _, ach in faculty_achievements.iterrows():
        date_obj = datetime.strptime(ach["التاريخ"], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        st.markdown(f"""
        <div class='achievement-item'>
            <p><strong>{ach['العضو']}</strong> ({ach['البرنامج']})</p>
            <p>{ach['الإنجاز']}</p>
            <p><small>التاريخ: {formatted_date} | النقاط: {ach['النقاط']}</small></p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("[عرض لوحة إنجاز المهام الكاملة](http://localhost:8501/لوحة_إنجاز_المهام)")

# ---- المخطط الحراري ----
st.subheader("مؤشرات البرامج الرئيسية")
fig_heatmap = go.Figure(data=go.Heatmap(
    z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    x=["نسبة النجاح", "معدل الرضا"],
    y=latest_year_data["البرنامج"],
    colorscale="Viridis",
    text=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    texttemplate="%{text}%",
    textfont={"size": 12},
))
fig_heatmap.update_layout(title="مقارنة المؤشرات الرئيسية عبر البرامج", margin=dict(t=50, b=0), height=400, font=dict(family="Tajawal"))
st.plotly_chart(fig_heatmap, use_container_width=True)

# ---- نصائح للاستخدام ----
st.expander("📋 نصائح للاستخدام", expanded=False).markdown("""
- انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله  
- استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء  
- قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات  
- استخدم "لوحة إنجاز المهام" لتسجيل وعرض إنجازات أعضاء هيئة التدريس
""")
