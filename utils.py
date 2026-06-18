import streamlit as st
import requests
import math
import numpy as np

def inject_premium_styles():
    st.markdown("""
    <style>
        /* FontAwesome for icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

        /* Premium Typography Stack (Fixed icon bug) */
        html, body, p, h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0f172a;
        }
        
        /* Compact Container Spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* App Background */
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
        }
        
        /* Dense Input Controls */
        [data-testid="stSlider"], [data-testid="stNumberInput"], [data-testid="stSelectbox"] {
            padding-bottom: 0rem !important;
            margin-bottom: -0.75rem !important;
        }
        label {
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            color: #475569 !important;
        }
        
        /* Unified Card Styles for Metrics and Containers */
        [data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {
            padding: 1.25rem;
            background: linear-gradient(135deg, #ffffff 0%, #f4f7fb 50%, #ffffff 100%) !important;
            background-size: 200% 200% !important;
            animation: boxGradientBG 8s ease infinite !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            max-width: 100%;
            box-sizing: border-box;
            position: relative;
            z-index: 1;
            border: none !important;
        }
        @keyframes boxGradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Prevent Long Currency Numbers from Breaking Layout */
        [data-testid="stMetricValue"] {
            font-size: clamp(0.9rem, 1.8vw, 1.4rem) !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            max-width: 100% !important;
        }
        [data-testid="stMetricValue"] > div {
            font-size: clamp(0.9rem, 1.8vw, 1.4rem) !important;
        }
        
        .hero-container {
            position: relative;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(241, 245, 249, 0.8) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            overflow: hidden;
            z-index: 1;
        }
        .hero-container::before {
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle at 30% 30%, rgba(99,102,241,0.08) 0%, transparent 40%),
                        radial-gradient(circle at 70% 70%, rgba(236,72,153,0.08) 0%, transparent 40%);
            z-index: -1; animation: slowRotate 15s linear infinite;
        }
        @keyframes slowRotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* Floating Logo Animation */
        .hero-container img {
            animation: floatLogo 4s ease-in-out infinite;
        }
        @keyframes floatLogo {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }
        
        .hero-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            color: #0f172a !important;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hero-subtitle {
            font-size: 1rem;
            font-weight: 400;
            color: #475569;
        }
        
        /* Input Box Enhancements */
        div[data-baseweb="input"] > div, 
        div[data-baseweb="select"] > div {
            border-radius: 0.5rem !important;
            border: 1px solid #cbd5e1 !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }
        div[data-baseweb="input"] > div:hover, 
        div[data-baseweb="select"] > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        }
        div[data-baseweb="input"] > div:focus-within, 
        div[data-baseweb="select"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3) !important;
            animation: inputPulse 2s infinite !important;
        }
        @keyframes inputPulse {
            0% { box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3); }
            50% { box-shadow: 0 0 0 5px rgba(99, 102, 241, 0.5); }
            100% { box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3); }
        }
        
        /* DataFrames & Tables */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: cascadeSlideUp 0.6s ease-out both;
        }
        [data-testid="stDataFrame"]:hover, [data-testid="stTable"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        
        /* Plotly Charts */
        [data-testid="stPlotlyChart"] {
            animation: popIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
            transition: transform 0.3s ease;
            border-radius: 12px;
        }
        [data-testid="stPlotlyChart"]:hover {
            transform: scale(1.02);
        }
        @keyframes popIn {
            0% { opacity: 0; transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        /* Smooth Cascade Fade-in Animation for UI Elements */
        @keyframes cascadeSlideUp {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        [data-testid="stVerticalBlock"] > div,
        [data-testid="stMarkdownContainer"],
        [data-testid="stSlider"] {
            animation: cascadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        
        /* Force Equal Height for Columns & Cards */
        [data-testid="column"] > [data-testid="stVerticalBlock"] {
            height: 100%;
        }
        [data-testid="column"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        /* Animated Gradient Border Magic */
        [data-testid="stMetric"]::before, [data-testid="stVerticalBlockBorderWrapper"]::before, [data-testid="stExpander"]::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 12px;
            padding: 2px; /* Border thickness */
            background: linear-gradient(270deg, #6366f1, #a855f7, #ec4899, #6366f1);
            background-size: 200% 200%;
            animation: gradientBorder 5s ease infinite;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            z-index: -1;
            opacity: 0.25;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        [data-testid="stMetric"]:hover, [data-testid="stVerticalBlockBorderWrapper"]:hover, [data-testid="stExpander"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        }
        [data-testid="stMetric"]:hover::before, [data-testid="stVerticalBlockBorderWrapper"]:hover::before, [data-testid="stExpander"]:hover::before {
            opacity: 0.8;
        }
        @keyframes gradientBorder {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Landing Page Feature Cards */
        .feature-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            height: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .feature-icon {
            font-size: 2.5rem;
            color: #6366f1;
            margin-bottom: 1rem;
            display: block;
        }
        .feature-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
        }
        .feature-text {
            font-size: 0.9rem;
            color: #475569;
            line-height: 1.5;
        }

        /* Quick-Start Preview Custom Alert */
        .preview-alert {
            background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
            border-left: 5px solid #6366f1;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: transform 0.2s ease;
        }
        .preview-alert:hover { transform: scale(1.01); }
        .preview-icon {
            font-size: 1.5rem; background: #ffffff; width: 50px; height: 50px;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex-shrink: 0;
        }
        .preview-content h4 { margin: 0 0 0.25rem 0 !important; color: #3730a3 !important; font-size: 1.05rem !important; font-weight: 800 !important; }
        .preview-content p { margin: 0 !important; color: #4338ca !important; font-size: 0.9rem !important; line-height: 1.5 !important; }
        .highlight-badge {
            background: #ef4444; color: white; padding: 0.15rem 0.5rem; border-radius: 6px; font-weight: 800; font-size: 0.9rem; display: inline-block; transform: rotate(-2deg);
        }
        
        /* Primary Button Pulse Animation */
        [data-testid="baseButton-primary"] {
            animation: pulse-primary 2s infinite !important;
            transition: transform 0.2s ease !important;
        }
        [data-testid="baseButton-primary"]:hover {
            transform: scale(1.05) !important;
        }
        @keyframes pulse-primary {
            0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.6); }
            70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
            100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
        }
        
        /* Professional Single-Bar Navigation Menu */
        div.element-container:has(.top-nav-anchor) + div.element-container {
            position: sticky;
            top: 2.875rem;
            z-index: 999;
        }
        
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            background-color: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.4rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            gap: 0.4rem;
        }
        
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: transparent;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none;
            flex: 1;
            margin: 0;
        }
        
        /* Hide default Streamlit radio circle */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
            display: none;
        }
        
        /* Nav Item Text */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label p {
            margin: 0;
            font-size: 0.95rem;
            font-weight: 600;
            color: #64748b;
            z-index: 2;
            transition: color 0.3s ease;
            white-space: nowrap;
        }
        
        /* Hover Effect */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            background-color: #f8fafc;
        }
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:hover p {
            color: #1e293b;
        }
        
        /* Active (Selected) Effect */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.25);
        }
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
            color: #ffffff !important; font-weight: 700; letter-spacing: 0.5px;
        }
    </style>
    """, unsafe_allow_html=True)

BASE_USD_RANGES = {
    "tuition": {"min": 10_000, "max": 100_000, "default": 40_000, "step": 1_000},
    "living": {"min": 5_000, "max": 50_000, "default": 20_000, "step": 500},
    "salary": {"min": 0, "max": 200_000, "default": 50_000, "step": 5_000},
}

STEM_DEGREES = [
    "Aerospace Engineering", "Architecture", "Artificial Intelligence", "Bioinformatics", 
    "Biomedical Engineering", "Business Analytics", "Chemical Engineering", "Civil Engineering", 
    "Computer Engineering", "Computer Science", "Cybersecurity", "Data Science", 
    "Electrical Engineering", "Environmental Science", "Industrial Engineering", 
    "Information Systems", "Information Technology", "Machine Learning", "Mathematics", 
    "Mechanical Engineering", "Mechatronics", "Physics", "Robotics", "Software Engineering", 
    "Statistics", "Urban Planning"
]

STEM_JOBS = [
    "Aerospace Engineer", "AI Engineer", "Architect", "Bioinformatician", 
    "Biomedical Engineer", "Business Analyst", "Chemical Engineer", "Civil Engineer", 
    "Cloud Architect", "Data Analyst", "Data Engineer", "Data Scientist", 
    "DevOps Engineer", "Electrical Engineer", "Environmental Engineer", 
    "Flight Dynamics Engineer", "Full Stack Developer", "Industrial Engineer", 
    "IT Consultant", "Machine Learning Engineer", "Mechanical Engineer", 
    "Mechatronics Engineer", "Product Manager", "Quantitative Analyst", 
    "Robotics Engineer", "Software Engineer", "Systems Analyst", "Urban Planner"
]

DEGREE_JOB_MAPPING = {
    "Aerospace Engineering": ["Aerospace Engineer", "Flight Dynamics Engineer"],
    "Architecture": ["Architect", "Urban Planner"],
    "Artificial Intelligence": ["AI Engineer", "Machine Learning Engineer", "Data Scientist", "Software Engineer"],
    "Bioinformatics": ["Bioinformatician", "Data Scientist"],
    "Biomedical Engineering": ["Biomedical Engineer"],
    "Business Analytics": ["Business Analyst", "Data Analyst", "Data Scientist", "Product Manager", "Systems Analyst", "Quantitative Analyst"],
    "Chemical Engineering": ["Chemical Engineer"],
    "Civil Engineering": ["Civil Engineer", "Urban Planner"],
    "Computer Engineering": ["Software Engineer", "Cloud Architect", "DevOps Engineer", "Electrical Engineer"],
    "Computer Science": ["Software Engineer", "Full Stack Developer", "Cloud Architect", "DevOps Engineer", "AI Engineer", "Data Scientist"],
    "Cybersecurity": ["Software Engineer", "Cloud Architect"],
    "Data Science": ["Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning Engineer", "AI Engineer"],
    "Electrical Engineering": ["Electrical Engineer", "Robotics Engineer", "Mechatronics Engineer"],
    "Environmental Science": ["Environmental Engineer", "Civil Engineer"],
    "Industrial Engineering": ["Industrial Engineer", "Product Manager", "Systems Analyst"],
    "Information Systems": ["Systems Analyst", "IT Consultant", "Business Analyst", "Cloud Architect"],
    "Information Technology": ["IT Consultant", "Systems Analyst", "DevOps Engineer", "Cloud Architect"],
    "Machine Learning": ["Machine Learning Engineer", "AI Engineer", "Data Scientist", "Software Engineer"],
    "Mathematics": ["Quantitative Analyst", "Data Scientist", "Data Analyst", "Machine Learning Engineer"],
    "Mechanical Engineering": ["Mechanical Engineer", "Aerospace Engineer", "Robotics Engineer", "Mechatronics Engineer"],
    "Mechatronics": ["Mechatronics Engineer", "Robotics Engineer", "Electrical Engineer", "Mechanical Engineer"],
    "Physics": ["Quantitative Analyst", "Data Scientist", "Aerospace Engineer"],
    "Robotics": ["Robotics Engineer", "Mechatronics Engineer", "AI Engineer"],
    "Software Engineering": ["Software Engineer", "Full Stack Developer", "Cloud Architect", "DevOps Engineer"],
    "Statistics": ["Data Analyst", "Data Scientist", "Quantitative Analyst", "Machine Learning Engineer"],
    "Urban Planning": ["Urban Planner", "Architect", "Civil Engineer"]
}

def calculate_opportunity_cost(current_salary: float, growth_rate_pct: float, duration: float) -> float:
    """Calculates foregone income over the study period, factoring in expected annual raises."""
    if current_salary <= 0 or duration <= 0:
        return 0.0
        
    salary_growth_rate = growth_rate_pct / 100.0
    total_lost_income = 0.0
    
    full_years = int(duration)
    for year in range(full_years):
        total_lost_income += current_salary * ((1 + salary_growth_rate) ** year)
        
    fraction = duration - full_years
    if fraction > 0:
        total_lost_income += (current_salary * ((1 + salary_growth_rate) ** full_years)) * fraction
        
    return total_lost_income

def calculate_capitalized_principal(total_loan: float, annual_rate: float, program_duration: float, grace_months: int) -> tuple[float, float]:
    """Simulates monthly interest compounding during the study and grace periods."""
    if total_loan <= 0:
        return 0.0, 0.0
        
    monthly_rate = annual_rate / 100.0 / 12.0
    study_months = int(program_duration * 12)
    total_moratorium_months = study_months + grace_months
    
    num_disbursements = math.ceil(program_duration)
    disbursement_amount = total_loan / num_disbursements
    
    principal_balance = 0.0
    accrued_simple_interest = 0.0
    
    for month in range(1, total_moratorium_months + 1):
        if month <= study_months and (month - 1) % 12 == 0:
            principal_balance += disbursement_amount
            
        accrued_simple_interest += principal_balance * monthly_rate
        
    total_capitalized_balance = principal_balance + accrued_simple_interest
    return total_capitalized_balance, accrued_simple_interest

def calculate_amortization(principal: float, annual_rate: float, months: int = 120, shock_month: int = 36, shock_rate_increase: float = 2.0):
    """Calculates 10-year standard amortization schedules with a built-in variable rate shock."""
    if principal <= 0:
        return 0.0, 0.0, 0.0, [0.0] * (months + 1), [0.0] * (months + 1)

    monthly_rate = annual_rate / 100.0 / 12.0

    if monthly_rate > 0:
        baseline_payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        balance_at_shock = principal * ((1 + monthly_rate)**months - (1 + monthly_rate)**shock_month) / ((1 + monthly_rate)**months - 1)
    else: 
        baseline_payment = principal / months
        balance_at_shock = principal - (baseline_payment * shock_month)
    
    total_baseline_interest = (baseline_payment * months) - principal

    shocked_annual_rate = annual_rate + shock_rate_increase
    shocked_monthly_rate = shocked_annual_rate / 100.0 / 12.0
    remaining_months = months - shock_month

    if shocked_monthly_rate > 0:
        shocked_payment = balance_at_shock * (shocked_monthly_rate * (1 + shocked_monthly_rate)**remaining_months) / ((1 + shocked_monthly_rate)**remaining_months - 1)
    else: 
        shocked_payment = balance_at_shock / remaining_months

    total_shock_interest = (baseline_payment * shock_month) + (shocked_payment * remaining_months) - principal
    extra_interest = total_shock_interest - total_baseline_interest

    baseline_history = []
    balance = principal
    for _ in range(months + 1):
        baseline_history.append(balance)
        if balance > 0:
            interest = balance * monthly_rate
            balance -= (baseline_payment - interest)
            balance = max(0, balance)

    shock_history = []
    balance = principal
    for m in range(months + 1):
        shock_history.append(balance)
        if balance > 0:
            if m < shock_month:
                interest = balance * monthly_rate
                balance -= (baseline_payment - interest)
            else:
                interest = balance * shocked_monthly_rate
                balance -= (shocked_payment - interest)
            balance = max(0, balance)

    return baseline_payment, total_baseline_interest, extra_interest, baseline_history, shock_history

def calculate_irr(cash_flows: list[float], iterations: int = 100) -> float:
    """Calculates Internal Rate of Return (IRR) using the bisection method to find where NPV = 0."""
    low, high = -0.99, 1.0
    for _ in range(iterations):
        mid = (low + high) / 2
        npv = sum(cf / ((1 + mid) ** t) for t, cf in enumerate(cash_flows))
        if npv > 0:
            low = mid
        else:
            high = mid
    return mid * 100

def calculate_roi_metrics(starting_salary: float, growth_rate: float, discount_rate: float, year_0_cost: float, years: int = 10) -> tuple[float, int, list[float]]:
    """Projects 10-year cash flows, Net Present Value (NPV), and Break-Even point."""
    cash_flows = [-year_0_cost]
    current_salary = starting_salary
    cumulative_earnings = 0.0
    break_even_year = None
    
    for year in range(1, years + 1):
        cash_flows.append(current_salary)
        cumulative_earnings += current_salary
        if break_even_year is None and cumulative_earnings >= year_0_cost:
            break_even_year = year
        current_salary *= (1 + (growth_rate / 100.0))
        
    npv = sum(cf / ((1 + (discount_rate / 100.0)) ** t) for t, cf in enumerate(cash_flows))
    return npv, break_even_year, cash_flows

def run_monte_carlo_roi(starting_salary: float, growth_rate: float, discount_rate: float, year_0_cost: float, iterations: int = 1000) -> dict:
    """Runs a Monte Carlo simulation using normal distributions to measure ROI risk."""
    npvs = []
    for _ in range(iterations):
        # Introduce real-world volatility: Salary varies by ~10%, Growth varies by ~1.5%
        sim_salary = np.random.normal(starting_salary, starting_salary * 0.10)
        sim_growth = np.random.normal(growth_rate, 1.5)
        
        npv, _, _ = calculate_roi_metrics(sim_salary, sim_growth, discount_rate, year_0_cost)
        npvs.append(npv)
        
    npvs = np.array(npvs)
    return {
        "npvs": npvs,
        "prob_positive": (npvs > 0).mean() * 100,
        "mean_npv": npvs.mean(),
        "worst_case_5th": np.percentile(npvs, 5),
        "best_case_95th": np.percentile(npvs, 95)
    }

def round_to_nearest(value: float, nearest: int) -> int:
    if nearest <= 0: return int(round(value))
    return int(round(value / nearest) * nearest)

def build_currency_config(symbol: str, exchange_rate: float, rounding: dict[str, int]) -> dict[str, dict[str, int] | str | float]:
    config = {"symbol": symbol, "exchange_rate": exchange_rate, "tuition": {}, "living": {}, "salary": {}}
    for key, base_values in BASE_USD_RANGES.items():
        nearest = rounding[key]
        config[key] = {
            "min": round_to_nearest(base_values["min"] * exchange_rate, nearest),
            "max": round_to_nearest(base_values["max"] * exchange_rate, nearest),
            "default": round_to_nearest(base_values["default"] * exchange_rate, nearest),
            "step": max(nearest, round_to_nearest(base_values["step"] * exchange_rate, nearest)),
        }
    return config

@st.cache_data(ttl=86_400)
def fetch_live_exchange_rates() -> dict:
    fallbacks = {
        "_last_updated": "Offline (Using Fallbacks)",
        "USD": 1.0, "INR": 83.5, "NZD": 1.65, "EUR": 0.92, "GBP": 0.79,
        "PKR": 278.0, "JPY": 150.0, "CNY": 7.2, "KRW": 1350.0,
        "SAR": 3.75, "MYR": 4.7, "VND": 25000.0, "IRR": 42000.0
    }
    try:
        response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD", timeout=5)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        return {
            "_last_updated": data.get("date", "Recently"),
            "USD": 1.0, 
            "INR": rates.get("INR", fallbacks["INR"]), 
            "NZD": rates.get("NZD", fallbacks["NZD"]), 
            "EUR": rates.get("EUR", fallbacks["EUR"]), 
            "GBP": rates.get("GBP", fallbacks["GBP"]),
            "PKR": rates.get("PKR", fallbacks["PKR"]),
            "JPY": rates.get("JPY", fallbacks["JPY"]),
            "CNY": rates.get("CNY", fallbacks["CNY"]),
            "KRW": rates.get("KRW", fallbacks["KRW"]),
            "SAR": rates.get("SAR", fallbacks["SAR"]),
            "MYR": rates.get("MYR", fallbacks["MYR"]),
            "VND": rates.get("VND", fallbacks["VND"]),
            "IRR": rates.get("IRR", fallbacks["IRR"])
        }
    except Exception:
        return fallbacks

LIVE_RATES = fetch_live_exchange_rates()
CURRENCY_CONFIGS = {
    "USD ($)": build_currency_config("$", LIVE_RATES["USD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), 
    "INR (₹)": build_currency_config("₹", LIVE_RATES["INR"], {"tuition": 50_000, "living": 25_000, "salary": 100_000}), 
    "NZD (NZ$)": build_currency_config("NZ$", LIVE_RATES["NZD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), 
    "EUR (€)": build_currency_config("€", LIVE_RATES["EUR"], {"tuition": 1_000, "living": 500, "salary": 2_000}), 
    "GBP (£)": build_currency_config("£", LIVE_RATES["GBP"], {"tuition": 1_000, "living": 500, "salary": 2_000}),
    "PKR (₨)": build_currency_config("₨", LIVE_RATES["PKR"], {"tuition": 100_000, "living": 50_000, "salary": 200_000}),
    "JPY (¥)": build_currency_config("¥", LIVE_RATES["JPY"], {"tuition": 100_000, "living": 50_000, "salary": 100_000}),
    "CNY (¥)": build_currency_config("¥", LIVE_RATES["CNY"], {"tuition": 10_000, "living": 5_000, "salary": 10_000}),
    "KRW (₩)": build_currency_config("₩", LIVE_RATES["KRW"], {"tuition": 1_000_000, "living": 500_000, "salary": 2_000_000}),
    "SAR (﷼)": build_currency_config("﷼", LIVE_RATES["SAR"], {"tuition": 5_000, "living": 2_500, "salary": 10_000}),
    "MYR (RM)": build_currency_config("RM", LIVE_RATES["MYR"], {"tuition": 5_000, "living": 2_500, "salary": 10_000}),
    "VND (₫)": build_currency_config("₫", LIVE_RATES["VND"], {"tuition": 10_000_000, "living": 5_000_000, "salary": 20_000_000}),
    "IRR (﷼)": build_currency_config("﷼", LIVE_RATES["IRR"], {"tuition": 10_000_000, "living": 5_000_000, "salary": 20_000_000})
}
def local_to_usd(amount: float, exchange_rate: float) -> float: 
    if exchange_rate <= 0: return amount # Prevent ZeroDivisionError fallback
    return amount / exchange_rate
def format_currency_markdown(symbol: str, amount: float) -> str: return f"{symbol.replace('$', r'\$')}{amount:,.0f}"