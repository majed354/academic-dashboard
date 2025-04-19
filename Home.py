import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime
import streamlit_shadcn_ui as ui

# إعدادات الصفحة
st.set_page_config(
    page_title="لوحة مؤشرات البرامج الأكاديمية",
    page_icon="📊",
    layout="wide"
)

# CSS مخصص لدعم اللغة العربية والتخطيط
st.markdown("""
<style>
    /* تعديلات عامة لدعم RTL */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* ... بقية التنسيقات كما في الأصل ... */
</style>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---- الترويسة ----
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
    st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
with col2:
    today = datetime.now().strftime("%Y/%m/%d")
    st.markdown(f"<div style='text-align: left;'>التاريخ: {today}</div>", unsafe_allow_html=True)

# رسالة ترحيبية في الشريط الجانبي
with st.sidebar:
    ui.alert(
        title="مرحباً بك في لوحة المعلومات",
        description="اختر برنامجًا من القائمة أعلاه لعرض تفاصيله",
        variant="default"
    )

# ---- تحميل البيانات ----
@st.cache_data(ttl=3600)
def load_department_summary():
    try:
        return get_github_file_content("data/department_summary.csv")
    except:
        data = {"البرنامج": ["بكالوريوس في القرآن وعلومه","بكالوريوس القراءات","ماجستير الدراسات القرآنية المعاصرة","ماجستير القراءات","دكتوراه علوم القرآن","دكتوراه القراءات"],
                "عدد الطلاب": [125,110,90,120,70,85],
                "عدد الطالبات": [85,70,60,80,50,55],
                "أعضاء هيئة التدريس": [15,12,8,10,5,6]}
        return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_yearly_data():
    years = list(range(2020,2025))
    data = []
    programs = load_department_summary()["البرنامج"].tolist()
    for year in years:
        for i, program in enumerate(programs):
            male = 60 + (year-2020)*5 + i*10
            female = 40 + (year-2020)*5 + i*8
            total = male + female
            data.append({"العام": year,
                         "البرنامج": program,
                         "عدد الطلاب": male,
                         "عدد الطالبات": female,
                         "المجموع": total,
                         "نسبة النجاح": min(95,70 + (year-2020)*2 + i*2),
                         "معدل الرضا": min(90,75 + (year-2020)*1.5 + i)})
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_faculty_achievements():
    achievements = [
        {"العضو":"د. محمد أحمد","الإنجاز":"نشر بحث في مجلة عالمية","التاريخ":"2025-04-15","النقاط":50,"البرنامج":"بكالوريوس في القرآن وعلومه"},
        {"العضو":"د. عائشة سعد","الإنجاز":"إطلاق مبادرة تعليمية","التاريخ":"2025-04-10","النقاط":40,"البرنامج":"دكتوراه علوم القرآن"},
        {"العضو":"د. عبدالله محمد","الإنجاز":"المشاركة في مؤتمر دولي","التاريخ":"2025-04-05","النقاط":35,"البرنامج":"بكالوريوس القراءات"}
    ]
    return pd.DataFrame(achievements)

@st.cache_data(ttl=3600)
def load_top_faculty():
    top = [
        {"الاسم":"د. عائشة سعد","اللقب":"العضو القمة","الشارة":"👑","النقاط":320,"البرنامج":"دكتوراه علوم القرآن"},
        {"الاسم":"د. محمد أحمد","اللقب":"العضو المميز","الشارة":"🌟","النقاط":280,"البرنامج":"بكالوريوس في القرآن وعلومه"}
    ]
    return pd.DataFrame(top)

# تحميل البيانات ومعالجة
try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_females = dept_data["عدد الطالبات"].sum()
    yearly = load_yearly_data()
    max_year = yearly["العام"].max()
    latest = yearly[yearly["العام"]==max_year]
    achievements = load_faculty_achievements()
    top_fac = load_top_faculty()
except Exception as e:
    ui.alert(title="خطأ في البيانات", description=str(e), variant="destructive")
    dept_data = pd.DataFrame([]); latest = pd.DataFrame([]); achievements = pd.DataFrame([]); top_fac = pd.DataFrame([])

# ---- المؤشرات الرئيسية ----
st.subheader("المؤشرات الرئيسية")
col1, col2, col3, col4 = st.columns(4)
ui.metric_card(title="عدد الطلاب", content=f"{total_students}", description="+3% منذ العام الماضي", trend="up", key="m1").render()
ui.metric_card(title="عدد الطالبات", content=f"{total_females}", description="+7% منذ العام الماضي", trend="up", key="m2").render()
ui.metric_card(title="معدل النجاح الإجمالي", content="87%", description="+3% منذ العام الماضي", trend="up", key="m3").render()
ui.metric_card(title="متوسط رضا الطلاب", content="92%", description="+4% منذ العام الماضي", trend="up", key="m4").render()

# ---- تحليل البرامج ----
st.subheader("تحليل البرامج الأكاديمية")
if not latest.empty:
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "توزيع الطلاب والطالبات"
    with ui.tabs(value=st.session_state.active_tab):
        ui.tab("توزيع الطلاب والطالبات", id="tab1")
        ui.tab("مقارنة البرامج", id="tab2")
        ui.tab("التطور السنوي", id="tab3")
    active = st.session_state.active_tab
    if active == "توزيع الطلاب والطالبات":
        c1, c2 = st.columns(2)
        with c1:
            pie = pd.DataFrame({"الفئة":["الطلاب","الطالبات"],"العدد":[total_students, total_females]})
            fig = px.pie(pie, names="الفئة", values="العدد", title="توزيع الطلاب والطالبات")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.bar(latest, y="البرنامج", x=["عدد الطلاب","عدد الطالبات"], barmode="stack", title="حسب البرنامج")
            st.plotly_chart(fig2, use_container_width=True)
    elif active == "مقارنة البرامج":
        fig3 = px.bar(latest, x="البرنامج", y=["نسبة النجاح","معدل الرضا"], barmode="group", title="مقارنة المؤشرات")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        sp, gp = st.columns([2,1])
        with sp:
            program = ui.select(label="اختر البرنامج:", options=[{"label":p,"value":p} for p in dept_data["البرنامج"]], default=dept_data["البرنامج"][0], key="sel_prog")
        with gp:
            gender = ui.radio_group(label="اختر الفئة:", options=[{"label":"الكل","value":"all"},{"label":"طلاب","value":"male"},{"label":"طالبات","value":"female"}], default="all", orientation="horizontal", key="sel_gen")
        dfp = yearly[yearly["البرنامج"]==program]
        if not dfp.empty:
            cols = ["عدد الطلاب","عدد الطالبات"] if gender=="all" else ["عدد الطلاب"] if gender=="male" else ["عدد الطالبات"]
            fig4 = px.line(dfp, x="العام", y=cols, title=f"تطور {program}")
            st.plotly_chart(fig4, use_container_width=True)

# ---- هيئة التدريس والإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")
colA, colB = st.columns(2)
with colA:
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    for _,row in top_fac.iterrows():
        with ui.card(title="{0} {1}".format(row['الشارة'],row['الاسم']), key=row['الاسم']):
            ui.badge(row['اللقب'], variant="outline").render()
            st.write(f"برنامج: {row['البرنامج']} — نقاط: {row['النقاط']}")
with colB:
    st.markdown("### 🌟 أحدث الإنجازات")
    for _,r in achievements.iterrows():
        with ui.card(title=r['العضو'], key=r['العضو']):
            st.write(r['الإنجاز'])
            ui.badge(f"التاريخ: {r['التاريخ']}", size="sm").render()
            ui.badge(f"نقاط: {r['النقاط']}", size="sm").render()

# ---- المخطط الحراري ----
st.subheader("مؤشرات البرامج الرئيسية")
if not latest.empty:
    figh = go.Figure(go.Heatmap(z=latest[["نسبة النجاح","معدل الرضا"]].values,
                                 x=["نسبة النجاح","معدل الرضا"],
                                 y=latest["البرنامج"],
                                 colorscale="Viridis"))
    st.plotly_chart(figh, use_container_width=True)

# ---- نصائح المستخدم ----
st.subheader("نصائح للاستخدام")
ui.alert(
    title="نصائح للاستخدام",
    description="- انقر على اسم برنامج في الشريط الجانبي\n- للمزيد شاهد صفحات هيئة التدريس والإنجازات",
    variant="default"
)
