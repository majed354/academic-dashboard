import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import hashlib
import numpy as np

# إعدادات الصفحة
st.set_page_config(
    page_title="إنجازات أعضاء هيئة التدريس",
    page_icon="🏆",
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
    /* ... بقية الـ CSS كما في الأصل ... */
</style>
""", unsafe_allow_html=True)

# ---- دوال مساعدة ----

@st.cache_data(ttl=3600)
def load_faculty_data():
    data = {
        "الاسم": ["د. محمد أحمد", "د. عبدالله محمد", "د. فاطمة علي", "د. خالد إبراهيم", 
                  "د. عائشة سعد", "د. علي حسن", "د. نورة خالد", "د. سارة ناصر",
                  "د. أحمد عبدالله", "د. عمر يوسف", "د. ليلى حامد", "د. زيد ياسر"],
        "الدرجة العلمية": ["أستاذ", "أستاذ مشارك", "أستاذ مساعد", "أستاذ مساعد", 
                           "أستاذ", "أستاذ مشارك", "أستاذ مساعد", "محاضر",
                           "أستاذ مساعد", "محاضر", "أستاذ مشارك", "أستاذ"],
        "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", 
                     "دكتوراه علوم القرآن", "دكتوراه القراءات", "بكالوريوس في القرآن وعلومه", "ماجستير القراءات",
                     "بكالوريوس في القرآن وعلومه", "ماجستير الدراسات القرآنية المعاصرة", "دكتوراه علوم القرآن", "دكتوراه القراءات"]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def generate_achievements_data():
    faculty_df = load_faculty_data()
    task_types = [
        "نشر بحث علمي", "تقديم محاضرة", "إشراف على رسالة", "تنظيم ورشة عمل", 
        "حضور مؤتمر", "مراجعة أبحاث", "تطوير مقرر", "المشاركة في لجنة", 
        "تقديم دورة تدريبية", "مبادرة خدمة مجتمعية"
    ]
    task_points_range = {
        "نشر بحث علمي": (30, 50), "تقديم محاضرة": (10, 25), "إشراف على رسالة": (20, 35),
        "تنظيم ورشة عمل": (15, 30), "حضور مؤتمر": (10, 20), "مراجعة أبحاث": (5, 15),
        "تطوير مقرر": (20, 40), "المشاركة في لجنة": (10, 20), "تقديم دورة تدريبية": (15, 30),
        "مبادرة خدمة مجتمعية": (20, 40)
    }
    achievements = []
    current_date = datetime(2025, 4, 19)
    for _ in range(100):
        idx = random.randint(0, len(faculty_df) - 1)
        name = faculty_df.iloc[idx]["الاسم"]
        program = faculty_df.iloc[idx]["البرنامج"]
        task = random.choice(task_types)
        days_back = random.randint(0, 180)
        date = (current_date - timedelta(days=days_back)).strftime("%Y-%m-%d")
        pts = random.randint(*task_points_range[task])
        desc_map = {
            "نشر بحث علمي": [
                f"نشر بحث في مجلة {random.choice(['الدراسات الإسلامية', 'العلوم الشرعية', 'الدراسات القرآنية'])}",
                f"نشر ورقة بحثية في مؤتمر {random.choice(['الدراسات القرآنية الدولي', 'علوم القرآن', 'التفسير المعاصر'])}",
                f"نشر كتاب بعنوان 'دراسات في {random.choice(['التفسير', 'القراءات', 'علوم القرآن'])}'"
            ],
            "تقديم محاضرة": [
                f"تقديم محاضرة عامة بعنوان '{random.choice(['أساليب التدبر', 'منهجيات التفسير', 'التجديد في الدراسات القرآنية'])}'",
                f"تقديم محاضرة في برنامج {random.choice(['الثقافة القرآنية', 'الأسبوع العلمي', 'الملتقى الأكاديمي'])}"
            ],
            "إشراف على رسالة": [
                f"الإشراف على رسالة ماجستير بعنوان '{random.choice(['دراسة في...', 'تحليل...', 'منهج...'])}'",
                f"الإشراف على رسالة دكتوراه في مجال {random.choice(['التفسير المقارن', 'الدراسات القرآنية', 'القراءات'])}"
            ]
        }
        description = random.choice(desc_map.get(task, [f"{task} في مجال {random.choice(['التفسير', 'القراءات', 'علوم القرآن'])}"]))
        rating = random.choices([1,2,3,4,5], weights=[0.05,0.1,0.15,0.3,0.4])[0]
        achievements.append({
            "العضو": name, "البرنامج": program, "نوع المهمة": task,
            "الوصف": description, "التاريخ": date, "النقاط": pts, "التقييم": rating
        })
    df = pd.DataFrame(achievements).sort_values(by="التاريخ", ascending=False)
    return df

@st.cache_data(ttl=3600)
def get_available_tasks():
    tasks = [
        {"اسم المهمة": "نشر بحث في مجلة محكمة", "الوصف": "نشر بحث علمي في مجلة محكمة في مجال التخصص", "نطاق النقاط": (30, 50), "المتطلبات": "رابط البحث أو صورة من القبول", "التصنيف": "بحث علمي"},
        # ... بقية المهام كما في الأصل ...
    ]
    return pd.DataFrame(tasks)

@st.cache_data(ttl=3600)
def calculate_faculty_achievements(achievements_df):
    summaries = achievements_df.groupby("العضو").agg({
        "النقاط": "sum", "الوصف": "count", "التقييم": "mean"
    }).rename(columns={"الوصف": "عدد المهام", "التقييم": "متوسط التقييم"}).reset_index()
    program_map = achievements_df.groupby("العضو")["البرنامج"].first().to_dict()
    summaries["البرنامج"] = summaries["العضو"].map(program_map)
    latest = achievements_df.sort_values("التاريخ", ascending=False).groupby("العضو").first()["التاريخ"].to_dict()
    summaries["آخر نشاط"] = summaries["العضو"].map(latest)

    def badge_title(points):
        if points >= 300: return "👑", "العضو القمة", 1
        if points >= 200: return "🌟", "العضو المميز", 2
        if points >= 150: return "🔥", "العضو الفعال", 3
        if points >= 100: return "✨", "العضو النشط", 4
        return "🌱", "العضو المشارك", 5

    summaries[["الشارة","اللقب","المستوى"]] = summaries["النقاط"].apply(lambda p: pd.Series(badge_title(p)))
    return summaries.sort_values("النقاط", ascending=False)

@st.cache_data(ttl=3600)
def get_task_distribution(achievements_df):
    dist = achievements_df["نوع المهمة"].value_counts().reset_index()
    dist.columns = ["نوع المهمة", "العدد"]
    return dist

@st.cache_data(ttl=3600)
def get_program_performance(achievements_df):
    perf = achievements_df.groupby("البرنامج").agg({"النقاط":"sum","الوصف":"count"}).rename(columns={"الوصف":"عدد المهام"}).reset_index()
    perf["متوسط النقاط للمهمة"] = perf["النقاط"] / perf["عدد المهام"]
    return perf

@st.cache_data(ttl=3600)
def get_monthly_activity(achievements_df):
    df = achievements_df.copy()
    df["تاريخ_dt"] = pd.to_datetime(df["التاريخ"])
    df["الشهر-السنة"] = df["تاريخ_dt"].dt.strftime("%Y-%m")
    ma = df.groupby("الشهر-السنة").agg({"النقاط":"sum","الوصف":"count"}).rename(columns={"الوصف":"عدد المهام"}).reset_index()
    ma["تاريخ_للترتيب"] = pd.to_datetime(ma["الشهر-السنة"] + "-01")
    return ma.sort_values("تاريخ_للترتيب")

def evaluate_task_automatically(task_name, task_description):
    length_score = min(5, max(1, len(task_description)//20))
    keywords = ["دولي","محكم","نشر","تطوير","ابتكار","مبادرة","تخطيط"]
    keyword_score = sum(1 for k in keywords if k in task_description)/2
    init = {
        "نشر بحث في مجلة محكمة":4.5, "نشر بحث في مؤتمر":4.0, "تأليف كتاب":5.0,
        "تقديم محاضرة عامة":3.5, "تقديم ورشة عمل":3.8, "المشاركة في لجنة علمية":3.0,
        "الإشراف على رسالة علمية":4.2, "تطوير مقرر دراسي":4.0,
        "مبادرة خدمة مجتمعية":4.3, "حضور دورة تدريبية":3.0
    }.get(task_name, 3.5)
    final = (init*0.6)+(length_score*0.2)+(keyword_score*0.2)
    return round(min(5,max(1,final))*2)/2

def calculate_points_from_rating(task_name, rating, tasks_df):
    row = tasks_df[tasks_df["اسم المهمة"]==task_name]
    if not row.empty:
        mn, mx = row.iloc[0]["نطاق النقاط"]
    else:
        mn, mx = (10,30)
    perc = (rating-1)/4
    return round(mn + perc*(mx-mn))

# ---- الترويسة ----
st.title("🏆 نظام إدارة إنجاز المهام")
st.write("لوحة تحفيزية لإنجازات أعضاء هيئة التدريس وتتبع المهام الأكاديمية")

# ---- التحضير الأولي ----
achievements_df = generate_achievements_data()
faculty_summaries = calculate_faculty_achievements(achievements_df)
tasks_df = get_available_tasks()
task_distribution = get_task_distribution(achievements_df)
program_performance = get_program_performance(achievements_df)
monthly_activity = get_monthly_activity(achievements_df)

# تحويل القيمة إلى int لحل مشكلة التسلسل إلى JSON
max_points = int(faculty_summaries["النقاط"].max())

# ---- الشريط الجانبي (عناصر التحكم) ----
with st.sidebar:
    st.header("تصفية البيانات")
    academic_years = ["2024-2025", "2023-2024"]
    selected_year = st.selectbox("العام الدراسي:", academic_years)
    programs = ["الكل"] + list(load_faculty_data()["البرنامج"].unique())
    selected_program = st.selectbox("البرنامج:", programs)
    task_types = ["الكل"] + list(achievements_df["نوع المهمة"].unique())
    selected_task_type = st.selectbox("نوع المهام:", task_types)
    st.divider()
    st.header("الإجراءات")
    if st.button("📝 تسجيل مهمة جديدة", use_container_width=True):
        st.session_state["active_tab"] = 2
    if st.button("⚙️ إدارة المهام المتاحة", use_container_width=True):
        st.session_state["active_tab"] = 3
    st.divider()
    st.caption("تم تسجيل الدخول كـ: د. محمد أحمد")
    st.caption("الصلاحية: عضو هيئة تدريس")

# ---- تطبيق التصفية ----
filtered_achievements = achievements_df.copy()
if selected_program != "الكل":
    filtered_achievements = filtered_achievements[filtered_achievements["البرنامج"] == selected_program]
    faculty_summaries = faculty_summaries[faculty_summaries["البرنامج"] == selected_program]
if selected_task_type != "الكل":
    filtered_achievements = filtered_achievements[filtered_achievements["نوع المهمة"] == selected_task_type]

# ---- التبويبات الرئيسية ----
active_tab = st.session_state.get("active_tab", 0)
tabs = st.tabs(["🥇 لوحة الإنجازات","🎖️ لوحة الشرف","📝 تسجيل المهام","⚙️ إدارة المهام"])

with tabs[0]:
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.subheader("🏆 الترتيب العام")
        st.dataframe(
            faculty_summaries[["العضو","الشارة","النقاط","عدد المهام","متوسط التقييم"]],
            hide_index=True,
            use_container_width=True,
            column_config={
                "العضو": st.column_config.TextColumn("العضو"),
                "الشارة": st.column_config.TextColumn(""),
                "النقاط": st.column_config.ProgressColumn(
                    "النقاط",
                    min_value=0,
                    max_value=max_points,
                    format="%d"
                ),
                "عدد المهام": st.column_config.NumberColumn("المهام"),
                "متوسط التقييم": st.column_config.NumberColumn("التقييم", format="%.1f ⭐")
            }
        )
    with col2:
        st.subheader("📊 إحصائيات الإنجازات")
        chart_tabs = st.tabs(["الأعضاء","أنواع المهام","النشاط الشهري"])
        with chart_tabs[0]:
            top10 = faculty_summaries.head(10)
            fig = px.bar(top10, x="العضو", y="النقاط", color="البرنامج",
                         title="أفضل 10 أعضاء حسب النقاط", text="النقاط",
                         hover_data=["عدد المهام","متوسط التقييم"])
            fig.update_layout(xaxis_title="العضو", yaxis_title="النقاط")
            st.plotly_chart(fig, use_container_width=True)
        with chart_tabs[1]:
            fig = px.pie(task_distribution, values="العدد", names="نوع المهمة",
                         title="توزيع المهام حسب النوع", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        with chart_tabs[2]:
            fig = px.line(monthly_activity, x="الشهر-السنة",
                          y=["النقاط","عدد المهام"],
                          title="النشاط الشهري على مدار العام",
                          labels={"الشهر-السنة":"الشهر","value":"القيمة","variable":"المؤشر"},
                          markers=True)
            fig.update_layout(xaxis_title="الشهر", yaxis_title="القيمة")
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("📈 أداء البرامج")
        pf = px.bar(program_performance, x="البرنامج", y="النقاط",
                    color="عدد المهام", title="إجمالي النقاط حسب البرنامج",
                    text="النقاط", hover_data=["متوسط النقاط للمهمة"])
        pf.update_layout(xaxis_title="البرنامج", yaxis_title="إجمالي النقاط")
        st.plotly_chart(pf, use_container_width=True)
    with col3:
        st.subheader("🔔 آخر الإنجازات")
        latest = filtered_achievements.head(8)
        for _, ach in latest.iterrows():
            date_obj = datetime.strptime(ach["التاريخ"], "%Y-%m-%d")
            friendly = date_obj.strftime("%d %b %Y")
            st.markdown(f"""
            <div class="achievement-card">
                <h4>{ach["العضو"]}</h4>
                <p><strong>{ach["نوع المهمة"]}</strong> ({ach["النقاط"]} نقطة)</p>
                <p>{ach["الوصف"]}</p>
                <p><small>{friendly} | ⭐ {ach["التقييم"]}</small></p>
            </div>
            """, unsafe_allow_html=True)

# ---- تبويب 2: لوحة الشرف ----
with tabs[1]:
    st.header("🎖️ لوحة الشرف")
    # ... بقية التبويب كما في الأصل ...

# ---- تبويب 3: تسجيل المهام ----
with tabs[2]:
    st.header("📝 تسجيل مهمة جديدة")
    # ... بقية التبويب كما في الأصل ...

# ---- تبويب 4: إدارة المهام المتاحة ----
with tabs[3]:
    st.header("⚙️ إدارة المهام المتاحة")
    # ... بقية التبويب كما في الأصل ...
