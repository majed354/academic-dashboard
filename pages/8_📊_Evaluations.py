import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# إعدادات الصفحة
st.set_page_config(
    page_title="Evaluations & Surveys",
    page_icon="📊",
    layout="wide"
)

st.title("📊 التقييمات والاستطلاعات")
st.write("صفحة عرض نتائج تقييمات المقررات واستطلاعات الرأي")

# بيانات تجريبية للتقييمات
def generate_evaluation_data():
    # بيانات تجريبية لتقييمات المقررات
    programs = [
        "بكالوريوس في القرآن وعلومه",
        "بكالوريوس القراءات",
        "ماجستير الدراسات القرآنية المعاصرة",
        "ماجستير القراءات",
        "دكتوراه علوم القرآن",
        "دكتوراه القراءات"
    ]

    years = [2020, 2021, 2022, 2023, 2024]
    courses = [
        {"رمز": "QUR101", "اسم": "مدخل لعلوم القرآن"},
        {"رمز": "QUR202", "اسم": "أصول التفسير"},
        {"رمز": "QUR305", "اسم": "مناهج المفسرين"},
        {"رمز": "READ101", "اسم": "القراءات العشر"},
        {"رمز": "READ202", "اسم": "الشاطبية"},
        {"رمز": "CONT305", "اسم": "مناهج المعاصرين"}
    ]

    aspects = [
        "محتوى المقرر",
        "طريقة التدريس",
        "تفاعل الأستاذ",
        "أساليب التقييم",
        "المصادر والمراجع"
    ]

    data = []

    for year in years:
        for program in programs:
            num_courses = np.random.randint(2, 5)  # عدد عشوائي من المقررات لكل برنامج
            for _ in range(num_courses):
                course = np.random.choice(courses)
                for aspect in aspects:
                    # توليد تقييم عشوائي مع ميل لتحسن مع مرور السنوات
                    base_score = np.random.randint(70, 90)
                    improvement = (year - 2020) * np.random.randint(1, 3)
                    score = min(100, base_score + improvement)

                    data.append({
                        "العام": year,
                        "البرنامج": program,
                        "رمز المقرر": course["رمز"],
                        "اسم المقرر": course["اسم"],
                        "جانب التقييم": aspect,
                        "نسبة الرضا": score
                    })

    return pd.DataFrame(data)

# بيانات تجريبية لاستطلاعات الرأي
def generate_survey_data():
    # بيانات تجريبية لاستطلاعات رضا الطلاب والخريجين
    categories = ["رضا الطلاب", "رضا الخريجين", "رضا أصحاب العمل"]
    years = [2020, 2021, 2022, 2023, 2024]
    programs = [
        "بكالوريوس في القرآن وعلومه",
        "بكالوريوس القراءات",
        "ماجستير الدراسات القرآنية المعاصرة",
        "ماجستير القراءات",
        "دكتوراه علوم القرآن",
        "دكتوراه القراءات"
    ]

    aspects = [
        "البيئة التعليمية",
        "المناهج الدراسية",
        "خدمات الطلاب",
        "المهارات المكتسبة",
        "فرص التوظيف"
    ]

    data = []

    for category in categories:
        for year in years:
            for program in programs:
                for aspect in aspects:
                    # توليد نسبة رضا عشوائية مع ميل لتحسن مع مرور السنوات
                    base_score = np.random.randint(65, 85)
                    improvement = (year - 2020) * np.random.randint(1, 3)
                    score = min(100, base_score + improvement)

                    data.append({
                        "نوع الاستطلاع": category,
                        "العام": year,
                        "البرنامج": program,
                        "جانب التقييم": aspect,
                        "نسبة الرضا": score
                    })

    return pd.DataFrame(data)

# تحميل البيانات
eval_df = generate_evaluation_data()
survey_df = generate_survey_data()

# تبويبات لعرض التقييمات والاستطلاعات
tab1, tab2 = st.tabs(["تقييم المقررات", "استطلاعات الرأي"])

with tab1:
    st.header("تقييم المقررات الدراسية")

    # عناصر التحكم للتصفية
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year_eval = st.selectbox(
            "اختر العام الدراسي:", 
            eval_df["العام"].unique(),
            key="eval_year"
        )

    with col2:
        selected_program_eval = st.selectbox(
            "اختر البرنامج:", 
            ["جميع البرامج"] + eval_df["البرنامج"].unique().tolist(),
            key="eval_program"
        )

    with col3:
        all_courses = eval_df[["رمز المقرر", "اسم المقرر"]].drop_duplicates()
        all_courses["المقرر الكامل"] = all_courses["رمز المقرر"] + " - " + all_courses["اسم المقرر"]

        selected_course = st.selectbox(
            "اختر المقرر:", 
            ["جميع المقررات"] + all_courses["المقرر الكامل"].tolist(),
            key="eval_course"
        )

    # تطبيق التصفية
    filtered_eval = eval_df[eval_df["العام"] == selected_year_eval]

    if selected_program_eval != "جميع البرامج":
        filtered_eval = filtered_eval[filtered_eval["البرنامج"] == selected_program_eval]

    if selected_course != "جميع المقررات":
        course_code = selected_course.split(" - ")[0]
        filtered_eval = filtered_eval[filtered_eval["رمز المقرر"] == course_code]

    # عرض النتائج
    if not filtered_eval.empty:
        # نظرة عامة
        st.subheader("نظرة عامة على التقييمات")

        # متوسط نسب الرضا لكل جانب
        avg_by_aspect = filtered_eval.groupby("جانب التقييم")["نسبة الرضا"].mean().reset_index()

        fig = px.bar(
            avg_by_aspect, 
            x="جانب التقييم", 
            y="نسبة الرضا",
            title=f"متوسط نسب الرضا لجوانب التقييم ({selected_year_eval})",
            color="نسبة الرضا",
            color_continuous_scale="Viridis",
            range_y=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)

        # تفاصيل التقييمات
        st.subheader("تفاصيل تقييمات المقررات")

        # إذا تم تحديد مقرر محدد
        if selected_course != "جميع المقررات":
            course_name = selected_course.split(" - ")[1]
            st.write(f"تفاصيل تقييم مقرر: **{selected_course}**")

            # إنشاء رسم راداري لتقييم المقرر
            fig = px.line_polar(
                filtered_eval, 
                r="نسبة الرضا", 
                theta="جانب التقييم",
                line_close=True,
                range_r=[0, 100],
                title=f"تقييم مقرر {course_name} ({selected_year_eval})"
            )
            st.plotly_chart(fig, use_container_width=True)

            # عرض البيانات كجدول
            st.dataframe(
                filtered_eval[["جانب التقييم", "نسبة الرضا"]].sort_values("جانب التقييم"),
                use_container_width=True
            )
        else:
            # عرض جميع المقررات
            pivoted = filtered_eval.pivot_table(
                index=["رمز المقرر", "اسم المقرر"],
                columns="جانب التقييم",
                values="نسبة الرضا",
                aggfunc="mean"
            ).reset_index()

            # إضافة عمود المتوسط العام
            pivoted["المتوسط العام"] = pivoted.iloc[:, 2:].mean(axis=1)

            # ترتيب حسب المتوسط العام تنازليًا
            pivoted = pivoted.sort_values("المتوسط العام", ascending=False)

            st.dataframe(pivoted, use_container_width=True)
    else:
        st.warning("لا توجد بيانات تقييم متاحة للمعايير المحددة")

with tab2:
    st.header("استطلاعات الرأي")

    # عناصر التحكم للتصفية
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_survey = st.selectbox(
            "نوع الاستطلاع:", 
            survey_df["نوع الاستطلاع"].unique(),
            key="survey_type"
        )

    with col2:
        selected_year_survey = st.selectbox(
            "العام الدراسي:", 
            survey_df["العام"].unique(),
            key="survey_year"
        )

    with col3:
        selected_program_survey = st.selectbox(
            "البرنامج:", 
            ["جميع البرامج"] + survey_df["البرنامج"].unique().tolist(),
            key="survey_program"
        )

    # تطبيق التصفية
    filtered_survey = survey_df[
        (survey_df["نوع الاستطلاع"] == selected_survey) & 
        (survey_df["العام"] == selected_year_survey)
    ]

    if selected_program_survey != "جميع البرامج":
        filtered_survey = filtered_survey[filtered_survey["البرنامج"] == selected_program_survey]

    # عرض النتائج
    if not filtered_survey.empty:
        st.subheader(f"نتائج استطلاع {selected_survey} لعام {selected_year_survey}")

        # رسم بياني لنتائج الاستطلاع
        if selected_program_survey == "جميع البرامج":
            # مقارنة بين البرامج
            avg_by_program = filtered_survey.groupby(["البرنامج", "جانب التقييم"])["نسبة الرضا"].mean().reset_index()

            fig = px.bar(
                avg_by_program, 
                x="جانب التقييم", 
                y="نسبة الرضا", 
                color="البرنامج",
                barmode="group",
                title=f"مقارنة نتائج {selected_survey} بين البرامج ({selected_year_survey})",
                range_y=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # رسم مفصل للبرنامج المحدد
            fig = px.bar(
                filtered_survey, 
                x="جانب التقييم", 
                y="نسبة الرضا",
                title=f"نتائج {selected_survey} لبرنامج {selected_program_survey} ({selected_year_survey})",
                color="نسبة الرضا",
                color_continuous_scale="Viridis",
                range_y=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)

        # تطور النتائج عبر السنوات
        st.subheader("تطور النتائج عبر السنوات")

        # الحصول على بيانات جميع السنوات للمقارنة
        trend_data = survey_df[survey_df["نوع الاستطلاع"] == selected_survey]
        if selected_program_survey != "جميع البرامج":
            trend_data = trend_data[trend_data["البرنامج"] == selected_program_survey]

        # متوسط للجوانب حسب السنة
        trend_avg = trend_data.groupby(["العام"])["نسبة الرضا"].mean().reset_index()

        fig = px.line(
            trend_avg, 
            x="العام", 
            y="نسبة الرضا",
            markers=True,
            title=f"تطور متوسط نتائج {selected_survey} عبر السنوات",
            range_y=[60, 100]
        )
        st.plotly_chart(fig, use_container_width=True)

        # جدول تفصيلي
        st.subheader("تفاصيل نتائج الاستطلاع")
        st.dataframe(
            filtered_survey[["البرنامج", "جانب التقييم", "نسبة الرضا"]].sort_values(["البرنامج", "جانب التقييم"]),
            use_container_width=True
        )
    else:
        st.warning("لا توجد بيانات استطلاع متاحة للمعايير المحددة")

# نموذج استطلاع جديد
with st.expander("استطلاع رأي جديد", expanded=False):
    st.subheader("استطلاع رأي الطلاب")
    st.write("هذا نموذج تجريبي لاستطلاع رأي الطلاب. يمكن تعديله حسب متطلبات الكلية.")

    # نموذج الاستطلاع
    with st.form("survey_form"):
        st.selectbox("البرنامج الأكاديمي:", programs)
        st.selectbox("المستوى الدراسي:", ["الأول", "الثاني", "الثالث", "الرابع"])

        st.write("**تقييم البرنامج**")
        st.slider("محتوى المقررات الدراسية:", 0, 10, 5)
        st.slider("طرق التدريس المستخدمة:", 0, 10, 5)
        st.slider("خدمات الإرشاد الأكاديمي:", 0, 10, 5)
        st.slider("المرافق والتجهيزات:", 0, 10, 5)
        st.slider("الأنشطة اللاصفية:", 0, 10, 5)

        st.text_area("ملاحظات ومقترحات:")

        submit = st.form_submit_button("إرسال الاستطلاع")

        if submit:
            st.success("تم استلام الاستطلاع بنجاح! شكرًا لمشاركتك.")
