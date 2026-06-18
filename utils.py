import streamlit as st
import requests
import math
import numpy as np

def inject_premium_styles():
    st.markdown("""
    <style>
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
        
        /* Clean Light Cards & Micro-Animations */
        [data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {
            padding: 1.25rem;
            background-color: #ffffff !important;
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
            max-width: 100%;
            box-sizing: border-box;
        }
        
        /* Soft Hover Elevation */
        [data-testid="stMetric"]:hover, [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            border-color: #6366f1 !important;
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
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 3rem 2rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            color: #ffffff !important;
        }
        .hero-subtitle {
            font-size: 1.25rem;
            font-weight: 400;
            color: #cbd5e1;
        }
        /* Input Box Enhancements */
        div[data-baseweb="input"] > div, 
        div[data-baseweb="select"] > div {
            border-radius: 0.5rem !important;
            border: 1px solid #cbd5e1 !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="input"] > div:focus-within, 
        div[data-baseweb="select"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        }
        /* Smooth Cascade Fade-in Animation for UI Elements */
        @keyframes cascadeSlideUp {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        [data-testid="stVerticalBlock"] > div {
            animation: cascadeSlideUp 0.4s ease-out both;
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
def fetch_live_exchange_rates() -> dict[str, float]:
    fallbacks = {"USD": 1.0, "INR": 83.5, "NZD": 1.65, "EUR": 0.92, "GBP": 0.79}
    try:
        response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD", timeout=5)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        return {"USD": 1.0, "INR": rates.get("INR", fallbacks["INR"]), "NZD": rates.get("NZD", fallbacks["NZD"]), "EUR": rates.get("EUR", fallbacks["EUR"]), "GBP": rates.get("GBP", fallbacks["GBP"])}
    except Exception:
        return fallbacks

LIVE_RATES = fetch_live_exchange_rates()
CURRENCY_CONFIGS = {"USD ($)": build_currency_config("$", LIVE_RATES["USD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), "INR (₹)": build_currency_config("₹", LIVE_RATES["INR"], {"tuition": 50_000, "living": 25_000, "salary": 100_000}), "NZD (NZ$)": build_currency_config("NZ$", LIVE_RATES["NZD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), "EUR (€)": build_currency_config("€", LIVE_RATES["EUR"], {"tuition": 1_000, "living": 500, "salary": 2_000}), "GBP (£)": build_currency_config("£", LIVE_RATES["GBP"], {"tuition": 1_000, "living": 500, "salary": 2_000})}
def local_to_usd(amount: float, exchange_rate: float) -> float: 
    if exchange_rate <= 0: return amount # Prevent ZeroDivisionError fallback
    return amount / exchange_rate
def format_currency_markdown(symbol: str, amount: float) -> str: return f"{symbol.replace('$', r'\$')}{amount:,.2f}"