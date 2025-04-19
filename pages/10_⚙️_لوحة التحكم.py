# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# === بيانات الاعتمادات (المستخدمين وكلمات المرور والأدوار) ===
credentials = {
    "admin":   {"password": st.secrets["ADMIN_PASSWORD"], "role": "admin"}
}

# دالة التحقق من اسم المستخدم وكلمة المرور
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل الدخول"):
        user = credentials.get(username)
        if user and user["password"] == password:
            # تم التحقق بنجاح
            st.session_state.authenticated = True
            st.session_state.user = username
            st.session_state.role = user["role"]
            st.rerun()
        else:
            st.error("خطأ في اسم المستخدم أو كلمة المرور")

    return False

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)
# إضافة CSS مخصص لدعم RTL
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
</style>
""", unsafe_allow_html=True)
st.title("⚙️ لوحة التحكم")
st.warning("هذه الصفحة للمستخدمين المخولين فقط. يمكن حمايتها بصلاحيات خاصة.")

# إذا تم تسجيل الدخول بنجاح:
if check_password():
    role = st.session_state.role

    # بناء أسماء التبويبات ديناميكياً بناءً على الدور
    tab_names = ["إدارة البيانات", "إدارة التقارير"]
    if role == "admin":
        tab_names.append("إدارة المستخدمين")
    tab_names.append("التقارير المجمعة")

    tabs = st.tabs(tab_names)
    data_tab, reports_tab, *rest = tabs
    if role == "admin":
        users_tab, summary_tab = rest
    else:
        summary_tab = rest[0]

    # ==== تبويب 1: إدارة البيانات ====
    with data_tab:
        st.header("تحميل وتعديل البيانات")

        program_options = [
            "بكالوريوس في القرآن وعلومه",
            "بكالوريوس القراءات",
            "ماجستير الدراسات القرآنية المعاصرة",
            "ماجستير القراءات",
            "دكتوراه علوم القرآن",
            "دكتوراه القراءات"
        ]
        program_codes = [
            "bachelor_quran",
            "bachelor_readings",
            "master_contemporary",
            "master_readings",
            "phd_quran",
            "phd_readings"
        ]
        program_dict = dict(zip(program_options, program_codes))

        selected_program = st.selectbox("اختر البرنامج:", program_options)
        selected_year = st.number_input("العام:", min_value=2020, max_value=2025, value=2024)

        st.subheader("تحميل ملف بيانات")
        uploaded_file = st.file_uploader("حدد ملف البيانات (CSV/Excel):", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success("تم تحميل الملف بنجاح.")
                st.dataframe(df, use_container_width=True)

                if st.button("حفظ البيانات"):
                    st.success(f"تم حفظ البيانات لبرنامج {selected_program} للعام {selected_year}")
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)
                    st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

        st.subheader("تعديل توصيف المقررات")
        course_code = st.text_input("رمز المقرر:", value="QUR101")
        course_name = st.text_input("اسم المقرر:", value="مدخل لعلوم القرآن")
        credit_hours = st.number_input("عدد الساعات:", min_value=1, max_value=5, value=3)
        description = st.text_area(
            "توصيف المقرر:",
            value="يهدف هذا المقرر إلى تعريف الطالب بالمفاهيم الأساسية لعلوم القرآن..."
        )
        if st.button("حفظ توصيف المقرر"):
            st.success(f"تم حفظ توصيف المقرر {course_code} - {course_name}")

    # ==== تبويب 2: إدارة التقارير ====
    with reports_tab:
        st.header("إدارة التقارير")
        st.subheader("رفع تقرير جديد")

        report_program = st.selectbox("البرنامج:", program_options, key="rp")
        report_year    = st.number_input("العام:", min_value=2020, max_value=2025, value=2024, key="ry")
        report_type    = st.selectbox("نوع التقرير:", ["تقرير سنوي", "توصيف البرنامج", "خطة تطوير"])
        uploaded_report = st.file_uploader("حدد ملف التقرير (PDF/Word):", type=["pdf", "docx", "md"])
        if uploaded_report is not None:
            st.success(f"تم تحميل ملف {uploaded_report.name} بنجاح.")
            if st.button("حفظ التقرير", key="save_report"):
                st.success(f"تم حفظ {report_type} لبرنامج {report_program} للعام {report_year}")
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

        st.subheader("قائمة التقارير الحالية")
        reports_data = {
            "البرنامج": [
                "بكالوريوس في القرآن وعلومه",
                "بكالوريوس القراءات",
                "ماجستير الدراسات القرآنية المعاصرة",
                "بكالوريوس في القرآن وعلومه"
            ],
            "العام": [2024, 2024, 2023, 2023],
            "نوع التقرير": ["تقرير سنوي", "توصيف البرنامج", "تقرير سنوي", "خطة تطوير"],
            "تاريخ الرفع": ["2024-03-15", "2024-02-20", "2023-12-10", "2023-10-05"],
            "الحجم": ["1.2 MB", "3.4 MB", "900 KB", "2.1 MB"]
        }
        st.dataframe(pd.DataFrame(reports_data), use_container_width=True)

    # ==== تبويب 3: إدارة المستخدمين (مشاهد فقط للمشرفين) ====
    if role == "admin":
        with users_tab:
            st.header("إدارة المستخدمين")
            st.subheader("إضافة مستخدم جديد")
            col1, col2 = st.columns(2)
            with col1:
                new_username    = st.text_input("اسم المستخدم:")
                new_password    = st.text_input("كلمة المرور:", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور:", type="password")
            with col2:
                full_name = st.text_input("الاسم الكامل:")
                role_sel  = st.selectbox("الدور:", ["admin","editor","viewer"])
                email     = st.text_input("البريد الإلكتروني:")
            if st.button("إضافة المستخدم"):
                if new_password != confirm_password:
                    st.error("كلمة المرور وتأكيدها غير متطابقين")
                elif not new_username or not new_password:
                    st.error("يرجى ملء جميع الحقول المطلوبة")
                else:
                    # هنا في التطبيق الحقيقي تحفظ الاعتماديات في قاعدة أو ملف YAML
                    st.success(f"تم إضافة المستخدم {new_username} بدور {role_sel}")

            st.subheader("قائمة المستخدمين الحالية")
            users_data = {
                "اسم المستخدم": list(credentials.keys()),
                "الدور": [u["role"] for u in credentials.values()]
            }
            st.dataframe(pd.DataFrame(users_data), use_container_width=True)

    # ==== تبويب الأخير: التقارير المجمعة ====
    with summary_tab:
        st.header("التقارير المجمعة")
        st.subheader("إنشاء تقرير مجمع")
        rpt_type = st.selectbox(
            "نوع التقرير:",
            ["تقرير أداء جميع البرامج", "تقرير تقييمات المقررات", "تقرير استطلاعات الرأي"]
        )
        rpt_year = st.selectbox("العام:", [2024, 2023, 2022, 2021, 2020])
        include_charts  = st.checkbox("تضمين الرسوم البيانية", value=True)
        include_comments = st.checkbox("تضمين التعليقات والملاحظات", value=True)

        if st.button("إنشاء التقرير", key="make_summary"):
            st.info("جاري إنشاء التقرير...")
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)
            st.success("تم إنشاء التقرير بنجاح")
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_name = f"{rpt_type}_{rpt_year}_{current_date}.pdf"
            st.download_button(
                label="تنزيل التقرير",
                data="محتوى تجريبي للتقرير",
                file_name=file_name,
                mime="application/pdf"
            )

        st.subheader("تصدير البيانات")
        export_options = st.multiselect(
            "اختر البيانات للتصدير:",
            ["أداء البرامج", "التقييمات", "الاستطلاعات", "أعضاء هيئة التدريس"]
        )
        export_format = st.radio("صيغة التصدير:", ["Excel (.xlsx)", "CSV (.csv)"])
        if export_options and st.button("تصدير البيانات", key="export_data"):
            st.info("جاري تصدير البيانات...")
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            st.success("تم تصدير البيانات بنجاح")
            ext = ".xlsx" if export_format.startswith("Excel") else ".csv"
            file_name = f"البيانات_المجمعة_{datetime.now().strftime('%Y-%m-%d')}{ext}"
            st.download_button(
                label="تنزيل البيانات",
                data="محتوى تجريبي للبيانات",
                file_name=file_name,
                mime="application/octet-stream"
            )
