# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
# Removed: from streamlit_pdf_viewer import pdf_viewer
# Assuming github_helpers exists in the specified path
from pages.utils.github_helpers import get_github_file_content, get_available_years, get_available_reports

# --- إعدادات الصفحة ---
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

# --- محدد السنة ---
available_years, data_file_map = get_available_years(program_code)
selected_year = None # Initialize selected_year

if available_years:
    # Place year selector at the top of the main page area
    selected_year = st.selectbox(
        "اختر السنة الأكاديمية لعرض بياناتها:",
        available_years,
        key=f'year_selector_{program_code}' # Unique key per program page
    )
else:
    st.warning("لا توجد بيانات سنوية متاحة لهذا البرنامج.")

# --- عرض محتوى الصفحة بناءً على السنة المختارة ---
if selected_year:
    st.info(f"عرض بيانات عام {selected_year}")
    st.divider()

    # --- 1. نبذة مختصرة ومعلومات عامة (ثابتة) ---
    with st.expander("نبذة عن البرنامج وأهدافه", expanded=False):
        st.subheader("رسالة البرنامج")
        # Placeholder - استبدل هذا النص بالرسالة الفعلية من ملف التوصيف أو الدليل
        st.write("""
        إعداد كفاءات متخصصة وتأهيلهم للعمل المهني في مجال تعليم القرآن وعلومه، بما يلبي حاجة المجتمع والبحث العلمي.
        """)

        st.subheader("أهداف البرنامج")
        # Placeholder - استبدل هذه القائمة بالأهداف الفعلية
        st.markdown("""
        - القدرة على تسميع وتلاوة كتاب الله عز وجل بمهارة عالية وإتقان.
        - التميز في تطبيق أحكام التلاوة وعلوم الآلة.
        - تأهيل معلمين متخصصين في مجال تعليم القرآن الكريم وعلومه.
        - التميز في كتابة بحوث علمية متخصصة في مجال القرآن وعلومه.
        - تكوين الملكة العلميّة لدى الطالب المبنيّة على التحليل والاستنباط والاستدلال ومناهج البحث العلمي.
        - المشاركة في خدمة المجتمع من خلال نشر الثقافة القرآنية.
        - تعزيز القيم الأخلاقية القرآنية وتحسين مهارات التواصل.
        - إعداد وتنمية الكوادر البشرية بما يواكب التوجهات الحديثة ويتواءم مع رؤية ٢٠٣٠.
        """)
        # يمكن إضافة معلومات ثابتة أخرى هنا مثل متطلبات القبول، الفرص الوظيفية، إلخ.

    st.divider()

    # --- تحميل وعرض البيانات والمؤشرات للسنة المختارة ---
    if selected_year in data_file_map:
        st.header(f"المؤشرات والبيانات لعام {selected_year}")
        # افترض أن get_github_file_content يعيد DataFrame لمؤشرات السنة أو بياناتها
        df = get_github_file_content(data_file_map[selected_year])

        if isinstance(df, pd.DataFrame) and not df.empty:
            # --- 2. المؤشرات (Indicators) ---
            st.subheader("جدول المؤشرات التفصيلي")
            # عرض البيانات بتنسيق جدول (يمكن تخصيص الأعمدة لاحقًا)
            st.dataframe(df, use_container_width=True)

            # رسم بياني لمقارنة النسبة بالهدف (إذا كانت الأعمدة موجودة)
            if "النسبة المئوية" in df.columns and "الهدف" in df.columns and "المعيار" in df.columns:
                st.subheader("مقارنة النسب المئوية بالأهداف")
                try:
                    # Ensure numeric types for plotting
                    df["النسبة المئوية"] = pd.to_numeric(df["النسبة المئوية"], errors='coerce')
                    df["الهدف"] = pd.to_numeric(df["الهدف"], errors='coerce')
                    df_plot = df.dropna(subset=["النسبة المئوية", "الهدف"]) # Drop rows where conversion failed

                    if not df_plot.empty:
                        fig_compare = px.bar(
                            df_plot,
                            x="المعيار",
                            y=["النسبة المئوية", "الهدف"],
                            barmode="group",
                            title=f"مؤشرات الأداء لعام {selected_year}",
                            labels={"value": "النسبة المئوية", "variable": "المقياس"}
                        )
                        # Apply custom layout (assuming prepare_chart_layout is defined or imported)
                        # fig_compare = prepare_chart_layout(fig_compare, f"مؤشرات الأداء لعام {selected_year}", chart_type="bar") # Requires prepare_chart_layout
                        fig_compare.update_layout(
                             font=dict(family="Tajawal"),
                             legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5) # Basic bottom legend
                        )
                        st.plotly_chart(fig_compare, use_container_width=True)
                    else:
                        st.warning("لا توجد بيانات رقمية صالحة لعرض رسم المقارنة.")
                except Exception as e:
                    st.error(f"خطأ في إنشاء رسم المقارنة: {e}")

            # --- 3. الاتجاهات (Trends) ---
            # رسم بياني للاتجاه والتطور (إذا لم تكن أقدم سنة)
            if available_years and selected_year != available_years[-1]:
                st.subheader("تطور المؤشرات عبر السنوات")
                trend_data = []
                years_to_include = [y for y in available_years if y <= selected_year] # Include selected year and previous

                for year in reversed(years_to_include): # Iterate from oldest to selected
                    if year in data_file_map:
                        year_df = get_github_file_content(data_file_map[year])
                        if isinstance(year_df, pd.DataFrame) and "المعيار" in year_df.columns and "النسبة المئوية" in year_df.columns:
                             # Ensure 'النسبة المئوية' is numeric
                             year_df["النسبة المئوية"] = pd.to_numeric(year_df["النسبة المئوية"], errors='coerce')
                             year_df = year_df.dropna(subset=["النسبة المئوية"])
                             for _, row in year_df.iterrows():
                                trend_data.append({
                                    "العام": str(year), # Ensure year is string for categorical axis
                                    "المعيار": row["المعيار"],
                                    "النسبة المئوية": row["النسبة المئوية"]
                                })

                if trend_data:
                    trend_df = pd.DataFrame(trend_data)
                    try:
                        fig_trend = px.line(
                            trend_df,
                            x="العام",
                            y="النسبة المئوية",
                            color="المعيار",
                            markers=True,
                            title="تطور النسب المئوية للمؤشرات حتى عام " + str(selected_year),
                            labels={"العام": "السنة الأكاديمية"}
                        )
                        # fig_trend = prepare_chart_layout(fig_trend, "تطور النسب المئوية للمؤشرات", chart_type="line") # Requires prepare_chart_layout
                        fig_trend.update_layout(
                             font=dict(family="Tajawal"),
                             legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5) # Basic bottom legend
                        )
                        st.plotly_chart(fig_trend, use_container_width=True)
                    except Exception as e:
                        st.error(f"خطأ في إنشاء رسم التطور: {e}")
                else:
                    st.warning("لا توجد بيانات كافية لعرض تطور المؤشرات.")

        else:
            st.error(f"تعذر تحميل أو معالجة البيانات لعام {selected_year} من المسار: {data_file_map[selected_year]}")

        st.divider()

        # --- 4. معلومات إضافية للسنة المختارة (مثل ملخص التقرير السنوي) ---
        with st.expander(f"ملخص وأبرز نقاط التقرير السنوي لعام {selected_year}", expanded=False):
            # Placeholder: هنا يجب إضافة كود لقراءة وتحليل التقرير السنوي للسنة المحددة
            # وعرض ملخص نصي أو نقاط القوة والضعف.
            # يتطلب هذا الوصول إلى ملف التقرير السنوي (Word أو PDF) للسنة المختارة ومعالجته.
            st.write(f"**ملاحظة:** يتطلب عرض هذا القسم قراءة ملف التقرير السنوي لعام {selected_year} واستخلاص المعلومات منه.")
            st.info("سيتم عرض ملخص التقرير السنوي هنا.")
            # مثال:
            # annual_report_summary = get_annual_report_summary(program_code, selected_year) # دالة افتراضية
            # if annual_report_summary:
            #     st.markdown(annual_report_summary)

        st.divider()

        # --- 5. تحميل الملفات (File Downloads) للسنة المختارة ---
        st.header(f"تحميل المستندات لعام {selected_year}")

        # Placeholder: يتطلب دوال مساعدة في github_helpers.py وتنظيم الملفات في المستودع
        # افترض وجود دالة get_reports_for_year(program_code, year) -> dict[filename, filepath]
        # وافترض وجود دالة get_file_bytes(filepath) -> bytes

        # --- دالة مؤقتة لقراءة البايتات (تحتاج لتنفيذ فعلي في github_helpers.py) ---
        @st.cache_data(ttl=3600) # Cache the bytes
        def get_file_bytes_placeholder(file_path_in_repo):
            # !!! استبدل هذا بالكود الفعلي لجلب الملف من GitHub باستخدام requests و st.secrets !!!
            pat = st.secrets.get("GITHUB_PAT")
            owner = st.secrets.get("GITHUB_OWNER")
            repo = st.secrets.get("GITHUB_REPO")
            if not (pat and owner and repo):
                 st.error("GitHub secrets (PAT, OWNER, REPO) not configured.")
                 return None
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path_in_repo}" # Assume main branch
            headers = {'Authorization': f'token {pat}'}
            try:
                response = requests.get(raw_url, headers=headers)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                print(f"Successfully fetched bytes for: {file_path_in_repo}") # Debug print
                return response.content
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching file '{file_path_in_repo}' from GitHub: {e}")
                return None
            except Exception as e:
                 st.error(f"An unexpected error occurred fetching file '{file_path_in_repo}': {e}")
                 return None
        # --- نهاية الدالة المؤقتة ---

        # --- دالة مؤقتة لجلب قائمة الملفات (تحتاج لتنفيذ فعلي في github_helpers.py) ---
        @st.cache_data(ttl=600) # Cache the list for 10 mins
        def get_reports_for_year_placeholder(prog_code, year):
             # !!! استبدل هذا بالكود الفعلي لجلب قائمة الملفات من GitHub API !!!
             # بناء المسار المتوقع
             reports_path = f"data/{prog_code}/reports/{year}"
             print(f"Attempting to list files in: {reports_path}") # Debug print

             # --- محاكاة للملفات المتوقعة ---
             # يجب أن يعتمد هذا على بنية المجلد الفعلية في GitHub
             expected_files = {
                 f"التقرير السنوي {year}.pdf": f"{reports_path}/التقرير السنوي {year}.pdf",
                 f"مؤشرات الأداء {year}.pdf": f"{reports_path}/مؤشرات الأداء {year}.pdf",
                 f"تقرير قياس المخرجات {year}.pdf": f"{reports_path}/تقرير قياس المخرجات {year}.pdf",
                 # أضف ملفات أخرى متوقعة هنا
             }
             # يمكنك استخدام list_github_dir_contents هنا إذا كانت تعمل بشكل صحيح
             # contents = list_github_dir_contents(reports_path)
             # if contents:
             #     actual_files = {item['name']: item['path'] for item in contents if item.get('type') == 'file'}
             #     return actual_files
             # else:
             #     print(f"Could not list contents for {reports_path}")
             #     return {} # Return empty if listing fails

             # --- استخدام القائمة المحاكاة مؤقتا ---
             return expected_files
        # --- نهاية الدالة المؤقتة ---


        available_files_for_year = get_reports_for_year_placeholder(program_code, selected_year)

        if available_files_for_year:
            file_found = False
            for file_name, file_path in available_files_for_year.items():
                # حاول تحميل الملف فقط إذا كان اسمه متوقعًا أو موجودًا فعليًا
                # (هذا الجزء يعتمد على دقة get_reports_for_year_placeholder)
                if file_name.lower().endswith(".pdf"): # Filter for PDFs or other desired types
                     print(f"Attempting to get bytes for {file_name} at {file_path}") # Debug
                     pdf_bytes = get_file_bytes_placeholder(file_path)
                     if pdf_bytes:
                         st.download_button(
                             label=f"تحميل {file_name.replace('.pdf', '')}",
                             data=pdf_bytes,
                             file_name=file_name,
                             mime="application/pdf"
                         )
                         file_found = True
                     else:
                          print(f"Failed to get bytes for {file_name}") # Debug

            if not file_found:
                 st.info(f"لم يتم العثور على ملفات PDF قابلة للتحميل لعام {selected_year} في المسار المتوقع.")

        else:
            st.info(f"لا توجد مستندات متاحة للتحميل لعام {selected_year}.")

    else:
        st.error(f"لا يوجد ملف بيانات مرتبط بالسنة المختارة: {selected_year}")

# --- نهاية كود الصفحة ---
```

**ملاحظات هامة وتعديلات مطلوبة:**

1.  **دوال `github_helpers.py`:**
    * الكود أعلاه يفترض وجود دوال مثل `get_available_years`, `get_github_file_content`, `get_reports_for_year`, `get_file_bytes`.
    * الدوال `get_reports_for_year_placeholder` و `get_file_bytes_placeholder` هي **مثالية ومؤقتة**. يجب عليك **تنفيذ المنطق الفعلي** لهذه الدوال داخل ملف `pages/utils/github_helpers.py` لتقوم بجلب قائمة الملفات ومحتوى الملفات كـ bytes من مستودع GitHub باستخدام `requests` و `st.secrets` بشكل صحيح.
2.  **تنظيم الملفات في GitHub:**
    * يجب أن تتأكد من تنظيم ملفات التقارير والبيانات في مستودع GitHub الخاص بك حسب البنية المتوقعة (مثل `data/bachelor_quran/reports/1444/`).
    * قم بتحويل ملفات Word الهامة (التقرير السنوي، التوصيف، إلخ) إلى **PDF** وضعها في المجلدات المناسبة لكل سنة.
3.  **محتوى النبذة والمعلومات:**
    * الأقسام التي تعرض "رسالة البرنامج"، "أهداف البرنامج"، و "ملخص التقرير السنوي" تحتوي حاليًا على نصوص مؤقتة أو ملاحظات. يجب عليك استبدالها بالمحتوى الفعلي المستخلص من ملفات الوثائق المرفقة.
4.  **تخصيص المؤشرات:** يمكنك تخصيص عرض المؤشرات بشكل أكبر (مثل استخدام `st.metric` لعرض أرقام رئيسية) بدلاً من عرض الجدول الكامل فقط.

بعد تنفيذ هذه التعديلات (خاصة في `github_helpers.py` وتنظيم الملفات)، يجب أن تعمل صفحة البرنامج بشكل تفاعلي وتعرض البيانات والمعلومات والملفات الخاصة بالسنة المختا
