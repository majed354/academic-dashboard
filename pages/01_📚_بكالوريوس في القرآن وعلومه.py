import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
from pages.utils.github_helpers import get_github_file_content, get_available_years, get_available_reports

# إعدادات الصفحة
st.set_page_config(
    page_title="بكالوريوس في القرآن وعلومه",
    page_icon="📚",
    layout="wide"
)
hide_streamlit_elements = """
<style>
  /* 1. أخفِ شريط الـheader والـmenu الافتراضي */
  [data-testid="stToolbar"] { visibility: hidden !important; }
  #MainMenu               { visibility: hidden !important; }
  header                  { visibility: hidden !important; }

  /* 2. أخفِ الفوتر */
  footer                  { visibility: hidden !important; }

  /* 3. أخفِ أيقونة GitHub وبادج “Created by” */
  [class^="viewerBadge_"], [id^="GithubIcon"] {
    display: none !important;
  }
  [data-testid="stThumbnailsChipContainer"] {
    display: none !important;
  }

  /* 4. أخفِ شريط التقدم */
  .stProgress             { display: none !important; }

  /* 5. استثناء للشريط الجانبي: أبقه مرئيًّا */
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

# إضافة CSS مخصص لدعم RTL وتحسين الاستجابة للجوال
st.markdown("""
<style>
    /* تعديلات عامة لدعم RTL */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* ترتيب العناوين من اليمين لليسار */
    h1, h2, h3, h4, h5, h6 {
        text-align: right;
    }
    
    /* ترتيب الجداول من اليمين لليسار */
    .dataframe {
        text-align: right;
    }
    
    /* محاذاة الأزرار والمدخلات من اليمين */
    button, input, select, textarea, .stButton>button, .stTextInput>div>div>input {
        text-align: right;
    }
    
    /* تعديل الهوامش للعناصر */
    .stMarkdown {
        text-align: right;
    }
    
    /* تعديل في القائمة الجانبية */
    .css-1inwz65 {
        text-align: right;
    }
    
    /* تعديل خاص للمخططات البيانية */
    .plotly {
        direction: ltr; /* المخططات تعمل بشكل أفضل مع اتجاه من اليسار لليمين */
    }
    
    /* تنسيق قائمة التنقل العلوية */
    .nav-container {
        display: flex;
        justify-content: space-between;
        overflow-x: auto;
        padding-bottom: 10px;
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
        white-space: nowrap;
    }
    
    .nav-link {
        flex-shrink: 0;
        padding: 8px 16px;
        margin: 0 5px;
        background-color: #f0f2f6;
        border-radius: 20px;
        text-decoration: none;
        color: #31333F;
        font-weight: bold;
        text-align: center;
    }
    
    .nav-link.active {
        background-color: #1e88e5;
        color: white;
    }
    
    /* تعديلات خاصة بالجوال */
    @media (max-width: 640px) {
        /* تقليل الهوامش والحشو */
        .stApp > header {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* تقليل حجم العناوين وهوامشها */
        h1 {
            font-size: 1.5rem !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        h2, h3 {
            font-size: 1.2rem !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.4rem !important;
        }
        
        /* تحسين أحجام الفجوات */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        /* تحسين حاويات st.expander */
        .streamlit-expanderHeader {
            font-size: 1rem !important;
            padding: 0.5rem !important;
        }
        
        /* تعديل عناصر تحكم الإدخال */
        .stSelectbox, .stButton>button {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* زيادة مساحة النقر للأزرار */
        .stButton>button {
            min-height: 44px;
        }
        
        /* تنسيق قائمة التنقل للجوال */
        .nav-link {
            padding: 6px 10px;
            margin: 0 3px;
            font-size: 12px;
        }
    }
    
    /* تحسين عناصر التبويب لتناسب الشاشات الصغيرة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding-left: 10px;
        padding-right: 10px;
    }
    
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab"] {
            padding-left: 5px;
            padding-right: 5px;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 12px;
        }
    }
    
    /* تنسيق بطاقات المعلومات */
    .info-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* شريط جانبي ملحوظ */
    .sidebar-highlight {
        background-color: #1e88e5;
        color: white;
        border-radius: 4px;
        padding: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>

<!-- قائمة التنقل العلوية -->
<div class="nav-container">
    <a href="/" class="nav-link">الرئيسية</a>
    <a href="/_%F0%9F%93%9A_%D8%A8%D9%83%D8%A7%D9%84%D9%88%D8%B1%D9%8A%D9%88%D8%B3_%D9%81%D9%8A_%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86_%D9%88%D8%B9%D9%84%D9%88%D9%85%D9%87" class="nav-link active">القرآن وعلومه</a>
    <a href="/_%F0%9F%93%96_%D8%A8%D9%83%D8%A7%D9%84%D9%88%D8%B1%D9%8A%D9%88%D8%B3_%D8%A7%D9%84%D9%82%D8%B1%D8%A7%D8%A1%D8%A7%D8%AA" class="nav-link">القراءات</a>
    <a href="/_%F0%9F%8E%93_%D9%85%D8%A7%D8%AC%D8%B3%D8%AA%D9%8A%D8%B1_%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D8%B3%D8%A7%D8%AA_%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86%D9%8A%D8%A9_%D8%A7%D9%84%D9%85%D8%B9%D8%A7%D8%B5%D8%B1%D8%A9" class="nav-link">الماجستير</a>
    <a href="/_%F0%9F%91%A5_%D9%87%D9%8A%D8%A6%D8%A9_%D8%A7%D9%84%D8%AA%D8%AF%D8%B1%D9%8A%D8%B3" class="nav-link">هيئة التدريس</a>
</div>
""", unsafe_allow_html=True)

# العنوان الرئيسي للصفحة
st.title("📚 بكالوريوس في القرآن وعلومه")

# استخراج السنوات المتاحة وملفات التقارير
program_code = "bachelor_quran"
available_years, data_file_map = get_available_years(program_code)
available_reports = get_available_reports(program_code)

# إنشاء عناصر التحكم في الشريط الجانبي مع تحسين الرؤية
st.sidebar.markdown('<div class="sidebar-highlight">⚙️ إعدادات التصفية</div>', unsafe_allow_html=True)

# اختيار السنة في الشريط الجانبي
if available_years:
    year_key = f'selected_year_{program_code}'
    if year_key not in st.session_state:
        st.session_state[year_key] = available_years[0]

    selected_year = st.sidebar.selectbox(
        "اختر السنة:",
        available_years,
        key=f'selectbox_{year_key}',
        index=available_years.index(st.session_state[year_key])
    )
    st.session_state[year_key] = selected_year
else:
    st.sidebar.warning("لا توجد بيانات سنوية متاحة")
    selected_year = None

# عناصر تحكم للتقارير في الشريط الجانبي
if available_reports:
    st.sidebar.markdown("---")
    st.sidebar.header("التقارير والمستندات")
    report_key = f'selected_report_{program_code}'

    # استخراج وتصنيف التقارير
    annual_reports = {k: v for k, v in available_reports.items() if k.startswith('تقرير_')}
    desc_files = {k: v for k, v in available_reports.items() if k.startswith('توصيف_')}

    # اختيار تقرير سنوي
    if annual_reports:
        report_names = list(annual_reports.keys())
        if report_key not in st.session_state:
            st.session_state[report_key] = report_names[0]

        selected_report = st.sidebar.selectbox(
            "اختر تقريرًا:",
            report_names,
            key=f'selectbox_{report_key}',
            index=report_names.index(st.session_state[report_key]) if st.session_state[report_key] in report_names else 0
        )
        st.session_state[report_key] = selected_report
else:
    st.sidebar.warning("لا توجد تقارير متاحة")
    selected_report = None

# تنظيم المحتوى الرئيسي في تبويبات للتنقل السهل
main_tabs = st.tabs(["نظرة عامة", "البيانات والإحصائيات", "التقارير", "المقررات"])

# التبويب الأول: نظرة عامة
with main_tabs[0]:
    # معلومات أساسية عن البرنامج
    st.markdown("""
    <div class="info-card">
        <h3>نبذة عن البرنامج</h3>
        <p>برنامج البكالوريوس في القرآن وعلومه هو برنامج أكاديمي يهدف إلى تأهيل الطلاب في مجال علوم القرآن الكريم من تفسير وتجويد وقراءات وغيرها من العلوم المرتبطة بالقرآن الكريم.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض بطاقات معلومات البرنامج
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>مدة البرنامج</h3>
            <p>4 سنوات دراسية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>الساعات المعتمدة</h3>
            <p>136 ساعة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>لغة الدراسة</h3>
            <p>اللغة العربية</p>
        </div>
        """, unsafe_allow_html=True)
    
    # عرض توصيف البرنامج إذا كان متاحًا
    if desc_files:
        with st.expander("توصيف البرنامج", expanded=True):
            desc_name = list(desc_files.keys())[0]
            desc_content = get_github_file_content(desc_files[desc_name])
            if desc_content:
                st.markdown(desc_content)

# التبويب الثاني: البيانات والإحصائيات
with main_tabs[1]:
    if selected_year and selected_year in data_file_map:
        st.header(f"بيانات عام {selected_year}")
        
        # جلب البيانات
        df = get_github_file_content(data_file_map[selected_year])
        
        # عرض البيانات والمخططات إذا كانت البيانات متاحة
        if isinstance(df, pd.DataFrame):
            # عرض الجدول في موسع للتوفير المساحة
            with st.expander("عرض بيانات الجدول", expanded=False):
                st.dataframe(df, use_container_width=True)
            
            # إنشاء رسم بياني متجاوب للمقارنة
            if "النسبة المئوية" in df.columns and "الهدف" in df.columns and "المعيار" in df.columns:
                st.subheader("مقارنة النسب المئوية بالأهداف")
                fig = px.bar(
                    df, 
                    x="المعيار", 
                    y=["النسبة المئوية", "الهدف"],
                    barmode="group",
                    title=f"مؤشرات الأداء لعام {selected_year}",
                    labels={"value": "النسبة المئوية", "variable": ""}
                )
                # تحسين استجابة الرسم البياني
                fig.update_layout(
                    autosize=True,
                    margin=dict(l=10, r=10, t=50, b=100),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.3,
                        xanchor="center",
                        x=0.5
                    ),
                    height=350,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)

                # رسم بياني للاتجاه والتطور (إذا تم تحديد سنة غير الأولى)
                if selected_year != available_years[-1]:  # إذا لم تكن أقدم سنة متاحة
                    with st.expander("تطور المؤشرات خلال السنوات", expanded=True):
                        st.subheader("تطور المؤشرات خلال السنوات")

                        # جمع بيانات السنوات السابقة
                        trend_data = []
                        for year in available_years:
                            if year >= selected_year:  # السنة الحالية وما قبلها فقط
                                year_df = get_github_file_content(data_file_map[year])
                                if isinstance(year_df, pd.DataFrame):
                                    for _, row in year_df.iterrows():
                                        trend_data.append({
                                            "العام": str(year),
                                            "المعيار": row["المعيار"],
                                            "النسبة المئوية": row["النسبة المئوية"]
                                        })

                        if trend_data:
                            trend_df = pd.DataFrame(trend_data)
                            fig_trend = px.line(
                                trend_df, 
                                x="العام", 
                                y="النسبة المئوية",
                                color="المعيار",
                                markers=True,
                                title="تطور النسب المئوية للمؤشرات"
                            )
                            # تحسين استجابة الرسم البياني
                            fig_trend.update_layout(
                                autosize=True,
                                margin=dict(l=10, r=10, t=50, b=30),
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.3,
                                    xanchor="center",
                                    x=0.5
                                ),
                                height=350
                            )
                            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.error("تعذر تحميل البيانات")
    else:
        st.warning("يرجى اختيار سنة من القائمة الجانبية لعرض البيانات")

# التبويب الثالث: التقارير
with main_tabs[2]:
    if selected_report and annual_reports:
        st.header(f"تقرير: {selected_report.replace('.md', '')}")
        report_content = get_github_file_content(annual_reports[selected_report])
        if report_content:
            # عرض محتوى التقرير حسب نوع الملف
            if selected_report.endswith('.md'):
                st.markdown(report_content)
            elif selected_report.endswith('.pdf'):
                # تخزين بيانات PDF في session_state لضمان استمرارية العرض
                pdf_key = f'pdf_data_{selected_report}'
                st.session_state[pdf_key] = report_content
                # عرض PDF باستخدام pdf_viewer
                try:
                    pdf_viewer(st.session_state[pdf_key], width=700)
                except Exception as e:
                    st.error(f"خطأ في عرض ملف PDF: {e}")
                    st.link_button("فتح التقرير في تبويب جديد", annual_reports[selected_report])
    else:
        st.info("يرجى اختيار تقرير من القائمة الجانبية لعرضه")

# التبويب الرابع: المقررات
with main_tabs[3]:
    st.header("المقررات الدراسية")
    
    # بيانات تجريبية للمقررات
    courses_data = {
        "رمز المقرر": ["QUR101", "QUR102", "QUR201", "QUR202", "QUR301", "QUR302", "QUR401", "QUR402"],
        "اسم المقرر": ["مدخل لعلوم القرآن", "التجويد (1)", "أصول التفسير", "علوم القرآن (1)", "مناهج المفسرين", "التجويد (2)", "علوم القرآن (2)", "مشروع التخرج"],
        "عدد الساعات": [3, 2, 3, 3, 3, 2, 3, 4],
        "المستوى": ["الأول", "الأول", "الثاني", "الثاني", "الثالث", "الثالث", "الرابع", "الرابع"]
    }
    
    courses_df = pd.DataFrame(courses_data)
    
    # تصفية المقررات حسب المستوى
    levels = ["الكل"] + sorted(courses_df["المستوى"].unique().tolist())
    selected_level = st.selectbox("تصفية حسب المستوى:", levels)
    
    if selected_level != "الكل":
        filtered_courses = courses_df[courses_df["المستوى"] == selected_level]
    else:
        filtered_courses = courses_df
    
    # عرض المقررات كجدول
    st.dataframe(filtered_courses, use_container_width=True)
    
    # معلومات إضافية حول المقررات
    with st.expander("معلومات إضافية حول المقررات"):
        st.write("""
        - يتم تدريس المقررات على مدار 8 فصول دراسية (4 سنوات).
        - المقررات التي تنتهي بأرقام فردية تدرس في الفصل الدراسي الأول.
        - المقررات التي تنتهي بأرقام زوجية تدرس في الفصل الدراسي الثاني.
        - يتطلب التخرج إتمام 136 ساعة معتمدة بنجاح.
        """)
    
    # الخطة الدراسية كمخطط زمني
    with st.expander("الخطة الدراسية"):
        st.subheader("الخطة الدراسية")
        for level in sorted(courses_df["المستوى"].unique()):
            st.write(f"### المستوى {level}")
            level_courses = courses_df[courses_df["المستوى"] == level]
            st.table(level_courses[["رمز المقرر", "اسم المقرر", "عدد الساعات"]])
            st.markdown("---")
