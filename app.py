import streamlit as st
from utils import inject_premium_styles, CURRENCY_CONFIGS
import tab_cost
import tab_loan
import tab_career
import developer_profile

# Configure page layout and title
st.set_page_config(
    page_title="STEM ROI Calculator",
    layout="wide"
)

inject_premium_styles()

# --- WIZARD STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "total_direct_cost_local" not in st.session_state:
    st.session_state.total_direct_cost_local = 0.0
if "true_economic_cost_local" not in st.session_state:
    st.session_state.true_economic_cost_local = 0.0
if "program_duration" not in st.session_state:
    st.session_state.program_duration = 2.0
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

# --- SIDEBAR GLOBAL SETTINGS ---
st.sidebar.header("Global Settings")
currency_choice = st.sidebar.selectbox(
    "Select Currency",
    options=list(CURRENCY_CONFIGS.keys()),
    index=0,
    help="This updates the slider labels, ranges, and display currency for the calculator."
)

currency_config = CURRENCY_CONFIGS[currency_choice]
currency_symbol = currency_config["symbol"]
exchange_rate = currency_config["exchange_rate"]

st.sidebar.caption(f"1 USD = {exchange_rate:,.2f} {currency_symbol}")

# --- APP MAIN HEADER ---
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">STEM ROI Calculator</h1>
    <p class="hero-subtitle">Plan your study abroad journey with clear, stress-free math.</p>
</div>
""", unsafe_allow_html=True)

# --- DEVELOPER PROFILE TOGGLE ---
if st.session_state.show_profile:
    developer_profile.render()
    if st.button("✖️ Close Profile"):
        st.session_state.show_profile = False
        st.rerun()
    st.divider()

# --- WIZARD PROGRESS BAR ---
st.progress(st.session_state.step / 3)

# --- STEP FUNCTIONS ---
def render_step_name():
    name_input = st.text_input("What is your name?", value=st.session_state.student_name, placeholder="Enter your name to personalize your experience...")
    st.session_state.student_name = name_input
    
    if st.session_state.student_name:
        st.markdown(f"### Hello {st.session_state.student_name}! Let's build your financial calculator step-by-step.")
    else:
        st.markdown("### Let's build your financial calculator step-by-step.")
        
    with st.expander("**Quick Guide: How to use this tool**", expanded=False):
        st.markdown("""
        1. **Set your currency:** Use the sidebar on the left to pick your home currency (e.g., INR, USD).
        2. **Step 1 (Costs):** Enter your tuition, living costs, and current salary to find the *true* cost of going to school.
        3. **Step 2 (Loans):** Input your loan details to reveal hidden bank fees and see your real monthly payments.
        4. **Step 3 (Careers):** Compare post-graduation jobs side-by-side to see if the degree actually pays off in the long run!
        """)

def render_step_investment():
    total_dir, true_eco, prog_dur = tab_cost.render(
        currency_choice, currency_config, currency_symbol, exchange_rate
    )
    # Save to session state so they persist when moving to steps 2 and 3
    st.session_state.total_direct_cost_local = total_dir
    st.session_state.true_economic_cost_local = true_eco
    st.session_state.program_duration = prog_dur

def render_step_loan():
    tab_loan.render(
        st.session_state.total_direct_cost_local, 
        st.session_state.program_duration, 
        currency_choice, currency_config, currency_symbol, exchange_rate
    )

def render_step_career():
    tab_career.render(
        st.session_state.true_economic_cost_local, 
        currency_symbol, exchange_rate
    )

# --- STEP RENDERING LOGIC ---
step_placeholder = st.empty()
with step_placeholder.container():
    if st.session_state.step == 0:
        render_step_name()
    elif st.session_state.step == 1:
        render_step_investment()
    elif st.session_state.step == 2:
        render_step_loan()
    elif st.session_state.step == 3:
        render_step_career()

st.divider()

# --- NAVIGATION BUTTONS ---
col_nav1, col_nav2, col_nav3 = st.columns([1, 8, 1])
with col_nav1:
    if st.session_state.step > 0:
        if st.button("⬅️ Back"):
            st.session_state.step -= 1
            st.rerun()
with col_nav3:
    if st.session_state.step < 3:
        if st.button("Next ➡️"):
            st.session_state.step += 1
            st.rerun()

# --- PERSISTENT REAL-TIME SUMMARY (SIDEBAR) ---
st.sidebar.divider()
st.sidebar.header("📊 Real-Time Tracker")
st.sidebar.metric(
    "True Cost of Degree", 
    f"{currency_symbol}{st.session_state.true_economic_cost_local:,.0f}",
    help="Updates instantly as you move sliders. This includes direct costs + lost salary."
)
st.sidebar.info(
    "💡 **Tip:** Adjust the sliders in *Step 1* and *Step 2*, then check *Step 3* to see how your Break-Even Year changes instantly!"
)

st.sidebar.divider()
if st.sidebar.button("☕ Meet the Developer", use_container_width=True):
    st.session_state.show_profile = not st.session_state.show_profile
    st.rerun()