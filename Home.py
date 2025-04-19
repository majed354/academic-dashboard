import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Assuming get_github_file_content is defined elsewhere or replace with pd.read_csv if applicable
# from pages.utils.github_helpers import get_github_file_content
from datetime import datetime
import streamlit_shadcn_ui as ui
import traceback # Import traceback for detailed error logging if needed

# Dummy function if get_github_file_content is not available
# Replace this with your actual function or data loading method
def get_github_file_content(file_path):
    # Simulate failure to trigger fallback
    raise FileNotFoundError(f"Simulated error: Could not find {file_path}")
    # Or simulate success with dummy data:
    # if file_path == "data/department_summary.csv":
    #     data = { ... } # Your fallback data here
    #     return pd.DataFrame(data)
    # else:
    #     raise FileNotFoundError(f"Path {file_path} not handled in dummy function")


# --- Page Settings ---
st.set_page_config(
    page_title="لوحة مؤشرات البرامج الأكاديمية",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for RTL and Font ---
st.markdown("""
<style>
    /* General adjustments for RTL support */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* Keep other styles as original */
    /* Ensure Plotly charts align correctly in RTL */
    .plotly-chart .main-svg {
        direction: ltr !important; /* Plotly usually works best LTR internally */
    }
    .stTabs [data-baseweb="tab-list"] {
      justify-content: flex-start; /* Align tabs to the start (right in RTL) */
    }
    .stButton>button {
        margin-left: 5px; /* Add some space between buttons if needed */
    }
    /* Adjust sidebar content alignment if necessary */
    .stSidebar .stMarkdown, .stSidebar .stInfo {
        text-align: right !important;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 لوحة مؤشرات البرامج الأكاديمية")
    st.markdown("### كلية القرآن الكريم والدراسات الإسلامية")
with col2:
    today = datetime.now().strftime("%Y/%m/%d")
    # Align date to the left (visual right in RTL page)
    st.markdown(f"<div style='text-align: left;'>التاريخ: {today}</div>", unsafe_allow_html=True)

# --- Sidebar Welcome Message ---
with st.sidebar:
    st.info(
        "مرحباً بك في لوحة المعلومات\n\n" +
        "استخدم هذه اللوحة لاستكشاف مؤشرات البرامج الأكاديمية المختلفة."
        # "اختر برنامجًا من القائمة أعلاه لعرض تفاصيله" # Commented out as there's no program selector in the sidebar in the provided code
    )
    st.markdown("---") # Add a separator

# --- Data Loading Functions with Fallback ---
@st.cache_data(ttl=3600)
def load_department_summary():
    """Loads department summary data, uses fallback on error."""
    try:
        # Replace with your actual data loading logic (e.g., from GitHub, DB, API)
        # df = get_github_file_content("data/department_summary.csv")
        # For demonstration, we'll force an error to show fallback
        raise ValueError("Forced error to load fallback department data")
        # return df
    except Exception as e:
        st.warning(f"⚠️ فشل تحميل ملخص الأقسام: {e}. استخدام بيانات تجريبية.")
        # Fallback data if loading fails
        data = {
            "البرنامج": [
                "بكالوريوس في القرآن وعلومه", "بكالوريوس القراءات",
                "ماجستير الدراسات القرآنية المعاصرة", "ماجستير القراءات",
                "دكتوراه علوم القرآن", "دكتوراه القراءات"
            ],
            "عدد الطلاب": [125, 110, 90, 120, 70, 85],
            "عدد الطالبات": [85, 70, 60, 80, 50, 55],
            "أعضاء هيئة التدريس": [15, 12, 8, 10, 5, 6]
        }
        return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_yearly_data(programs_list):
    """Generates or loads yearly data, uses fallback on error."""
    if not programs_list: # Handle case where program list is empty
         st.warning("⚠️ لا يمكن إنشاء بيانات سنوية بدون قائمة برامج. استخدام بيانات تجريبية.")
         programs_list = ["برنامج تجريبي 1", "برنامج تجريبي 2"] # Fallback programs

    try:
        # Replace with your actual data loading or generation logic
        # For demonstration, we generate data
        years = list(range(2020, 2025))
        data = []
        for year in years:
            for i, program in enumerate(programs_list):
                # Simulate some data trends
                male_students = 60 + (year - 2020) * 5 + i * 10 + (i%2)*5 # Base + year trend + program diff + variation
                female_students = 40 + (year - 2020) * 5 + i * 8 + ((i+1)%2)*5 # Base + year trend + program diff + variation
                data.append({
                    "العام": year,
                    "البرنامج": program,
                    "عدد الطلاب": male_students,
                    "عدد الطالبات": female_students,
                    "المجموع": male_students + female_students,
                    "نسبة النجاح": min(95, 70 + (year - 2020) * 2 + i * 2 + (i%3)), # Ensure max 95%
                    "معدل الرضا": min(90, 75 + (year - 2020) * 1.5 + i + (i%2)*2) # Ensure max 90%
                })
        if not data: # If loop didn't run
             raise ValueError("No yearly data generated.")
        return pd.DataFrame(data)

    except Exception as e:
        st.warning(f"⚠️ فشل تحميل/إنشاء البيانات السنوية: {e}. استخدام بيانات تجريبية.")
        # Fallback yearly data
        years = list(range(2020, 2025))
        data = []
        fallback_programs = ["برنامج تجريبي أ", "برنامج تجريبي ب"]
        for year in years:
            for i, program in enumerate(fallback_programs):
                 data.append({
                    "العام": year, "البرنامج": program,
                    "عدد الطلاب": 50 + (year-2020)*2, "عدد الطالبات": 40 + (year-2020)*3,
                    "المجموع": 90 + (year-2020)*5, "نسبة النجاح": 75 + (year-2020), "معدل الرضا": 80 + (year-2020)
                 })
        return pd.DataFrame(data)


@st.cache_data(ttl=3600)
def load_faculty_achievements():
    """Loads faculty achievements, uses fallback on error."""
    try:
        # Replace with your actual data loading logic
        # raise ValueError("Forced error to load fallback achievements")
        achievements = [
            {"العضو": "د. محمد أحمد", "الإنجاز": "نشر بحث في مجلة عالمية", "التاريخ": "2025-04-15", "النقاط": 50, "البرنامج": "بكالوريوس في القرآن وعلومه"},
            {"العضو": "د. عائشة سعد", "الإنجاز": "إطلاق مبادرة تعليمية", "التاريخ": "2025-03-10", "النقاط": 40, "البرنامج": "دكتوراه علوم القرآن"},
            {"العضو": "د. عبدالله محمد", "الإنجاز": "المشاركة في مؤتمر دولي", "التاريخ": "2025-02-25", "النقاط": 35, "البرنامج": "بكالوريوس القراءات"},
            {"العضو": "د. فاطمة علي", "الإنجاز": "الحصول على جائزة تميز", "التاريخ": "2025-01-20", "النقاط": 60, "البرنامج": "ماجستير القراءات"},
            {"العضو": "د. خالد يوسف", "الإنجاز": "تأليف كتاب منهجي", "التاريخ": "2024-12-05", "النقاط": 45, "البرنامج": "بكالوريوس القراءات"},
        ]
        df = pd.DataFrame(achievements)
        # Ensure date column is datetime type
        df['التاريخ'] = pd.to_datetime(df['التاريخ'])
        return df
    except Exception as e:
        st.warning(f"⚠️ فشل تحميل إنجازات الأعضاء: {e}. استخدام بيانات تجريبية.")
        # Fallback achievement data
        achievements = [
            {"العضو": "عضو تجريبي 1", "الإنجاز": "إنجاز تجريبي أ", "التاريخ": "2025-01-01", "النقاط": 10, "البرنامج": "برنامج تجريبي"},
            {"العضو": "عضو تجريبي 2", "الإنجاز": "إنجاز تجريبي ب", "التاريخ": "2025-02-01", "النقاط": 15, "البرنامج": "برنامج تجريبي"},
        ]
        df = pd.DataFrame(achievements)
        df['التاريخ'] = pd.to_datetime(df['التاريخ'])
        return df


@st.cache_data(ttl=3600)
def load_top_faculty():
    """Loads top faculty data, uses fallback on error."""
    try:
        # Replace with your actual data loading logic
        # raise ValueError("Forced error to load fallback top faculty")
        top_faculty = [
            {"الاسم": "د. عائشة سعد", "اللقب": "العضو القمة", "الشارة": "👑", "النقاط": 320, "البرنامج": "دكتوراه علوم القرآن"},
            {"الاسم": "د. محمد أحمد", "اللقب": "العضو المميز", "الشارة": "🌟", "النقاط": 280, "البرنامج": "بكالوريوس في القرآن وعلومه"},
            {"الاسم": "د. عبدالله محمد", "اللقب": "العضو الفعال", "الشارة": "🔥", "النقاط": 210, "البرنامج": "بكالوريوس القراءات"}
        ]
        return pd.DataFrame(top_faculty)
    except Exception as e:
        st.warning(f"⚠️ فشل تحميل بيانات الأعضاء المميزين: {e}. استخدام بيانات تجريبية.")
        # Fallback top faculty data
        top_faculty = [
            {"الاسم": "عضو تجريبي مميز 1", "اللقب": "مميز", "الشارة": "⭐", "النقاط": 100, "البرنامج": "برنامج تجريبي"},
            {"الاسم": "عضو تجريبي مميز 2", "اللقب": "فعال", "الشارة": "💡", "النقاط": 80, "البرنامج": "برنامج تجريبي"},
        ]
        return pd.DataFrame(top_faculty)


# --- Main Data Loading and Processing ---
# Initialize variables with default values before the try block
total_students = 0
total_female_students = 0
dept_data = pd.DataFrame([])
yearly_data = pd.DataFrame([])
latest_year_data = pd.DataFrame([])
faculty_achievements = pd.DataFrame([])
top_faculty = pd.DataFrame([])
programs = []
data_load_successful = False # Flag to track success

try:
    # Attempt to load real data
    dept_data = load_department_summary()

    if not dept_data.empty and "عدد الطلاب" in dept_data.columns and "عدد الطالبات" in dept_data.columns:
        total_students = int(dept_data["عدد الطلاب"].sum()) # Ensure integer
        total_female_students = int(dept_data["عدد الطالبات"].sum()) # Ensure integer
        programs = dept_data["البرنامج"].unique().tolist()
    else:
        # Handle case where dept_data loaded but is empty or lacks columns
        st.warning("⚠️ بيانات الأقسام المحملة فارغة أو تفتقد أعمدة ضرورية.")
        # Keep totals as 0, programs list empty

    # Load yearly data, passing the loaded programs list
    yearly_data = load_yearly_data(programs) # Use fallback within function if needed

    if not yearly_data.empty and "العام" in yearly_data.columns:
        max_year = yearly_data["العام"].max()
        latest_year_data = yearly_data[yearly_data["العام"] == max_year].copy()
    else:
        st.warning("⚠️ البيانات السنوية فارغة أو تفتقد عمود 'العام'.")
        latest_year_data = pd.DataFrame([]) # Ensure it's an empty DF

    faculty_achievements = load_faculty_achievements()
    top_faculty = load_top_faculty()

    # If we reach here without major errors in essential data (dept_data, yearly_data)
    if not dept_data.empty and not yearly_data.empty:
         data_load_successful = True

except Exception as e:
    st.error(f"❌ حدث خطأ عام أثناء تحميل ومعالجة البيانات: {e}")
    st.error("سيتم عرض اللوحة ببيانات محدودة أو تجريبية.")
    # Print traceback for debugging if needed (optional)
    # st.error("Traceback:")
    # st.code(traceback.format_exc())

    # Ensure variables are reset to safe defaults / empty states
    total_students = 0
    total_female_students = 0
    dept_data = pd.DataFrame([])
    yearly_data = pd.DataFrame([])
    latest_year_data = pd.DataFrame([])
    faculty_achievements = load_faculty_achievements() # Load fallback
    top_faculty = load_top_faculty() # Load fallback
    programs = []
    data_load_successful = False

# --- Key Performance Indicators (KPIs) ---
st.subheader("المؤشرات الرئيسية")
cols = st.columns(4)

# Default KPI values
kpi_success_rate = "N/A"
kpi_success_desc = ""
kpi_satisfaction_rate = "N/A"
kpi_satisfaction_desc = ""

# Calculate KPIs only if data is available
if not latest_year_data.empty:
    # Avoid division by zero if no students
    total_latest_students = latest_year_data['المجموع'].sum()
    if total_latest_students > 0:
        # Calculate weighted average for success and satisfaction if possible
        # Example: Weighted by total students per program
        weighted_success = (latest_year_data['نسبة النجاح'] * latest_year_data['المجموع']).sum() / total_latest_students
        weighted_satisfaction = (latest_year_data['معدل الرضا'] * latest_year_data['المجموع']).sum() / total_latest_students
        kpi_success_rate = f"{weighted_success:.1f}%"
        kpi_satisfaction_rate = f"{weighted_satisfaction:.1f}%"
        # Add descriptions based on comparison with previous year if available
        # kpi_success_desc = "+X% عن العام الماضي"
        # kpi_satisfaction_desc = "+Y% عن العام الماضي"
    else:
        # Handle case with data but zero students
        kpi_success_rate = "0%"
        kpi_satisfaction_rate = "0%"


with cols[0]:
    desc_m1 = "لا توجد بيانات للمقارنة" if not data_load_successful else "+3% عن العام الماضي (مثال)"
    ui.metric_card(title="إجمالي الطلاب", content=f"{total_students:,}", description=desc_m1, key="m1").render()
with cols[1]:
    desc_m2 = "لا توجد بيانات للمقارنة" if not data_load_successful else "+7% عن العام الماضي (مثال)"
    ui.metric_card(title="إجمالي الطالبات", content=f"{total_female_students:,}", description=desc_m2, key="m2").render()
with cols[2]:
    desc_m3 = "" if not data_load_successful else "+3% عن العام الماضي (مثال)"
    ui.metric_card(title="معدل النجاح الإجمالي", content=kpi_success_rate, description=desc_m3, key="m3").render()
with cols[3]:
    desc_m4 = "" if not data_load_successful else "+4% عن العام الماضي (مثال)"
    ui.metric_card(title="متوسط رضا الطلاب", content=kpi_satisfaction_rate, description=desc_m4, key="m4").render()

st.markdown("---")

# --- Academic Program Analysis ---
st.subheader("تحليل البرامج الأكاديمية")

# Check if essential data for this section is available
if not latest_year_data.empty and not dept_data.empty and 'البرنامج' in latest_year_data.columns:
    # Initialize session state for tabs if it doesn't exist
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "tab1" # Default to first tab ID

    # Define tabs using ui.tabs
    with ui.tabs(value=st.session_state.active_tab, key="analysis_tabs"):
        ui.tab("توزيع الطلاب والطالبات", id="tab1")
        ui.tab("مقارنة البرامج", id="tab2")
        ui.tab("التطور السنوي", id="tab3")

    # Get the currently selected tab value from session state
    active_tab_id = st.session_state.analysis_tabs # The key of ui.tabs holds the selected tab's id

    # --- Tab 1: Student Distribution ---
    if active_tab_id == "tab1":
        st.markdown("##### توزيع الطلاب والطالبات الإجمالي وحسب البرنامج")
        c1, c2 = st.columns(2)
        with c1:
            if total_students > 0 or total_female_students > 0:
                pie_df = pd.DataFrame({"الفئة": ["الطلاب", "الطالبات"], "العدد": [total_students, total_female_students]})
                fig_pie = px.pie(pie_df, values="العدد", names="الفئة", title="التوزيع الإجمالي للطلاب والطالبات",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_layout(legend_title_text='الفئة', title_x=0.5) # Center title
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("لا توجد بيانات لعرض توزيع الطلاب والطالبات.")
        with c2:
            if not latest_year_data.empty and "عدد الطلاب" in latest_year_data.columns and "عدد الطالبات" in latest_year_data.columns:
                fig_bar_dist = px.bar(latest_year_data, y="البرنامج", x=["عدد الطلاب", "عدد الطالبات"],
                                      barmode="stack", title="توزيع الطلاب والطالبات حسب البرنامج (آخر سنة)",
                                      labels={"value": "عدد الطلاب/الطالبات", "variable": "الفئة"},
                                      color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_bar_dist.update_layout(yaxis_title="البرنامج", xaxis_title="العدد", legend_title_text='الفئة', title_x=0.5)
                st.plotly_chart(fig_bar_dist, use_container_width=True)
            else:
                st.info("لا توجد بيانات لعرض التوزيع حسب البرنامج.")

    # --- Tab 2: Program Comparison ---
    elif active_tab_id == "tab2":
        st.markdown("##### مقارنة مؤشرات الأداء ونسبة الطالبات بين البرامج (آخر سنة)")
        c3, c4 = st.columns(2)
        with c3:
            if not latest_year_data.empty and "نسبة النجاح" in latest_year_data.columns and "معدل الرضا" in latest_year_data.columns:
                fig_bar_comp = px.bar(latest_year_data, x="البرنامج", y=["نسبة النجاح", "معدل الرضا"],
                                      barmode="group", title="مقارنة نسبة النجاح ومعدل الرضا",
                                      labels={"value": "النسبة (%)", "variable": "المؤشر"},
                                      color_discrete_sequence=px.colors.qualitative.Set2)
                fig_bar_comp.update_layout(xaxis_title="البرنامج", yaxis_title="النسبة (%)", legend_title_text='المؤشر', title_x=0.5)
                st.plotly_chart(fig_bar_comp, use_container_width=True)
            else:
                st.info("لا توجد بيانات كافية لمقارنة مؤشرات البرامج.")

        with c4:
            if not latest_year_data.empty and "عدد الطلاب" in latest_year_data.columns and "عدد الطالبات" in latest_year_data.columns:
                # Calculate female-to-male ratio, handle division by zero
                latest_year_data["نسبة الطالبات للطلاب"] = (
                    latest_year_data.apply(lambda row: (row["عدد الطالبات"] / row["عدد الطلاب"] * 100) if row["عدد الطلاب"] > 0 else 0, axis=1)
                ).round(1)
                fig_bar_ratio = px.bar(latest_year_data, x="البرنامج", y="نسبة الطالبات للطلاب",
                                       title="نسبة الطالبات إلى الطلاب في كل برنامج (%)",
                                       text='نسبة الطالبات للطلاب', # Show value on bar
                                       color_discrete_sequence=px.colors.qualitative.Set3)
                fig_bar_ratio.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_bar_ratio.update_layout(xaxis_title="البرنامج", yaxis_title="النسبة (%)", title_x=0.5)
                st.plotly_chart(fig_bar_ratio, use_container_width=True)
            else:
                st.info("لا توجد بيانات كافية لحساب نسبة الطالبات للطلاب.")

    # --- Tab 3: Yearly Evolution ---
    elif active_tab_id == "tab3":
        st.markdown("##### التطور السنوي لأعداد الطلاب والمؤشرات لبرنامج محدد")
        if programs: # Check if programs list is available
            sp, gp = st.columns([2, 1])
            with sp:
                # Use standard Streamlit selectbox if ui.select causes issues or isn't needed
                selected_program = st.selectbox(
                    label="اختر البرنامج لعرض تطوره السنوي:",
                    options=programs,
                    index=0, # Default to the first program
                    key="sel_prog_st"
                )
                # selected_program = ui.select( # Using shadcn ui select
                #     label="اختر البرنامج لعرض تطوره السنوي:",
                #     options=[{"label": prog, "value": prog} for prog in programs],
                #     default_value=programs[0], # Use default_value for ui.select
                #     key="sel_prog_ui"
                # )

            with gp:
                # Use standard Streamlit radio if ui.radio_group causes issues
                gender_option = st.radio(
                     label="اختر الفئة:",
                     options=["الكل", "الطلاب", "الطالبات"],
                     index=0, # Default to 'الكل'
                     horizontal=True,
                     key="sel_gen_st"
                )
                gender_map = {"الكل": "all", "الطلاب": "male", "الطالبات": "female"}
                gender_value = gender_map[gender_option]

                # gender_option_ui = ui.radio_group( # Using shadcn ui radio_group
                #     label="اختر الفئة:",
                #     options=[{"label": "الكل", "value": "all"},
                #              {"label": "الطلاب", "value": "male"},
                #              {"label": "الطالبات", "value": "female"}],
                #     default_value="all", # Use default_value for ui.radio_group
                #     orientation="horizontal",
                #     key="sel_gen_ui"
                # )
                # gender_value = gender_option_ui # Get value directly

            # Filter yearly data for the selected program
            prog_df = yearly_data[yearly_data["البرنامج"] == selected_program].copy()

            if prog_df.empty:
                st.warning(f"لا توجد بيانات سنوية متاحة للبرنامج المحدد: {selected_program}")
            else:
                # Determine columns to plot based on gender selection
                if gender_value == "all":
                    plot_cols_students = ["عدد الطلاب", "عدد الطالبات", "المجموع"]
                    plot_cols_kpi = ["نسبة النجاح", "معدل الرضا"]
                elif gender_value == "male":
                    plot_cols_students = ["عدد الطلاب"]
                    plot_cols_kpi = [] # KPIs usually apply to all
                else: # female
                    plot_cols_students = ["عدد الطالبات"]
                    plot_cols_kpi = []

                # Plot student numbers evolution
                if plot_cols_students:
                    fig_line_students = px.line(prog_df, x="العام", y=plot_cols_students,
                                                title=f"تطور أعداد الطلاب في برنامج {selected_program}",
                                                markers=True, labels={"value": "العدد", "variable": "الفئة"})
                    fig_line_students.update_layout(xaxis_title="العام", yaxis_title="العدد", legend_title_text='الفئة', title_x=0.5)
                    st.plotly_chart(fig_line_students, use_container_width=True)

                # Plot KPI evolution (only if 'all' is selected or KPIs make sense per gender)
                if plot_cols_kpi:
                     fig_line_kpi = px.line(prog_df, x="العام", y=plot_cols_kpi,
                                           title=f"تطور المؤشرات في برنامج {selected_program}",
                                           markers=True, labels={"value": "النسبة (%)", "variable": "المؤشر"})
                     fig_line_kpi.update_layout(xaxis_title="العام", yaxis_title="النسبة (%)", legend_title_text='المؤشر', title_x=0.5)
                     st.plotly_chart(fig_line_kpi, use_container_width=True)

        else:
            st.warning("لا توجد قائمة برامج متاحة للاختيار.")
else:
    st.warning("لا يمكن عرض تحليل البرامج بسبب عدم توفر بيانات البرامج أو البيانات السنوية.")

st.markdown("---")

# --- Faculty and Achievements ---
st.subheader("أعضاء هيئة التدريس والإنجازات")
colA, colB = st.columns(2)

with colA:
    st.markdown("#### 🏆 أعضاء هيئة التدريس المميزين")
    if not top_faculty.empty:
        # Sort by points descending if needed
        top_faculty_sorted = top_faculty.sort_values(by="النقاط", ascending=False)
        for _, member in top_faculty_sorted.iterrows():
            # Use unique key for each card
            with ui.card(key=f"top_faculty_{member['الاسم']}"):
                st.markdown(f"**{member['الشارة']} {member['الاسم']}**")
                ui.badge(member['اللقب'], variant="outline").render()
                st.write(f"البرنامج: {member['البرنامج']}")
                st.write(f"النقاط: {member['النقاط']}")
    else:
        st.info("لا توجد بيانات متاحة حالياً عن أعضاء هيئة التدريس المميزين.")
    # Add button to navigate (ensure the target page exists)
    # st.button("عرض جميع الأعضاء", key="btn_all_faculty", on_click=lambda: st.experimental_set_query_params(page="هيئة_التدريس"))

with colB:
    st.markdown("#### 🌟 أحدث الإنجازات")
    if not faculty_achievements.empty:
        # Sort by date descending
        achievements_sorted = faculty_achievements.sort_values(by='التاريخ', ascending=False)
        # Display top 5 achievements
        for _, ach in achievements_sorted.head(5).iterrows():
             st.write(f"**{ach['العضو']}** ({ach['البرنامج']})")
             st.write(f"— {ach['الإنجاز']}")
             st.write(f"— التاريخ: {ach['التاريخ']:%d/%m/%Y} | النقاط: {ach['النقاط']}")
             st.markdown("---") # Separator between achievements
    else:
        st.info("لا توجد بيانات متاحة حالياً عن إنجازات أعضاء هيئة التدريس.")
    # Add button to navigate (ensure the target page exists)
    # st.button("عرض جميع الإنجازات", key="btn_all_ach", on_click=lambda: st.experimental_set_query_params(page="إنجازات_الأعضاء"))

st.markdown("---")

# --- Key Program Indicators Heatmap ---
st.subheader("مؤشرات البرامج الرئيسية (آخر سنة)")
# Check if data and necessary columns are available
if not latest_year_data.empty and "نسبة النجاح" in latest_year_data.columns and "معدل الرضا" in latest_year_data.columns and "البرنامج" in latest_year_data.columns:
    try:
        # Select and ensure numeric types for heatmap
        heat_data = latest_year_data[["نسبة النجاح", "معدل الرضا"]].astype(float)
        program_labels = latest_year_data["البرنامج"].tolist()
        indicator_labels = ["نسبة النجاح (%)", "معدل الرضا (%)"]

        heat = go.Figure(data=go.Heatmap(
            z=heat_data.values,
            x=indicator_labels,
            y=program_labels,
            colorscale="Viridis", # Or choose another scale like 'Blues', 'Greens'
            hoverongaps=False,
            text=heat_data.values, # Add text on cells
            texttemplate="%{text:.1f}" # Format text
            ))
        heat.update_layout(
            title="مقارنة المؤشرات الرئيسية بين البرامج (Heatmap)",
            xaxis_title="المؤشر",
            yaxis_title="البرنامج",
            yaxis_autorange='reversed', # Show top programs higher if desired
            title_x=0.5
        )
        st.plotly_chart(heat, use_container_width=True)
    except Exception as plot_err:
        st.warning(f"⚠️ حدث خطأ أثناء رسم المخطط الحراري: {plot_err}")
else:
    st.warning("لا يمكن عرض المخطط الحراري بسبب عدم توفر بيانات المؤشرات اللازمة لآخر سنة.")

st.markdown("---")

# --- Usage Tips ---
with ui.card(key="usage_tips_card"):
    st.markdown(
        """
        **💡 نصائح للاستخدام**
        - استخدم علامات التبويب في قسم "تحليل البرامج الأكاديمية" لاستكشاف البيانات من زوايا مختلفة.
        - مرر الفأرة فوق الرسوم البيانية لعرض تفاصيل إضافية.
        - في تبويب "التطور السنوي"، يمكنك اختيار برنامج وفئة محددة (طلاب/طالبات/الكل) لعرض التغيرات عبر السنوات.
        - يتم تحديث البيانات بشكل دوري (أو عند إعادة تحميل الصفحة إذا لم يتم استخدام cache).
        """
    )

# Add footer (optional)
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 كلية القرآن الكريم والدراسات الإسلامية</div>", unsafe_allow_html=True)

