# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Assuming get_github_file_content exists in pages.utils.github_helpers
# from pages.utils.github_helpers import get_github_file_content
from datetime import datetime
import hashlib # Added for dummy data generation

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="الرئيسية",
    page_icon="🏠",
    layout="wide"
)

# --- CSS لإخفاء عناصر Streamlit وإضافة قائمة البرجر المنسدلة ---
custom_css = """
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
    /* 1. إخفاء عناصر Streamlit الافتراضية (بما في ذلك الشريط الجانبي وزر التبديل الخاص به) */
    [data-testid="stToolbar"],
    #MainMenu,
    header,
    footer,
    [class^="viewerBadge_"],
    [id^="GithubIcon"],
    [data-testid="stThumbnailsChipContainer"],
    .stProgress,
    [data-testid="stBottomNavBar"],
    [data-testid*="bottomNav"],
    [aria-label*="community"],
    [aria-label*="profile"],
    [title*="community"],
    [title*="profile"],
    h1 > div > a, h2 > div > a, h3 > div > a,
    h4 > div > a, h5 > div > a, h6 > div > a {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    /* --- إخفاء زر تبديل الشريط الجانبي الإضافي --- */
    [data-testid="stSidebarNavToggler"],
    [data-testid="stSidebarCollapseButton"] {
         display: none !important;
    }


    /* 2. تطبيق الخط العربي وتنسيقات RTL */
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* 3. تنسيقات عامة (تبقى كما هي) */
    h1 { color: #1e88e5; padding-bottom: 15px; border-bottom: 2px solid #1e88e5; margin-bottom: 30px; font-weight: 700; font-size: calc(1.2rem + 1vw); }
    h2, h3 { color: #1e88e5; margin-top: 30px; margin-bottom: 20px; font-weight: 600; font-size: calc(1rem + 0.5vw); }
    .metric-card { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); text-align: center; margin-bottom: 15px; }
    .chart-container { background-color: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; width: 100%; overflow: hidden; }
    .faculty-card { background: linear-gradient(135deg, #f5f7fa 0%, #e3e6f0 100%); border-radius: 10px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
    .achievement-item { padding: 10px; border-right: 3px solid #1e88e5; margin-bottom: 10px; background-color: rgba(30, 136, 229, 0.05); }
    .stSelectbox label, .stMultiselect label { font-weight: 500; }

    /* 4. تنسيقات قائمة البرجر المنسدلة (تبقى كما هي) */
    .burger-trigger { position: fixed; top: 15px; right: 20px; z-index: 1001; cursor: pointer; background-color: #1e88e5; color: white; padding: 8px 12px; border-radius: 5px; font-size: 1.5rem; line-height: 1; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s ease; }
    .burger-trigger:hover { background-color: #1565c0; }
    #burger-menu { position: fixed; top: 60px; right: 20px; width: 250px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.15); z-index: 1000; padding: 10px; overflow: hidden; max-height: 80vh; overflow-y: auto; opacity: 0; transform: translateY(-10px) scale(0.98); transform-origin: top right; pointer-events: none; transition: opacity 0.2s ease-out, transform 0.2s ease-out; }
    #burger-menu.show-menu { opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }
    #burger-menu a { display: block; padding: 10px 15px; color: #333; text-decoration: none; font-size: 0.95rem; border-radius: 5px; margin-bottom: 5px; transition: background-color 0.2s ease, color 0.2s ease; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    #burger-menu a:hover { background-color: #e9ecef; color: #1e88e5; }
    #burger-menu a.active-link { background-color: #1e88e5; color: white; font-weight: 500; }
    #burger-menu a.active-link:hover { background-color: #1565c0; }

    /* 5. زر العودة للأعلى (Kept as is) */
     .back-to-top { position: fixed; bottom: 20px; left: 20px; width: 40px; height: 40px; background-color: #1e88e5; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 998; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); opacity: 0; transition: opacity 0.3s, transform 0.3s; transform: scale(0); }
    .back-to-top.visible { opacity: 1; transform: scale(1); }

    /* 6. تعديلات للهواتف المحمولة (تبقى كما هي) */
    @media only screen and (max-width: 768px) {
        .main .block-container { padding-right: 1rem !important; padding-left: 1rem !important; }
        h1 { font-size: 1.3rem; margin-bottom: 15px; padding-bottom: 10px; }
        h2 { font-size: 1.1rem; margin-top: 15px; margin-bottom: 10px; }
        h3 { font-size: 1rem; margin-top: 12px; margin-bottom: 8px; }
        #burger-menu { width: 220px; top: 55px; right: 15px; }
        .burger-trigger { top: 10px; right: 15px; padding: 6px 10px; font-size: 1.3rem;}
    }

    /* 7. تعديلات للأجهزة اللوحية (تبقى كما هي) */
    @media only screen and (min-width: 769px) and (max-width: 1024px) {
        h1 { font-size: 1.7rem; }
        h2, h3 { font-size: 1.2rem; }
    }
</style>

<div class="burger-trigger" onclick="toggleBurgerMenu(event)">☰</div>
<div id="burger-menu">
    <a href="/" class="menu-link">🏠 الرئيسية</a>
    <a href="/هيئة_التدريس" class="menu-link">👥 هيئة التدريس</a>
    <a href="/التقييمات_والاستطلاعات" class="menu-link">📊 التقييمات والاستطلاعات</a>
    <a href="/لوحة_إنجاز_المهام" class="menu-link">🎯 لوحة إنجاز المهام</a>
    <a href="/صفحة_اخرى" class="menu-link">📄 صفحة أخرى</a>
    </div>

<div class="back-to-top" onclick="scrollToTop()">
    <span style="font-size: 1.2rem;">↑</span>
</div>

<script>
    // Wrap main logic in a function to ensure elements exist
    function initializeBurgerMenu() {
        const menu = document.getElementById('burger-menu');
        const trigger = document.querySelector('.burger-trigger');

        // Check if elements exist before adding listeners
        if (!menu || !trigger) {
            console.warn("Burger menu elements not found yet.");
            // Optionally, retry after a short delay
            // setTimeout(initializeBurgerMenu, 100);
            return;
        }

        // Function to toggle the menu
        window.toggleBurgerMenu = function(event) {
            try {
                 event.stopPropagation(); // Prevent click from reaching document listener immediately
                 menu.classList.toggle('show-menu');
            } catch (e) {
                 console.error("Error toggling burger menu:", e);
            }
        }

        // Function to close the menu
        window.closeMenu = function() {
            try {
                 if (menu.classList.contains('show-menu')) {
                    menu.classList.remove('show-menu');
                 }
            } catch (e) {
                 console.error("Error closing burger menu:", e);
            }
        }

        // Close menu when clicking a link inside it
        try {
            menu.querySelectorAll('a.menu-link').forEach(link => {
                 link.addEventListener('click', window.closeMenu);
            });
        } catch (e) {
            console.error("Error adding link listeners:", e);
        }


        // Close menu when clicking outside
        try {
            document.addEventListener('click', function(event) {
                 // Check if the menu exists and is shown before trying to close
                 const currentMenu = document.getElementById('burger-menu'); // Re-fetch in case of re-render
                 const currentTrigger = document.querySelector('.burger-trigger'); // Re-fetch
                 if (currentMenu && currentTrigger && currentMenu.classList.contains('show-menu')) {
                    if (!currentMenu.contains(event.target) && !currentTrigger.contains(event.target)) {
                         window.closeMenu();
                    }
                 }
            });
        } catch (e) {
            console.error("Error adding document click listener:", e);
        }


        // --- Active Link Logic ---
        try {
            const currentPath = window.location.pathname;
            menu.querySelectorAll('a.menu-link').forEach(link => {
                 link.classList.remove('active-link');
                 const linkPath = link.getAttribute('href');
                 if (!linkPath) return;
                 if (currentPath === linkPath ||
                    (currentPath.endsWith('/') && currentPath.slice(0,-1) === linkPath) ||
                    (linkPath.endsWith('/') && linkPath.slice(0,-1) === currentPath) ||
                    (currentPath === '/' && linkPath === '/'))
                 {
                    link.classList.add('active-link');
                 }
            });
        } catch (e) {
            console.error("Error setting active link:", e);
        }
    }

    // --- Scroll to Top Logic ---
    window.scrollToTop = function() {
        try {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch(e){
            console.error("Error scrolling to top:", e);
        }
    }
    try {
        window.addEventListener('scroll', function() {
             const backToTopButton = document.querySelector('.back-to-top');
             if(backToTopButton){ // Check if button exists
                 if (window.scrollY > 300) {
                    backToTopButton.classList.add('visible');
                 } else {
                    backToTopButton.classList.remove('visible');
                 }
             }
        });
    } catch(e){
        console.error("Error adding scroll listener:", e);
    }


    // Try initializing after DOM is loaded, and again after a short delay as fallback
    if (document.readyState === "loading") {
        document.addEventListener('DOMContentLoaded', initializeBurgerMenu);
    } else {
        // DOMContentLoaded already fired
        initializeBurgerMenu();
    }
    // Fallback initialization in case Streamlit timing is tricky
    // setTimeout(initializeBurgerMenu, 500); // Removed this for now, rely on DOMContentLoaded or immediate execution

</script>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# --- دوال مساعدة ---

def is_mobile():
    """تحقق مما إذا كان المستخدم يستخدم جهازًا محمولًا (تقدير بسيط)"""
    if 'IS_MOBILE' not in st.session_state:
        st.session_state.IS_MOBILE = False
    return st.session_state.IS_MOBILE

# --- *** تعديل دالة prepare_chart_layout *** ---
def prepare_chart_layout(fig, title, is_mobile=False, chart_type="bar"):
    """Apply uniform settings to charts and make them responsive, with legend at the bottom."""
    try: # Add try-except block for robustness
        fig.update_layout(dragmode=False)
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

        # Common layout settings
        layout_settings = {
            "title": title,
            "font": {"family": "Tajawal"},
            "plot_bgcolor": "rgba(240, 240, 240, 0.8)",
            "paper_bgcolor": "white",
            # --- Universal Legend Settings (Positioned at Bottom) ---
            "legend": {
                "orientation": "h",      # Horizontal orientation
                "yanchor": "bottom",     # Anchor legend to the bottom
                "xanchor": "center",     # Center legend horizontally
                "x": 0.5,                # Position at horizontal center
                # y position and font size will be adjusted based on mobile/desktop
            }
            # Ensure showlegend is True by default if legend items exist, Plotly usually handles this.
            # We only explicitly set showlegend=False for mobile pie charts below.
        }

        # Settings specific to device type
        if is_mobile:
            # Mobile specific settings
            mobile_settings = {
                "height": 300 if chart_type != "heatmap" else 350,
                # Increase bottom margin MORE to ensure legend fits
                "margin": {"t": 40, "b": 100, "l": 10, "r": 10, "pad": 0}, # Increased bottom margin
                "font": {"size": 10},
                "title": {"font": {"size": 13}},
                # Adjust legend position and font for mobile
                "legend": {"y": -0.4, "font": {"size": 9}} # Further down (-0.4), smaller font
            }
            layout_settings.update(mobile_settings) # Update common settings with mobile specifics

            # Specific chart type adjustments for mobile
            if chart_type == "bar":
                fig.update_traces(textfont_size=8)
                fig.update_xaxes(tickangle=0, tickfont={"size": 8}) # Try 0 angle first
            elif chart_type == "pie":
                 fig.update_traces(textfont_size=9, textposition="inside", textinfo="percent")
                 layout_settings["showlegend"] = False # Keep legend hidden for pie on mobile
            elif chart_type == "line":
                 fig.update_traces(marker=dict(size=5))


        else: # Desktop settings
            desktop_settings = {
                "height": 450 if chart_type != "heatmap" else 400,
                # Increase bottom margin slightly for desktop legend
                "margin": {"t": 50, "b": 90, "l": 30, "r": 30, "pad": 4}, # Increased bottom margin
                 # Adjust legend position and font for desktop
                "legend": {"y": -0.25, "font": {"size": 10}} # Slightly further down (-0.25), default font size
            }
            layout_settings.update(desktop_settings) # Update common settings with desktop specifics

        # Apply the final combined layout settings
        fig.update_layout(**layout_settings)

    except Exception as e:
        st.warning(f"Could not apply layout settings for chart '{title}': {e}")


    return fig

# --- دوال تحميل البيانات (Dummy implementations - Kept as is) ---
def get_github_file_content(path):
     st.warning(f"Using dummy data for {path}. Implement `get_github_file_content`.")
     if "department_summary.csv" in path:
         data = { "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"], "عدد الطلاب": [210, 180, 150, 200, 120, 140], "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6] }
         return pd.DataFrame(data)
     return pd.DataFrame()
@st.cache_data(ttl=3600)
def load_department_summary():
    try:
        data = { "البرنامج": ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"], "عدد الطلاب": [210, 180, 150, 200, 120, 140], "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6] }
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading department summary: {e}")
        return pd.DataFrame({ "البرنامج": [], "عدد الطلاب": [], "أعضاء هيئة التدريس": [] })
@st.cache_data(ttl=3600)
def load_yearly_data():
    years = list(range(2020, 2025)); data = []; programs = ["بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات", "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات", "دكتوراه علوم القرآن", "دكتوراه القراءات"]
    for year in years:
        for program in programs:
            program_hash = int(hashlib.md5(program.encode()).hexdigest(), 16) % 100
            data.append({ "العام": year, "البرنامج": program, "عدد الطلاب": 100 + (year - 2020) * 10 + program_hash % 100, "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + program_hash % 10), "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + (program_hash // 2) % 10) })
    return pd.DataFrame(data)
@st.cache_data(ttl=3600)
def load_faculty_achievements():
    achievements = [ {"العضو": "د. محمد أحمد", "الإنجاز": "نشر بحث في مجلة عالمية", "التاريخ": "2025-04-15", "النقاط": 50, "البرنامج": "بكالوريوس في القرآن وعلومه"}, {"العضو": "د. عائشة سعد", "الإنجاز": "إطلاق مبادرة تعليمية", "التاريخ": "2025-04-10", "النقاط": 40, "البرنامج": "دكتوراه علوم القرآن"}, {"العضو": "د. عبدالله محمد", "الإنجاز": "المشاركة في مؤتمر دولي", "التاريخ": "2025-04-05", "النقاط": 35, "البرنامج": "بكالوريوس القراءات"}, {"العضو": "د. فاطمة علي", "الإنجاز": "تطوير مقرر دراسي", "التاريخ": "2025-04-01", "النقاط": 30, "البرنامج": "ماجستير الدراسات القرآنية المعاصرة"}, {"العضو": "د. خالد إبراهيم", "الإنجاز": "تقديم ورشة عمل", "التاريخ": "2025-03-25", "النقاط": 25, "البرنامج": "ماجستير القراءات"} ]
    return pd.DataFrame(achievements)
@st.cache_data(ttl=3600)
def load_top_faculty():
    top_faculty = [ {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"}, {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"}, {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"} ]
    return pd.DataFrame(top_faculty)

# --- محتوى الصفحة (Kept mostly as is, uses the updated prepare_chart_layout) ---
mobile_view = is_mobile()
st.title("🏠 الرئيسية")
st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
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

st.subheader("المؤشرات الرئيسية")
cols = st.columns(4)
with cols[0]: st.metric("إجمالي الطلاب", f"{total_students:,}")
with cols[1]: st.metric("أعضاء هيئة التدريس", f"{total_faculty:,}")
indicators_to_plot = [] # Define indicators_to_plot here
if not latest_year_data.empty and "نسبة النجاح" in latest_year_data.columns: avg_success = latest_year_data["نسبة النجاح"].mean(); indicators_to_plot.append("نسبة النجاح"); cols[2].metric("متوسط النجاح", f"{avg_success:.0f}%")
if not latest_year_data.empty and "معدل الرضا" in latest_year_data.columns: avg_satisfaction = latest_year_data["معدل الرضا"].mean(); indicators_to_plot.append("معدل الرضا"); cols[3].metric("متوسط الرضا", f"{avg_satisfaction:.0f}%")

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
         # Now prepare_chart_layout handles the legend position automatically
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
            # Now prepare_chart_layout handles the legend position automatically
            if trend_indicators and "العام" in program_data.columns: fig_trend = px.line(program_data, x="العام", y=trend_indicators, title=f"تطور مؤشرات: {selected_display_program}", labels={"value": "القيمة", "variable": "المؤشر", "العام": "السنة"}, markers=True); fig_trend = prepare_chart_layout(fig_trend, f"تطور: {selected_display_program}", is_mobile=mobile_view, chart_type="line"); st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
            else: st.info(f"لا توجد بيانات كافية لعرض التطور السنوي لبرنامج {selected_display_program}.")
        else: st.info("لا توجد بيانات سنوية لعرض التطور.")
else: st.info("لا توجد بيانات كافية لعرض الرسوم البيانية للبرامج.")

st.subheader("أعضاء هيئة التدريس والإنجازات")
if not top_faculty.empty or not faculty_achievements.empty:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 🏆 المميزون")
        if not top_faculty.empty:
            num_to_display = min(len(top_faculty), 3)
            for _, member in top_faculty.head(num_to_display).iterrows(): name = member.get('الاسم', 'غير متوفر'); badge = member.get('الشارة', ''); title = member.get('اللقب', ''); points = member.get('النقاط', ''); st.markdown(f"""<div class='faculty-card'><h5 style="margin-bottom: 5px;">{badge} {name}</h5><p style="font-size: 0.9em; margin: 2px 0;">{title} ({points} نقطة)</p></div>""", unsafe_allow_html=True)
            st.markdown("<a href='/هيئة_التدريس' target='_self' style='font-size: 0.9em;'>عرض الكل...</a>", unsafe_allow_html=True)
        else: st.info("لا توجد بيانات لأعضاء هيئة التدريس المميزين.")
    with col2:
        st.markdown("#### 🌟 أحدث الإنجازات")
        if not faculty_achievements.empty:
            num_to_display = min(len(faculty_achievements), 3)
            if 'التاريخ' in faculty_achievements.columns: faculty_achievements['التاريخ'] = pd.to_datetime(faculty_achievements['التاريخ'], errors='coerce'); achievements_to_display = faculty_achievements.sort_values('التاريخ', ascending=False).head(num_to_display)
            else: achievements_to_display = faculty_achievements.head(num_to_display)
            for _, achievement in achievements_to_display.iterrows(): member_name = achievement.get('العضو', 'غير معروف'); desc = achievement.get('الإنجاز', 'لا يوجد وصف'); date_str = achievement.get('التاريخ', None); formatted_date = date_str.strftime("%Y/%m/%d") if pd.notna(date_str) else ""; st.markdown(f"""<div class='achievement-item'><p style="font-size: 0.95em; margin-bottom: 3px;"><strong>{member_name}</strong></p><p style="font-size: 0.9em; margin-bottom: 3px;">{desc}</p>{f'<p style="font-size: 0.8em; color: grey; margin-bottom: 0;">{formatted_date}</p>' if formatted_date else ''}</div>""", unsafe_allow_html=True)
            st.markdown("<a href='/لوحة_إنجاز_المهام' target='_self' style='font-size: 0.9em;'>عرض الكل...</a>", unsafe_allow_html=True)
        else: st.info("لا توجد بيانات لأحدث الإنجازات.")
else: st.info("لا تتوفر بيانات أعضاء هيئة التدريس أو الإنجازات حاليًا.")

# Heatmap section remains the same, as prepare_chart_layout applies general layout
if not latest_year_data.empty and "البرنامج_المختصر" in display_data.columns and indicators_to_plot:
    st.subheader("نظرة عامة على المؤشرات")
    try:
        heatmap_plot_data = display_data[["البرنامج_المختصر"] + indicators_to_plot].set_index("البرنامج_المختصر")
        fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_plot_data.values, x=heatmap_plot_data.columns, y=heatmap_plot_data.index, colorscale="Blues", text=heatmap_plot_data.values, texttemplate="%{text:.0f}", textfont={"size": 10 if mobile_view else 12}, hoverongaps = False))
        # Call prepare_chart_layout which handles title, font, bg colors etc.
        fig_heatmap = prepare_chart_layout(fig_heatmap, "مقارنة المؤشرات الرئيسية", is_mobile=mobile_view, chart_type="heatmap")
        # Add specific heatmap layout adjustments *after* prepare_chart_layout
        fig_heatmap.update_layout(xaxis_title="المؤشر", yaxis_title="البرنامج", yaxis=dict(tickfont=dict(size=9 if mobile_view else 10)), margin=dict(l=100)) # Keep left margin
        st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
    except Exception as heatmap_error: st.warning(f"لم يتمكن من إنشاء المخطط الحراري: {heatmap_error}")
elif not latest_year_data.empty: st.info("لا تتوفر بيانات مؤشرات كافية لإنشاء المخطط الحراري.")


with st.expander("💡 نصائح للاستخدام", expanded=False):
    st.markdown("""
    - انقر على أيقونة ☰ في الأعلى لفتح القائمة والتنقل بين الصفحات.
    - ستظهر القائمة أسفل الأيقونة مباشرة.
    - انقر في أي مكان خارج القائمة لإغلاقها.
    - استخدم الروابط في القائمة لاستعراض تفاصيل البرامج، هيئة التدريس، أو الإنجازات.
    - الرسوم البيانية تفاعلية، مرر الفأرة فوقها لرؤية التفاصيل.
    - **مفاتيح الرسوم البيانية تظهر الآن أسفلها لتوفير المساحة.**
    - انقر على زر السهم ↑ في الأسفل للعودة إلى أعلى الصفحة بسرعة.
    """)

