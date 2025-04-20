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

# ضبط viewport للشاشات المتجاوبة
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

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
        overflow: hidden;
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
    
    /* منع تكبير المخططات */
    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }
    
    /* جعل الجداول قابلة للتمرير أفقيًا على الشاشات الصغيرة */
    .stDataFrame {
        overflow-x: auto;
    }
    
    /* تحسين نمط المؤشرات الإحصائية */
    div[data-testid="stMetricValue"] {
        font-size: calc(1rem + 0.5vw) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: calc(0.7rem + 0.2vw) !important;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: calc(0.6rem + 0.1vw) !important;
    }
    
    /* استعلامات الوسائط للتكيف مع أحجام الشاشات المختلفة */
    
    /* للهواتف المحمولة: نحتاج تبسيط العرض */
    @media only screen and (max-width: 768px) {
        /* تعديل الشريط الجانبي على الشاشات الصغيرة */
        section[data-testid="stSidebar"] {
            width: 18rem !important;
            min-width: 18rem !important;
            max-width: 18rem !important;
            position: fixed !important;
            right: 0;
            top: 0;
            bottom: 0;
            transform: translateX(100%);
            transition: transform 300ms ease;
            z-index: 1000;
            box-shadow: -4px 0 15px rgba(0,0,0,0.2);
        }
        
        section[data-testid="stSidebar"].show-sidebar {
            transform: translateX(0) !important;
        }
        
        /* تعديل حاوية المحتوى الرئيسي */
        .main .block-container {
            padding-right: 1rem !important;
            padding-left: 1rem !important;
        }
        
        /* إضافة طبقة لإظلام الخلفية عند فتح الشريط الجانبي */
        #sidebar-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
        
        /* تنسيق زر القائمة */
        .sidebar-trigger {
            position: fixed;
            top: 0.8rem;
            right: 0.8rem;
            width: 35px;
            height: 35px;
            background-color: #1e88e5;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 998;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* جعل التبويبات تتجاوب بشكل أفضل */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 5px 10px;
            white-space: normal;
            text-align: center;
            font-size: 0.8rem;
        }
        
        /* جعل أسماء البرامج الطويلة تظهر بشكل جيد */
        text {
            font-size: 9px !important;
        }
        
        /* تصغير حجم البطاقات والهوامش */
        .metric-card {
            padding: 8px;
            margin-bottom: 8px;
        }
        
        /* تعديل حجم العناصر */
        h1 {
            font-size: 1.3rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
        }
        
        h2 {
            font-size: 1.1rem;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        
        h3 {
            font-size: 1rem;
            margin-top: 12px;
            margin-bottom: 8px;
        }
        
        /* تعديلات للمخططات */
        .stPlotlyChart, .js-plotly-plot {
            margin-bottom: 30px !important;
            overflow-x: hidden !important;
        }
        
        /* تعديل عرض الجداول */
        .stDataFrame > div {
            width: 100% !important;
            padding-right: 0 !important;
            padding-left: 0 !important;
        }
    }
    
    /* للأجهزة اللوحية مثل الآيباد */
    @media only screen and (min-width: 769px) and (max-width: 1024px) {
        h1 {
            font-size: 1.7rem;
        }
        
        h2, h3 {
            font-size: 1.2rem;
        }
        
        /* تعديل الشريط الجانبي للأجهزة اللوحية */
        [data-testid="stSidebar"] {
            width: 16rem !important;
            min-width: 16rem !important;
        }
        
        /* تعديل المسافات بين العناصر */
        .metric-card {
            padding: 10px;
        }
        
        /* تحسين عرض الرسوم البيانية */
        .chart-container {
            padding: 8px;
        }
        
        /* تعديل هوامش الحاوية الرئيسية */
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    }
    
    /* للشاشات الكبيرة */
    @media only screen and (min-width: 1025px) {
        /* تخصيصات إضافية للشاشات الكبيرة */
        .block-container {
            max-width: 1200px;
            padding-left: 5% !important;
            padding-right: 5% !important;
            margin: 0 auto;
        }
    }
</style>

<!-- إضافة طبقة لإظلام الخلفية عند فتح الشريط الجانبي -->
<div id="sidebar-overlay" onclick="toggleSidebar()"></div>

<!-- إضافة زر جديد للشريط الجانبي على الأجهزة المحمولة -->
<div class="sidebar-trigger" onclick="toggleSidebar()">
    <span style="font-size: 1.2rem;">☰</span>
</div>

<script>
    // وظيفة لفتح وإغلاق الشريط الجانبي
    function toggleSidebar() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar.classList.contains('show-sidebar')) {
            // إغلاق الشريط الجانبي
            sidebar.classList.remove('show-sidebar');
            overlay.style.display = 'none';
        } else {
            // فتح الشريط الجانبي
            sidebar.classList.add('show-sidebar');
            overlay.style.display = 'block';
        }
    }
    
    // انتظر تحميل الصفحة بالكامل ثم قم بتهيئة الشريط الجانبي
    window.addEventListener('DOMContentLoaded', (event) => {
        // تهيئة الشريط الجانبي للأجهزة المحمولة
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && window.innerWidth <= 768) {
            // تعيين حدث النقر لإغلاق الشريط الجانبي عند النقر على أي رابط داخله
            sidebar.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', function() {
                    setTimeout(() => toggleSidebar(), 300);
                });
            });
        }
    });
</script>
""", unsafe_allow_html=True)

# دالة مساعدة للتكيف مع الأجهزة المحمولة
def is_mobile():
    try:
        # محاولة قراءة حالة الجهاز المحمول من session_state
        if 'IS_MOBILE' not in st.session_state:
            # نستخدم JavaScript لكشف حجم الشاشة
            st.markdown("""
            <script>
                // تحقق من عرض الشاشة وحفظ النتيجة في sessionStorage
                var width = window.innerWidth;
                if (width < 768) {
                    sessionStorage.setItem('IS_MOBILE', 'true');
                } else {
                    sessionStorage.setItem('IS_MOBILE', 'false');
                }
                
                // عند تغيير حجم الشاشة، تحديث القيمة
                window.addEventListener('resize', function() {
                    var width = window.innerWidth;
                    if (width < 768) {
                        sessionStorage.setItem('IS_MOBILE', 'true');
                    } else {
                        sessionStorage.setItem('IS_MOBILE', 'false');
                    }
                });
            </script>
            """, unsafe_allow_html=True)
            
            # استخدام المعاينة للجهاز ليقرر
            import re
            # محاولة كشف وكيل المستخدم (لن تعمل في Streamlit بشكل معتاد)
            # لذا سنستخدم حجم النافذة كمؤشر بديل
            ua_hint = ""
            mobile_pattern = re.compile(r"(android|avantgo|blackberry|bolt|boost|cricket|docomo|fone|hiptop|mini|mobi|palm|phone|pie|tablet|up\.browser|up\.link|webos|wos)", re.I)
            is_mobile_device = bool(mobile_pattern.search(ua_hint))
            width_hint = 800  # قيمة افتراضية متوسطة
            
            # تحديد الجهاز بناءً على حجم الشاشة المقدر أو وكيل المستخدم
            st.session_state.IS_MOBILE = width_hint < 768 or is_mobile_device
        
        # إرجاع الحالة المخزنة
        return st.session_state.IS_MOBILE
    except:
        # في حالة الفشل، نرجع قيمة تقريبية
        # يمكن تحسينها باستخدام معلومات أخرى مثل نسبة العرض إلى الارتفاع
        import random
        # قيمة عشوائية للعرض (لأغراض العرض فقط)
        demo_width = random.choice([350, 1200])
        return demo_width < 768

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

# دالة مساعدة لتحضير المخططات والرسوم البيانية متوافقة مع الشاشات المختلفة
def prepare_chart_layout(fig, title, is_mobile=False, chart_type="bar"):
    """تطبيق إعدادات موحدة على المخططات وجعلها متوافقة مع الشاشات المختلفة"""
    
    # إيقاف خاصية التكبير والحركة
    fig.update_layout(
        dragmode=False,
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    
    # إعدادات مشتركة
    layout_settings = {
        "title": title,
        "font": {"family": "Tajawal"},
        "plot_bgcolor": "rgba(240, 240, 240, 0.8)",
        "paper_bgcolor": "white",
    }
    
    # إعدادات مخصصة حسب نوع الجهاز
    if is_mobile:
        # إعدادات للشاشات الصغيرة
        mobile_settings = {
            "height": 300 if chart_type != "heatmap" else 350,
            "margin": {"t": 40, "b": 70, "l": 10, "r": 10, "pad": 0},
            "font": {"size": 10},
            "title": {"font": {"size": 13}},
            "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.3, "x": 0.5, "xanchor": "center", "font": {"size": 9}}
        }
        layout_settings.update(mobile_settings)
        
        # تكييف حسب نوع المخطط
        if chart_type == "bar":
            fig.update_traces(textfont_size=8)
            fig.update_xaxes(tickangle=45, tickfont={"size": 8})
        elif chart_type == "pie":
            fig.update_traces(textfont_size=9, textposition="inside", textinfo="percent")
            layout_settings["showlegend"] = False
    else:
        # إعدادات للشاشات المتوسطة والكبيرة
        desktop_settings = {
            "height": 450 if chart_type != "heatmap" else 400,
            "margin": {"t": 50, "b": 50, "l": 30, "r": 30, "pad": 4},
        }
        layout_settings.update(desktop_settings)
    
    # تطبيق الإعدادات
    fig.update_layout(**layout_settings)
    
    return fig

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

# تبويبات للتبديل بين التحليلات المختلفة - تبسيط على الأجهزة المحمولة
if is_mobile():
    tab_labels = ["توزيع", "مقارنة", "تطور"]
else:
    tab_labels = ["توزيع الطلاب", "مقارنة المؤشرات", "التطور السنوي"]

tabs = st.tabs(tab_labels)

# تبويب 1: توزيع الطلاب
with tabs[0]:
    if is_mobile():
        # عرض المخططات في عمود واحد للشاشات الصغيرة
        # مخطط دائري مبسط لتوزيع الطلاب
        # اختصار أسماء البرامج
        mapping = {
            "بكالوريوس في القرآن وعلومه": "بكالوريوس القرآن",
            "بكالوريوس القراءات": "بكالوريوس القراءات",
            "ماجستير الدراسات القرآنية المعاصرة": "ماجستير الدراسات",
            "ماجستير القراءات": "ماجستير القراءات",
            "دكتوراه علوم القرآن": "دكتوراه القرآن",
            "دكتوراه القراءات": "دكتوراه القراءات"
        }
        
        # نسخة من البيانات مع أسماء مختصرة للشاشات الصغيرة
        mobile_data = latest_year_data.copy()
        mobile_data["البرنامج"] = mobile_data["البرنامج"].map(mapping)
        
        # مخطط دائري لتوزيع الطلاب
        fig_pie = px.pie(
            mobile_data, 
            values="عدد الطلاب", 
            names="البرنامج",
            title="توزيع الطلاب بين البرامج",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        # تطبيق إعدادات المخطط المتجاوبة
        fig_pie = prepare_chart_layout(fig_pie, "توزيع الطلاب بين البرامج", is_mobile=True, chart_type="pie")
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        
        # مخطط شريطي للطلاب حسب البرنامج
        fig_bar = px.bar(
            mobile_data, 
            y="البرنامج", 
            x="عدد الطلاب",
            title="عدد الطلاب في كل برنامج",
            color="عدد الطلاب",
            orientation='h',
            color_continuous_scale="Viridis"
        )
        
        # تطبيق إعدادات المخطط المتجاوبة
        fig_bar = prepare_chart_layout(fig_bar, "عدد الطلاب في كل برنامج", is_mobile=True, chart_type="bar")
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        
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
            
            # تطبيق إعدادات المخطط المتجاوبة
            fig_pie = prepare_chart_layout(fig_pie, "توزيع الطلاب بين البرامج", is_mobile=False, chart_type="pie")
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        
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
            
            # تطبيق إعدادات المخطط المتجاوبة
            fig_bar = prepare_chart_layout(fig_bar, "عدد الطلاب في كل برنامج", is_mobile=False, chart_type="bar")
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# تبويب 2: مقارنة المؤشرات
with tabs[1]:
    # للأجهزة المحمولة، نستخدم أسماء مختصرة
    if is_mobile():
        mobile_data = latest_year_data.copy()
        mobile_data["البرنامج"] = mobile_data["البرنامج"].map({
            "بكالوريوس في القرآن وعلومه": "بكالوريوس القرآن",
            "بكالوريوس القراءات": "بكالوريوس القراءات",
            "ماجستير الدراسات القرآنية المعاصرة": "ماجستير الدراسات",
            "ماجستير القراءات": "ماجستير القراءات",
            "دكتوراه علوم القرآن": "دكتوراه القرآن",
            "دكتوراه القراءات": "دكتوراه القراءات"
        })
        
        # مخطط بياني مقارن للمؤشرات بين البرامج
        fig_indicators = px.bar(
            mobile_data,
            x="البرنامج",
            y=["نسبة النجاح", "معدل الرضا"],
            barmode="group",
            title="مقارنة المؤشرات",
            labels={"value": "النسبة المئوية", "variable": "المؤشر"},
            color_discrete_sequence=["#1e88e5", "#27AE60"]
        )
        
        # تطبيق إعدادات المخطط المتجاوبة
        fig_indicators = prepare_chart_layout(fig_indicators, "مقارنة المؤشرات", is_mobile=True, chart_type="bar")
        st.plotly_chart(fig_indicators, use_container_width=True, config={"displayModeBar": False})
    else:
        # مخطط بياني مقارن للمؤشرات بين البرامج للشاشات الكبيرة
        fig_indicators = px.bar(
            latest_year_data,
            x="البرنامج",
            y=["نسبة النجاح", "معدل الرضا"],
            barmode="group",
            title="مقارنة المؤشرات بين البرامج",
            labels={"value": "النسبة المئوية", "variable": "المؤشر"},
            color_discrete_sequence=["#1e88e5", "#27AE60"]
        )
        
        # تطبيق إعدادات المخطط المتجاوبة
        fig_indicators = prepare_chart_layout(fig_indicators, "مقارنة المؤشرات بين البرامج", is_mobile=False, chart_type="bar")
        st.plotly_chart(fig_indicators, use_container_width=True, config={"displayModeBar": False})

# تبويب 3: التطور السنوي
with tabs[2]:
    # اختيار البرنامج
    # تحديد قائمة الخيارات حسب حجم الشاشة
    if is_mobile():
        program_options = {
            "بكالوريوس في القرآن وعلومه": "بكالوريوس القرآن",
            "بكالوريوس القراءات": "بكالوريوس القراءات",
            "ماجستير الدراسات القرآنية المعاصرة": "ماجستير الدراسات",
            "ماجستير القراءات": "ماجستير القراءات",
            "دكتوراه علوم القرآن": "دكتوراه القرآن",
            "دكتوراه القراءات": "دكتوراه القراءات"
        }
        display_options = list(program_options.values())
        options = list(program_options.keys())
        # القيمة الافتراضية للاختيار
        default_idx = 0 if "selected_program_idx" not in st.session_state else st.session_state.selected_program_idx
        selected_display = st.selectbox(
            "اختر البرنامج:",
            options=display_options,
            index=default_idx
        )
        # تحويل الاسم المختصر إلى الاسم الكامل
        reverse_mapping = {v: k for k, v in program_options.items()}
        selected_program = reverse_mapping[selected_display]
        # حفظ الاختيار
        st.session_state.selected_program_idx = display_options.index(selected_display)
    else:
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
        title=f"تطور مؤشرات البرنامج (2020-2024)" if is_mobile() else f"تطور مؤشرات برنامج {selected_program} (2020-2024)",
        labels={"value": "القيمة", "variable": "المؤشر"},
        markers=True
    )
    
    # تطبيق إعدادات المخطط المتجاوبة
    fig_trend = prepare_chart_layout(fig_trend, 
                                     f"تطور المؤشرات" if is_mobile() else f"تطور مؤشرات البرنامج", 
                                     is_mobile=is_mobile(), 
                                     chart_type="line")
    
    # تعديلات إضافية خاصة بالمخطط الخطي
    if is_mobile():
        # تعديل علامات المحور س لتقليل التداخل
        fig_trend.update_xaxes(
            dtick=2,  # إظهار سنة واحدة من كل سنتين
            tickangle=0
        )
    
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

# ---- أعضاء هيئة التدريس المميزين وأحدث الإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")

# تكييف التخطيط حسب حجم الشاشة
if is_mobile():
    # عرض في عمود واحد للأجهزة المحمولة
    # أعضاء هيئة التدريس المميزين - اقتصر على أهم عضوين
    st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
    
    for i, (_, member) in enumerate(top_faculty.iterrows()):
        if i >= 2:  # عرض أول عضوين فقط على الشاشات الصغيرة
            break
        with st.container():
            st.markdown(f"""
            <div class='faculty-card'>
                <h3 style="font-size: 1.1rem; margin-bottom: 5px;">{member['الشارة']} {member['الاسم']}</h3>
                <p style="font-size: 0.9rem; margin: 2px 0;"><strong>اللقب:</strong> {member['اللقب']}</p>
                <p style="font-size: 0.9rem; margin: 2px 0;"><strong>النقاط:</strong> {member['النقاط']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("[عرض جميع أعضاء هيئة التدريس](http://localhost:8501/هيئة_التدريس)")
    
    # أحدث الإنجازات - اقتصر على أهم 2 إنجازات
    st.markdown("### 🌟 أحدث الإنجازات")
    
    for i, (_, achievement) in enumerate(faculty_achievements.iterrows()):
        if i >= 2:  # عرض أول إنجازين فقط على الشاشات الصغيرة
            break
            
        date_obj = datetime.strptime(achievement['التاريخ'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        
        st.markdown(f"""
        <div class='achievement-item'>
            <p style="font-size: 0.9rem; margin: 2px 0;"><strong>{achievement['العضو']}</strong></p>
            <p style="font-size: 0.9rem; margin: 2px 0;">{achievement['الإنجاز']}</p>
            <p style="font-size: 0.8rem; margin: 2px 0;"><small>{formatted_date} | {achievement['النقاط']} نقطة</small></p>
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

# تحضير بيانات المخطط الحراري حسب حجم الشاشة
if is_mobile():
    # استخدام أسماء مختصرة للبرامج
    heatmap_data = latest_year_data.copy()
    heatmap_data["البرنامج"] = heatmap_data["البرنامج"].map({
        "بكالوريوس في القرآن وعلومه": "بكالوريوس القرآن",
        "بكالوريوس القراءات": "بكالوريوس القراءات",
        "ماجستير الدراسات القرآنية المعاصرة": "ماجستير الدراسات",
        "ماجستير القراءات": "ماجستير القراءات",
        "دكتوراه علوم القرآن": "دكتوراه القرآن",
        "دكتوراه القراءات": "دكتوراه القراءات"
    })
    
    # وضع المخطط الحراري باستخدام Plotly مع تكييفه للشاشات الصغيرة
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data[["نسبة النجاح", "معدل الرضا"]].values,
        x=["نسبة النجاح", "معدل الرضا"],
        y=heatmap_data["البرنامج"],
        colorscale="Viridis",
        text=heatmap_data[["نسبة النجاح", "معدل الرضا"]].values,
        texttemplate="%{text}%",
        textfont={"size": 9},
    ))
else:
    # وضع المخطط الحراري للشاشات الكبيرة
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
        x=["نسبة النجاح", "معدل الرضا"],
        y=latest_year_data["البرنامج"],
        colorscale="Viridis",
        text=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
        texttemplate="%{text}%",
        textfont={"size": 12},
    ))

# تطبيق إعدادات المخطط المتجاوبة
fig_heatmap = prepare_chart_layout(
    fig_heatmap, 
    "مقارنة المؤشرات الرئيسية" if is_mobile() else "مقارنة المؤشرات الرئيسية عبر البرامج", 
    is_mobile=is_mobile(), 
    chart_type="heatmap"
)

# تعديلات إضافية للمخطط الحراري
if is_mobile():
    # زيادة الهامش السفلي للشاشات الصغيرة
    fig_heatmap.update_layout(margin=dict(b=30))

# عرض المخطط الحراري مع إيقاف شريط التكبير
st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})

# ---- نصائح للمستخدم ----
# استخدام expander للنصائح لتوفير المساحة على الشاشات الصغيرة
with st.expander("📋 نصائح للاستخدام", expanded=not is_mobile()):
    st.markdown("""
    - انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله
    - استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء
    - قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات
    - استخدم "لوحة إنجاز المهام" لتسجيل وعرض إنجازات أعضاء هيئة التدريس
    """)

# إضافة تنبيه بتجاوب الموقع
if is_mobile():
    st.info("👋 تم تحسين العرض للأجهزة المحمولة. مرر الشاشة للمزيد من المحتوى!")

# إذا كنت تريد دعم المزيد من لغات البرمجة وتطوير العرض التقديمي بشكل أكثر تفاعلية
# يمكن إضافة المزيد من التخصيصات والتفاعلات هنا
