# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
# Assuming github_helpers exists in the specified path
# !! Temporarily comment out the import to isolate potential issues !!
# from pages.utils.github_helpers import get_github_file_content, get_available_years, get_available_reports

# --- إعدادات الصفحة ---
# Ensure this is the very first Streamlit command
st.set_page_config(
    page_title="بكالوريوس في القرآن وعلومه",
    page_icon="📚",
    layout="wide"
)

# --- CSS مخصص لدعم RTL وتنسيقات أساسية ---
st.markdown("""
<style>
    /* تعديلات عامة لدعم RTL */
    .stApp { direction: rtl; text-align: right; }
    h1, h2, h3, h4, h5, h6 { text-align: right; }
    .stDataFrame { text-align: right; }
    /* محاذاة عناصر التحكم الرئيسية إذا لزم الأمر */
    .stSelectbox [data-baseweb="select"] > div { text-align: right !important; }
    .stSelectbox [data-baseweb="select"] input { text-align: right !important; }
    /* تعديل خاص للمخططات البيانية لضمان العرض الصحيح */
    .plotly { direction: ltr; }
    /* إخفاء الشريط الجانبي الافتراضي إذا ظهر */
    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# --- تعريفات أساسية ---
program_code = "bachelor_quran"
program_title = "📚 بكالوريوس في القرآن وعلومه"
st.title(program_title)
st.write("--- صفحة قيد الاختبار ---") # Add a marker

# --- محدد السنة (بيانات وهمية مؤقتًا) ---
# !! Temporarily use dummy data instead of calling get_available_years !!
available_years = [1445, 1444, 1443]
# data_file_map = {1445: "path/to/1445.csv", 1444: "path/to/1444.csv", 1443:"path/to/1443.csv"} # Dummy map
selected_year = None

if available_years:
    selected_year = st.selectbox(
        "اختر السنة الأكاديمية لعرض بياناتها:",
        available_years,
        key=f'year_selector_{program_code}'
    )
else:
    st.warning("لا توجد بيانات سنوية متاحة لهذا البرنامج (بيانات وهمية).")

# --- عرض محتوى الصفحة بناءً على السنة المختارة (مُعلق مؤقتًا) ---
if selected_year:
    st.info(f"تم اختيار عام {selected_year}. سيتم عرض البيانات هنا لاحقًا.")
    st.divider()

    # --- الأقسام التالية معلقة للتشخيص ---

    # # --- 1. نبذة مختصرة ومعلومات عامة (ثابتة) ---
    # with st.expander("نبذة عن البرنامج وأهدافه", expanded=False):
    #     st.subheader("رسالة البرنامج")
    #     st.write("إعداد كفاءات متخصصة...") # Placeholder
    #     st.subheader("أهداف البرنامج")
    #     st.markdown("- القدرة على تسميع...") # Placeholder

    # st.divider()

    # # --- تحميل وعرض البيانات والمؤشرات للسنة المختارة ---
    # st.header(f"المؤشرات والبيانات لعام {selected_year}")
    # # !! Temporarily skip data loading and processing !!
    # # if selected_year in data_file_map:
    #     # df = get_github_file_content(data_file_map[selected_year])
    #     # if isinstance(df, pd.DataFrame) and not df.empty:
    #         # --- 2. المؤشرات (Indicators) ---
    #         # st.subheader("جدول المؤشرات التفصيلي")
    #         # st.dataframe(df, use_container_width=True)
    #         # ... (plotting code commented out) ...
    #         # --- 3. الاتجاهات (Trends) ---
    #         # ... (trend plotting code commented out) ...
    #     # else:
    #     #     st.error(f"تعذر تحميل البيانات لعام {selected_year}")
    # # else:
    # #     st.error(f"لا يوجد ملف بيانات مرتبط بالسنة المختارة: {selected_year}")


    # st.divider()

    # # --- 4. معلومات إضافية للسنة المختارة ---
    # with st.expander(f"ملخص وأبرز نقاط التقرير السنوي لعام {selected_year}", expanded=False):
    #     st.info("سيتم عرض ملخص التقرير السنوي هنا.")

    # st.divider()

    # # --- 5. تحميل الملفات (File Downloads) للسنة المختارة ---
    # st.header(f"تحميل المستندات لعام {selected_year}")
    # st.info("سيتم إضافة أزرار تحميل ملفات PDF هنا.")

# --- نهاية كود الصفحة ---
```

**الخطوات التالية:**

1.  **جرب تشغيل التطبيق بهذا الكود المبسط.** هل تظهر صفحة "بكالوريوس في القرآن وعلومه" الآن أم لا يزال يظهر خطأ "Page not found"؟
2.  **إذا نجح التحميل:** ابدأ بإزالة التعليقات تدريجيًا:
    * أولاً، أعد تفعيل استيراد `from pages.utils.github_helpers import ...`. هل لا تزال الصفحة تعمل؟ (إذا فشلت هنا، فالمشكلة في `github_helpers.py` أو في `st.secrets`).
    * ثانيًا، أعد تفعيل استدعاء `get_available_years` بدلاً من البيانات الوهمية. هل لا تزال تعمل؟
    * ثالثًا، أعد تفعيل استدعاء `get_github_file_content` وعرض الجدول `st.dataframe(df, ...)`. هل لا تزال تعمل؟
    * رابعًا، أعد تفعيل كود الرسوم البيانية.
    * خامسًا، أعد تفعيل كود تحميل الملفات (بعد التأكد من صحة الدوال المساعدة).
3.  **إذا فشل التحميل حتى مع الكود المبسط:** تأكد تمامًا من اسم الملف (`01_📚_بكالوريوس في القرآن وعلومه.py`) وموقعه (داخل مجلد `pages`).

أخبرني بنتيجة تجربة الكود المبسط لنحدد الخطوة التال
