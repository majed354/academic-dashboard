import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime

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
    
    /* تنسيق العنوان الرئيسي */
    h1 {
        color: #1e88e5;
        padding-bottom: 15px;
        border-bottom: 2px solid #1e88e5;
        margin-bottom: 30px;
    }
    
    /* تنسيق العناوين الفرعية */
    h2, h3 {
        color: #1e88e5;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* تنسيق البطاقات */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* تنسيق الرسم البياني */
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
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
</style>
""", unsafe_allow_html=True)

# ---- الترويسة ----
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
    st.markdown("### قسم القراءات")

with col2:
    # عرض التاريخ الحالي
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
        # إنشاء بيانات تجريبية في حالة عدم وجود البيانات - تم تعديلها لإضافة الطلاب والطالبات بشكل منفصل
        data = {
            "البرنامج": [
                "بكالوريوس في القرآن وعلومه",
                "بكالوريوس القراءات",
                "ماجستير الدراسات القرآنية المعاصرة",
                "ماجستير القراءات",
                "دكتوراه علوم القرآن",
                "دكتوراه القراءات"
            ],
            "عدد الطلاب": [125, 110, 90, 120, 70, 85],  # أعداد الطلاب الذكور
            "عدد الطالبات": [85, 70, 60, 80, 50, 55],   # أعداد الطالبات
            "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6]
        }
        return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_yearly_data():
    """تحميل بيانات السنوات من 2020 إلى 2024 (للعرض التوضيحي)"""
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
            # هنا نضيف بيانات عشوائية في حالة عدم وجود بيانات حقيقية
            # في التطبيق الحقيقي، استبدل هذا بجلب البيانات من GitHub
            import hashlib
            program_hash = int(hashlib.md5(program.encode()).hexdigest(), 16) % 100
            
            # تقسيم مختلف للطلاب والطالبات
            male_students = 60 + (year - 2020) * 5 + program_hash % 50
            female_students = 40 + (year - 2020) * 5 + (program_hash // 2) % 40
            total_students = male_students + female_students
            
            data.append({
                "العام": year,
                "البرنامج": program,
                "عدد الطلاب": male_students,
                "عدد الطالبات": female_students,
                "المجموع": total_students,
                "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + program_hash % 10),
                "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + (program_hash // 2) % 10)
            })
            
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_faculty_achievements():
    """تحميل أحدث إنجازات أعضاء هيئة التدريس"""
    # نموذج بسيط للإنجازات
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
    """تحميل أفضل أعضاء هيئة التدريس"""
    # نموذج بسيط لأفضل الأعضاء
    top_faculty = [
        {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"},
        {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"},
        {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"}
    ]
    return pd.DataFrame(top_faculty)

# محاولة تحميل البيانات
try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_female_students = dept_data["عدد الطالبات"].sum()
    total_faculty = dept_data["أعضاء هيئة التدريس"].sum()
    yearly_data = load_yearly_data()
    latest_year_data = yearly_data[yearly_data["العام"] == 2024]
    faculty_achievements = load_faculty_achievements()
    top_faculty = load_top_faculty()
except Exception as e:
    st.error(f"خطأ في تحميل البيانات: {e}")
    st.warning("سيتم استخدام بيانات تجريبية لأغراض العرض.")
    # إنشاء بيانات تجريبية في حالة الفشل
    total_students = 600
    total_female_students = 400
    total_faculty = 50

# ---- بطاقات المقاييس الرئيسية ----
st.subheader("المؤشرات الرئيسية")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("عدد الطلاب", f"{total_students:,}", "+3% منذ العام الماضي")
    
with c2:
    st.metric("عدد الطالبات", f"{total_female_students:,}", "+7% منذ العام الماضي")
    
with c3:
    st.metric("معدل النجاح الإجمالي", "87%", "+3% منذ العام الماضي")
    
with c4:
    st.metric("متوسط رضا الطلاب", "92%", "+4% منذ العام الماضي")

# ---- الرسومات البيانية ----
st.subheader("تحليل البرامج الأكاديمية")

# تبويبات للتبديل بين التحليلات المختلفة
tabs = st.tabs(["توزيع الطلاب والطالبات", "مقارنة البرامج", "التطور السنوي"])

# تبويب 1: توزيع الطلاب والطالبات
with tabs[0]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # مخطط دائري لتوزيع إجمالي الطلاب والطالبات
        pie_data = pd.DataFrame({
            "الفئة": ["الطلاب", "الطالبات"],
            "العدد": [total_students, total_female_students]
        })
        
        fig_pie = px.pie(
            pie_data, 
            values="العدد", 
            names="الفئة",
            title="توزيع الطلاب والطالبات في جميع البرامج",
            color_discrete_sequence=["#1e88e5", "#E91E63"]  # أزرق للطلاب، وردي للطالبات
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            margin=dict(t=50, b=0, l=0, r=0),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # مخطط شريطي للطلاب والطالبات حسب البرنامج
        fig_bar = px.bar(
            latest_year_data, 
            y="البرنامج", 
            x=["عدد الطلاب", "عدد الطالبات"],
            title="توزيع الطلاب والطالبات حسب البرنامج",
            orientation='h',
            color_discrete_sequence=["#1e88e5", "#E91E63"],  # أزرق للطلاب، وردي للطالبات
            barmode="stack"
        )
        fig_bar.update_layout(
            xaxis_title="عدد الطلاب والطالبات",
            yaxis_title="البرنامج",
            yaxis={'categoryorder':'total ascending'},
            legend_title="الفئة",
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# تبويب 2: مقارنة البرامج
with tabs[1]:
    # مخطط بياني مقارن للمؤشرات بين البرامج
    fig_indicators = px.bar(
        latest_year_data,
        x="البرنامج",
        y=["نسبة النجاح", "معدل الرضا"],
        barmode="group",
        title="مقارنة المؤشرات بين البرامج",
        labels={"value": "النسبة المئوية", "variable": "المؤشر"},
        color_discrete_sequence=["#1e88e5", "#27AE60"]
    )
    fig_indicators.update_layout(
        xaxis_title="البرنامج",
        yaxis_title="النسبة المئوية",
        legend_title="المؤشر",
        height=500
    )
    st.plotly_chart(fig_indicators, use_container_width=True)

    # إضافة مخطط جديد لنسبة الطالبات إلى الطلاب
    latest_year_data["نسبة الطالبات للطلاب"] = (latest_year_data["عدد الطالبات"] / latest_year_data["عدد الطلاب"] * 100).round(1)
    
    fig_gender_ratio = px.bar(
        latest_year_data,
        x="البرنامج",
        y="نسبة الطالبات للطلاب",
        title="نسبة الطالبات إلى الطلاب في كل برنامج (%)",
        color="نسبة الطالبات للطلاب",
        color_continuous_scale="RdBu",
        text_auto='.1f'
    )
    fig_gender_ratio.update_layout(
        xaxis_title="البرنامج",
        yaxis_title="النسبة المئوية (%)",
        height=400
    )
    st.plotly_chart(fig_gender_ratio, use_container_width=True)

# تبويب 3: التطور السنوي
with tabs[2]:
    # اختيار البرنامج
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_program = st.selectbox(
            "اختر البرنامج لعرض تطوره السنوي:",
            options=yearly_data["البرنامج"].unique()
        )
    
    with col2:
        gender_option = st.radio(
            "اختر الفئة:",
            ["الكل", "الطلاب", "الطالبات"],
            horizontal=True
        )
    
    # تصفية البيانات حسب البرنامج المختار
    program_data = yearly_data[yearly_data["البرنامج"] == selected_program]
    
    # مخطط خطي للتطور السنوي للطلاب والطالبات
    if gender_option == "الكل":
        fig_students = px.line(
            program_data,
            x="العام",
            y=["عدد الطلاب", "عدد الطالبات", "المجموع"],
            title=f"تطور أعداد الطلاب والطالبات في برنامج {selected_program} (2020-2024)",
            labels={"value": "العدد", "variable": "الفئة"},
            markers=True,
            color_discrete_sequence=["#1e88e5", "#E91E63", "#27AE60"]
        )
    elif gender_option == "الطلاب":
        fig_students = px.line(
            program_data,
            x="العام",
            y=["عدد الطلاب"],
            title=f"تطور أعداد الطلاب في برنامج {selected_program} (2020-2024)",
            labels={"value": "العدد", "variable": "الفئة"},
            markers=True,
            color_discrete_sequence=["#1e88e5"]
        )
    else:  # الطالبات
        fig_students = px.line(
            program_data,
            x="العام",
            y=["عدد الطالبات"],
            title=f"تطور أعداد الطالبات في برنامج {selected_program} (2020-2024)",
            labels={"value": "العدد", "variable": "الفئة"},
            markers=True,
            color_discrete_sequence=["#E91E63"]
        )
        
    fig_students.update_layout(
        xaxis_title="السنة",
        yaxis_title="العدد",
        legend_title="الفئة",
        height=400
    )
    st.plotly_chart(fig_students, use_container_width=True)
    
    # مخطط خطي للتطور السنوي للمؤشرات الأخرى
    fig_indicators = px.line(
        program_data,
        x="العام",
        y=["نسبة النجاح", "معدل الرضا"],
        title=f"تطور المؤشرات في برنامج {selected_program} (2020-2024)",
        labels={"value": "النسبة المئوية", "variable": "المؤشر"},
        markers=True,
        color_discrete_sequence=["#1e88e5", "#27AE60"]
    )
    fig_indicators.update_layout(
        xaxis_title="السنة",
        yaxis_title="النسبة المئوية",
        legend_title="المؤشر",
        height=400
    )
    st.plotly_chart(fig_indicators, use_container_width=True)

# ---- أعضاء هيئة التدريس المميزين وأحدث الإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")

col1, col2 = st.columns([1, 1])

# أعضاء هيئة التدريس المميزين
with col1:
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    
    for _, member in top_faculty.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='faculty-card'>
                <h3>{member['الشارة']} {member['الاسم']}</h3>
                <p><strong>اللقب:</strong> {member['اللقب']}</p>
                <p><strong>البرنامج:</strong> {member['البرنامج']}</p>
                <p><strong>النقاط:</strong> {member['النقاط']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("[عرض جميع أعضاء هيئة التدريس](http://localhost:8501/هيئة_التدريس)")
    st.markdown("[عرض لوحة الإنجازات الكاملة](http://localhost:8501/إنجازات_الأعضاء)")

# أحدث الإنجازات
with col2:
    st.markdown("### 🌟 أحدث الإنجازات")
    
    for _, achievement in faculty_achievements.iterrows():
        date_obj = datetime.strptime(achievement['التاريخ'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        
        st.markdown(f"""
        <div class='achievement-item'>
            <p><strong>{achievement['العضو']}</strong> ({achievement['البرنامج']})</p>
            <p>{achievement['الإنجاز']}</p>
            <p><small>التاريخ: {formatted_date} | النقاط: {achievement['النقاط']}</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("[عرض جميع الإنجازات](http://localhost:8501/إنجازات_الأعضاء)")

# ---- مخطط حراري للمؤشرات الرئيسية ----
st.subheader("مؤشرات البرامج الرئيسية")

# وضع المخطط الحراري باستخدام Plotly بطريقة مباشرة دون استخدام pivot
fig_heatmap = go.Figure(data=go.Heatmap(
    z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    x=["نسبة النجاح", "معدل الرضا"],
    y=latest_year_data["البرنامج"],
    colorscale="Viridis",
    text=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    texttemplate="%{text}%",
    textfont={"size":12},
))

fig_heatmap.update_layout(
    title="مقارنة المؤشرات الرئيسية عبر البرامج",
    margin=dict(t=50, b=0, l=0, r=0),
    height=400,
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ---- نصائح للمستخدم ----
st.info("""
**نصائح للاستخدام:**
- انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله
- استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء
- قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات
- استخدم "لوحة إنجازات الأعضاء" لتسجيل وعرض إنجازات أعضاء هيئة التدريس
""")
