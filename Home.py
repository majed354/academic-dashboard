import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils.github_helpers import get_github_file_content
from datetime import datetime
from streamlit_shadcn_ui import ui

# إعدادات الصفحة
st.set_page_config(
    page_title="لوحة مؤشرات البرامج الأكاديمية",
    page_icon="📊",
    layout="wide"
)

# CSS مخصص لدعم اللغة العربية والتخطيط
st.markdown("""
<style>
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
    }
    
    /* تنسيق العناوين الفرعية */
    h2, h3 {
        color: #1e88e5;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* تنسيق البطاقات المخصصة */
    .stat-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        height: 100%;
    }
    
    .stat-card-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .stat-card-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .stat-card-delta {
        font-size: 0.875rem;
        display: flex;
        align-items: center;
    }
    
    .delta-positive {
        color: #16a34a;
    }
    
    .delta-negative {
        color: #dc2626;
    }
    
    /* تنسيق بطاقات الأعضاء */
    .faculty-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* تنسيق الإنجازات */
    .achievement-item {
        padding: 1rem;
        border-right: 3px solid #1e88e5;
        margin-bottom: 0.75rem;
        background-color: rgba(241, 245, 249, 0.6);
        border-radius: 0.5rem;
    }
    
    /* تنسيق التبويبات */
    .custom-tabs {
        margin-bottom: 2rem;
    }
    
    /* تنسيق الخطوط */
    body {
        font-family: 'Tajawal', sans-serif;
    }
</style>

<!-- إضافة خط Tajawal من Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---- الترويسة ----
with ui.card(class_="border-0 shadow-none"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
        st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")

    with col2:
        # عرض التاريخ الحالي
        today = datetime.now().strftime("%Y/%m/%d")
        st.markdown(f"<div style='text-align: left;'>التاريخ: {today}</div>", unsafe_allow_html=True)

# رسالة ترحيبية في الشريط الجانبي
with st.sidebar:
    ui.alert(
        title="مرحباً بك في لوحة المعلومات",
        description="اختر برنامجًا من القائمة أعلاه لعرض تفاصيله",
        variant="default"
    )

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
            "عدد الطلاب": [125, 110, 90, 120, 70, 85],
            "عدد الطالبات": [85, 70, 60, 80, 50, 55],
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
            # استخدام المعلمة التالية لتوليد أرقام مناسبة
            program_index = programs.index(program)
            male_students = 60 + (year - 2020) * 5 + program_index * 10
            female_students = 40 + (year - 2020) * 5 + program_index * 8
            total_students = male_students + female_students
            
            data.append({
                "العام": year,
                "البرنامج": program,
                "عدد الطلاب": male_students,
                "عدد الطالبات": female_students,
                "المجموع": total_students,
                "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + program_index * 2),
                "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + program_index)
            })
            
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_faculty_achievements():
    """تحميل أحدث إنجازات أعضاء هيئة التدريس"""
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
    top_faculty = [
        {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"},
        {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"},
        {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"}
    ]
    return pd.DataFrame(top_faculty)

# محاولة تحميل البيانات
try:
    dept_data = load_department_summary()
    total_students = dept_data["عدد الطلاب"].sum()
    total_female_students = dept_data["عدد الطالبات"].sum()
    total_faculty = dept_data["أعضاء هيئة التدريس"].sum()
    yearly_data = load_yearly_data()
    
    # التعامل مع البيانات بشكل صحيح - استخدام أحدث عام متاح
    max_year = yearly_data["العام"].max()
    latest_year_data = yearly_data[yearly_data["العام"] == max_year].copy()
    
    faculty_achievements = load_faculty_achievements()
    top_faculty = load_top_faculty()
except Exception as e:
    ui.alert(
        title="خطأ في تحميل البيانات",
        description=f"{e}. سيتم استخدام بيانات تجريبية لأغراض العرض.",
        variant="destructive"
    )
    # إنشاء بيانات تجريبية في حالة الفشل
    total_students = 600
    total_female_students = 400
    total_faculty = 50

# ---- بطاقات المقاييس الرئيسية ----
st.subheader("المؤشرات الرئيسية")

with ui.card(class_="border-0 shadow-sm"):
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        ui.metric_card(
            title="عدد الطلاب",
            content=f"{total_students:,}",
            description="+3% منذ العام الماضي",
            trend="up"
        )
        
    with c2:
        ui.metric_card(
            title="عدد الطالبات",
            content=f"{total_female_students:,}",
            description="+7% منذ العام الماضي",
            trend="up"
        )
        
    with c3:
        ui.metric_card(
            title="معدل النجاح الإجمالي",
            content="87%",
            description="+3% منذ العام الماضي",
            trend="up"
        )
        
    with c4:
        ui.metric_card(
            title="متوسط رضا الطلاب",
            content="92%",
            description="+4% منذ العام الماضي",
            trend="up"
        )

# ---- الرسومات البيانية ----
st.subheader("تحليل البرامج الأكاديمية")

# تأكد من أن latest_year_data موجود قبل إنشاء التبويبات
if 'latest_year_data' in locals():
    # استخدام متغير لتتبع التبويب النشط
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "توزيع الطلاب والطالبات"
    
    # إنشاء تبويبات للتبديل بين التحليلات المختلفة
    tab_labels = ["توزيع الطلاب والطالبات", "مقارنة البرامج", "التطور السنوي"]
    
    with ui.tabs(value=st.session_state.active_tab):
        ui.tab("توزيع الطلاب والطالبات", id="توزيع الطلاب والطالبات")
        ui.tab("مقارنة البرامج", id="مقارنة البرامج")
        ui.tab("التطور السنوي", id="التطور السنوي")
        
    # احفظ التبويب النشط
    active_tab = st.session_state.active_tab
    
    # محتوى التبويب 1: توزيع الطلاب والطالبات
    if active_tab == "توزيع الطلاب والطالبات":
        with ui.card(class_="border-0 shadow-sm p-4"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # مخطط دائري لتوزيع إجمالي الطلاب والطالبات
                pie_data = pd.DataFrame({
                    "الفئة": ["الطلاب", "الطالبات"],
                    "العدد": [total_students, total_female_students]
                })
                
                fig_pie = px.pie(
                    pie_data, 
                    values="العدد", 
                    names="الفئة",
                    title="توزيع الطلاب والطالبات في جميع البرامج",
                    color_discrete_sequence=["#1e88e5", "#E91E63"]  # أزرق للطلاب، وردي للطالبات
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    margin=dict(t=50, b=0, l=0, r=0),
                    height=400,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # مخطط شريطي للطلاب والطالبات حسب البرنامج
                fig_bar = px.bar(
                    latest_year_data, 
                    y="البرنامج", 
                    x=["عدد الطلاب", "عدد الطالبات"],
                    title="توزيع الطلاب والطالبات حسب البرنامج",
                    orientation='h',
                    color_discrete_sequence=["#1e88e5", "#E91E63"],  
                    barmode="stack"
                )
                fig_bar.update_layout(
                    xaxis_title="عدد الطلاب والطالبات",
                    yaxis_title="البرنامج",
                    yaxis={'categoryorder':'total ascending'},
                    legend_title="الفئة",
                    height=400
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # محتوى التبويب 2: مقارنة البرامج
    elif active_tab == "مقارنة البرامج":
        with ui.card(class_="border-0 shadow-sm p-4"):
            # مخطط بياني مقارن للمؤشرات بين البرامج
            fig_indicators = px.bar(
                latest_year_data,
                x="البرنامج",
                y=["نسبة النجاح", "معدل الرضا"],
                barmode="group",
                title="مقارنة المؤشرات بين البرامج",
                labels={"value": "النسبة المئوية", "variable": "المؤشر"},
                color_discrete_sequence=["#1e88e5", "#27AE60"]
            )
            fig_indicators.update_layout(
                xaxis_title="البرنامج",
                yaxis_title="النسبة المئوية",
                legend_title="المؤشر",
                height=500
            )
            st.plotly_chart(fig_indicators, use_container_width=True)
        
            # إضافة مخطط نسبة الطالبات للطلاب
            latest_year_data["نسبة الطالبات للطلاب"] = (latest_year_data["عدد الطالبات"] / latest_year_data["عدد الطلاب"] * 100).round(1)
            
            fig_gender_ratio = px.bar(
                latest_year_data,
                x="البرنامج",
                y="نسبة الطالبات للطلاب",
                title="نسبة الطالبات إلى الطلاب في كل برنامج (%)",
                color="نسبة الطالبات للطلاب",
                color_continuous_scale="RdBu",
                text_auto='.1f'
            )
            fig_gender_ratio.update_layout(
                xaxis_title="البرنامج",
                yaxis_title="النسبة المئوية (%)",
                height=400
            )
            st.plotly_chart(fig_gender_ratio, use_container_width=True)
    
    # محتوى التبويب 3: التطور السنوي
    elif active_tab == "التطور السنوي":
        with ui.card(class_="border-0 shadow-sm p-4"):
            # اختيار البرنامج
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_program = ui.select(
                    label="اختر البرنامج لعرض تطوره السنوي:",
                    options=[{"label": prog, "value": prog} for prog in dept_data["البرنامج"].unique()],
                    default=dept_data["البرنامج"].unique()[0]
                )
            
            with col2:
                options = [
                    {"label": "الكل", "value": "الكل"},
                    {"label": "الطلاب", "value": "الطلاب"},
                    {"label": "الطالبات", "value": "الطالبات"}
                ]
                gender_option = ui.radio_group(
                    label="اختر الفئة:",
                    options=options,
                    default="الكل",
                    orientation="horizontal"
                )
            
            # تصفية البيانات حسب البرنامج المختار
            program_data = yearly_data[yearly_data["البرنامج"] == selected_program]
            
            # تأكد من وجود بيانات قبل عرض المخطط
            if not program_data.empty:
                # مخطط خطي للتطور السنوي للطلاب والطالبات
                if gender_option == "الكل":
                    y_cols = ["عدد الطلاب", "عدد الطالبات", "المجموع"]
                    colors = ["#1e88e5", "#E91E63", "#27AE60"]
                elif gender_option == "الطلاب":
                    y_cols = ["عدد الطلاب"]
                    colors = ["#1e88e5"]
                else:  # "الطالبات"
                    y_cols = ["عدد الطالبات"]
                    colors = ["#E91E63"]
                    
                fig_students = px.line(
                    program_data,
                    x="العام",
                    y=y_cols,
                    title=f"تطور أعداد الطلاب في برنامج {selected_program} (2020-2024)",
                    labels={"value": "العدد", "variable": "الفئة"},
                    markers=True,
                    color_discrete_sequence=colors
                )
                
                fig_students.update_layout(
                    xaxis_title="السنة",
                    yaxis_title="العدد",
                    legend_title="الفئة",
                    height=400
                )
                st.plotly_chart(fig_students, use_container_width=True)
                
                # مخطط خطي للمؤشرات الأخرى
                fig_indicators = px.line(
                    program_data,
                    x="العام",
                    y=["نسبة النجاح", "معدل الرضا"],
                    title=f"تطور المؤشرات في برنامج {selected_program} (2020-2024)",
                    labels={"value": "النسبة المئوية", "variable": "المؤشر"},
                    markers=True,
                    color_discrete_sequence=["#1e88e5", "#27AE60"]
                )
                fig_indicators.update_layout(
                    xaxis_title="السنة",
                    yaxis_title="النسبة المئوية",
                    legend_title="المؤشر",
                    height=400
                )
                st.plotly_chart(fig_indicators, use_container_width=True)
            else:
                ui.alert(
                    title="تنبيه",
                    description=f"لا توجد بيانات متاحة للبرنامج المحدد: {selected_program}",
                    variant="warning"
                )
else:
    ui.alert(
        title="تنبيه",
        description="لا يمكن عرض الرسومات البيانية بسبب عدم توفر البيانات.",
        variant="warning"
    )

# ---- أعضاء هيئة التدريس المميزين وأحدث الإنجازات ----
st.subheader("أعضاء هيئة التدريس والإنجازات")

with ui.card(class_="border-0 shadow-sm p-4"):
    col1, col2 = st.columns([1, 1])
    
    # أعضاء هيئة التدريس المميزين
    with col1:
        st.markdown("### 🏆 أعضاء هيئة التدريس المميزين")
        
        if 'top_faculty' in locals() and not top_faculty.empty:
            for _, member in top_faculty.iterrows():
                with ui.card(class_="mb-3"):
                    st.markdown(f"#### {member['الشارة']} {member['الاسم']}")
                    ui.badge(member['اللقب'], variant="outline")
                    st.markdown(f"**البرنامج:** {member['البرنامج']}")
                    
                    with ui.progress_with_text(value=member['النقاط']/500*100):
                        st.write(f"النقاط: {member['النقاط']}")
        else:
            ui.alert(
                title="معلومات",
                description="لا توجد بيانات متاحة حالياً عن أعضاء هيئة التدريس المميزين.",
                variant="info"
            )
        
        col1_buttons = st.columns([1, 1])
        with col1_buttons[0]:
            ui.button(
                "عرض جميع الأعضاء",
                variant="outline",
                size="sm",
                class_="w-full",
                on_click=lambda: st.switch_page("pages/7_👥_هيئة التدريس.py")
            )
        with col1_buttons[1]:
            ui.button(
                "لوحة الإنجازات",
                variant="outline",
                size="sm",
                class_="w-full",
                on_click=lambda: st.switch_page("pages/10_🏆_إنجازات_الأعضاء.py")
            )
    
    # أحدث الإنجازات
    with col2:
        st.markdown("### 🌟 أحدث الإنجازات")
        
        if 'faculty_achievements' in locals() and not faculty_achievements.empty:
            for _, achievement in faculty_achievements.iterrows():
                date_obj = datetime.strptime(achievement['التاريخ'], "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
                
                with ui.card(class_="mb-3"):
                    st.markdown(f"**{achievement['العضو']}** ({achievement['البرنامج']})")
                    st.markdown(achievement['الإنجاز'])
                    ui.badge(f"التاريخ: {formatted_date}", variant="secondary", size="sm")
                    ui.badge(f"النقاط: {achievement['النقاط']}", variant="primary", size="sm")
        else:
            ui.alert(
                title="معلومات",
                description="لا توجد بيانات متاحة حالياً عن إنجازات أعضاء هيئة التدريس.",
                variant="info"
            )
        
        st.markdown("")
        ui.button(
            "عرض جميع الإنجازات",
            variant="outline",
            size="sm",
            class_="w-full",
            on_click=lambda: st.switch_page("pages/10_🏆_إنجازات_الأعضاء.py")
        )

# ---- مخطط حراري للمؤشرات الرئيسية ----
st.subheader("مؤشرات البرامج الرئيسية")

# التأكد من وجود البيانات قبل إنشاء المخطط
if 'latest_year_data' in locals() and not latest_year_data.empty:
    with ui.card(class_="border-0 shadow-sm p-4"):
        # وضع المخطط الحراري باستخدام Plotly بطريقة مباشرة دون استخدام pivot
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
            x=["نسبة النجاح", "معدل الرضا"],
            y=latest_year_data["البرنامج"],
            colorscale="Viridis",
            text=latest_year_data[["نسبة النجاح", "معدل الرضا"]].values,
            texttemplate="%{text}%",
            textfont={"size":12},
        ))
        
        fig_heatmap.update_layout(
            title="مقارنة المؤشرات الرئيسية عبر البرامج",
            margin=dict(t=50, b=0, l=0, r=0),
            height=400,
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    ui.alert(
        title="تنبيه",
        description="لا يمكن عرض المخطط الحراري بسبب عدم توفر البيانات.",
        variant="warning"
    )

# ---- نصائح للمستخدم ----
with ui.card(class_="mt-3"):
    ui.alert(
        title="نصائح للاستخدام",
        description="""
        - انقر على اسم أي برنامج في القائمة الجانبية لاستعراض تفاصيله
        - استخدم صفحة "هيئة التدريس" لعرض معلومات الأعضاء
        - قم بزيارة "التقييمات والاستطلاعات" للاطلاع على نتائج التقييمات
        - استخدم "لوحة إنجازات الأعضاء" لتسجيل وعرض إنجازات أعضاء هيئة التدريس
        """,
        variant="default"
    )
