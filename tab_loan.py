import streamlit as st
import pandas as pd
from utils import local_to_usd, format_currency_markdown, calculate_capitalized_principal, calculate_amortization

def render(total_direct_cost_local, program_duration, currency_choice, currency_config, currency_symbol, exchange_rate):
    with st.container(border=True):
        st.markdown("#### Financing & Loan Settings")
        
        max_loan_amount = float(total_direct_cost_local) if total_direct_cost_local > 0 else 10_000.0
        
        top_c1, top_c2 = st.columns(2)
        with top_c1:
            loan_principal_local = st.slider(f"Loan Principal Borrowed ({currency_symbol}):", min_value=0.0, max_value=max_loan_amount, value=min(max_loan_amount, float(total_direct_cost_local * 0.7)), step=float(currency_config["tuition"]["step"]), help="The stated amount you borrow for your degree.")
        with top_c2:
            custom_monthly_payment = st.number_input(f"Custom Monthly Payment (Optional):", min_value=0.0, value=0.0, step=100.0, help="Want to pay less each month? Enter a lower custom payment to simulate Income-Driven Repayment. Leave at 0.0 for standard 10-year rules.")
        
        col_set1, col_set2, col_set3 = st.columns(3)
        with col_set1: loan_interest_rate = st.slider("Annual Interest Rate (%):", min_value=3.0, max_value=15.0, value=6.5, step=0.1, help="The expected annual interest rate on your student loans.")
        with col_set2: origination_fee = st.slider("Loan Origination Fee (%):", min_value=0.0, max_value=10.0, value=1.5, step=0.1, help="An upfront fee charged by the lender just to process the loan (e.g., US Federal Grad PLUS is ~4.2%). It forces you to borrow more to get the target amount.")
        with col_set3: grace_period_months = st.slider("Months to Find a Job (Post-Grad):", min_value=0, max_value=12, value=6, step=1, help="Time spent job hunting after graduation. Standard grace periods are 6 months, but interest still compounds while your income is $0!")
            
        loan_principal_usd = local_to_usd(loan_principal_local, exchange_rate)
        custom_monthly_payment_usd = local_to_usd(custom_monthly_payment, exchange_rate)
        if currency_choice == "INR (₹)":
            st.success("**Indian Tax Benefit:** If you take an education loan from an Indian bank, the interest you pay is fully tax-deductible under Section 80E of the Income Tax Act!")
        
        gross_loan_usd = loan_principal_usd / (1.0 - (origination_fee / 100.0)) if origination_fee < 100 else loan_principal_usd
        origination_fee_usd = gross_loan_usd - loan_principal_usd
        gross_loan_local = gross_loan_usd * exchange_rate
        origination_fee_local = origination_fee_usd * exchange_rate
        
        capitalized_principal_usd, moratorium_interest_usd = calculate_capitalized_principal(total_loan=gross_loan_usd, annual_rate=loan_interest_rate, program_duration=program_duration, grace_months=grace_period_months)
        capitalized_principal_local = capitalized_principal_usd * exchange_rate
        moratorium_interest_local = moratorium_interest_usd * exchange_rate
        
        balance_at_grad_usd, _ = calculate_capitalized_principal(total_loan=gross_loan_usd, annual_rate=loan_interest_rate, program_duration=program_duration, grace_months=0)
        job_hunt_penalty_usd = capitalized_principal_usd - balance_at_grad_usd
        job_hunt_penalty_local = job_hunt_penalty_usd * exchange_rate
        
        st.divider()
        st.markdown(f"### The Hidden Traps: Interest Before You Graduate")
        
        col_cap1, col_cap2, col_cap3 = st.columns(3)
        with col_cap1: st.metric(label=f"Target Funding Needed ({currency_symbol})", value=f"{currency_symbol}{loan_principal_local:,.2f}", help="The actual cash you need deposited into your bank account to pay tuition and living expenses.")
        with col_cap2: st.metric(label=f"Required Loan Amount ({currency_symbol})", value=f"{currency_symbol}{gross_loan_local:,.2f}", delta=f"+{currency_symbol}{origination_fee_local:,.2f} (Processing Fee)", delta_color="inverse", help="Lenders often charge a 'Processing' or 'Origination' fee. If the fee is 5% and you need $100k, you actually have to borrow $105k to get your money.")
        with col_cap3: st.metric(label=f"Actual Starting Debt ({currency_symbol})", value=f"{currency_symbol}{capitalized_principal_local:,.2f}", delta=f"+{currency_symbol}{moratorium_interest_local:,.2f} (Study Interest)", delta_color="inverse", help=f"Capitalized Principal: This is your TRUE starting loan balance. It includes the original loan PLUS all the interest that secretly accumulated during your {int(program_duration*12) + grace_period_months} months of studying and job hunting.")
            
        inflation_pct = ((capitalized_principal_usd - loan_principal_usd) / loan_principal_usd * 100) if loan_principal_usd > 0 else 0
        if inflation_pct > 10.0:
            st.warning(f"**Hidden Debt Growth Alert:** Due to upfront bank fees and interest charged while you study, your actual debt grew by **{inflation_pct:.1f}%** before you even made your first monthly payment!")
            
        if grace_period_months >= 6 and job_hunt_penalty_usd > 0:
            st.error(f"**Job Hunt Delay Alert:** Taking {grace_period_months} months to find a job adds **{currency_symbol}{job_hunt_penalty_local:,.2f}** in extra interest to your debt while you are unemployed!")
        
        baseline_payment_usd, amort_total_interest_usd, extra_interest_usd, baseline_history, shock_history = calculate_amortization(principal=capitalized_principal_usd, annual_rate=loan_interest_rate)
        total_lifetime_interest_usd = amort_total_interest_usd + moratorium_interest_usd + origination_fee_usd
        
        st.divider()
        st.markdown("#### Monthly Repayment Outcomes")
        
        monthly_interest_accrual_usd = capitalized_principal_usd * (loan_interest_rate / 100.0 / 12.0)
        monthly_interest_accrual_local = monthly_interest_accrual_usd * exchange_rate
        
        if custom_monthly_payment > 0 and custom_monthly_payment_usd < monthly_interest_accrual_usd:
            st.error(f"**Danger - Debt Will Grow Forever:** Your custom payment of **{currency_symbol}{custom_monthly_payment:,.2f}** is smaller than the **{currency_symbol}{monthly_interest_accrual_local:,.2f}** in interest charged each month. Your loan will never be paid off!")
        
        col_amt1, col_amt2, col_amt3 = st.columns(3)
        display_payment_usd = custom_monthly_payment_usd if custom_monthly_payment > 0 else baseline_payment_usd
        payment_label = "Custom Monthly Payment" if custom_monthly_payment > 0 else "Standard Monthly Payment"

        with col_amt1: st.metric(label=f"{payment_label} ({currency_symbol})", value=f"{currency_symbol}{display_payment_usd * exchange_rate:,.2f}", help="Your expected monthly cash outflow. Standard assumes a rigid 10-year term.")
        with col_amt2: st.metric(label=f"Total Interest Paid to Bank ({currency_symbol})", value=f"{currency_symbol}{total_lifetime_interest_usd * exchange_rate:,.2f}", help="The total amount of pure interest the bank makes off of you.")
        with col_amt3: st.metric(label=f"Rate Hike Risk ({currency_symbol})", value=f"{currency_symbol}{extra_interest_usd * exchange_rate:,.2f}", help="The extra interest you would pay if your variable interest rate jumps by 2% at Year 3.", delta="vs. Baseline", delta_color="inverse")

        if capitalized_principal_usd > 0:
            st.markdown("#### Loan Balance Over Time (Standard 10-Year Track)")
            chart_data = pd.DataFrame({"Month": range(len(baseline_history)), "Baseline Repayment": [b * exchange_rate for b in baseline_history], "Shock Scenario (+2% Rate Hike)": [s * exchange_rate for s in shock_history]}).set_index("Month")
            st.line_chart(chart_data)

        with st.expander("**How do these loan traps actually work?**"):
            st.markdown("""
            * **Processing / Origination Fee:** Banks often charge 1-5% upfront. If you need $100k and the fee is 5%, they loan you $105k but only hand you $100k. You pay interest on the $105k!
            * **Study Interest (Capitalization):** Even if you aren't required to make payments while in school, interest is still silently accumulating every single month. When you graduate, that massive pile of interest gets added to your principal.
            * **Rate Hike Risk:** Variable interest rates change with the economy. If rates jump just 2%, your lifetime interest paid will skyrocket.
            """)

        st.divider()
        st.markdown("### The Golden Rule of Student Debt")
        st.info(
            f"**Rule of Thumb:** Financial experts strongly advise that your total debt at graduation (**{format_currency_markdown(currency_symbol, capitalized_principal_local)}**) should never exceed your **expected first-year starting salary**.\n\n"
            "Keep this target anchor in mind as we head into **Phase 2: The Career Pathway Analyzer**, where we will test if your target job can actually support this debt burden!"
        )