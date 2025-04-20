import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="الرئيسية",
    page_icon="🏠",
    layout="wide"
)

# إعداد CSS وإخفاء عناصر واجهة Streamlit الافتراضية
hide_streamlit_elements = """
<style>
  /* 1. أخفِ شريط الـheader والـmenu الافتراضي */
  [data-testid="stToolbar"] { visibility: hidden !important; }
  #MainMenu               { visibility: hidden !important; }
  header                  { visibility: hidden !important; }

  /* 2. أخفِ الفوتر */
  footer                  { visibility: hidden !important; }

  /* 3. أخفِ أيقونة GitHub وبادج "Created by" */
  [class^="viewerBadge_"], [id^="GithubIcon"] {
    display: none !important;
  }
  [data-testid="stThumbnailsChipContainer"] {
    display: none !important;
  }

  /* 4. أخفِ شريط التقدم */
  .stProgress             { display: none !important; }

  /* 5. استثناء للشريط الجانبي: أبقه مرئيًّا */
  [data-testid="stSidebar"] {
    display: block !important;
  }

  /* 6. أخفِ عناصر التنقل السفلية فقط (بدون تعميم nav) */
  [data-testid="stBottomNavBar"],
  [data-testid*="bottomNav"],
  [aria-label*="community"],
  [aria-label*="profile"],
  [title*="community"],
  [title*="profile"] {
    display: none !important;
  }

  /* 7. إزالة روابط الترسّخ في العناوين */
  h1 > div > a, h2 > div > a, h3 > div > a,
  h4 > div > a, h5 > div > a, h6 > div > a {
    display: none !important;
  }
</style>
"""

st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

# CSS مخصص لدعم اللغة العربية والتخطيط
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
        
        /* إضافة زر للعودة للأعلى */
        .back-to-top {
            position: fixed;
            bottom: 20px;
            left: 20px;
            width: 40px;
            height: 40px;
            background-color: #1e88e5;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 998;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .back-to-top.visible {
            opacity: 1;
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
    }
</style>

<!-- إضافة طبقة لإظلام الخلفية عند فتح الشريط الجانبي -->
<div id="sidebar-overlay" onclick="toggleSidebar()"></div>

<!-- إضافة زر جديد للشريط الجانبي على الأجهزة المحمولة -->
<div class="sidebar-trigger" onclick="toggleSidebar()">
    <span style="font-size: 1.2rem;">☰</span>
</div>

<!-- إضافة زر العودة للأعلى -->
<div class="back-to-top" onclick="scrollToTop()">
    <span style="font-size: 1.2rem;">↑</span>
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
    
    // وظيفة للعودة للأعلى
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    
    // إظهار زر العودة للأعلى عند التمرير للأسفل
    window.addEventListener('scroll', function() {
        const backToTopButton = document.querySelector('.back-to-top');
        if (window.scrollY > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });
    
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

# دالة مساعدة للتكيف مع الأجهزة المحمولة - نسخة محسنة
def is_mobile():
    """تحقق مما إذا كان المستخدم يستخدم جهازًا محمولًا"""
    if 'IS_MOBILE' not in st.session_state:
        # تحديد القيمة الافتراضية بناءً على حجم النافذة المقدر
        # يمكن تحسين هذا باستخدام معلمة URL أو وضع تبديل في واجهة المستخدم
        st.session_state.IS_MOBILE = False
        
        # إضافة زر تبديل في الشريط الجانبي للاختبار (اختياري)
        # st.sidebar.checkbox("عرض نسخة الجوال", key="mobile_view")
    
    # بدلاً من ذلك، يمكن أن تستخدم متغير session_state تم تعيينه من خلال صندوق الاختيار أعلاه
    # return st.session_state.mobile_view
    
    # للعرض التوضيحي، نقوم بتقدير حجم الشاشة - في التطبيق الحقيقي
    # قد ترغب في تنفيذ طريقة أكثر دقة
    return st.session_state.IS_MOBILE

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

# ... (الدوال الأخرى المتعلقة بتحميل البيانات)

# ---- محتوى الصفحة ----
# تحديد إذا كان المستخدم على جهاز محمول
mobile_view = is_mobile()

# ---- الترويسة ----
if mobile_view:
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

# ---- المزيد من المحتوى ----
# ... (باقي الكود للمؤشرات والرسوم البيانية)
