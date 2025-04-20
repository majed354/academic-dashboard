import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
# تأكد من أن هذا الاستيراد صحيح وأن الملف موجود في المسار الصحيح
# إذا كانت هذه الدوال معرفة في نفس الملف، فلا حاجة لهذا الاستيراد
# from pages.utils.github_helpers import get_github_file_content, get_available_years, get_available_reports
import base64 # لاستخدامها في get_github_file_content إذا لزم الأمر
import requests # لاستخدامها في get_github_file_content إذا لزم الأمر
import io # لاستخدامها في قراءة البيانات

# ==============================================================================
# تعريف الدوال المساعدة (إذا لم تكن مستوردة من ملف آخر)
# استبدل هذه الدوال بالاستيراد الفعلي إذا كانت موجودة في ملف منفصل
# ==============================================================================

# مثال لدالة جلب محتوى ملف من GitHub (قد تحتاج لتعديلها حسب طريقة عملك)
@st.cache_data(ttl=3600) # تخزين مؤقت لمدة ساعة
def get_github_file_content(file_path):
    """
    تجلب محتوى ملف من مستودع GitHub عام.
    file_path: يجب أن يكون الرابط الخام للملف (raw URL).
    """
    try:
        # افترض أن file_path هو الرابط الخام للملف
        response = requests.get(file_path)
        response.raise_for_status() # يثير خطأ إذا كانت الاستجابة غير ناجحة

        # التحقق من نوع الملف
        if file_path.endswith('.csv'):
            # قراءة ملف CSV باستخدام Pandas
            content = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        elif file_path.endswith('.md'):
            # قراءة ملف Markdown كنص
            content = response.content.decode('utf-8')
        elif file_path.endswith('.pdf'):
             # إرجاع محتوى PDF كبايتات
             content = response.content
        else:
             # إرجاع المحتوى كنص لأنواع أخرى (يمكن تعديلها)
             content = response.content.decode('utf-8')

        return content
    except requests.exceptions.RequestException as e:
        st.error(f"خطأ في جلب الملف من GitHub: {e}")
        return None
    except pd.errors.ParserError as e:
        st.error(f"خطأ في قراءة ملف CSV: {e}")
        return None
    except Exception as e:
        st.error(f"خطأ غير متوقع: {e}")
        return None

# مثال لدالة جلب السنوات المتاحة (تحتاج لتحديد منطقها)
@st.cache_data(ttl=3600)
def get_available_years(program_code):
    """
    تجلب قائمة بالسنوات المتاحة وملفات البيانات المرتبطة بها لبرنامج معين.
    تحتاج لتحديد كيفية العثور على هذه الملفات (مثل فحص مجلد في GitHub).
    """
    # مثال: افترض أن لديك روابط مباشرة للملفات
    # استبدل هذا بمنطقك الفعلي
    if program_code == "bachelor_quran":
        # يجب أن تكون هذه روابط خام (raw URLs) للملفات على GitHub
        data_files = {
            "2023-2024": "https://raw.githubusercontent.com/your_username/your_repo/main/data/bachelor_quran/2023-2024.csv",
            "2022-2023": "https://raw.githubusercontent.com/your_username/your_repo/main/data/bachelor_quran/2022-2023.csv",
        }
        available_years = sorted(list(data_files.keys()), reverse=True)
        return available_years, data_files
    else:
        return [], {}

# مثال لدالة جلب التقارير المتاحة (تحتاج لتحديد منطقها)
@st.cache_data(ttl=3600)
def get_available_reports(program_code):
    """
    تجلب قائمة بالتقارير والمستندات المتاحة لبرنامج معين.
    تحتاج لتحديد كيفية العثور على هذه الملفات.
    """
    # مثال: افترض أن لديك روابط مباشرة للملفات
    if program_code == "bachelor_quran":
        # يجب أن تكون هذه روابط خام (raw URLs) للملفات على GitHub
        report_files = {
            "تقرير_2023-2024.md": "https://raw.githubusercontent.com/your_username/your_repo/main/reports/bachelor_quran/report_2023-2024.md",
            "توصيف_البرنامج.md": "https://raw.githubusercontent.com/your_username/your_repo/main/descriptions/bachelor_quran/description.md",
            "تقرير_سنوي_2022.pdf": "https://raw.githubusercontent.com/your_username/your_repo/main/reports/bachelor_quran/annual_report_2022.pdf", # مثال لملف PDF
        }
        return report_files
    else:
        return {}

# ==============================================================================
# إعدادات الصفحة
# ==============================================================================
st.set_page_config(
    page_title="بكالوريوس في القرآن وعلومه",
    page_icon="📚",
    layout="wide"
)

# ==============================================================================
# تعريف CSS لإخفاء عناصر Streamlit الافتراضية (هذا هو الإصلاح)
# ==============================================================================
hide_streamlit_elements = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* يمكنك إضافة المزيد من العناصر هنا إذا لزم الأمر */
            </style>
            """
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

# ==============================================================================
# إضافة CSS مخصص لدعم RTL وتحسين الاستجابة للجوال
# ==============================================================================
st.markdown("""
<style>
    /* تعديلات عامة لدعم RTL */
    body {
        direction: rtl;
    }
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* ترتيب العناوين من اليمين لليسار */
    h1, h2, h3, h4, h5, h6 {
        text-align: right !important; /* استخدام !important لضمان التطبيق */
    }

    /* ترتيب الجداول من اليمين لليسار */
    .dataframe {
        text-align: right;
        direction: rtl;
    }
    /* التأكد من محاذاة خلايا الجدول */
     .dataframe th, .dataframe td {
        text-align: right !important;
     }

    /* محاذاة الأزرار والمدخلات من اليمين */
    button, input, select, textarea, .stButton>button, .stTextInput>div>div>input, .stSelectbox>div>div>select {
        text-align: right !important; /* قد تحتاج لتعديل المحددات بناءً على إصدار Streamlit */
        direction: rtl;
    }

    /* تعديل الهوامش للعناصر */
    .stMarkdown {
        text-align: right;
    }

    /* تعديل في القائمة الجانبية */
    .css-1d391kg { /* قد يتغير هذا الكلاس مع تحديثات Streamlit، تحقق منه إذا لم يعمل */
        text-align: right;
        right: 0; /* تأكد من أن القائمة الجانبية تظهر على اليمين */
        left: auto;
    }
    /* محاذاة محتويات القائمة الجانبية */
    .stSidebar .stMarkdown, .stSidebar .stSelectbox, .stSidebar .stButton {
         text-align: right !important;
         direction: rtl;
    }
     .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
         text-align: right !important;
     }

    /* تعديل خاص للمخططات البيانية */
    .plotly {
        direction: ltr; /* المخططات تعمل بشكل أفضل مع اتجاه من اليسار لليمين */
    }

    /* تنسيق قائمة التنقل العلوية */
    .nav-container {
        display: flex;
        justify-content: flex-start; /* البدء من اليمين في RTL */
        overflow-x: auto;
        padding-bottom: 10px;
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
        white-space: nowrap;
    }

    .nav-link {
        flex-shrink: 0;
        padding: 8px 16px;
        margin: 0 0 0 10px; /* تعديل الهامش لـ RTL */
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
            margin: 0 0 0 5px; /* تعديل الهامش لـ RTL */
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
        text-align: right; /* تأكيد المحاذاة */
    }

    /* شريط جانبي ملحوظ */
    .sidebar-highlight {
        background-color: #1e88e5;
        color: white;
        border-radius: 4px;
        padding: 10px;
        text-align: center; /* أو right إذا أردت النص محاذياً لليمين */
        margin-bottom: 20px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>

<div class="nav-container">
    <a href="/" class="nav-link">الرئيسية</a>
    <a href="/_%F0%9F%93%9A_%D8%A8%D9%83%D8%A7%D9%84%D9%88%D8%B1%D9%8A%D9%88%D8%B3_%D9%81%D9%8A_%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86_%D9%88%D8%B9%D9%84%D9%88%D9%85%D9%87" class="nav-link active">القرآن وعلومه</a>
    <a href="/_%F0%9F%93%96_%D8%A8%D9%83%D8%A7%D9%84%D9%88%D8%B1%D9%8A%D9%88%D8%B3_%D8%A7%D9%84%D9%82%D8%B1%D8%A7%D8%A1%D8%A7%D8%AA" class="nav-link">القراءات</a>
    <a href="/_%F0%9F%8E%93_%D9%85%D8%A7%D8%AC%D8%B3%D8%AA%D9%8A%D8%B1_%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D8%B3%D8%A7%D8%AA_%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86%D9%8A%D8%A9_%D8%A7%D9%84%D9%85%D8%B9%D8%A7%D8%B5%D8%B1%D8%A9" class="nav-link">الماجستير</a>
    <a href="/_%F0%9F%91%A5_%D9%87%D9%8A%D8%A6%D8%A9_%D8%A7%D9%84%D8%AA%D8%AF%D8%B1%D9%8A%D8%B3" class="nav-link">هيئة التدريس</a>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# المحتوى الرئيسي للصفحة
# ==============================================================================

# العنوان الرئيسي للصفحة
st.title("📚 بكالوريوس في القرآن وعلومه")

# استخراج السنوات المتاحة وملفات التقارير
program_code = "bachelor_quran"
# تأكد من استبدال الدوال الوهمية أعلاه بالاستيراد الفعلي أو التعريف الصحيح
available_years, data_file_map = get_available_years(program_code)
available_reports = get_available_reports(program_code)

# إنشاء عناصر التحكم في الشريط الجانبي مع تحسين الرؤية
st.sidebar.markdown('<div class="sidebar-highlight">⚙️ إعدادات التصفية</div>', unsafe_allow_html=True)

# اختيار السنة في الشريط الجانبي
selected_year = None # قيمة افتراضية
if available_years:
    year_key = f'selected_year_{program_code}'
    # تعيين قيمة افتراضية إذا لم تكن موجودة في حالة الجلسة
    if year_key not in st.session_state:
        st.session_state[year_key] = available_years[0]

    # التأكد من أن القيمة المخزنة لا تزال صالحة
    if st.session_state[year_key] not in available_years:
         st.session_state[year_key] = available_years[0]

    selected_year = st.sidebar.selectbox(
        "اختر السنة:",
        available_years,
        key=f'selectbox_{year_key}', # استخدام مفتاح فريد
        index=available_years.index(st.session_state[year_key])
    )
    # تحديث حالة الجلسة عند التغيير
    st.session_state[year_key] = selected_year
else:
    st.sidebar.warning("لا توجد بيانات سنوية متاحة")


# عناصر تحكم للتقارير في الشريط الجانبي
selected_report = None # قيمة افتراضية
annual_reports = {} # قيمة افتراضية
desc_files = {} # قيمة افتراضية

if available_reports:
    st.sidebar.markdown("---")
    st.sidebar.header("التقارير والمستندات")
    report_key = f'selected_report_{program_code}'

    # استخراج وتصنيف التقارير
    annual_reports = {k: v for k, v in available_reports.items() if k.startswith('تقرير_') or k.endswith('.pdf')} # توسيع ليشمل PDF
    desc_files = {k: v for k, v in available_reports.items() if k.startswith('توصيف_')}

    # اختيار تقرير سنوي
    if annual_reports:
        report_names = list(annual_reports.keys())
        # تعيين قيمة افتراضية إذا لم تكن موجودة
        if report_key not in st.session_state or st.session_state[report_key] not in report_names:
            st.session_state[report_key] = report_names[0]

        selected_report = st.sidebar.selectbox(
            "اختر تقريرًا:",
            report_names,
            key=f'selectbox_{report_key}', # استخدام مفتاح فريد
            index=report_names.index(st.session_state[report_key])
        )
        # تحديث حالة الجلسة عند التغيير
        st.session_state[report_key] = selected_report
    else:
        st.sidebar.info("لا توجد تقارير سنوية متاحة.") # رسالة إعلامية

else:
    st.sidebar.warning("لا توجد تقارير أو مستندات متاحة")


# تنظيم المحتوى الرئيسي في تبويبات للتنقل السهل
main_tabs = st.tabs(["نظرة عامة", "البيانات والإحصائيات", "التقارير", "المقررات"])

# ======================== التبويب الأول: نظرة عامة ========================
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
        # افتراض وجود ملف توصيف واحد فقط
        desc_name = list(desc_files.keys())[0]
        desc_file_path = desc_files[desc_name] # الحصول على المسار أو الرابط
        with st.expander("توصيف البرنامج", expanded=True):
             # جلب المحتوى
             desc_content = get_github_file_content(desc_file_path)
             if isinstance(desc_content, str): # التأكد من أنه نص (Markdown)
                 st.markdown(desc_content, unsafe_allow_html=True) # السماح بـ HTML إذا كان موجودًا في الملف
             elif desc_content is not None:
                 st.warning("تم جلب محتوى توصيف البرنامج ولكن نوعه غير متوقع (ليس نصًا).")
             else:
                 st.error(f"لم يتم العثور على محتوى لملف التوصيف: {desc_name}")
    else:
        st.info("ملف توصيف البرنامج غير متاح حاليًا.")

# ======================== التبويب الثاني: البيانات والإحصائيات ========================
with main_tabs[1]:
    if selected_year and selected_year in data_file_map:
        st.header(f"بيانات عام {selected_year}")

        # جلب البيانات للسنة المختارة
        data_file_path = data_file_map[selected_year]
        df = get_github_file_content(data_file_path)

        # عرض البيانات والمخططات إذا كانت البيانات متاحة وهي DataFrame
        if isinstance(df, pd.DataFrame) and not df.empty:
            # عرض الجدول في موسع للتوفير المساحة
            with st.expander("عرض بيانات الجدول", expanded=False):
                # استخدام عرض الحاوية وتعيين الفهرس إذا كان مناسبًا
                st.dataframe(df.reset_index(drop=True), use_container_width=True)

            # التحقق من وجود الأعمدة المطلوبة للرسم البياني
            required_cols = ["النسبة المئوية", "الهدف", "المعيار"]
            if all(col in df.columns for col in required_cols):
                st.subheader("مقارنة النسب المئوية بالأهداف")
                try:
                    # التأكد من أن الأعمدة الرقمية هي بالفعل رقمية
                    df["النسبة المئوية"] = pd.to_numeric(df["النسبة المئوية"], errors='coerce')
                    df["الهدف"] = pd.to_numeric(df["الهدف"], errors='coerce')
                    # إزالة الصفوف التي قد تحتوي على قيم NaN بعد التحويل
                    df_chart = df.dropna(subset=["النسبة المئوية", "الهدف", "المعيار"])

                    if not df_chart.empty:
                        fig = px.bar(
                            df_chart,
                            x="المعيار",
                            y=["النسبة المئوية", "الهدف"],
                            barmode="group",
                            title=f"مؤشرات الأداء لعام {selected_year}",
                            labels={"value": "النسبة", "variable": "المقياس", "المعيار": "المعيار"},
                            height=400 # زيادة الارتفاع قليلاً
                        )
                        # تحسين استجابة الرسم البياني وتنسيقه
                        fig.update_layout(
                            autosize=True,
                            margin=dict(l=20, r=20, t=60, b=150), # زيادة الهامش السفلي للعناوين الطويلة
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.4, # تعديل الموضع لتجنب التداخل
                                xanchor="center",
                                x=0.5,
                                title_text="" # إزالة عنوان وسيلة الإيضاح إذا لم يكن ضروريًا
                            ),
                            xaxis_tickangle=-45, # تدوير عناوين المحور السيني
                            yaxis_title="النسبة (%)", # إضافة عنوان للمحور الصادي
                            xaxis_title="المعيار" # إضافة عنوان للمحور السيني
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                         st.warning("لا توجد بيانات صالحة لرسم المخطط البياني للمقارنة.")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء إنشاء مخطط المقارنة: {e}")
            else:
                st.warning(f"لم يتم العثور على الأعمدة المطلوبة ({', '.join(required_cols)}) لرسم مخطط المقارنة.")

            # ----- رسم بياني للاتجاه والتطور -----
            # التحقق إذا كانت هناك سنوات أخرى للمقارنة وإذا كان العمود المطلوب موجودًا
            if len(available_years) > 1 and "النسبة المئوية" in df.columns and "المعيار" in df.columns:
                 # التأكد من أن السنة الحالية ليست أقدم سنة (لأن الاتجاه يحتاج لسنتين على الأقل)
                 current_year_index = available_years.index(selected_year)
                 if current_year_index < len(available_years) - 1:
                     with st.expander("تطور المؤشرات خلال السنوات", expanded=True):
                         st.subheader("تطور المؤشرات خلال السنوات")
                         trend_data = []
                         # المرور على السنوات من الأقدم حتى السنة المختارة
                         years_for_trend = available_years[current_year_index:][::-1] # عكس الترتيب للبدء من الأقدم

                         for year in years_for_trend:
                             if year in data_file_map:
                                 year_df = get_github_file_content(data_file_map[year])
                                 if isinstance(year_df, pd.DataFrame) and not year_df.empty:
                                     if "النسبة المئوية" in year_df.columns and "المعيار" in year_df.columns:
                                         # التأكد من أن العمود رقمي
                                         year_df["النسبة المئوية"] = pd.to_numeric(year_df["النسبة المئوية"], errors='coerce')
                                         year_df_clean = year_df.dropna(subset=["النسبة المئوية", "المعيار"])
                                         for _, row in year_df_clean.iterrows():
                                             trend_data.append({
                                                 "العام": str(year), # تحويل العام إلى نص للمحور السيني
                                                 "المعيار": row["المعيار"],
                                                 "النسبة المئوية": row["النسبة المئوية"]
                                             })
                                 else:
                                     st.warning(f"لم يتم تحميل بيانات صالحة لعام {year} لعرض الاتجاه.")
                             else:
                                 st.warning(f"لم يتم العثور على ملف بيانات لعام {year}.")

                         if trend_data:
                             trend_df = pd.DataFrame(trend_data)
                             try:
                                 fig_trend = px.line(
                                     trend_df,
                                     x="العام",
                                     y="النسبة المئوية",
                                     color="المعيار",
                                     markers=True, # إظهار نقاط البيانات
                                     title="تطور النسب المئوية للمؤشرات عبر السنوات",
                                     labels={"العام": "السنة الدراسية", "النسبة المئوية": "النسبة (%)", "المعيار": "المعيار"}
                                 )
                                 # تحسين استجابة الرسم البياني وتنسيقه
                                 fig_trend.update_layout(
                                     autosize=True,
                                     margin=dict(l=20, r=20, t=60, b=50),
                                     legend=dict(
                                         orientation="h",
                                         yanchor="bottom",
                                         y=-0.3,
                                         xanchor="center",
                                         x=0.5,
                                         title_text="المعايير"
                                     ),
                                     height=400,
                                     xaxis={'categoryorder':'array', 'categoryarray':years_for_trend} # ترتيب المحور السيني حسب السنوات
                                 )
                                 st.plotly_chart(fig_trend, use_container_width=True)
                             except Exception as e:
                                 st.error(f"حدث خطأ أثناء إنشاء مخطط الاتجاه: {e}")
                         else:
                             st.info("لا توجد بيانات كافية لعرض تطور المؤشرات.")
                 else:
                     st.info("لا يمكن عرض تطور المؤشرات لأنه تم اختيار أقدم سنة متاحة.")
            elif len(available_years) <= 1:
                 st.info("لا يمكن عرض تطور المؤشرات لأنه لا توجد بيانات لسنوات متعددة.")

        elif df is None:
            # الخطأ تم عرضه بالفعل في دالة get_github_file_content
            pass
        else:
            st.warning("تم تحميل البيانات ولكنها ليست بالتنسيق المتوقع (DataFrame) أو أنها فارغة.")
    else:
        st.warning("يرجى اختيار سنة من القائمة الجانبية لعرض البيانات.")

# ======================== التبويب الثالث: التقارير ========================
with main_tabs[2]:
    if selected_report and annual_reports and selected_report in annual_reports:
        st.header(f"عرض: {selected_report}") # تعديل العنوان ليكون أوضح
        report_file_path = annual_reports[selected_report]
        report_content = get_github_file_content(report_file_path)

        if report_content is not None:
            # عرض محتوى التقرير حسب نوع الملف
            if report_file_path.lower().endswith('.md'):
                st.markdown(report_content, unsafe_allow_html=True) # السماح بـ HTML داخل الماركداون
            elif report_file_path.lower().endswith('.pdf'):
                # عرض PDF باستخدام pdf_viewer
                try:
                    # لا حاجة لتخزين PDF في session_state إذا كان get_github_file_content يعيد المحتوى مباشرة
                    # تأكد من أن report_content هو بايتات PDF
                    if isinstance(report_content, bytes):
                         pdf_viewer(report_content, height=600) # تعديل الارتفاع حسب الحاجة
                    else:
                         st.error("المحتوى الذي تم جلبه ليس بتنسيق PDF المتوقع (بايتات).")
                         # محاولة عرض رابط إذا كان report_file_path رابطًا صالحًا
                         if isinstance(report_file_path, str) and report_file_path.startswith('http'):
                              st.link_button("فتح التقرير في تبويب جديد", report_file_path)

                except Exception as e:
                    st.error(f"خطأ في عرض ملف PDF: {e}")
                    # توفير رابط بديل للتحميل أو الفتح
                    if isinstance(report_file_path, str) and report_file_path.startswith('http'):
                         st.link_button("فتح التقرير في تبويب جديد", report_file_path)
            else:
                 st.warning(f"نوع الملف '{report_file_path.split('.')[-1]}' غير مدعوم للعرض المباشر. حاول تنزيله.")
                 # توفير رابط للتحميل إذا كان متاحًا
                 if isinstance(report_file_path, str) and report_file_path.startswith('http'):
                      st.link_button(f"تنزيل/فتح {selected_report}", report_file_path)
        else:
            st.error(f"تعذر تحميل محتوى التقرير: {selected_report}")
    elif selected_report:
         st.warning(f"التقرير المحدد '{selected_report}' غير موجود في قائمة التقارير المتاحة.")
    else:
        st.info("يرجى اختيار تقرير من القائمة الجانبية لعرضه.")


# ======================== التبويب الرابع: المقررات ========================
with main_tabs[3]:
    st.header("المقررات الدراسية")

    # بيانات تجريبية للمقررات (يمكن استبدالها ببيانات حقيقية لاحقًا)
    courses_data = {
        "رمز المقرر": ["QUR101", "QUR102", "QUR201", "QUR202", "QUR301", "QUR302", "QUR401", "QUR402"],
        "اسم المقرر": ["مدخل لعلوم القرآن", "التجويد (1)", "أصول التفسير", "علوم القرآن (1)", "مناهج المفسرين", "التجويد (2)", "علوم القرآن (2)", "مشروع التخرج"],
        "عدد الساعات": [3, 2, 3, 3, 3, 2, 3, 4],
        "المستوى": ["الأول", "الأول", "الثاني", "الثاني", "الثالث", "الثالث", "الرابع", "الرابع"]
    }

    courses_df = pd.DataFrame(courses_data)

    # تصفية المقررات حسب المستوى
    # الحصول على قائمة فريدة ومرتبة للمستويات
    levels = ["الكل"] + sorted(courses_df["المستوى"].unique().tolist(), key=lambda x: ["الأول", "الثاني", "الثالث", "الرابع"].index(x))
    selected_level = st.selectbox("تصفية حسب المستوى:", levels, key="course_level_filter")

    if selected_level != "الكل":
        filtered_courses = courses_df[courses_df["المستوى"] == selected_level].reset_index(drop=True)
    else:
        filtered_courses = courses_df.reset_index(drop=True)

    # عرض المقررات كجدول
    st.dataframe(filtered_courses, use_container_width=True, hide_index=True) # إخفاء الفهرس الافتراضي

    # معلومات إضافية حول المقررات
    with st.expander("معلومات إضافية حول المقررات"):
        st.write("""
        - يتم تدريس المقررات على مدار 8 فصول دراسية (4 سنوات).
        - المقررات التي تنتهي بأرقام فردية تدرس عادة في الفصل الدراسي الأول من العام الدراسي.
        - المقررات التي تنتهي بأرقام زوجية تدرس عادة في الفصل الدراسي الثاني من العام الدراسي.
        - يتطلب التخرج إتمام 136 ساعة معتمدة بنجاح وفقًا للخطة الدراسية المعتمدة.
        """)

    # الخطة الدراسية كمخطط زمني (عرض محسن)
    with st.expander("الخطة الدراسية التفصيلية"):
        st.subheader("الخطة الدراسية مقسمة حسب المستويات")
        # الحصول على قائمة المستويات مرتبة
        sorted_levels = sorted(courses_df["المستوى"].unique().tolist(), key=lambda x: ["الأول", "الثاني", "الثالث", "الرابع"].index(x))
        for level in sorted_levels:
            st.write(f"#### المستوى {level}") # استخدام مستوى عنوان أصغر
            level_courses = courses_df[courses_df["المستوى"] == level]
            # عرض الجدول بدون فهرس ومع عرض كامل للمحتوى
            st.table(level_courses[["رمز المقرر", "اسم المقرر", "عدد الساعات"]])
            # لا حاجة لـ st.markdown("---") هنا لأن st.table تضيف فاصلاً بصرياً

