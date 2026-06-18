import streamlit as st
from utils import local_to_usd, format_currency_markdown, calculate_opportunity_cost

def render(currency_choice, currency_config, currency_symbol, exchange_rate):
    st.header("Your True Cost of Studying")
    st.markdown(f"Calculate the real cost of your Master's degree, including what you pay out-of-pocket and the salary you give up by choosing to study instead of work in **{currency_choice}**.")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(f"#### Direct Out-of-Pocket Costs ({currency_symbol})")
            
            c1_a, c1_b = st.columns(2)
            with c1_a:
                annual_tuition = st.number_input("Annual Tuition", min_value=0.0, value=float(currency_config["tuition"]["default"]), step=float(currency_config["tuition"]["step"]), help=f"The amount you expect to pay per year for tuition in {currency_choice}.")
                scholarship = st.number_input("Scholarships / Grants", min_value=0.0, value=0.0, step=float(currency_config["tuition"]["step"]), help=f"Enter any scholarships, grants, or institutional aid received per year in {currency_choice}.")
            with c1_b:
                annual_living_expenses = st.number_input("Living Expenses", min_value=0.0, value=float(currency_config["living"]["default"]), step=float(currency_config["living"]["step"]), help=f"Rent, food, health insurance, and other necessary living expenses per year in {currency_choice}.")
                program_duration = st.number_input("Duration (Years)", min_value=1.0, max_value=5.0, value=2.0, step=0.5, help="Select the total length of your Master's program.")

            if currency_choice == "INR (₹)":
                st.info("**Indian Student Alert:** When transferring money abroad, remember the government applies a 5% TCS (Tax Collected at Source) on education remittances above ₹7 Lakhs. Also, expect the Rupee to depreciate ~3-5% yearly against foreign currencies, making your second year slightly more expensive!")

    with col2:
        with st.container(border=True):
            st.markdown(f"#### Lost Income / Opportunity Cost ({currency_symbol})")
            st.markdown("*(If you don't currently have a job, leave these at zero!)*")
            
            c2_a, c2_b = st.columns(2)
            with c2_a:
                    current_salary = st.number_input("Current Salary", min_value=0.0, value=float(currency_config["salary"]["default"]), step=float(currency_config["salary"]["step"]), help=f"Your current or expected annual salary in {currency_choice}. This is the income you give up while studying.")
            with c2_b:
                    salary_growth = st.number_input("Expected Raise (%)", min_value=0.0, value=3.0, step=0.5, help="The estimated annual raise percentage you would receive if you stayed at your current job.")

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

    st.divider()
    st.markdown(f"### Cost Projection Summary ({currency_choice})")
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(label=f"Total Direct Cost ({currency_symbol})", value=f"{currency_symbol}{total_direct_cost_local:,.2f}", help=f"Total tuition (minus scholarships) plus living expenses over the entire duration of the program in {currency_choice}.")
        if currency_choice != "USD ($)": st.caption(f"Baseline USD equivalent: **${total_direct_cost_usd:,.2f}**")

    with metric_col2:
        st.metric(label=f"Total Lost Income ({currency_symbol})", value=f"{currency_symbol}{total_opportunity_cost_local:,.2f}", help=f"The salary you miss out on earning over the duration of the degree in {currency_choice}.")
        if currency_choice != "USD ($)": st.caption(f"Baseline USD equivalent: **${total_opportunity_cost_usd:,.2f}**")

    with metric_col3:
        st.metric(label=f"True Economic Cost ({currency_symbol})", value=f"{currency_symbol}{true_economic_cost_local:,.2f}", help=f"The absolute real cost of your degree = Direct Costs + Lost Income in {currency_choice}.", delta=f"-{currency_symbol}{total_opportunity_cost_local:,.2f} (Lost Income)", delta_color="inverse")
        if currency_choice != "USD ($)": st.caption(f"Baseline USD equivalent: **${true_economic_cost_usd:,.2f}**")

    with st.expander("**How did we calculate this? (See the Math)**"):
        st.markdown(f"""
        * **Direct Cost:** (Annual Tuition - Scholarships + Living Expenses) × {program_duration} Years
        * **Lost Income:** Your current salary compounded by your {salary_growth}% expected raise for each year you are studying.
        * **True Economic Cost:** Direct Cost + Lost Income
        """)

    st.divider()
    if current_salary > 0:
        st.markdown("### Strategic Takeaway")
        col_ins1, col_ins2, col_ins3 = st.columns(3)
        with col_ins1: st.error(f"**Out-of-Pocket Cost:** You will actually need to pay **{format_currency_markdown(currency_symbol, total_direct_cost_local)}** for your tuition and living expenses.")
        with col_ins2: st.info(f"**The Hidden Cost:** By leaving the workforce, you are sacrificing **{format_currency_markdown(currency_symbol, total_opportunity_cost_local)}** in standard earnings.")
        with col_ins3: st.warning(f"**Your Break-Even Goal:** For this degree to be worth it financially, your new job must help you recover a total value of **{format_currency_markdown(currency_symbol, true_economic_cost_local)}** over what your old job would have paid.")
    else:
        st.success(f"**Student Advantage:** Since you are entering this degree without leaving an existing salary, your financial target to achieve a positive return is strictly limited to clearing your out-of-pocket direct expenses: **{format_currency_markdown(currency_symbol, total_direct_cost_local)}**.")

    return total_direct_cost_local, true_economic_cost_local, program_duration