import streamlit as st
from utils import local_to_usd, format_currency_markdown, calculate_opportunity_cost

def render(currency_choice, currency_config, currency_symbol, exchange_rate):
    st.info("💡 **Why does this matter?** Before you take a loan, you need to know exactly how much money you need. But there's a catch: the 'real' cost of a degree isn't just tuition—it's also the salary you give up by going to school instead of working. Let's calculate both.")
    
    # Initialize widget session state from persistent USD variables if not present
    if "w_tuition" not in st.session_state:
        st.session_state.w_tuition = float(st.session_state.tuition_usd * exchange_rate)
    if "w_schol" not in st.session_state:
        st.session_state.w_schol = float(st.session_state.schol_usd * exchange_rate)
    if "w_living" not in st.session_state:
        st.session_state.w_living = float(st.session_state.living_usd * exchange_rate)
    if "w_current_salary" not in st.session_state:
        st.session_state.w_current_salary = float(st.session_state.current_salary_usd * exchange_rate)
    if "w_salary_growth" not in st.session_state:
        st.session_state.w_salary_growth = float(st.session_state.salary_growth)
    if "w_employment_status" not in st.session_state:
        st.session_state.w_employment_status = st.session_state.employment_status
    if "widget_program_duration" not in st.session_state:
        st.session_state.widget_program_duration = float(st.session_state.program_duration)

    left_col, right_col = st.columns([1.1, 1], gap="large")

    def render_direct_costs():
        st.markdown(f"#### 1. What You Will Actually Pay ({currency_symbol})")
        st.markdown("*(The out-of-pocket expenses)*")
        
        c1_a, c1_b = st.columns(2)
        with c1_a:
            tuition = st.number_input("Annual Tuition", min_value=0.0, step=float(currency_config["tuition"]["step"]), key="w_tuition", help=f"The amount you expect to pay per year for tuition in {currency_choice}.")
            schol = st.number_input("Scholarships / Grants", min_value=0.0, step=float(currency_config["tuition"]["step"]), key="w_schol", help=f"Enter any scholarships, grants, or institutional aid received per year in {currency_choice}.")
        with c1_b:
            living = st.number_input("Living Expenses", min_value=0.0, step=float(currency_config["living"]["step"]), key="w_living", help=f"Rent, food, health insurance, and other necessary living expenses per year in {currency_choice}.")
            duration = st.number_input("Duration (Years)", min_value=1.0, max_value=4.0, step=0.5, key="widget_program_duration", help="Select the total length of your program (e.g., 4 years for Bachelor's, 2 years for Master's).")
        if currency_choice == "INR (₹)":
            st.info("**Indian Student Alert:** When transferring money abroad, remember the government applies a 5% TCS (Tax Collected at Source) on education remittances above ₹7 Lakhs. Also, expect the Rupee to depreciate ~3-5% yearly against foreign currencies, making your second year slightly more expensive!")
        return tuition, schol, living, duration

    with left_col:
        st.header("The Real Price Tag")
        st.markdown(f"Let's calculate the absolute real cost of your degree in **{currency_choice}**.")

        emp_options = ["I am a Student / Not Employed", "I am a Working Professional"]
        try:
            emp_index = emp_options.index(st.session_state.w_employment_status)
        except ValueError:
            emp_index = 0

        employment_status = st.radio("Current Employment Status:", options=emp_options, index=emp_index, horizontal=True, key="w_employment_status")
        st.divider()
        
        if employment_status == "I am a Working Professional":
            with st.container(border=True):
                annual_tuition, scholarship, annual_living_expenses, program_duration = render_direct_costs()
            with st.container(border=True):
                st.markdown(f"#### 2. The Income You're Giving Up ({currency_symbol})")
                st.markdown("*(If you study, you can't work full-time. This missed salary is a hidden cost of your degree.)*")
                c2_a, c2_b = st.columns(2)
                with c2_a: current_salary = st.number_input("Current Salary", min_value=0.0, step=float(currency_config["salary"]["step"]), key="w_current_salary", help=f"Your current or expected annual salary in {currency_choice}. This is the income you give up while studying.")
                with c2_b: salary_growth = st.number_input("Expected Raise (%)", min_value=0.0, step=0.5, key="w_salary_growth", help="The estimated annual raise percentage you would receive if you stayed at your current job.")
        else:
            st.success("🎉 **Student Advantage:** Since you are currently a student, you aren't leaving a full-time job. This means your 'hidden cost of lost salary' is zero!")
            with st.container(border=True):
                annual_tuition, scholarship, annual_living_expenses, program_duration = render_direct_costs()
            current_salary = 0.0
            salary_growth = 3.0

    # Save inputs back to persistent session state (converted to USD)
    st.session_state.tuition_usd = float(annual_tuition / exchange_rate) if exchange_rate > 0 else 0.0
    st.session_state.schol_usd = float(scholarship / exchange_rate) if exchange_rate > 0 else 0.0
    st.session_state.living_usd = float(annual_living_expenses / exchange_rate) if exchange_rate > 0 else 0.0
    st.session_state.program_duration = float(program_duration)
    st.session_state.employment_status = employment_status
    st.session_state.current_salary_usd = float(current_salary / exchange_rate) if exchange_rate > 0 else 0.0
    st.session_state.salary_growth = float(salary_growth)

    annual_tuition_usd = local_to_usd(annual_tuition, exchange_rate)
    annual_living_expenses_usd = local_to_usd(annual_living_expenses, exchange_rate)
    current_salary_usd = local_to_usd(current_salary, exchange_rate)
    scholarship_usd = local_to_usd(scholarship, exchange_rate)

    net_annual_direct_usd = max(0.0, (annual_tuition_usd - scholarship_usd) + annual_living_expenses_usd)
    total_direct_cost_usd = net_annual_direct_usd * program_duration

    total_opportunity_cost_usd = calculate_opportunity_cost(current_salary_usd, salary_growth, program_duration)

    true_economic_cost_usd = total_direct_cost_usd + total_opportunity_cost_usd

    total_direct_cost_local = total_direct_cost_usd * exchange_rate
    total_opportunity_cost_local = total_opportunity_cost_usd * exchange_rate
    true_economic_cost_local = true_economic_cost_usd * exchange_rate

    with right_col:
        st.markdown(f"### The Final Math ({currency_choice})")
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(label=f"Total Direct Cost ({currency_symbol})", value=f"{currency_symbol}{total_direct_cost_local:,.0f}", help=f"Total tuition (minus scholarships) plus living expenses over the entire duration of the program in {currency_choice}.")
            if currency_choice != "USD ($)": st.caption(f"Baseline USD: **${total_direct_cost_usd:,.0f}**")

        with metric_col2:
            st.metric(label=f"Total Lost Income ({currency_symbol})", value=f"{currency_symbol}{total_opportunity_cost_local:,.0f}", help=f"The salary you miss out on earning over the duration of the degree in {currency_choice}.")
            if currency_choice != "USD ($)": st.caption(f"Baseline USD: **${total_opportunity_cost_usd:,.0f}**")

        st.metric(label=f"True Economic Cost ({currency_symbol})", value=f"{currency_symbol}{true_economic_cost_local:,.0f}", help=f"The absolute real cost of your degree = Direct Costs + Lost Income in {currency_choice}.", delta=f"-{currency_symbol}{total_opportunity_cost_local:,.0f} (Lost Income)", delta_color="inverse")
        if currency_choice != "USD ($)": st.caption(f"Baseline USD: **${true_economic_cost_usd:,.0f}**")

        with st.expander("**How did we calculate this? (See the Math)**"):
            st.markdown(f"""
            * **Direct Cost:** (Annual Tuition - Scholarships + Living Expenses) × {program_duration} Years
            * **Lost Income:** Your current salary compounded by your {salary_growth}% expected raise for each year you are studying.
            * **True Economic Cost:** Direct Cost + Lost Income
            """)

        st.divider()
        if current_salary > 0:
            st.markdown("### The Verdict")
            st.error(f"**What you pay the university:** You need exactly **{format_currency_markdown(currency_symbol, total_direct_cost_local)}** in cash or loans to pay for this degree.")
            st.warning(f"**What your degree needs to earn:** Because you are giving up your current salary, this degree is only 'worth it' if your new job pays you back at least **{format_currency_markdown(currency_symbol, true_economic_cost_local)}** over time.")
        else:
            st.markdown("### The Verdict")
            st.success(f"**What you pay the university:** You need exactly **{format_currency_markdown(currency_symbol, total_direct_cost_local)}** in cash or loans to pay for this degree.")
            st.info(f"**What your degree needs to earn:** Your new job only needs to pay back the **{format_currency_markdown(currency_symbol, total_direct_cost_local)}** you spent, since you didn't give up a salary to study.")

    return total_direct_cost_local, true_economic_cost_local, program_duration