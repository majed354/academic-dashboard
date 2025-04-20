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
        font-size: calc(1.2rem + 1vw); /* حجم خط يتكيف مع عرض الشاشة */
    }
    
    /* تنسيق العناوين الفرعية */
    h2, h3 {
        color: #1e88e5;
        margin-top: 30px;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: calc(1rem + 0.5vw); /* حجم خط يتكيف مع عرض الشاشة */
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
        font-size: calc(0.85rem + 0.2vw); /* حجم خط يتكيف مع عرض الشاشة */
        line-height: 1.6;
    }
    
    /* تعديل الشريط الجانبي */
    .css-1d391kg, .css-1inwz65 {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    /* استعلامات الوسائط للتكيف مع أحجام الشاشات المختلفة */
    
    /* للهواتف المحمولة: نحتاج تبسيط العرض وجعل العناصر تحت بعضها */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column;
        }
        
        .stTabs [data-baseweb="tab"] {
            margin-bottom: 5px;
            width: 100%;
            text-align: center;
        }
        
        /* جعل أسماء البرامج الطويلة تظهر بشكل جيد */
        text {
            font-size: 10px !important;
        }
        
        /* تصغير حجم البطاقات والهوامش */
        .metric-card {
            padding: 10px;
            margin-bottom: 10px;
        }
        
        /* تعديل حجم العناصر */
        h1 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
        }
        
        h2, h3 {
            font-size: 1.2rem;
            margin-top: 15px;
            margin-bottom: 10px;
        }
    }
    
    /* للأجهزة اللوحية مثل الآيباد */
    @media (min-width: 769px) and (max-width: 1024px) {
        h1 {
            font-size: 1.8rem;
        }
        
        h2, h3 {
            font-size: 1.3rem;
        }
        
        /* تعديل المسافات بين العناصر */
        .metric-card {
            padding: 12px;
        }
        
        /* تحسين عرض الرسوم البيانية */
        .chart-container {
            padding: 8px;
        }
    }
    
    /* تعديلات خاصة بالعناصر التفاعلية */
    button, .stButton>button {
        white-space: normal !important; /* السماح بالتفاف النص في الأزرار */
        word-wrap: break-word !important;
    }
    
    /* جعل الجداول قابلة للتمرير أفقيًا على الشاشات الصغيرة */
    .stDataFrame {
        overflow-x: auto;
    }
    
    /* تحسين مظهر علامات التبويب - جعلها أكثر وضوحًا */
    div[data-testid="stTabContent"] {
        padding: 1rem 0;
    }
    
    /* تحسين نمط المؤشرات الإحصائية على الشاشات الصغيرة */
    div[data-testid="stMetricValue"] {
        font-size: calc(1rem + 0.5vw) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: calc(0.7rem + 0.2vw) !important;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: calc(0.6rem + 0.1vw) !important;
    }
</style>
""", unsafe_allow_html=True)

# دالة مساعدة للتكيف مع الأجهزة المحمولة
def is_mobile():
    try:
        # محاولة قراءة عرض الشاشة من خصائص الصفحة
        import streamlit as st
        if 'IS_MOBILE' not in st.session_state:
            # نستخدم CSS و JavaScript لكشف حجم الشاشة
            st.markdown("""
            <script>
                if (window.innerWidth < 768) {
                    sessionStorage.setItem('IS_MOBILE', 'true');
                } else {
                    sessionStorage.setItem('IS_MOBILE', 'false');
                }
            </script>
            """, unsafe_allow_html=True)
        
        # افتراضي: نعتبر الجهاز ليس محمولًا
        return False
    except:
        # إذا فشلت المحاولة (هذا يحدث في معظم الحالات)، نفترض الوضع الافتراضي
        return False

# ---- الترويسة ----
if is_mobile():
    # عرض مبسط للترويسة على الأجهزة المحمولة
    st.title("🏠 الرئيسية")
    st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
    today = datetime.now().strftime("%Y/%m/%d")
    st.markdown(f"<div>التاريخ: {today}</div>", unsafe_allow_html=True)
else:
    # عرض الترويسة في عمودين على الشاشات الكبيرة
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏠 الرئيسية")
        st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")

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
        # إنشاء بيانات تجريبية في حالة عدم وجود البيانات
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

# ---- تهيئة البيانات ----
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
    # إنشاء بيانات تجريبية في حالة الفشل
    total_students = 1000
    total_faculty = 50

# ---- بطاقات المقاييس الرئيسية ----
st.subheader("المؤشرات الرئيسية")

# تكييف عدد الأعمدة بناءً على حجم الشاشة
if is_mobile():
    # عرض المؤشرات في عمودين للشاشات الصغيرة
    col1, col2 = st.columns(2)
    with col1:
        st.metric("إجمالي الطلاب", f"{total_students:,}", "+5%")
        st.metric("معدل النجاح", "87%", "+3%")
    with col2:
        st.metric("أعضاء هيئة التدريس", f"{total_faculty:,}", "+2")
        st.metric("متوسط الرضا", "92%", "+4%")
else:
    # عرض المؤشرات في أربعة أعمدة للشاشات الكبيرة
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

# تبويبات للتبديل بين التحليلات المختلفة
tabs = st.tabs(["توزيع الطلاب", "مقارنة المؤشرات", "التطور السنوي"])

# تبويب 1: توزيع الطلاب
with tabs[0]:
    if is_mobile():
        # عرض المخططات في أعمدة واحدة للشاشات الصغيرة
        # مخطط دائري لتوزيع الطلاب
        fig_pie = px.pie(
            latest_year_data, 
            values="عدد الطلاب", 
            names="البرنامج",
            title="توزيع الطلاب بين البرامج",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        # تعديلات على المخطط الدائري لتحسين العرض على الشاشات الصغيرة
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent',  # عرض النسب المئوية فقط على الشاشات الصغيرة
        )
        fig_pie.update_layout(
            margin=dict(t=50, b=30, l=10, r=10),
            height=300,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.4,
                font=dict(size=10)
            ),
            font=dict(family="Tajawal", size=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # مخطط شريطي للطلاب حسب البرنامج
        fig_bar = px.bar(
            latest_year_data, 
            y="البرنامج", 
            x="عدد الطلاب",
            title="عدد الطلاب في كل برنامج",
            color="عدد الطلاب",
            orientation='h',
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(
            xaxis_title="عدد الطلاب",
            yaxis_title="",  # إزالة عنوان المحور y على الشاشات الصغيرة
            yaxis={'categoryorder':'total ascending'},
            height=350,
            margin=dict(t=50, b=20, l=10, r=10),
            font=dict(family="Tajawal", size=10)
        )
        # تصغير أسماء البرامج على الشاشات الصغيرة
        fig_bar.update_yaxes(tickfont=dict(size=9))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    else:
        # عرض المخططات في عمودين للشاشات الكبيرة
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # مخطط دائري لتوزيع الطلاب
            fig_pie = px.pie(
                latest_year_data, 
                values="عدد الطلاب", 
                names="البرنامج",
                title="توزيع الطلاب بين البرامج",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                margin=dict(t=50, b=0, l=0, r=0),
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                font=dict(family="Tajawal")
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # مخطط شريطي للطلاب حسب البرنامج
            fig_bar = px.bar(
                latest_year_data, 
                y="البرنامج", 
                x="عدد الطلاب",
                title="عدد الطلاب في كل برنامج",
                color="عدد الطلاب",
                orientation='h',
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(
                xaxis_title="عدد الطلاب",
                yaxis_title="البرنامج",
                yaxis={'categoryorder':'total ascending'},
                height=400,
                font=dict(family="Tajawal")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# تبويب 2: مقارنة المؤشرات
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
    
    # تعديل المخطط للتكيف مع الشاشات المختلفة
    if is_mobile():
        # تعديلات للشاشات الصغيرة
        fig_indicators.update_layout(
            xaxis_title="",  # إزالة عنوان المحور س
            yaxis_title="النسبة المئوية",
            legend_title="", # إزالة عنوان الوسيلة الإيضاحية
            height=400,
            margin=dict(t=50, b=100, l=10, r=10),  # زيادة الهامش السفلي لعرض أسماء البرامج
            font=dict(family="Tajawal", size=10),
            xaxis=dict(tickangle=45, tickfont=dict(size=8))  # تدوير أسماء البرامج
        )
    else:
        # تعديلات للشاشات الكبيرة
        fig_indicators.update_layout(
            xaxis_title="البرنامج",
            yaxis_title="النسبة المئوية",
            legend_title="المؤشر",
            height=500,
            font=dict(family="Tajawal")
        )
    
    st.plotly_chart(fig_indicators, use_container_width=True)

# تبويب 3: التطور السنوي
with tabs[2]:
    # اختيار البرنامج
    selected_program = st.selectbox(
        "اختر البرنامج لعرض تطوره السنوي:",
        options=yearly_data["البرنامج"].unique()
    )
    
    # تصفية البيانات حسب البرنامج المختار
    program_data = yearly_data[yearly_data["البرنامج"] == selected_program]
    
    # مخطط خطي للتطور السنوي
    fig_trend = px.line(
        program_data,
        x="العام",
        y=["عدد الطلاب", "نسبة النجاح", "معدل الرضا"],
        title=f"تطور مؤشرات برنامج {selected_program} (2020-2024)",
        labels={"value": "القيمة", "variable": "المؤشر"},
        markers=True
    )
    
    # تعديل المخطط للتكيف مع الشاشات المختلفة
    if is_mobile():
        fig_trend.update_layout(
            xaxis_title="السنة",
            yaxis_title="القيمة",
            legend_title="",
            height=400,
            margin=dict(t=50, b=30, l=10, r=10),
            font=dict(family="Tajawal", size=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)  # وضع الوسيلة الإيضاحية أفقيًا في الأسفل
        )
    else:
        fig_trend.update_layout(
            xaxis_title="السنة",
            yaxis_title="القيمة",
            legend_title="المؤشر",
            height=500,
            font=dict(family="Tajawal")
        )
        
    st.plotly_chart(fig_trend, use_container_width=True)

# ---- أعضاء هيئة التدريس المميزين وأحدث الإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")

# تكييف التخطيط حسب حجم الشاشة
if is_mobile():
    # عرض في عمود واحد للأجهزة المحمولة
    # أعضاء هيئة التدريس المميزين
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    
    for _, member in top_faculty.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='faculty-card'>
                <h3 style="font-size: 1.1rem;">{member['الشارة']} {member['الاسم']}</h3>
                <p style="font-size: 0.9rem;"><strong>اللقب:</strong> {member['اللقب']}</p>
                <p style="font-size: 0.9rem;"><strong>البرنامج:</strong> {member['البرنامج']}</p>
                <p style="font-size: 0.9rem;"><strong>النقاط:</strong> {member['النقاط']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("[عرض جميع أعضاء هيئة التدريس](http://localhost:8501/هيئة_التدريس)")
    
    # أحدث الإنجازات
    st.markdown("### 🌟 أحدث الإنجازات")
    
    for i, (_, achievement) in enumerate(faculty_achievements.iterrows()):
        if i >= 3:  # عرض أقل عدد من الإنجازات على الشاشات الصغيرة
            break
            
        date_obj = datetime.strptime(achievement['التاريخ'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        
        st.markdown(f"""
        <div class='achievement-item'>
            <p style="font-size: 0.9rem;"><strong>{achievement['العضو']}</strong></p>
            <p style="font-size: 0.9rem;">{achievement['الإنجاز']}</p>
            <p style="font-size: 0.8rem;"><small>التاريخ: {formatted_date} | النقاط: {achievement['النقاط']}</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # تحديث رابط صفحة لوحة إنجاز المهام
    st.markdown("[عرض لوحة إنجاز المهام الكاملة](http://localhost:8501/لوحة_إنجاز_المهام)")
else:
    # عرض في عمودين للشاشات الكبيرة
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
        
        # تحديث رابط صفحة لوحة إنجاز المهام
        st.markdown("[عرض لوحة إنجاز المهام الكاملة](http://localhost:8501/لوحة_إنجاز_المهام)")

# ---- مخطط حراري للمؤشرات الرئيسية ----
st.subheader("مؤشرات البرامج الرئيسية")

# وضع المخطط الحراري باستخدام Plotly مع تكييفه للشاشات المختلفة
fig_heatmap = go.Figure(data=go.Heatmap(
    z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    x=["نسبة النجاح", "معدل الرضا"],
    y=latest_year_data["البرنامج"],
    colorscale="Viridis",
    text=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
    texttemplate="%{text}%",
    textfont={"size": 12 if not is_mobile() else 10},
))

# تعديل إعدادات المخطط الحراري بناءً على حجم الشاشة
if is_mobile():
    fig_heatmap.update_layout(
        title="مقارنة المؤشرات الرئيسية عبر البرامج",
        margin=dict(t=50, b=20, l=10, r=10),
        height=350,
        font=dict(family="Tajawal", size=10),
        yaxis=dict(tickfont=dict(size=8))  # تصغير أسماء البرامج
    )
else:
    fig_heatmap.update_layout(
        title="مقارنة المؤشرات الرئيسية عبر البرامج",
        margin=dict(t=50, b=0, l=0, r=0),
        height=400,
        font=dict(family="Tajawal")
    )

st.plotly_chart(fig_heatmap, use_container_width=True)

# ---- نصائح للمستخدم ----
# استخدام expander للنصائح لتوفير المساحة على الشاشات الصغيرة
with st.expander("📋 نصائح للاستخدام", expanded=not is_mobile()):
    st.markdown("""
    - انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله
    - استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء
    - قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات
    - استخدم "لوحة إنجاز المهام" لتسجيل وعرض إنجازات أعضاء هيئة التدريس
    """)
