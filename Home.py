# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# components import is removed as it's not used
from datetime import datetime
import hashlib # Added for dummy data generation

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="الرئيسية",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed
)

# --- CSS عام (لإخفاء عناصر Streamlit وتطبيق الخطوط و RTL) ---
# تم تبسيط هذا الجزء ليحتوي فقط على CSS الضروري
general_css = """
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
    /* 1. إخفاء عناصر Streamlit الافتراضية غير المرغوب فيها */
    [data-testid="stToolbar"], #MainMenu, header, footer,
    [class^="viewerBadge_"], [id^="GithubIcon"],
    [data-testid="stThumbnailsChipContainer"], .stProgress,
    [data-testid="stBottomNavBar"], [data-testid*="bottomNav"],
    [aria-label*="community"], [aria-label*="profile"],
    [title*="community"], [title*="profile"],
    h1 > div > a, h2 > div > a, h3 > div > a,
    h4 > div > a, h5 > div > a, h6 > div > a { display: none !important; visibility: hidden !important; }

    /* --- إخفاء الشريط الجانبي الافتراضي وزر تبديله تمامًا --- */
    /* We will control the sidebar content visibility via session_state */
    /* Hide the default sidebar structural elements if needed, */
    /* but allow content to be shown conditionally */
    /* Let's try hiding only the toggle button first */
     [data-testid="stSidebarNavToggler"],
     [data-testid="stSidebarCollapseButton"] {
          display: none !important;
     }
     /* Optional: Hide the sidebar container itself if content is empty */
     /* section[data-testid="stSidebar"] > div:first-child { display: none; } */


    /* 2. تطبيق الخط العربي وتنسيقات RTL */
    * { font-family: 'Tajawal', sans-serif !important; }
    .stApp { direction: rtl; text-align: right; }

    /* 3. تنسيقات عامة للعناوين والبطاقات والمقاييس */
    h1 { color: #1e88e5; padding-bottom: 15px; border-bottom: 2px solid #1e88e5; margin-bottom: 30px; font-weight: 700; font-size: calc(1.2rem + 1vw); }
    h2, h3 { color: #1e88e5; margin-top: 30px; margin-bottom: 20px; font-weight: 600; font-size: calc(1rem + 0.5vw); }
    .metric-card { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); text-align: center; margin-bottom: 15px; }
    .chart-container { background-color: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; width: 100%; overflow: hidden; }
    .faculty-card { background: linear-gradient(135deg, #f5f7fa 0%, #e3e6f0 100%); border-radius: 10px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
    .achievement-item { padding: 10px; border-right: 3px solid #1e88e5; margin-bottom: 10px; background-color: rgba(30, 136, 229, 0.05); }
    .stSelectbox label, .stMultiselect label { font-weight: 500; }

     /* 4. زر العودة للأعلى */
     .back-to-top { position: fixed; bottom: 20px; left: 20px; width: 40px; height: 40px; background-color: #1e88e5; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 998; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); opacity: 0; transition: opacity 0.3s, transform 0.3s; transform: scale(0); }
    .back-to-top.visible { opacity: 1; transform: scale(1); }

    /* 5. تعديلات للهواتف المحمولة (للتباعد العام والعناوين) */
    @media only screen and (max-width: 768px) {
        .main .block-container { padding-right: 1rem !important; padding-left: 1rem !important; }
        h1 { font-size: 1.3rem; margin-bottom: 15px; padding-bottom: 10px; }
        h2 { font-size: 1.1rem; margin-top: 15px; margin-bottom: 10px; }
        h3 { font-size: 1rem; margin-top: 12px; margin-bottom: 8px; }
    }

    /* 6. تعديلات للأجهزة اللوحية (للتباعد العام والعناوين) */
    @media only screen and (min-width: 769px) and (max-width: 1024px) {
        h1 { font-size: 1.7rem; }
        h2, h3 { font-size: 1.2rem; }
    }
</style>

<div class="back-to-top" onclick="scrollToTop()">
    <span style="font-size: 1.2rem;">↑</span>
</div>
<script>
    // --- Scroll to Top Logic ---
    window.scrollToTop = function() {
        try { window.scrollTo({ top: 0, behavior: 'smooth' }); }
        catch(e){ console.error("Error scrolling to top:", e); }
    }
    try {
        window.addEventListener('scroll', function() {
             const backToTopButton = document.querySelector('.back-to-top');
             if(backToTopButton){
                 if (window.scrollY > 300) { backToTopButton.classList.add('visible'); }
                 else { backToTopButton.classList.remove('visible'); }
             }
        });
    } catch(e){ console.error("Error adding scroll listener:", e); }
</script>
"""
# تطبيق CSS العام وزر العودة للأعلى
st.markdown(general_css, unsafe_allow_html=True)

# --- زر البرجر للتحكم في الشريط الجانبي ---
# وضع الزر في الأعلى باستخدام الأعمدة (أو st.container) للتحكم في الموضع
col1_main, col2_main = st.columns([0.9, 0.1]) # Adjust ratio as needed

with col2_main: # Place button in the smaller right column
    # استخدام مفتاح فريد للزر
    if st.button("☰", key="burger_button_toggle", help="فتح/إغلاق القائمة"):
        # Toggle the state in session_state
        st.session_state.show_sidebar_content = not st.session_state.get("show_sidebar_content", False)
        # Force a rerun to update the sidebar visibility immediately (st.button already does this)
        # st.experimental_rerun() # Usually not needed after st.button

# --- محتوى الشريط الجانبي (يظهر بناءً على الحالة) ---
# Check the state to decide whether to show sidebar content
if st.session_state.get("show_sidebar_content", False):
    with st.sidebar: # Use the default sidebar container
        st.markdown("### القائمة الرئيسية")
        # Add navigation links using Markdown
        # Ensure these paths are correct for your multi-page app structure
        st.markdown("""
        - [🏠 الرئيسية](/)
        - [👥 هيئة التدريس](/هيئة_التدريس)
        - [📊 التقييمات والاستطلاعات](/التقييمات_والاستطلاعات)
        - [🎯 لوحة إنجاز المهام](/لوحة_إنجاز_المهام)
        - [📄 صفحة أخرى](/صفحة_اخرى)
        """, unsafe_allow_html=True) # Use unsafe_allow_html if needed for complex markdown/html in links
        st.markdown("---")
        st.info("انقر على زر ☰ مرة أخرى لإخفاء القائمة.")


# --- دوال مساعدة (تبقى كما هي) ---
def is_mobile():
    if 'IS_MOBILE' not in st.session_state: st.session_state.IS_MOBILE = False
    return st.session_state.IS_MOBILE

def prepare_chart_layout(fig, title, is_mobile=False, chart_type="bar"):
    try:
        fig.update_layout(dragmode=False)
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        layout_settings = { "title": title, "font": {"family": "Tajawal"}, "plot_bgcolor": "rgba(240, 240, 240, 0.8)", "paper_bgcolor": "white", "legend": { "orientation": "h", "yanchor": "bottom", "xanchor": "center", "x": 0.5, } }
        if is_mobile:
            mobile_settings = { "height": 300 if chart_type != "heatmap" else 350, "margin": {"t": 40, "b": 100, "l": 10, "r": 10, "pad": 0}, "font": {"size": 10}, "title": {"font": {"size": 13}}, "legend": {"y": -0.4, "font": {"size": 9}} }
            layout_settings.update(mobile_settings)
            if chart_type == "pie": layout_settings["showlegend"] = False
            elif chart_type == "line": fig.update_traces(marker=dict(size=5))
            elif chart_type == "bar": fig.update_xaxes(tickangle=0, tickfont={"size": 8})
        else: # Desktop settings
            desktop_settings = { "height": 450 if chart_type != "heatmap" else 400, "margin": {"t": 50, "b": 90, "l": 30, "r": 30, "pad": 4}, "legend": {"y": -0.25, "font": {"size": 10}} }
            layout_settings.update(desktop_settings)
        fig.update_layout(**layout_settings)
    except Exception as e: st.warning(f"Could not apply layout settings for chart '{title}': {e}")
    return fig

# --- دوال تحميل البيانات (Dummy implementations - Kept as is) ---
def get_github_file_content(path):
     st.warning(f"Using dummy data for {path}. Implement `get_github_file_content`.")
     if "department_summary.csv" in path: data = { "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"], "عدد الطلاب": [210, 180, 150, 200, 120, 140], "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6] }; return pd.DataFrame(data)
     return pd.DataFrame()
@st.cache_data(ttl=3600)
def load_department_summary():
    try: data = { "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"], "عدد الطلاب": [210, 180, 150, 200, 120, 140], "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6] }; return pd.DataFrame(data)
    except Exception as e: st.error(f"Error loading department summary: {e}"); return pd.DataFrame({ "البرنامج": [], "عدد الطلاب": [], "أعضاء هيئة التدريس": [] })
@st.cache_data(ttl=3600)
def load_yearly_data():
    years = list(range(2020, 2025)); data = []; programs = ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"]
    for year in years:
        for program in programs: program_hash = int(hashlib.md5(program.encode()).hexdigest(), 16) % 100; data.append({ "العام": year, "البرنامج": program, "عدد الطلاب": 100 + (year - 2020) * 10 + program_hash % 100, "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + program_hash % 10), "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + (program_hash // 2) % 10) })
    return pd.DataFrame(data)
@st.cache_data(ttl=3600)
def load_faculty_achievements():
    achievements = [ {"العضو": "د. محمد أحمد", "الإنجاز": "نشر بحث في مجلة عالمية", "التاريخ": "2025-04-15", "النقاط": 50, "البرنامج": "بكالوريوس في القرآن وعلومه"}, {"العضو": "د. عائشة سعد", "الإنجاز": "إطلاق مبادرة تعليمية", "التاريخ": "2025-04-10", "النقاط": 40, "البرنامج": "دكتوراه علوم القرآن"}, {"العضو": "د. عبدالله محمد", "الإنجاز": "المشاركة في مؤتمر دولي", "التاريخ": "2025-04-05", "النقاط": 35, "البرنامج": "بكالوريوس القراءات"}, {"العضو": "د. فاطمة علي", "الإنجاز": "تطوير مقرر دراسي", "التاريخ": "2025-04-01", "النقاط": 30, "البرنامج": "ماجستير الدراسات القرآنية المعاصرة"}, {"العضو": "د. خالد إبراهيم", "الإنجاز": "تقديم ورشة عمل", "التاريخ": "2025-03-25", "النقاط": 25, "البرنامج": "ماجستير القراءات"} ]
    return pd.DataFrame(achievements)
@st.cache_data(ttl=3600)
def load_top_faculty():
    top_faculty = [ {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"}, {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"}, {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"} ]
    return pd.DataFrame(top_faculty)

# --- محتوى الصفحة الرئيسي (Main Page Content) ---
# (The rest of the page content displaying titles, metrics, charts, etc. remains the same)
# ... (Previous code for displaying metrics, tabs, charts, faculty info) ...
mobile_view = is_mobile()
# Display title etc. (no change needed here)
st.title("🏠 الرئيسية")
st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")

# Load data (no change needed here)
try:
    dept_data = load_department_summary(); total_students = dept_data["عدد الطلاب"].sum() if "عدد الطلاب" in dept_data.columns else 0; total_faculty = dept_data["أعضاء هيئة التدريس"].sum() if "أعضاء هيئة التدريس" in dept_data.columns else 0
    yearly_data = load_yearly_data()
    if "العام" in yearly_data.columns and 2024 in yearly_data["العام"].values: latest_year_data = yearly_data[yearly_data["العام"] == 2024].copy()
    else: st.warning("بيانات عام 2024 غير متوفرة."); latest_year_data = pd.DataFrame()
    faculty_achievements = load_faculty_achievements(); top_faculty = load_top_faculty()
    if latest_year_data.empty and not dept_data.empty: st.info("استخدام بيانات ملخص القسم للرسوم البيانية."); latest_year_data = dept_data
except Exception as e:
    st.error(f"خطأ في تحميل أو تهيئة البيانات: {e}"); st.warning("استخدام بيانات تجريبية.")
    total_students = 1000; total_faculty = 50
    dept_data = pd.DataFrame({"البرنامج": ["برنامج تجريبي"], "عدد الطلاب": [1000], "أعضاء هيئة التدريس": [50]})
    latest_year_data = pd.DataFrame({ "العام": [2024], "البرنامج": ["برنامج تجريبي"], "عدد الطلاب": [1000], "نسبة النجاح": [85], "معدل الرضا": [90] })
    yearly_data = latest_year_data.copy(); faculty_achievements = pd.DataFrame(); top_faculty = pd.DataFrame()

# Display metrics (no change needed here)
st.subheader("المؤشرات الرئيسية")
cols = st.columns(4)
with cols[0]: st.metric("إجمالي الطلاب", f"{total_students:,}")
with cols[1]: st.metric("أعضاء هيئة التدريس", f"{total_faculty:,}")
indicators_to_plot = []
if not latest_year_data.empty and "نسبة النجاح" in latest_year_data.columns: avg_success = latest_year_data["نسبة النجاح"].mean(); indicators_to_plot.append("نسبة النجاح"); cols[2].metric("متوسط النجاح", f"{avg_success:.0f}%")
if not latest_year_data.empty and "معدل الرضا" in latest_year_data.columns: avg_satisfaction = latest_year_data["معدل الرضا"].mean(); indicators_to_plot.append("معدل الرضا"); cols[3].metric("متوسط الرضا", f"{avg_satisfaction:.0f}%")

# Display charts within tabs (no change needed here, uses updated prepare_chart_layout)
if not latest_year_data.empty and "البرنامج" in latest_year_data.columns and "عدد الطلاب" in latest_year_data.columns:
    st.subheader("تحليل البرامج الأكاديمية")
    program_mapping = { "بكالوريوس في القرآن وعلومه": "ب. قرآن", "بكالوريوس القراءات": "ب. قراءات", "ماجستير الدراسات القرآنية المعاصرة": "م. دراسات", "ماجستير القراءات": "م. قراءات", "دكتوراه علوم القرآن": "د. قرآن", "دكتوراه القراءات": "د. قراءات" }
    display_data = latest_year_data.copy()
    if "البرنامج" in display_data.columns: display_data["البرنامج_المختصر"] = display_data["البرنامج"].map(program_mapping).fillna(display_data["البرنامج"])
    else: display_data["البرنامج_المختصر"] = display_data["البرنامج"]
    tab_labels = ["توزيع الطلاب", "مقارنة المؤشرات", "التطور السنوي"]; tabs = st.tabs(tab_labels)
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1: fig_pie = px.pie(display_data, values="عدد الطلاب", names="البرنامج_المختصر", title="توزيع الطلاب", color_discrete_sequence=px.colors.qualitative.Pastel); fig_pie = prepare_chart_layout(fig_pie, "توزيع الطلاب", is_mobile=mobile_view, chart_type="pie"); st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        with col2: fig_bar = px.bar(display_data.sort_values("عدد الطلاب", ascending=True), y="البرنامج_المختصر", x="عدد الطلاب", title="عدد الطلاب لكل برنامج", color="عدد الطلاب", orientation='h', color_continuous_scale="Blues"); fig_bar = prepare_chart_layout(fig_bar, "عدد الطلاب لكل برنامج", is_mobile=mobile_view, chart_type="bar"); st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    with tabs[1]:
         if indicators_to_plot: fig_indicators = px.bar(display_data, x="البرنامج_المختصر", y=indicators_to_plot, barmode="group", title="مقارنة المؤشرات", labels={"value": "النسبة المئوية", "variable": "المؤشر", "البرنامج_المختصر": "البرنامج"}, color_discrete_sequence=["#1e88e5", "#27AE60"]); fig_indicators = prepare_chart_layout(fig_indicators, "مقارنة المؤشرات", is_mobile=mobile_view, chart_type="bar"); st.plotly_chart(fig_indicators, use_container_width=True, config={"displayModeBar": False})
         else: st.info("لا توجد بيانات مؤشرات لعرض المقارنة.")
    with tabs[2]:
        if not yearly_data.empty and "البرنامج" in yearly_data.columns:
            unique_programs_full = yearly_data["البرنامج"].unique(); program_options_display = {program_mapping.get(p, p): p for p in unique_programs_full}
            selected_display_program = st.selectbox("اختر البرنامج لعرض تطوره:", options=list(program_options_display.keys())); selected_program_full = program_options_display[selected_display_program]
            program_data = yearly_data[yearly_data["البرنامج"] == selected_program_full].copy()
            trend_indicators = [];
            if "عدد الطلاب" in program_data.columns: trend_indicators.append("عدد الطلاب")
            if "نسبة النجاح" in program_data.columns: trend_indicators.append("نسبة النجاح")
            if "معدل الرضا" in program_data.columns: trend_indicators.append("معدل الرضا")
            if trend_indicators and "العام" in program_data.columns: fig_trend = px.line(program_data, x="العام", y=trend_indicators, title=f"تطور مؤشرات: {selected_display_program}", labels={"value": "القيمة", "variable": "المؤشر", "العام": "السنة"}, markers=True); fig_trend = prepare_chart_layout(fig_trend, f"تطور: {selected_display_program}", is_mobile=mobile_view, chart_type="line"); st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
            else: st.info(f"لا توجد بيانات كافية لعرض التطور السنوي لبرنامج {selected_display_program}.")
        else: st.info("لا توجد بيانات سنوية لعرض التطور.")
else: st.info("لا توجد بيانات كافية لعرض الرسوم البيانية للبرامج.")

# Display faculty info (no change needed here)
st.subheader("أعضاء هيئة التدريس والإنجازات")
if not top_faculty.empty or not faculty_achievements.empty:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 🏆 المميزون")
        if not top_faculty.empty:
            num_to_display = min(len(top_faculty), 3)
            for _, member in top_faculty.head(num_to_display).iterrows(): name = member.get('الاسم', 'غير متوفر'); badge = member.get('الشارة', ''); title = member.get('اللقب', ''); points = member.get('النقاط', ''); st.markdown(f"""<div class='faculty-card'><h5 style="margin-bottom: 5px;">{badge} {name}</h5><p style="font-size: 0.9em; margin: 2px 0;">{title} ({points} نقطة)</p></div>""", unsafe_allow_html=True)
            st.markdown("<a href='/هيئة_التدريس' target='_top' style='font-size: 0.9em;'>عرض الكل...</a>", unsafe_allow_html=True)
        else: st.info("لا توجد بيانات لأعضاء هيئة التدريس المميزين.")
    with col2:
        st.markdown("#### 🌟 أحدث الإنجازات")
        if not faculty_achievements.empty:
            num_to_display = min(len(faculty_achievements), 3)
            if 'التاريخ' in faculty_achievements.columns: faculty_achievements['التاريخ'] = pd.to_datetime(faculty_achievements['التاريخ'], errors='coerce'); achievements_to_display = faculty_achievements.sort_values('التاريخ', ascending=False).head(num_to_display)
            else: achievements_to_display = faculty_achievements.head(num_to_display)
            for _, achievement in achievements_to_display.iterrows(): member_name = achievement.get('العضو', 'غير معروف'); desc = achievement.get('الإنجاز', 'لا يوجد وصف'); date_str = achievement.get('التاريخ', None); formatted_date = date_str.strftime("%Y/%m/%d") if pd.notna(date_str) else ""; st.markdown(f"""<div class='achievement-item'><p style="font-size: 0.95em; margin-bottom: 3px;"><strong>{member_name}</strong></p><p style="font-size: 0.9em; margin-bottom: 3px;">{desc}</p>{f'<p style="font-size: 0.8em; color: grey; margin-bottom: 0;">{formatted_date}</p>' if formatted_date else ''}</div>""", unsafe_allow_html=True)
            st.markdown("<a href='/لوحة_إنجاز_المهام' target='_top' style='font-size: 0.9em;'>عرض الكل...</a>", unsafe_allow_html=True)
        else: st.info("لا توجد بيانات لأحدث الإنجازات.")
else: st.info("لا تتوفر بيانات أعضاء هيئة التدريس أو الإنجازات حاليًا.")

# Display heatmap (no change needed here)
if not latest_year_data.empty and "البرنامج_المختصر" in display_data.columns and indicators_to_plot:
    st.subheader("نظرة عامة على المؤشرات")
    try:
        heatmap_plot_data = display_data[["البرنامج_المختصر"] + indicators_to_plot].set_index("البرنامج_المختصر")
        fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_plot_data.values, x=heatmap_plot_data.columns, y=heatmap_plot_data.index, colorscale="Blues", text=heatmap_plot_data.values, texttemplate="%{text:.0f}", textfont={"size": 10 if mobile_view else 12}, hoverongaps = False))
        fig_heatmap = prepare_chart_layout(fig_heatmap, "مقارنة المؤشرات الرئيسية", is_mobile=mobile_view, chart_type="heatmap")
        fig_heatmap.update_layout(xaxis_title="المؤشر", yaxis_title="البرنامج", yaxis=dict(tickfont=dict(size=9 if mobile_view else 10)), margin=dict(l=100))
        st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
    except Exception as heatmap_error: st.warning(f"لم يتمكن من إنشاء المخطط الحراري: {heatmap_error}")
elif not latest_year_data.empty: st.info("لا تتوفر بيانات مؤشرات كافية لإنشاء المخطط الحراري.")

# Display usage tips (updated)
with st.expander("💡 نصائح للاستخدام", expanded=False):
    st.markdown("""
    - **تم استبدال قائمة البرجر المخصصة بزر (☰) في الأعلى يتحكم بظهور الشريط الجانبي القياسي لـ Streamlit.** هذا هو الحل الأكثر موثوقية.
    - انقر على زر ☰ لإظهار/إخفاء قائمة التنقل في الشريط الجانبي.
    - **تم إخفاء السهم الإضافي في الزاوية العلوية اليسرى.**
    - استخدم الروابط في الشريط الجانبي للتنقل بين الصفحات.
    - الرسوم البيانية تفاعلية، مرر الفأرة فوقها لرؤية التفاصيل.
    - **مفاتيح الرسوم البيانية تظهر الآن أسفلها لتوفير المساحة.**
    - انقر على زر السهم ↑ في الأسفل للعودة إلى أعلى الصفحة بسرعة.
    """)

