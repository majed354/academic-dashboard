import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import hashlib
import numpy as np

# إعدادات الصفحة
st.set_page_config(
    page_title="إنجازات أعضاء هيئة التدريس",
    page_icon="🏆",
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
    
    /* بطاقات الإنجازات */
    .achievement-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e6f0 100%);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* بطاقات أعضاء هيئة التدريس المميزين */
    .top-faculty-card {
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* ألوان لبطاقات المستويات المختلفة */
    .level-1 {
        background: linear-gradient(135deg, #f7d6ff 0%, #9B59B6 100%);
        color: white;
    }
    
    .level-2 {
        background: linear-gradient(135deg, #fcf8e3 0%, #F1C40F 100%);
    }
    
    .level-3 {
        background: linear-gradient(135deg, #fef5ec 0%, #E67E22 100%);
    }
    
    .level-4 {
        background: linear-gradient(135deg, #e9f7fe 0%, #3498DB 100%);
    }
    
    .level-5 {
        background: linear-gradient(135deg, #ebf9f1 0%, #27AE60 100%);
    }
    
    /* حاوية المهمة */
    .task-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border-right: 4px solid #1e88e5;
    }
    
    /* شريط تقدم تقييم المهمة */
    .rating-bar {
        background-color: #e9ecef;
        border-radius: 5px;
        height: 15px;
        position: relative;
        margin-top: 5px;
    }
    
    .rating-fill {
        background-color: #1e88e5;
        height: 100%;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ---- دوال مساعدة ----

@st.cache_data(ttl=3600)
def load_faculty_data():
    """تحميل بيانات أعضاء هيئة التدريس"""
    data = {
        "الاسم": ["د. محمد أحمد", "د. عبدالله محمد", "د. فاطمة علي", "د. خالد إبراهيم", 
                  "د. عائشة سعد", "د. علي حسن", "د. نورة خالد", "د. سارة ناصر",
                  "د. أحمد عبدالله", "د. عمر يوسف", "د. ليلى حامد", "د. زيد ياسر"],
        "الدرجة العلمية": ["أستاذ", "أستاذ مشارك", "أستاذ مساعد", "أستاذ مساعد", 
                           "أستاذ", "أستاذ مشارك", "أستاذ مساعد", "محاضر",
                           "أستاذ مساعد", "محاضر", "أستاذ مشارك", "أستاذ"],
        "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", 
                     "دكتوراه علوم القرآن", "دكتوراه القراءات", "بكالوريوس في القرآن وعلومه", "ماجستير القراءات",
                     "بكالوريوس في القرآن وعلومه", "ماجستير الدراسات القرآنية المعاصرة", "دكتوراه علوم القرآن", "دكتوراه القراءات"]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def generate_achievements_data():
    """توليد بيانات الإنجازات - في التطبيق الفعلي، ستأتي من GitHub"""
    faculty_df = load_faculty_data()
    
    # أنواع المهام المتاحة
    task_types = [
        "نشر بحث علمي", "تقديم محاضرة", "إشراف على رسالة", "تنظيم ورشة عمل", 
        "حضور مؤتمر", "مراجعة أبحاث", "تطوير مقرر", "المشاركة في لجنة", 
        "تقديم دورة تدريبية", "مبادرة خدمة مجتمعية"
    ]
    
    # قاموس لمدى نقاط كل نوع مهمة
    task_points_range = {
        "نشر بحث علمي": (30, 50),
        "تقديم محاضرة": (10, 25),
        "إشراف على رسالة": (20, 35),
        "تنظيم ورشة عمل": (15, 30),
        "حضور مؤتمر": (10, 20),
        "مراجعة أبحاث": (5, 15),
        "تطوير مقرر": (20, 40),
        "المشاركة في لجنة": (10, 20),
        "تقديم دورة تدريبية": (15, 30),
        "مبادرة خدمة مجتمعية": (20, 40)
    }
    
    # توليد بيانات الإنجازات
    achievements = []
    
    # الآن هو 19 أبريل 2025 كما هو مذكور في المتطلبات
    current_date = datetime(2025, 4, 19)
    
    # توليد 50 إنجاز لأعضاء مختلفين
    for _ in range(100):
        # اختيار عضو عشوائي
        faculty_idx = random.randint(0, len(faculty_df) - 1)
        faculty_name = faculty_df.iloc[faculty_idx]["الاسم"]
        faculty_program = faculty_df.iloc[faculty_idx]["البرنامج"]
        
        # اختيار نوع مهمة عشوائي
        task_type = random.choice(task_types)
        
        # توليد تاريخ عشوائي في آخر 6 أشهر
        days_back = random.randint(0, 180)
        task_date = current_date - timedelta(days=days_back)
        
        # توليد نقاط ضمن المدى المحدد للمهمة
        points_range = task_points_range[task_type]
        points = random.randint(points_range[0], points_range[1])
        
        # إنشاء وصف مهمة نموذجي
        descriptions = {
            "نشر بحث علمي": [
                f"نشر بحث في مجلة {random.choice(['الدراسات الإسلامية', 'العلوم الشرعية', 'الدراسات القرآنية'])}",
                f"نشر ورقة بحثية في مؤتمر {random.choice(['الدراسات القرآنية الدولي', 'علوم القرآن', 'التفسير المعاصر'])}",
                f"نشر كتاب بعنوان 'دراسات في {random.choice(['التفسير', 'القراءات', 'علوم القرآن'])}'",
            ],
            "تقديم محاضرة": [
                f"تقديم محاضرة عامة بعنوان '{random.choice(['أساليب التدبر', 'منهجيات التفسير', 'التجديد في الدراسات القرآنية'])}'",
                f"تقديم محاضرة في برنامج {random.choice(['الثقافة القرآنية', 'الأسبوع العلمي', 'الملتقى الأكاديمي'])}",
            ],
            "إشراف على رسالة": [
                f"الإشراف على رسالة ماجستير بعنوان '{random.choice(['دراسة في...', 'تحليل...', 'منهج...'])}'",
                f"الإشراف على رسالة دكتوراه في مجال {random.choice(['التفسير المقارن', 'الدراسات القرآنية', 'القراءات'])}",
            ],
        }
        
        # استخدام وصف محدد للمهمة إذا كان متاحًا، وإلا استخدام النوع كوصف
        if task_type in descriptions:
            description = random.choice(descriptions[task_type])
        else:
            description = f"{task_type} في مجال {random.choice(['التفسير', 'القراءات', 'علوم القرآن'])}"
        
        # توليد معدل تقييم (1-5) مع ترجيح نحو التقييمات الأعلى
        rating_weights = [0.05, 0.1, 0.15, 0.3, 0.4]  # أوزان للتقييمات من 1 إلى 5
        rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
        
        # إضافة المهمة إلى قائمة الإنجازات
        achievements.append({
            "العضو": faculty_name,
            "البرنامج": faculty_program,
            "نوع المهمة": task_type,
            "الوصف": description,
            "التاريخ": task_date.strftime("%Y-%m-%d"),
            "النقاط": points,
            "التقييم": rating
        })
    
    # ترتيب الإنجازات حسب التاريخ (الأحدث أولًا)
    achievements_df = pd.DataFrame(achievements)
    achievements_df = achievements_df.sort_values(by="التاريخ", ascending=False)
    
    return achievements_df

@st.cache_data(ttl=3600)
def get_available_tasks():
    """الحصول على قائمة المهام المتاحة"""
    tasks = [
        {
            "اسم المهمة": "نشر بحث في مجلة محكمة",
            "الوصف": "نشر بحث علمي في مجلة محكمة في مجال التخصص",
            "نطاق النقاط": (30, 50),
            "المتطلبات": "رابط البحث أو صورة من القبول",
            "التصنيف": "بحث علمي"
        },
        {
            "اسم المهمة": "نشر بحث في مؤتمر",
            "الوصف": "نشر ورقة بحثية في مؤتمر علمي محلي أو دولي",
            "نطاق النقاط": (20, 40),
            "المتطلبات": "شهادة المشاركة أو قبول الورقة",
            "التصنيف": "بحث علمي"
        },
        {
            "اسم المهمة": "تأليف كتاب",
            "الوصف": "تأليف كتاب منشور في مجال التخصص",
            "نطاق النقاط": (50, 100),
            "المتطلبات": "معلومات الكتاب وصورة الغلاف",
            "التصنيف": "تأليف"
        },
        {
            "اسم المهمة": "تقديم محاضرة عامة",
            "الوصف": "تقديم محاضرة علمية عامة في موضوع متخصص",
            "نطاق النقاط": (10, 25),
            "المتطلبات": "عنوان المحاضرة وتاريخها ومكانها",
            "التصنيف": "تعليم"
        },
        {
            "اسم المهمة": "تقديم ورشة عمل",
            "الوصف": "تقديم ورشة عمل متخصصة للطلاب أو الزملاء",
            "نطاق النقاط": (15, 30),
            "المتطلبات": "وصف الورشة والحضور",
            "التصنيف": "تعليم"
        },
        {
            "اسم المهمة": "المشاركة في لجنة علمية",
            "الوصف": "المشاركة في لجنة علمية على مستوى القسم أو الكلية",
            "نطاق النقاط": (10, 20),
            "المتطلبات": "اسم اللجنة ومدة المشاركة",
            "التصنيف": "خدمة أكاديمية"
        },
        {
            "اسم المهمة": "الإشراف على رسالة علمية",
            "الوصف": "الإشراف على رسالة ماجستير أو دكتوراه",
            "نطاق النقاط": (20, 35),
            "المتطلبات": "معلومات الطالب وعنوان الرسالة",
            "التصنيف": "إشراف"
        },
        {
            "اسم المهمة": "تطوير مقرر دراسي",
            "الوصف": "تطوير أو تحديث مقرر دراسي",
            "نطاق النقاط": (20, 40),
            "المتطلبات": "رمز المقرر ووصف التطوير",
            "التصنيف": "تطوير"
        },
        {
            "اسم المهمة": "مبادرة خدمة مجتمعية",
            "الوصف": "تقديم مبادرة أو نشاط في خدمة المجتمع",
            "نطاق النقاط": (20, 40),
            "المتطلبات": "وصف المبادرة وتأثيرها",
            "التصنيف": "خدمة مجتمعية"
        },
        {
            "اسم المهمة": "حضور دورة تدريبية",
            "الوصف": "حضور دورة تدريبية في مجال التخصص أو التطوير المهني",
            "نطاق النقاط": (5, 15),
            "المتطلبات": "شهادة الحضور ووصف الدورة",
            "التصنيف": "تطوير مهني"
        },
    ]
    return pd.DataFrame(tasks)

@st.cache_data(ttl=3600)
def calculate_faculty_achievements(achievements_df):
    """حساب إجمالي الإنجازات والنقاط لكل عضو هيئة تدريس"""
    # تجميع البيانات حسب العضو
    faculty_summaries = achievements_df.groupby("العضو").agg({
        "النقاط": "sum",
        "الوصف": "count",
        "التقييم": "mean"
    }).rename(columns={
        "الوصف": "عدد المهام",
        "التقييم": "متوسط التقييم"
    }).reset_index()
    
    # إضافة البرنامج لكل عضو
    program_map = achievements_df.groupby("العضو")["البرنامج"].first().to_dict()
    faculty_summaries["البرنامج"] = faculty_summaries["العضو"].map(program_map)
    
    # تحديد آخر نشاط لكل عضو
    latest_activity = achievements_df.sort_values("التاريخ", ascending=False).groupby("العضو").first()["التاريخ"].to_dict()
    faculty_summaries["آخر نشاط"] = faculty_summaries["العضو"].map(latest_activity)
    
    # تحديد اللقب والشارة بناءً على إجمالي النقاط
    def get_badge_and_title(points):
        if points >= 300:
            return "👑", "العضو القمة", 1
        elif points >= 200:
            return "🌟", "العضو المميز", 2
        elif points >= 150:
            return "🔥", "العضو الفعال", 3
        elif points >= 100:
            return "✨", "العضو النشط", 4
        else:
            return "🌱", "العضو المشارك", 5
    
    # إضافة الشارة واللقب والمستوى
    faculty_summaries[["الشارة", "اللقب", "المستوى"]] = faculty_summaries.apply(
        lambda row: pd.Series(get_badge_and_title(row["النقاط"])), axis=1
    )
    
    # ترتيب البيانات حسب النقاط (تنازليًا)
    faculty_summaries = faculty_summaries.sort_values("النقاط", ascending=False)
    
    return faculty_summaries

@st.cache_data(ttl=3600)
def get_task_distribution(achievements_df):
    """تحليل توزيع المهام حسب النوع"""
    task_dist = achievements_df["نوع المهمة"].value_counts().reset_index()
    task_dist.columns = ["نوع المهمة", "العدد"]
    return task_dist

@st.cache_data(ttl=3600)
def get_program_performance(achievements_df):
    """تحليل أداء البرامج من حيث الإنجازات والنقاط"""
    program_perf = achievements_df.groupby("البرنامج").agg({
        "النقاط": "sum",
        "الوصف": "count"
    }).rename(columns={
        "الوصف": "عدد المهام"
    }).reset_index()
    
    # حساب متوسط النقاط لكل مهمة
    program_perf["متوسط النقاط للمهمة"] = program_perf["النقاط"] / program_perf["عدد المهام"]
    
    return program_perf

@st.cache_data(ttl=3600)
def get_monthly_activity(achievements_df):
    """تحليل النشاط الشهري على مدار العام"""
    # تحويل التاريخ إلى نوع datetime
    achievements_df["تاريخ"] = pd.to_datetime(achievements_df["التاريخ"])
    
    # استخراج الشهر والسنة
    achievements_df["الشهر-السنة"] = achievements_df["تاريخ"].dt.strftime("%Y-%m")
    
    # تجميع البيانات حسب الشهر
    monthly_activity = achievements_df.groupby("الشهر-السنة").agg({
        "النقاط": "sum",
        "الوصف": "count"
    }).rename(columns={
        "الوصف": "عدد المهام"
    }).reset_index()
    
    # ترتيب البيانات حسب التاريخ
    monthly_activity["تاريخ_للترتيب"] = pd.to_datetime(monthly_activity["الشهر-السنة"] + "-01")
    monthly_activity = monthly_activity.sort_values("تاريخ_للترتيب")
    
    return monthly_activity

def evaluate_task_automatically(task_name, task_description):
    """تقييم المهمة تلقائيًا بناءً على الوصف (نموذج بسيط)"""
    # في النظام الحقيقي، يمكن استخدام نماذج ذكاء اصطناعي للتقييم
    # هنا نستخدم التقييم العشوائي مع بعض المنطق البسيط
    
    # طول الوصف يؤثر في التقييم
    length_score = min(5, max(1, len(task_description) // 20))
    
    # كلمات مفتاحية تزيد من التقييم
    keywords = ["دولي", "محكم", "نشر", "تطوير", "ابتكار", "مبادرة", "تخطيط"]
    keyword_score = sum(1 for keyword in keywords if keyword in task_description) / 2
    
    # تقييم أولي يعتمد على نوع المهمة
    initial_rating = {
        "نشر بحث في مجلة محكمة": 4.5,
        "نشر بحث في مؤتمر": 4.0,
        "تأليف كتاب": 5.0,
        "تقديم محاضرة عامة": 3.5,
        "تقديم ورشة عمل": 3.8,
        "المشاركة في لجنة علمية": 3.0,
        "الإشراف على رسالة علمية": 4.2,
        "تطوير مقرر دراسي": 4.0,
        "مبادرة خدمة مجتمعية": 4.3,
        "حضور دورة تدريبية": 3.0,
    }.get(task_name, 3.5)
    
    # الجمع بين كل العوامل
    final_rating = (initial_rating * 0.6) + (length_score * 0.2) + (keyword_score * 0.2)
    
    # تقريب التقييم إلى أقرب 0.5
    return round(min(5, max(1, final_rating)) * 2) / 2

def calculate_points_from_rating(task_name, rating, tasks_df):
    """حساب النقاط بناءً على التقييم ونوع المهمة"""
    # البحث عن نطاق النقاط للمهمة المحددة
    task_row = tasks_df[tasks_df["اسم المهمة"] == task_name]
    if len(task_row) > 0:
        min_points, max_points = task_row.iloc[0]["نطاق النقاط"]
    else:
        # نطاق افتراضي إذا لم يتم العثور على المهمة
        min_points, max_points = (10, 30)
    
    # حساب النقاط بناءً على التقييم (1-5)
    # 1 نجمة = الحد الأدنى، 5 نجوم = الحد الأقصى
    percentage = (rating - 1) / 4  # تحويل التقييم إلى نسبة (0-1)
    points = min_points + (percentage * (max_points - min_points))
    
    return round(points)

# ---- الترويسة ----
st.title("🏆 نظام إدارة إنجاز المهام")
st.write("لوحة تحفيزية لإنجازات أعضاء هيئة التدريس وتتبع المهام الأكاديمية")

# ---- التحضير الأولي ----
# تحميل البيانات
achievements_df = generate_achievements_data()
faculty_df = load_faculty_data()
tasks_df = get_available_tasks()

# حساب البيانات الملخصة
faculty_summaries = calculate_faculty_achievements(achievements_df)
task_distribution = get_task_distribution(achievements_df)
program_performance = get_program_performance(achievements_df)
monthly_activity = get_monthly_activity(achievements_df)

# ---- الشريط الجانبي (عناصر التحكم) ----
with st.sidebar:
    st.header("تصفية البيانات")
    
    # اختيار العام الدراسي
    academic_years = ["2024-2025", "2023-2024"]
    selected_year = st.selectbox("العام الدراسي:", academic_years)
    
    # اختيار البرنامج
    programs = ["الكل"] + list(faculty_df["البرنامج"].unique())
    selected_program = st.selectbox("البرنامج:", programs)
    
    # اختيار نوع المهام
    task_types = ["الكل"] + list(achievements_df["نوع المهمة"].unique())
    selected_task_type = st.selectbox("نوع المهام:", task_types)
    
    # أزرار الإجراءات
    st.divider()
    st.header("الإجراءات")
    
    # زر تسجيل مهمة جديدة يؤدي إلى التمرير إلى تبويب تسجيل المهام
    if st.button("📝 تسجيل مهمة جديدة", use_container_width=True):
        # حفظ الإعداد في حالة الجلسة لاستخدامه لاحقًا
        st.session_state["active_tab"] = 2  # القيمة 2 تمثل تبويب "تسجيل المهام"
    
    # زر إدارة المهام المتاحة (للمشرفين)
    if st.button("⚙️ إدارة المهام المتاحة", use_container_width=True):
        st.session_state["active_tab"] = 3  # القيمة 3 تمثل تبويب "إدارة المهام"
    
    # حالة تسجيل الدخول (في النظام الفعلي، هذا سيرتبط بنظام المصادقة)
    st.divider()
    st.caption("تم تسجيل الدخول كـ: د. محمد أحمد")
    st.caption("الصلاحية: عضو هيئة تدريس")

# ---- تطبيق التصفية ----
filtered_achievements = achievements_df.copy()

# تصفية حسب البرنامج
if selected_program != "الكل":
    filtered_achievements = filtered_achievements[filtered_achievements["البرنامج"] == selected_program]
    faculty_summaries = faculty_summaries[faculty_summaries["البرنامج"] == selected_program]

# تصفية حسب نوع المهمة
if selected_task_type != "الكل":
    filtered_achievements = filtered_achievements[filtered_achievements["نوع المهمة"] == selected_task_type]

# ---- التبويبات الرئيسية ----
# تعيين التبويب النشط إما من حالة الجلسة أو الافتراضي (0)
active_tab = st.session_state.get("active_tab", 0)

tabs = st.tabs([
    "🥇 لوحة الإنجازات", 
    "🎖️ لوحة الشرف", 
    "📝 تسجيل المهام", 
    "⚙️ إدارة المهام"
])

# ---- تبويب 1: لوحة الإنجازات ----
with tabs[0]:
    # تقسيم الشاشة إلى 3 أعمدة
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # العمود الأول: الترتيب العام
    with col1:
        st.subheader("🏆 الترتيب العام")
        
        # عرض الترتيب العام كجدول تفاعلي
        st.dataframe(
            faculty_summaries[["العضو", "الشارة", "النقاط", "عدد المهام", "متوسط التقييم"]],
            hide_index=True,
            use_container_width=True,
            column_config={
                "العضو": st.column_config.TextColumn("العضو"),
                "الشارة": st.column_config.TextColumn(""),
                "النقاط": st.column_config.ProgressColumn(
                    "النقاط",
                    min_value=0,
                    max_value=faculty_summaries["النقاط"].max(),
                    format="%d"
                ),
                "عدد المهام": st.column_config.NumberColumn("المهام"),
                "متوسط التقييم": st.column_config.NumberColumn("التقييم", format="%.1f ⭐")
            }
        )
    
    # العمود الثاني: المخططات البيانية
    with col2:
        st.subheader("📊 إحصائيات الإنجازات")
        
        # تبويبات داخلية للمخططات البيانية
        chart_tabs = st.tabs(["الأعضاء", "أنواع المهام", "النشاط الشهري"])
        
        # مخطط المقارنة بين الأعضاء
        with chart_tabs[0]:
            # الحصول على أفضل 10 أعضاء
            top_10_faculty = faculty_summaries.head(10)
            
            # رسم بياني شريطي للمقارنة
            fig = px.bar(
                top_10_faculty,
                x="العضو",
                y="النقاط",
                color="البرنامج",
                title="أفضل 10 أعضاء حسب النقاط",
                text="النقاط",
                hover_data=["عدد المهام", "متوسط التقييم"]
            )
            fig.update_layout(xaxis_title="العضو", yaxis_title="النقاط")
            st.plotly_chart(fig, use_container_width=True)
        
        # مخطط توزيع المهام حسب النوع
        with chart_tabs[1]:
            fig = px.pie(
                task_distribution,
                values="العدد",
                names="نوع المهمة",
                title="توزيع المهام حسب النوع",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # مخطط النشاط الشهري
        with chart_tabs[2]:
            fig = px.line(
                monthly_activity,
                x="الشهر-السنة",
                y=["النقاط", "عدد المهام"],
                title="النشاط الشهري على مدار العام",
                labels={"الشهر-السنة": "الشهر", "value": "القيمة", "variable": "المؤشر"},
                markers=True
            )
            fig.update_layout(xaxis_title="الشهر", yaxis_title="القيمة")
            st.plotly_chart(fig, use_container_width=True)
        
        # مقارنة أداء البرامج
        st.subheader("📈 أداء البرامج")
        program_fig = px.bar(
            program_performance,
            x="البرنامج",
            y="النقاط",
            color="عدد المهام",
            title="إجمالي النقاط حسب البرنامج",
            text="النقاط",
            hover_data=["متوسط النقاط للمهمة"]
        )
        program_fig.update_layout(xaxis_title="البرنامج", yaxis_title="إجمالي النقاط")
        st.plotly_chart(program_fig, use_container_width=True)
    
    # العمود الثالث: آخر الإنجازات
    with col3:
        st.subheader("🔔 آخر الإنجازات")
        
        # عرض آخر 8 إنجازات
        latest_achievements = filtered_achievements.head(8)
        
        for _, achievement in latest_achievements.iterrows():
            # تحويل التاريخ إلى صيغة أكثر وضوحًا
            date_obj = datetime.strptime(achievement["التاريخ"], "%Y-%m-%d")
            friendly_date = date_obj.strftime("%d %b %Y")
            
            # عرض بطاقة الإنجاز
            st.markdown(f"""
            <div class="achievement-card">
                <h4>{achievement["العضو"]}</h4>
                <p><strong>{achievement["نوع المهمة"]}</strong> ({achievement["النقاط"]} نقطة)</p>
                <p>{achievement["الوصف"]}</p>
                <p><small>{friendly_date} | ⭐ {achievement["التقييم"]}</small></p>
            </div>
            """, unsafe_allow_html=True)

# ---- تبويب 2: لوحة الشرف ----
with tabs[1]:
    st.header("🎖️ لوحة الشرف")
    st.write("تكريم لأعضاء هيئة التدريس المتميزين وفقًا لمستوى الإنجاز")
    
    # تقسيم الأعضاء حسب المستوى
    level_1 = faculty_summaries[faculty_summaries["المستوى"] == 1]
    level_2 = faculty_summaries[faculty_summaries["المستوى"] == 2]
    level_3 = faculty_summaries[faculty_summaries["المستوى"] == 3]
    level_4 = faculty_summaries[faculty_summaries["المستوى"] == 4]
    level_5 = faculty_summaries[faculty_summaries["المستوى"] == 5]
    
    # عرض كل مستوى في قسم منفصل
    if not level_1.empty:
        st.subheader("👑 العضو القمة")
        
        # تقسيم إلى أعمدة لعرض البطاقات
        level_1_cols = st.columns(min(3, len(level_1)))
        
        for i, (_, member) in enumerate(level_1.iterrows()):
            with level_1_cols[i % len(level_1_cols)]:
                # الحصول على آخر 3 إنجازات للعضو
                member_achievements = achievements_df[achievements_df["العضو"] == member["العضو"]].head(3)
                
                # بناء قائمة الإنجازات
                achievements_list = ""
                for _, achievement in member_achievements.iterrows():
                    achievements_list += f"• {achievement['نوع المهمة']}: {achievement['الوصف'][:50]}...\n"
                
                st.markdown(f"""
                <div class="top-faculty-card level-1">
                    <h3>{member["الشارة"]} {member["العضو"]}</h3>
                    <p><strong>اللقب: {member["اللقب"]}</strong></p>
                    <p>البرنامج: {member["البرنامج"]}</p>
                    <p>النقاط: {member["النقاط"]}</p>
                    <p>عدد المهام: {member["عدد المهام"]}</p>
                    <p>التقييم: {"⭐" * round(member["متوسط التقييم"])}</p>
                    <hr>
                    <p><strong>أبرز الإنجازات:</strong></p>
                    <p style="white-space: pre-line;">{achievements_list}</p>
                </div>
                """, unsafe_allow_html=True)
    
    if not level_2.empty:
        st.subheader("🌟 الأعضاء المميزون")
        
        # تقسيم إلى أعمدة لعرض البطاقات
        level_2_cols = st.columns(min(3, len(level_2)))
        
        for i, (_, member) in enumerate(level_2.iterrows()):
            with level_2_cols[i % len(level_2_cols)]:
                st.markdown(f"""
                <div class="top-faculty-card level-2">
                    <h3>{member["الشارة"]} {member["العضو"]}</h3>
                    <p><strong>اللقب: {member["اللقب"]}</strong></p>
                    <p>البرنامج: {member["البرنامج"]}</p>
                    <p>النقاط: {member["النقاط"]}</p>
                    <p>عدد المهام: {member["عدد المهام"]}</p>
                    <p>التقييم: {"⭐" * round(member["متوسط التقييم"])}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # صف أفقي للمستويات الأخرى
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not level_3.empty:
            st.subheader("🔥 الأعضاء الفعالون")
            for _, member in level_3.iterrows():
                st.markdown(f"""
                <div class="top-faculty-card level-3">
                    <h4>{member["الشارة"]} {member["العضو"]}</h4>
                    <p>اللقب: {member["اللقب"]}</p>
                    <p>النقاط: {member["النقاط"]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if not level_4.empty:
            st.subheader("✨ الأعضاء النشطون")
            for _, member in level_4.iterrows()[:3]:  # نعرض أول 3 فقط لتوفير المساحة
                st.markdown(f"""
                <div class="top-faculty-card level-4">
                    <h4>{member["الشارة"]} {member["العضو"]}</h4>
                    <p>اللقب: {member["اللقب"]}</p>
                    <p>النقاط: {member["النقاط"]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col3:
        if not level_5.empty:
            st.subheader("🌱 الأعضاء المشاركون")
            for _, member in level_5.iterrows()[:3]:  # نعرض أول 3 فقط لتوفير المساحة
                st.markdown(f"""
                <div class="top-faculty-card level-5">
                    <h4>{member["الشارة"]} {member["العضو"]}</h4>
                    <p>اللقب: {member["اللقب"]}</p>
                    <p>النقاط: {member["النقاط"]}</p>
                </div>
                """, unsafe_allow_html=True)

# ---- تبويب 3: تسجيل المهام ----
with tabs[2]:
    st.header("📝 تسجيل مهمة جديدة")
    st.write("استخدم النموذج أدناه لتسجيل مهمة جديدة قمت بإنجازها.")
    
    # تقسيم الشاشة إلى عمودين
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # نموذج إضافة مهمة
        with st.form("task_submission_form"):
            # اختيار نوع المهمة
            task_options = tasks_df["اسم المهمة"].tolist()
            selected_task = st.selectbox("اختر نوع المهمة:", task_options)
            
            # الحصول على المتطلبات والوصف للمهمة المختارة
            task_info = tasks_df[tasks_df["اسم المهمة"] == selected_task].iloc[0]
            st.info(f"**وصف المهمة:** {task_info['الوصف']}\n\n**المتطلبات:** {task_info['المتطلبات']}")
            
            # تفاصيل المهمة
            task_description = st.text_area("وصف الإنجاز:", height=120, 
                placeholder="ادخل وصفاً تفصيلياً للمهمة التي قمت بها...")
            
            # روابط إضافية
            additional_links = st.text_input("روابط إضافية (اختياري):", 
                placeholder="أدخل روابط ذات صلة بالمهمة...")
            
            # تحميل ملفات (سيتم تعطيله في هذا النموذج)
            file_upload = st.file_uploader("إرفاق ملفات داعمة (اختياري):", type=["pdf", "jpg", "png", "docx"])
            
            # تاريخ الإنجاز
            # استخدام التاريخ الحالي كقيمة افتراضية
            submission_date = st.date_input("تاريخ الإنجاز:", datetime.now())
            
            # زر الإرسال
            submitted = st.form_submit_button("تقديم المهمة")
            
            if submitted:
                if not task_description:
                    st.error("يرجى إدخال وصف للإنجاز.")
                else:
                    # تقييم المهمة تلقائيًا
                    rating = evaluate_task_automatically(selected_task, task_description)
                    points = calculate_points_from_rating(selected_task, rating, tasks_df)
                    
                    # عرض نتيجة التقييم
                    st.success(f"تم تقديم المهمة بنجاح! التقييم: {rating}/5 | النقاط: {points}")
                    
                    # عرض التفاصيل
                    st.json({
                        "المهمة": selected_task,
                        "التقييم": rating,
                        "النقاط": points,
                        "التاريخ": submission_date.strftime("%Y-%m-%d")
                    })
    
    with col2:
        # معلومات عن نظام التقييم والنقاط
        st.subheader("📋 معلومات التقييم")
        st.markdown("""
        **نظام التقييم:**
        
        يتم تقييم المهام تلقائيًا بناءً على الوصف المقدم ونوع المهمة. العوامل التي تؤثر في التقييم:
        
        - نوع المهمة ومستوى الصعوبة
        - جودة الوصف وتفاصيله
        - المستندات والروابط الداعمة
        - التأثير الأكاديمي للإنجاز
        
        **نطاقات النقاط:**
        
        - نشر بحث: 30-50 نقطة
        - تأليف كتاب: 50-100 نقطة
        - تقديم محاضرة: 10-25 نقطة
        - المشاركة في لجنة: 10-20 نقطة
        - تطوير مقرر: 20-40 نقطة
        
        **الألقاب والمستويات:**
        
        - 👑 العضو القمة: 300+ نقطة
        - 🌟 العضو المميز: 200-299 نقطة
        - 🔥 العضو الفعال: 150-199 نقطة
        - ✨ العضو النشط: 100-149 نقطة
        - 🌱 العضو المشارك: 0-99 نقطة
        """)
        
        # عرض المهام المقدمة سابقًا
        st.subheader("🕒 مهامي السابقة")
        
        # نفترض أن "د. محمد أحمد" هو المستخدم الحالي
        current_user = "د. محمد أحمد"
        user_achievements = achievements_df[achievements_df["العضو"] == current_user].head(5)
        
        if len(user_achievements) > 0:
            for _, achievement in user_achievements.iterrows():
                st.markdown(f"""
                <div class="task-container">
                    <strong>{achievement["نوع المهمة"]}</strong> <small>({achievement["التاريخ"]})</small>
                    <p>{achievement["الوصف"]}</p>
                    <div>⭐ {achievement["التقييم"]} | {achievement["النقاط"]} نقطة</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد مهام سابقة لعرضها.")

# ---- تبويب 4: إدارة المهام المتاحة (للمشرفين) ----
with tabs[3]:
    st.header("⚙️ إدارة المهام المتاحة")
    st.write("يمكن للمشرفين إضافة وتعديل المهام المتاحة للأعضاء من هنا.")
    
    # تقسيم الشاشة إلى عمودين
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("قائمة المهام الحالية")
        
        # عرض المهام المتاحة كجدول تفاعلي
        edited_tasks = st.data_editor(
            tasks_df,
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        if st.button("حفظ التغييرات"):
            st.success("تم حفظ التغييرات على المهام بنجاح!")
    
    with col2:
        st.subheader("إضافة مهمة جديدة")
        
        # نموذج إضافة مهمة جديدة
        with st.form("add_new_task_form"):
            task_name = st.text_input("اسم المهمة:", placeholder="أدخل اسم المهمة...")
            task_desc = st.text_area("وصف المهمة:", placeholder="أدخل وصفاً للمهمة...")
            
            # استخدام عمودين للمزيد من العناصر
            point_col1, point_col2 = st.columns(2)
            with point_col1:
                min_points = st.number_input("الحد الأدنى للنقاط:", min_value=5, max_value=100, value=10)
            with point_col2:
                max_points = st.number_input("الحد الأقصى للنقاط:", min_value=5, max_value=100, value=30)
            
            task_requirements = st.text_area("متطلبات المهمة:", placeholder="أدخل متطلبات إتمام المهمة...")
            
            # قائمة التصنيفات
            categories = ["بحث علمي", "تأليف", "تعليم", "خدمة أكاديمية", "إشراف", "تطوير", "خدمة مجتمعية", "تطوير مهني"]
            task_category = st.selectbox("تصنيف المهمة:", categories)
            
            # زر الإرسال
            submitted = st.form_submit_button("إضافة المهمة")
            
            if submitted:
                if not task_name or not task_desc or not task_requirements:
                    st.error("يرجى ملء جميع الحقول المطلوبة.")
                elif min_points >= max_points:
                    st.error("يجب أن يكون الحد الأدنى للنقاط أقل من الحد الأقصى.")
                else:
                    st.success(f"تمت إضافة المهمة '{task_name}' بنجاح!")
        
        # نصائح للمشرفين
        with st.expander("نصائح لإدارة المهام"):
            st.markdown("""
            **إرشادات لإنشاء مهام فعالة:**
            
            1. **وضوح الهدف**: حدد بوضوح ما هو المطلوب من العضو.
            2. **تحديد المتطلبات**: اذكر بالتفصيل المستندات المطلوبة للإثبات.
            3. **تعيين نقاط متوازنة**: اضبط النقاط بما يتناسب مع جهد المهمة وأهميتها.
            4. **التصنيف المناسب**: صنف المهام بشكل صحيح لتسهيل البحث والتصفية.
            5. **مراجعة دورية**: قم بتحديث قائمة المهام دوريًا لإبقائها ذات صلة.
            """)
