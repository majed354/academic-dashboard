import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(
    page_title="Faculty Members",
    page_icon="👥",
    layout="wide"
)

st.title("👥 أعضاء هيئة التدريس")
st.write("صفحة عرض معلومات أعضاء هيئة التدريس في جميع البرامج الأكاديمية")

# بيانات أعضاء هيئة التدريس (نموذج تجريبي)
def load_faculty_data():
    # يمكن تعديل هذه الدالة لاحقًا لتحميل البيانات من GitHub
    data = {
        "الاسم": ["د. محمد أحمد", "د. عبدالله محمد", "د. فاطمة علي", "د. خالد إبراهيم", 
                  "د. عائشة سعد", "د. علي حسن", "د. نورة خالد", "د. سارة ناصر"],
        "الدرجة العلمية": ["أستاذ", "أستاذ مشارك", "أستاذ مساعد", "أستاذ مساعد", 
                           "أستاذ", "أستاذ مشارك", "أستاذ مساعد", "محاضر"],
        "التخصص": ["علوم القرآن", "القراءات", "التفسير", "علوم القرآن", 
                    "القراءات", "التفسير", "علوم القرآن", "القراءات"],
        "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", 
                     "دكتوراه علوم القرآن", "دكتوراه القراءات", "بكالوريوس في القرآن وعلومه", "ماجستير القراءات"],
        "الأبحاث المنشورة": [15, 8, 12, 7, 20, 14, 5, 9],
        "سنوات الخبرة": [18, 12, 8, 10, 22, 16, 6, 9]
    }
    return pd.DataFrame(data)

# تحميل البيانات
faculty_df = load_faculty_data()

# عناصر التحكم في الشريط الجانبي
st.sidebar.header("تصفية البيانات")

# تصفية حسب البرنامج
all_programs = ["جميع البرامج"] + faculty_df["البرنامج"].unique().tolist()
selected_program = st.sidebar.selectbox("اختر البرنامج:", all_programs)

# تصفية حسب الدرجة العلمية
all_degrees = ["جميع الدرجات العلمية"] + faculty_df["الدرجة العلمية"].unique().tolist()
selected_degree = st.sidebar.selectbox("الدرجة العلمية:", all_degrees)

# تطبيق التصفية
filtered_df = faculty_df.copy()
if selected_program != "جميع البرامج":
    filtered_df = filtered_df[filtered_df["البرنامج"] == selected_program]
if selected_degree != "جميع الدرجات العلمية":
    filtered_df = filtered_df[filtered_df["الدرجة العلمية"] == selected_degree]

# عرض النتائج
st.header("قائمة أعضاء هيئة التدريس")
st.dataframe(filtered_df, use_container_width=True)

# إحصائيات وتحليلات
st.header("إحصائيات أعضاء هيئة التدريس")

col1, col2 = st.columns(2)

with col1:
    # توزيع الأعضاء حسب البرنامج
    program_counts = faculty_df["البرنامج"].value_counts().reset_index()
    program_counts.columns = ["البرنامج", "عدد الأعضاء"]

    fig1 = px.pie(
        program_counts, 
        values="عدد الأعضاء", 
        names="البرنامج", 
        title="توزيع أعضاء هيئة التدريس حسب البرنامج"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # توزيع الأعضاء حسب الدرجة العلمية
    degree_counts = faculty_df["الدرجة العلمية"].value_counts().reset_index()
    degree_counts.columns = ["الدرجة العلمية", "عدد الأعضاء"]

    fig2 = px.bar(
        degree_counts, 
        x="الدرجة العلمية", 
        y="عدد الأعضاء", 
        title="توزيع أعضاء هيئة التدريس حسب الدرجة العلمية"
    )
    st.plotly_chart(fig2, use_container_width=True)

# معلومات تفصيلية
st.header("المعلومات التفصيلية لأعضاء هيئة التدريس")
st.write("اختر عضو هيئة تدريس من القائمة لعرض معلوماته التفصيلية")

selected_faculty = st.selectbox("اختر عضو هيئة تدريس:", faculty_df["الاسم"])
if selected_faculty:
    faculty_info = faculty_df[faculty_df["الاسم"] == selected_faculty].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**الاسم**: {faculty_info['الاسم']}")
        st.info(f"**الدرجة العلمية**: {faculty_info['الدرجة العلمية']}")
    with col2:
        st.info(f"**التخصص**: {faculty_info['التخصص']}")
        st.info(f"**البرنامج**: {faculty_info['البرنامج']}")
    with col3:
        st.info(f"**الأبحاث المنشورة**: {faculty_info['الأبحاث المنشورة']}")
        st.info(f"**سنوات الخبرة**: {faculty_info['سنوات الخبرة']}")

    # عرض بيانات وهمية عن المواد التي يدرسها
    st.subheader("المواد التي يدرسها")
    courses = {
        "رمز المقرر": ["QUR101", "QUR202", "QUR305"],
        "اسم المقرر": ["مدخل لعلوم القرآن", "أصول التفسير", "مناهج المفسرين"],
        "الفصل الدراسي": ["الأول", "الثاني", "الأول"]
    }
    st.dataframe(pd.DataFrame(courses))

    # رسم بياني لتطور الأبحاث
    st.subheader("تطور الأبحاث المنشورة (نموذج)")
    research_data = {
        "السنة": [2019, 2020, 2021, 2022, 2023],
        "عدد الأبحاث": [2, 3, 1, 4, 3]
    }
    research_df = pd.DataFrame(research_data)
    fig = px.line(
        research_df, 
        x="السنة", 
        y="عدد الأبحاث", 
        markers=True,
        title=f"الإنتاج البحثي لـ {selected_faculty}"
    )
    st.plotly_chart(fig)
