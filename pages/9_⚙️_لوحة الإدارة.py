import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ لوحة الإدارة")
st.warning("هذه الصفحة للمستخدمين المخولين فقط. يمكن حمايتها بصلاحيات خاصة.")

# تسجيل الدخول البسيط
def check_password():
    # غالبًا يتم استخدام مكتبة خارجية مثل streamlit-authenticator بدلاً من هذا النهج البسيط
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل الدخول"):
        # في الاستخدام الحقيقي، استخدم تحقق آمن لكلمة المرور
        if username == "admin" and password == "admin123":
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("خطأ في اسم المستخدم أو كلمة المرور")

    return False

if check_password():
    # تبويبات لوحة الإدارة
    tabs = st.tabs([
        "إدارة البيانات", 
        "إدارة التقارير", 
        "إدارة المستخدمين",
        "التقارير المجمعة"
    ])

    with tabs[0]:
        st.header("تحميل وتعديل البيانات")

        # اختيار البرنامج
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

        # تحميل ملف بيانات
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
                    # في التطبيق الحقيقي، هنا يتم حفظ البيانات في GitHub
                    st.success(f"تم حفظ البيانات لبرنامج {selected_program} للعام {selected_year}")

                    # محاكاة تأخير قصير للعملية
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)

                    st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

        # تعديل توصيف المقررات
        st.subheader("تعديل توصيف المقررات")

        course_code = st.text_input("رمز المقرر:", value="QUR101")
        course_name = st.text_input("اسم المقرر:", value="مدخل لعلوم القرآن")
        credit_hours = st.number_input("عدد الساعات:", min_value=1, max_value=5, value=3)
        description = st.text_area("توصيف المقرر:", value="يهدف هذا المقرر إلى تعريف الطالب بالمفاهيم الأساسية لعلوم القرآن...")

        if st.button("حفظ توصيف المقرر"):
            st.success(f"تم حفظ توصيف المقرر {course_code} - {course_name}")

    with tabs[1]:
        st.header("إدارة التقارير")

        # رفع تقرير جديد
        st.subheader("رفع تقرير جديد")

        report_program = st.selectbox("البرنامج:", program_options, key="report_program")
        report_year = st.number_input("العام:", min_value=2020, max_value=2025, value=2024, key="report_year")
        report_type = st.selectbox("نوع التقرير:", ["تقرير سنوي", "توصيف البرنامج", "خطة تطوير"])

        uploaded_report = st.file_uploader("حدد ملف التقرير (PDF/Word):", type=["pdf", "docx", "md"])

        if uploaded_report is not None:
            st.success(f"تم تحميل ملف {uploaded_report.name} بنجاح.")

            if st.button("حفظ التقرير"):
                # في التطبيق الحقيقي، هنا يتم حفظ التقرير في GitHub
                st.success(f"تم حفظ {report_type} لبرنامج {report_program} للعام {report_year}")

                # محاكاة تأخير قصير للعملية
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)

        # قائمة التقارير
        st.subheader("قائمة التقارير الحالية")

        # بيانات تجريبية للتقارير
        reports_data = {
            "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", 
                        "ماجستير الدراسات القرآنية المعاصرة", "بكالوريوس في القرآن وعلومه"],
            "العام": [2024, 2024, 2023, 2023],
            "نوع التقرير": ["تقرير سنوي", "توصيف البرنامج", "تقرير سنوي", "خطة تطوير"],
            "تاريخ الرفع": ["2024-03-15", "2024-02-20", "2023-12-10", "2023-10-05"],
            "الحجم": ["1.2 MB", "3.4 MB", "900 KB", "2.1 MB"]
        }
        reports_df = pd.DataFrame(reports_data)

        st.dataframe(reports_df, use_container_width=True)

    with tabs[2]:
        st.header("إدارة المستخدمين")

        # إضافة مستخدم جديد
        st.subheader("إضافة مستخدم جديد")

        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("اسم المستخدم:")
            new_password = st.text_input("كلمة المرور:", type="password")
            confirm_password = st.text_input("تأكيد كلمة المرور:", type="password")

        with col2:
            full_name = st.text_input("الاسم الكامل:")
            role = st.selectbox("الدور:", ["مشرف", "محرر", "مستخدم عادي"])
            email = st.text_input("البريد الإلكتروني:")

        if st.button("إضافة المستخدم"):
            if new_password != confirm_password:
                st.error("كلمة المرور وتأكيدها غير متطابقين")
            elif not new_username or not new_password:
                st.error("يرجى ملء جميع الحقول المطلوبة")
            else:
                st.success(f"تم إضافة المستخدم {new_username} بنجاح")

        # قائمة المستخدمين
        st.subheader("قائمة المستخدمين")

        # بيانات تجريبية للمستخدمين
        users_data = {
            "اسم المستخدم": ["admin", "editor1", "user1", "user2"],
            "الاسم الكامل": ["مدير النظام", "محمد أحمد", "سارة محمد", "أحمد علي"],
            "الدور": ["مشرف", "محرر", "مستخدم عادي", "مستخدم عادي"],
            "البريد الإلكتروني": ["admin@example.com", "editor1@example.com", "user1@example.com", "user2@example.com"],
            "تاريخ الإنشاء": ["2023-01-10", "2023-05-20", "2023-08-15", "2024-02-05"],
            "آخر تسجيل دخول": ["2024-04-19", "2024-04-15", "2024-04-10", "2024-04-05"]
        }
        users_df = pd.DataFrame(users_data)

        # إضافة أزرار للإجراءات
        users_df["الإجراءات"] = None
        st.dataframe(users_df, use_container_width=True)

        # حذف مستخدم
        st.subheader("حذف مستخدم")

        user_to_delete = st.selectbox("اختر المستخدم للحذف:", users_df["اسم المستخدم"])
        if st.button("حذف المستخدم"):
            st.warning(f"هل أنت متأكد من حذف المستخدم {user_to_delete}؟")
            confirm_delete = st.button("تأكيد الحذف")
            if confirm_delete:
                st.success(f"تم حذف المستخدم {user_to_delete} بنجاح")

    with tabs[3]:
        st.header("التقارير المجمعة")

        # إنشاء تقرير مجمع
        st.subheader("إنشاء تقرير مجمع")

        report_type = st.selectbox(
            "نوع التقرير:", 
            ["تقرير أداء جميع البرامج", "تقرير تقييمات المقررات", "تقرير استطلاعات الرأي"]
        )

        report_year = st.selectbox("العام:", [2024, 2023, 2022, 2021, 2020])

        include_charts = st.checkbox("تضمين الرسوم البيانية", value=True)
        include_comments = st.checkbox("تضمين التعليقات والملاحظات", value=True)

        if st.button("إنشاء التقرير"):
            # محاكاة إنشاء التقرير
            st.info("جاري إنشاء التقرير...")

            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)

            st.success("تم إنشاء التقرير بنجاح")

            # زر تنزيل التقرير (وهمي)
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_name = f"{report_type}_{report_year}_{current_date}.pdf"

            st.download_button(
                label="تنزيل التقرير",
                data=b"محتوى تجريبي للتقرير",  # محتوى وهمي للتنزيل
                file_name=file_name,
                mime="application/pdf"
            )

        # تصدير البيانات
        st.subheader("تصدير البيانات")

        export_options = st.multiselect(
            "اختر البيانات للتصدير:",
            ["بيانات أداء البرامج", "بيانات التقييمات", "بيانات الاستطلاعات", "بيانات أعضاء هيئة التدريس"]
        )

        export_format = st.radio("صيغة التصدير:", ["Excel (.xlsx)", "CSV (.csv)"])

        if export_options and st.button("تصدير البيانات"):
            # محاكاة تصدير البيانات
            st.info("جاري تصدير البيانات...")

            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            st.success("تم تصدير البيانات بنجاح")

            # زر تنزيل البيانات (وهمي)
            format_ext = ".xlsx" if export_format.startswith("Excel") else ".csv"
            file_name = f"البيانات_المجمعة_{datetime.now().strftime('%Y-%m-%d')}{format_ext}"

            st.download_button(
                label="تنزيل البيانات",
                data=b"محتوى تجريبي للبيانات",  # محتوى وهمي للتنزيل
                file_name=file_name,
                mime="application/octet-stream"
            )
