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
    /* التنسيقات الأخرى تبقى كما في الأصل */
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
    st.info(
        "مرحباً بك في لوحة المعلومات\n\n" +
        "اختر برنامجًا من القائمة أعلاه لعرض تفاصيله"
    )

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
            "عدد الطلاب": [125, 110, 90, 120, 70, 85],
            "عدد الطالبات": [85, 70, 60, 80, 50, 55],
            "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6]
        }
        return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_yearly_data():
    years = list(range(2020, 2025))
    data = []
    programs = load_department_summary()["البرنامج"].tolist()
    for year in years:
        for i, program in enumerate(programs):
            male_students = 60 + (year - 2020) * 5 + i * 10
            female_students = 40 + (year - 2020) * 5 + i * 8
            data.append({
                "العام": year,
                "البرنامج": program,
                "عدد الطلاب": male_students,
                "عدد الطالبات": female_students,
                "المجموع": male_students + female_students,
                "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + i * 2),
                "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + i)
            })
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_faculty_achievements():
    achievements = [
        {"العضو": "د. محمد أحمد", "الإنجاز": "نشر بحث في مجلة عالمية", "التاريخ": "2025-04-15", "النقاط": 50, "البرنامج": "بكالوريوس في القرآن وعلومه"},
        {"العضو": "د. عائشة سعد", "الإنجاز": "إطلاق مبادرة تعليمية", "التاريخ": "2025-04-10", "النقاط": 40, "البرنامج": "دكتوراه علوم القرآن"},
        {"العضو": "د. عبدالله محمد", "الإنجاز": "المشاركة في مؤتمر دولي", "التاريخ": "2025-04-05", "النقاط": 35, "البرنامج": "بكالوريوس القراءات"}
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

# ---- محاولة تحميل البيانات ----
try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_female_students = dept_data["عدد الطالبات"].sum()
    yearly_data = load_yearly_data()
    max_year = yearly_data["العام"].max()
    latest_year_data = yearly_data[yearly_data["العام"] == max_year].copy()
    faculty_achievements = load_faculty_achievements()
    top_faculty = load_top_faculty()
except Exception as e:
    st.error(f"خطأ في تحميل البيانات: {e}\nسيتم استخدام بيانات تجريبية لأغراض العرض.")
    dept_data = pd.DataFrame([])
    latest_year_data = pd.DataFrame([])
    faculty_achievements = pd.DataFrame([])
    top_faculty = pd.DataFrame([])

# ---- المؤشرات الرئيسية ----
st.subheader("المؤشرات الرئيسية")
cols = st.columns(4)
ui.metric_card(title="عدد الطلاب", content=f"{total_students:,}", description="+3% منذ العام الماضي", trend="up", key="m1").render()
ui.metric_card(title="عدد الطالبات", content=f"{total_female_students:,}", description="+7% منذ العام الماضي", trend="up", key="m2").render()
ui.metric_card(title="معدل النجاح الإجمالي", content="87%", description="+3% منذ العام الماضي", trend="up", key="m3").render()
ui.metric_card(title="متوسط رضا الطلاب", content="92%", description="+4% منذ العام الماضي", trend="up", key="m4").render()

# ---- تحليل البرامج الأكاديمية ----
st.subheader("تحليل البرامج الأكاديمية")
if not latest_year_data.empty:
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "توزيع الطلاب والطالبات"
    with ui.tabs(value=st.session_state.active_tab):
        ui.tab("توزيع الطلاب والطالبات", id="tab1")
        ui.tab("مقارنة البرامج", id="tab2")
        ui.tab("التطور السنوي", id="tab3")
    active_tab = st.session_state.active_tab
    if active_tab == "توزيع الطلاب والطالبات":
        c1, c2 = st.columns(2)
        with c1:
            pie_df = pd.DataFrame({"الفئة": ["الطلاب", "الطالبات"], "العدد": [total_students, total_female_students]})
            fig = px.pie(pie_df, values="العدد", names="الفئة", title="توزيع الطلاب والطالبات")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.bar(latest_year_data, y="البرنامج", x=["عدد الطلاب", "عدد الطالبات"], barmode="stack", title="توزيع الطلاب والطالبات حسب البرنامج")
            st.plotly_chart(fig2, use_container_width=True)
    elif active_tab == "مقارنة البرامج":
        fig3 = px.bar(latest_year_data, x="البرنامج", y=["نسبة النجاح", "معدل الرضا"], barmode="group", title="مقارنة المؤشرات بين البرامج")
        st.plotly_chart(fig3, use_container_width=True)
        latest_year_data["نسبة الطالبات للطلاب"] = (
            latest_year_data["عدد الطالبات"] / latest_year_data["عدد الطلاب"] * 100
        ).round(1)
        fig4 = px.bar(latest_year_data, x="البرنامج", y="نسبة الطالبات للطلاب", title="نسبة الطالبات إلى الطلاب في كل برنامج (%)", text_auto='.1f')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        sp, gp = st.columns([2, 1])
        with sp:
            selected_program = ui.select(
                label="اختر البرنامج لعرض تطوره السنوي:",
                options=[{"label": prog, "value": prog} for prog in dept_data["البرنامج"].unique()],
                default=dept_data["البرنامج"].unique()[0],
                key="sel_prog"
            )
        with gp:
            gender_option = ui.radio_group(
                label="اختر الفئة:",
                options=[{"label": "الكل", "value": "all"}, {"label": "الطلاب", "value": "male"}, {"label": "الطالبات", "value": "female"}],
                default="all",
                orientation="horizontal",
                key="sel_gen"
            )
        prog_df = yearly_data[yearly_data["البرنامج"] == selected_program]
        if prog_df.empty:
            st.warning(f"لا توجد بيانات متاحة للبرنامج المحدد: {selected_program}")
        else:
            cols = ["عدد الطلاب", "عدد الطالبات"] if gender_option == "all" else (["عدد الطلاب"] if gender_option == "male" else ["عدد الطالبات"])
            fig5 = px.line(prog_df, x="العام", y=cols, title=f"تطور أعداد الطلاب في برنامج {selected_program} (2020-2024)", markers=True)
            st.plotly_chart(fig5, use_container_width=True)

else:
    st.warning("لا يمكن عرض الرسومات البيانية بسبب عدم توفر البيانات.")

# ---- أعضاء هيئة التدريس والإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")
colA, colB = st.columns(2)
with colA:
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    if not top_faculty.empty:
        for _, member in top_faculty.iterrows():
            with ui.card(title=f"{member['الشارة']} {member['الاسم']}", key=member['الاسم']):
                ui.badge(member['اللقب'], variant="outline").render()
                st.write(f"البرنامج: {member['البرنامج']} — نقاط: {member['النقاط']}")
    else:
        st.info("لا توجد بيانات متاحة حالياً عن أعضاء هيئة التدريس المميزين.")
    st.button("عرض جميع الأعضاء", on_click=lambda: st.experimental_set_query_params(page="هيئة_التدريس"))
with colB:
    st.markdown("### 🌟 أحدث الإنجازات")
    if not faculty_achievements.empty:
        for _, ach in faculty_achievements.iterrows():
            date_obj = datetime.strptime(ach['التاريخ'], "%Y-%m-%d")
            st.write(f"**{ach['العضو']}** ({ach['البرنامج']}) — {ach['الإنجاز']} — {date_obj:%d/%m/%Y} — نقاط: {ach['النقاط']}")
    else:
        st.info("لا توجد بيانات متاحة حالياً عن إنجازات أعضاء هيئة التدريس.")
    st.button("عرض جميع الإنجازات", on_click=lambda: st.experimental_set_query_params(page="إنجازات_الأعضاء"))

# ---- مخطط حراري للمؤشرات الرئيسية ----
st.subheader("مؤشرات البرامج الرئيسية")
if not latest_year_data.empty:
    heat = go.Figure(go.Heatmap(
        z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
        x=["نسبة النجاح", "معدل الرضا"],
        y=latest_year_data["البرنامج"],
        colorscale="Viridis"
    ))
    st.plotly_chart(heat, use_container_width=True)
else:
    st.warning("لا يمكن عرض المخطط الحراري بسبب عدم توفر البيانات.")

# ---- نصائح للمستخدم ----
with ui.card(key="usage_tips"):
    st.markdown(
        """
        **نصائح للاستخدام**  
        - انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله  
        - استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء  
        - قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات  
        - استخدم "لوحة إنجازات الأعضاء" لتسجيل وعرض إنجازات أعضاء هيئة التدريس  
        """
    )
