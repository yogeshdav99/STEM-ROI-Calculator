import streamlit as st
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

# --- SESSION STATE INITIALIZATION ---
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
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- SIDEBAR — Clean Global Settings ---
st.sidebar.markdown("#### ⚙️ Settings")

dark_mode = st.sidebar.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
st.session_state.dark_mode = dark_mode

# Inject design system (must come after dark mode state is set)
inject_premium_styles(dark_mode=st.session_state.dark_mode)

currency_choice = st.sidebar.selectbox(
    "Currency",
    options=list(CURRENCY_CONFIGS.keys()),
    index=0,
    help="Updates slider ranges and display currency."
)

currency_config = CURRENCY_CONFIGS[currency_choice]
currency_symbol = currency_config["symbol"]
exchange_rate = currency_config["exchange_rate"]

st.sidebar.caption(f"1 USD = {exchange_rate:,.2f} {currency_symbol} · Updated: {LIVE_RATES.get('_last_updated', 'Unknown')}")

# --- SIDEBAR — Real-Time Tracker ---
st.sidebar.divider()
true_cost_val = st.session_state.true_economic_cost_local
direct_cost_val = st.session_state.total_direct_cost_local

st.sidebar.markdown(f"""
<div class="md-tracker-card">
    <h4>Real-Time Tracker</h4>
    <div class="md-tracker-value">{currency_symbol}{true_cost_val:,.0f}</div>
    <div class="md-tracker-label">True Economic Cost</div>
    <hr style="border: none; border-top: 1px solid rgba(26,115,232,0.15); margin: 0.75rem 0;">
    <div class="md-tracker-value" style="font-size: 1.1rem;">{currency_symbol}{direct_cost_val:,.0f}</div>
    <div class="md-tracker-label">Direct Cost</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.step == 0:
    st.sidebar.caption("Values will populate once you begin Task 1.")
else:
    st.sidebar.info("**Tip:** Adjust sliders in Task 1 & 2, then check Task 3 to see Break-Even changes!")

st.sidebar.divider()

col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.clear()
        st.rerun()
with col_sb2:
    if st.button("👤 Developer", use_container_width=True):
        st.session_state.show_profile = not st.session_state.show_profile
        st.rerun()

# --- Developer Profile Modal ---
if st.session_state.show_profile:
    col_prof1, col_prof2, col_prof3 = st.columns([1, 8, 1])
    with col_prof3:
        # Wrap button in a container for custom positioning if needed
        st.markdown('<div class="profile-close-btn">', unsafe_allow_html=True)
        if st.button("✖", key="close_profile_top", help="Close Profile"):
            st.session_state.show_profile = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_prof2:
        developer_profile.render()
    
    st.divider()

# --- TOP NAVIGATION BAR ---
st.markdown('<div class="top-nav-anchor"></div>', unsafe_allow_html=True)
nav_options = [
    "Welcome", 
    "1. What Will It Cost?", 
    "2. What About My Loan?", 
    "3. Will It Pay Off?",
    "4. What If Things Go Wrong?"
]
selected_nav = st.radio("Navigation", nav_options, index=st.session_state.step, horizontal=True, label_visibility="collapsed")

new_step = nav_options.index(selected_nav)
if new_step != st.session_state.step:
    st.session_state.step = new_step
    st.rerun()

# --- STEP INDICATOR ---
completed_steps = 0
if st.session_state.total_direct_cost_local > 0 or st.session_state.true_economic_cost_local > 0:
    completed_steps = 1
if "saved_salary_A" in st.session_state:
    completed_steps = max(completed_steps, 2)
if "mc_results_a" in st.session_state:
    completed_steps = max(completed_steps, 3)

progress_val = st.session_state.step / max(1, (len(nav_options) - 1))
st.progress(progress_val)

# Step chips
chip_html = ""
for i, name in enumerate(nav_options):
    short_name = name.split(":")[0].strip()
    active_class = "active" if i == st.session_state.step else ""
    if i > 0 and i <= completed_steps:
        icon = "✓"
    elif i == st.session_state.step:
        icon = "●"
    else:
        icon = f"{i}"
    chip_html += f'<span class="md-step-chip {active_class}">{icon} {short_name}</span> '

st.markdown(f'<div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1rem;">{chip_html}</div>', unsafe_allow_html=True)


# --- INLINE SVG LOGO ---
def render_logo_svg():
    """Returns a minimalist globe + chart SVG logo."""
    return """
    <div class="md-logo">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Globe circle -->
            <circle cx="32" cy="32" r="28" stroke="var(--md-primary)" stroke-width="2.5" fill="none" opacity="0.2"/>
            <circle cx="32" cy="32" r="28" stroke="var(--md-primary)" stroke-width="2.5" fill="none" stroke-dasharray="176" stroke-dashoffset="44"/>
            <!-- Globe meridians -->
            <ellipse cx="32" cy="32" rx="12" ry="28" stroke="var(--md-primary)" stroke-width="1.5" fill="none" opacity="0.3"/>
            <line x1="4" y1="32" x2="60" y2="32" stroke="var(--md-primary)" stroke-width="1.5" opacity="0.3"/>
            <!-- Upward trend line -->
            <polyline points="14,46 24,38 34,40 46,22 54,16" stroke="var(--md-primary)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <!-- Trend arrow head -->
            <polyline points="48,16 54,16 54,22" stroke="var(--md-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <!-- Dot at end -->
            <circle cx="54" cy="16" r="2.5" fill="var(--md-primary)"/>
        </svg>
    </div>
    """


# --- PROGRESSIVE DISCLOSURE HELPER ---
def is_task1_complete():
    """Returns True if the user has entered meaningful data in Task 1."""
    return st.session_state.total_direct_cost_local > 0 or st.session_state.true_economic_cost_local > 0


def render_locked_task(task_name):
    """Renders a friendly locked-task placeholder."""
    st.markdown(f"""
    <div class="md-locked-task">
        <i class="fas fa-lock"></i>
        <h3>{task_name} — Locked</h3>
        <p>Complete <strong>1. What Will It Cost?</strong> first to unlock this section.<br>
        Enter your tuition and living expenses to get started.</p>
    </div>
    """, unsafe_allow_html=True)


# --- STEP 0: WELCOME / HERO ---
def render_step_welcome():
    # Hero Section
    logo_svg = render_logo_svg()
    hero_html = (
        '<div class="md-hero">'
        + logo_svg
        + '<div class="md-hero-title">Global Degree Planner</div>'
        + '<div class="md-hero-subtitle">Uncover the true financial reality of studying abroad. Make smarter decisions with data-driven cost projections, loan analysis, and career ROI forecasting.</div>'
        + '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # Quick-Start Preview Alert
    st.markdown("""
    <div class="preview-alert">
        <div class="preview-icon"><i class="fas fa-bolt"></i></div>
        <div class="preview-content">
            <h4>Did You Know?</h4>
            <p>The average international student underestimates their degree cost by <span class="highlight-badge">> 25%</span>. This tool shows you the <strong>hidden costs</strong> no brochure mentions, the <strong>extra fees</strong> banks add to your loan, and whether your <strong>dream job can actually pay it all back</strong>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    st.markdown("#### What you'll discover:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-search-dollar"></i></span><div class="feature-title">The Real Price Tag</div><div class="feature-text">Find out what you will actually spend, plus the money you lose by leaving your current job.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-university"></i></span><div class="feature-title">The Bank\'s Cut</div><div class="feature-text">See how bank fees and interest add up while you are studying, before you even graduate.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><span class="feature-icon"><i class="fas fa-chart-line"></i></span><div class="feature-title">The Final Verdict</div><div class="feature-text">Compare career options to see when you will break even and if the degree is worth the cost.</div></div>', unsafe_allow_html=True)
    
    st.write("")  # Spacer

    # Personalization & Get Started
    with st.container(border=True):
        if st.session_state.student_name:
            st.markdown(f"### Welcome back, {st.session_state.student_name}!")
        else:
            st.markdown("### Let's get started")
        
        col_input, col_btn = st.columns([3, 1], vertical_alignment="bottom")
        with col_input:
            name_input = st.text_input("Your name (optional)", value=st.session_state.student_name, placeholder="Enter your name to personalize...")
            st.session_state.student_name = name_input
        with col_btn:
            if st.button("Begin Analysis →", type="primary", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

    st.divider()

    with st.expander("**Quick Guide: How to use this tool**", expanded=False):
        st.markdown("""
        1. **Set your currency** in the sidebar (e.g., INR, USD, NZD).
        2. **Use the navigation bar** at the top to move between steps.
        
        ---
        - **1. What Will It Cost?:** Enter tuition, living costs, and current salary to find the *true* cost.
        - **2. What About My Loan?:** Input loan details to reveal hidden fees and real monthly payments.
        - **3. Will It Pay Off?:** Compare post-graduation careers side-by-side for long-term value.
        - **4. What If Things Go Wrong?:** Stress-test your plan against the real-world economy.
        """)


# --- STEP RENDERING FUNCTIONS ---
def render_step_investment():
    total_dir, true_eco, prog_dur = tab_cost.render(
        currency_choice, currency_config, currency_symbol, exchange_rate
    )
    st.session_state.total_direct_cost_local = total_dir
    st.session_state.true_economic_cost_local = true_eco
    st.session_state.program_duration = prog_dur

def render_step_loan():
    if not is_task1_complete():
        render_locked_task("Debt Analysis")
        return
    tab_loan.render(
        st.session_state.total_direct_cost_local, 
        st.session_state.program_duration, 
        currency_choice, currency_config, currency_symbol, exchange_rate
    )

def render_step_career():
    if not is_task1_complete():
        render_locked_task("Career & ROI Forecaster")
        return
    tab_career.render(
        st.session_state.true_economic_cost_local, 
        currency_symbol, exchange_rate
    )

def render_step_risk():
    if not is_task1_complete():
        render_locked_task("Risk Analysis")
        return
    tab_risk.render(
        st.session_state.true_economic_cost_local, 
        currency_symbol
    )


# --- MAIN CONTENT AREA ---
step_placeholder = st.empty()
with step_placeholder.container():
    if st.session_state.step == 0:
        render_step_welcome()
    elif st.session_state.step == 1:
        render_step_investment()
    elif st.session_state.step == 2:
        render_step_loan()
    elif st.session_state.step == 3:
        render_step_career()
    elif st.session_state.step == 4:
        render_step_risk()

# --- STICKY FOOTER NAVIGATION ---
if st.session_state.step > 0:
    st.markdown('<div class="sticky-footer"></div>', unsafe_allow_html=True)
    # Inject an empty div just as a marker, the actual buttons need to be positioned via CSS wrapper
    st.markdown("""
    <div class="sticky-footer-wrapper">
    """, unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
    with f_col1:
        if st.session_state.step > 1:
            if st.button("← Previous Step", use_container_width=True, key="prev_btn_footer"):
                st.session_state.step -= 1
                st.rerun()
        else:
            if st.button("🏠 Home", use_container_width=True, key="home_btn_footer"):
                st.session_state.step = 0
                st.rerun()
    with f_col3:
        if st.session_state.step < 4:
            if st.button("Next Step →", type="primary", use_container_width=True, key="next_btn_footer"):
                st.session_state.step += 1
                st.rerun()
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)