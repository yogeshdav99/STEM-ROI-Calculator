import streamlit as st
import base64
import os
from utils import inject_premium_styles, CURRENCY_CONFIGS, LIVE_RATES
import tab_cost
import tab_loan
import tab_career
import tab_risk
import developer_profile

# Configure page layout and title
st.set_page_config(
    page_title="Global Degree Planner",
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
    st.session_state.program_duration = 4.0
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

# --- TOP NAVIGATION BAR ---
st.markdown('<div class="top-nav-anchor"></div>', unsafe_allow_html=True)
nav_options = [
    "Welcome Dashboard", 
    "Task 1: Cost Projection", 
    "Task 2: Debt Analysis", 
    "Task 3: Career & ROI",
    "Task 4: Risk Analysis"
]
selected_nav = st.radio("Navigation", nav_options, index=st.session_state.step, horizontal=True, label_visibility="collapsed")

new_step = nav_options.index(selected_nav)
if new_step != st.session_state.step:
    st.session_state.step = new_step
    st.rerun()

st.divider()

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
st.sidebar.caption(f"🔄 Rates Updated: {LIVE_RATES.get('_last_updated', 'Unknown')}")

if st.session_state.show_profile:
    developer_profile.render()
    if st.button("✖️ Close Profile"):
        st.session_state.show_profile = False
        st.rerun()
    st.divider()

# --- STEP FUNCTIONS ---
def get_logo_base64():
    if os.path.exists("img"):
        for file in os.listdir("img"):
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp', 'svg')) and "pfp" not in file.lower():
                with open(os.path.join("img", file), "rb") as f:
                    ext = file.split('.')[-1].lower()
                    mime = "svg+xml" if ext == "svg" else ext
                    return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"
    return "https://cdn-icons-png.flaticon.com/512/2941/2941573.png"

def render_step_name():
    logo_src = get_logo_base64()
    # --- APP MAIN HEADER (Only renders on Step 0) ---
    col_logo, col_name, _ = st.columns([1.2, 1.5, 1], gap="medium")
    with col_logo:
        st.markdown(f"""
        <div class="hero-container" style="padding: 0.5rem; border-radius: 16px; height: 100%; display: flex; align-items: center; justify-content: center;">
            <img src="{logo_src}" alt="Logo" style="height: 120px;">
        </div>
        """, unsafe_allow_html=True)
    with col_name:
        name_input = st.text_input("What is your name?", value=st.session_state.student_name, placeholder="Enter your name to personalize your experience...")
        st.session_state.student_name = name_input
    
    if st.session_state.student_name:
        st.markdown(f"### Welcome, {st.session_state.student_name}! Let’s audit the investment in your future.")
    else:
        st.markdown("### Welcome! Let's build your financial calculator step-by-step.")
    
    st.write("This tool uncovers the financial realities of studying abroad so you can make a smarter decision. Let's get started.")
    st.divider()

    # --- NEW: "IMMEDIATE VALUE" & "RISK FACTORS" WIDGETS ---
    st.markdown("""
    <div class="preview-alert">
        <div class="preview-icon"><i class="fas fa-bolt"></i></div>
        <div class="preview-content">
            <h4>Quick-Start Preview</h4>
            <p>Did you know the average international student underestimates their degree cost by <span class="highlight-badge">> 25%</span>? This tool reveals the hidden math: your <strong>True Economic Cost</strong>, your loan's <strong>Capitalization Trap</strong>, and your career's <strong>Probability of Profit</strong>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### We'll help you answer the tough questions:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-search-dollar"></i></span><div class="feature-title">What is the True Cost?</div><div class="feature-text">We calculate your direct costs PLUS the hidden "opportunity cost" of lost salary.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-user-graduate"></i></span><div class="feature-title">Can I Afford the Debt?</div><div class="feature-text">We reveal how bank fees and study-period interest inflate your loan before you even graduate.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-chart-line"></i></span><div class="feature-title">Will the Degree Pay Off?</div><div class="feature-text">We use corporate finance models (NPV, IRR) and run 1,000 simulations to forecast your ROI.</div></div>', unsafe_allow_html=True)
    
    st.divider()

    with st.expander("**Quick Guide: How to use this tool**", expanded=True):
        st.markdown("""
        1. **Set your currency:** Use the sidebar on the left to pick your home currency (e.g., INR, USD).
        2. **Use the Navigation Menu** at the top of the page to jump between tasks.
        
        ---
        - **Task 1 (Cost):** Enter your tuition, living costs, and current salary to find the *true* cost of going to school.
        - **Task 2 (Debt):** Input your loan details to reveal hidden bank fees and see your real monthly payments.
        - **Task 3 (ROI):** Compare post-graduation jobs side-by-side to see if the degree actually pays off in the long run!
        - **Task 4 (Risk):** Run Monte Carlo simulations to view statistical probabilities of success.
        """)

def render_step_investment():
    total_dir, true_eco, prog_dur = tab_cost.render(
        currency_choice, currency_config, currency_symbol, exchange_rate
    )
    # Save to session state so they persist when moving to steps 2 and 3
    st.session_state.total_direct_cost_local = total_dir
    st.session_state.true_economic_cost_local = true_eco

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

def render_step_risk():
    tab_risk.render(
        st.session_state.true_economic_cost_local, 
        currency_symbol
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
    elif st.session_state.step == 4:
        render_step_risk()

st.divider()

# --- PERSISTENT REAL-TIME SUMMARY (SIDEBAR) ---
st.sidebar.divider()
st.sidebar.header("Real-Time Tracker")
st.sidebar.metric(
    "True Cost of Degree", 
    f"{currency_symbol}{st.session_state.true_economic_cost_local:,.0f}",
    help="Updates instantly as you move sliders. This includes direct costs + lost salary."
)

if st.session_state.step == 0:
    st.sidebar.caption("*(Values will populate once you begin Task 1)*")
else:
    st.sidebar.info(
        "**Tip:** Adjust the sliders in *Task 1* and *Task 2*, then check *Task 3* to see how your Break-Even Year changes instantly!"
    )

st.sidebar.divider()
if st.sidebar.button("Reset All / Start Over", use_container_width=True):
    st.session_state.clear()
    st.rerun()

if st.sidebar.button("Methodology & Developer", use_container_width=True):
    st.session_state.show_profile = not st.session_state.show_profile
    st.rerun()