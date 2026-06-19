import streamlit as st
import math
import plotly.graph_objects as go
from utils import local_to_usd, format_currency_markdown, calculate_capitalized_principal, calculate_amortization

def render(total_direct_cost_local, program_duration, currency_choice, currency_config, currency_symbol, exchange_rate):
    st.info(f"💡 **The Story So Far:** In Step 1, we calculated that you need **{format_currency_markdown(currency_symbol, total_direct_cost_local)}** to pay for this degree. Now, let's see what happens when you borrow that money from a bank.")
    
    # Initialize widget session state from persistent variables if not present
    if "w_loan_amount" not in st.session_state:
        default_loan = st.session_state.loan_amount_usd if st.session_state.loan_amount_usd > 0 else float(total_direct_cost_local * 0.7 / exchange_rate)
        st.session_state.w_loan_amount = float(default_loan * exchange_rate)
    if "w_custom_payment" not in st.session_state:
        st.session_state.w_custom_payment = float(st.session_state.custom_payment_usd * exchange_rate)
    if "w_interest_rate" not in st.session_state:
        st.session_state.w_interest_rate = float(st.session_state.loan_interest_rate)
    if "w_repayment_years" not in st.session_state:
        st.session_state.w_repayment_years = int(st.session_state.target_repayment_years)
    if "w_origination_fee" not in st.session_state:
        st.session_state.w_origination_fee = float(st.session_state.origination_fee)
    if "w_grace_months" not in st.session_state:
        st.session_state.w_grace_months = int(st.session_state.grace_period_months)
    if "w_extra_monthly_payment" not in st.session_state:
        st.session_state.w_extra_monthly_payment = float(st.session_state.extra_monthly_payment_usd * exchange_rate)
    if "w_lump_sum_payment" not in st.session_state:
        st.session_state.w_lump_sum_payment = float(st.session_state.lump_sum_payment_usd * exchange_rate)
    if "w_lump_sum_year" not in st.session_state:
        st.session_state.w_lump_sum_year = int(st.session_state.lump_sum_year)

    left_col, right_col = st.columns([1, 1.2], gap="large")
        
    max_loan_amount = max(250_000.0 * exchange_rate, float(total_direct_cost_local) * 1.5)
    loan_step = max(100.0, float(currency_config["living"]["step"]))
    if loan_step > max_loan_amount / 10.0:
        loan_step = max(1.0, float(max_loan_amount / 10.0))
    
    with left_col:
        with st.container(border=True):
            st.markdown("#### 1. What are you borrowing?")
            
            top_c1, top_c2 = st.columns(2)
            with top_c1: loan_principal_local = st.number_input(f"Loan Amount ({currency_symbol}):", min_value=0.0, max_value=max_loan_amount, step=loan_step, key="w_loan_amount", help="The amount you actually ask the bank for.")
            with top_c2: custom_monthly_payment = st.number_input(f"Custom Monthly Payment (Optional):", min_value=0.0, step=loan_step, key="w_custom_payment", help="Want to pay less each month? Enter a custom payment. Leave at 0 for standard timeline rules.")
            
            st.markdown("#### 2. What are the bank's terms?")
            col_set1, col_set2 = st.columns(2)
            with col_set1: loan_interest_rate = st.slider("Annual Interest Rate (%):", min_value=3.0, max_value=15.0, step=0.1, key="w_interest_rate", help="The expected annual interest rate on your student loans.")
            with col_set2: target_repayment_years = st.slider("Target Repayment Time (Years):", min_value=1, max_value=30, step=1, key="w_repayment_years", help="How many years do you plan to take to pay off this loan?")
            
            col_set3, col_set4 = st.columns(2)
            with col_set3: origination_fee = st.slider("Bank Processing Fee (%):", min_value=0.0, max_value=10.0, step=0.1, key="w_origination_fee", help="An upfront fee charged by the lender just to process the loan.")
            with col_set4: grace_period_months = st.slider("Months to Find a Job (Post-Grad):", min_value=0, max_value=12, step=1, key="w_grace_months", help="Time spent job hunting after graduation. Interest still grows!")
                
            st.markdown("#### 3. 💡 Prepayment & Refinancing")
            st.markdown("*(Accelerate your payoff to save interest)*")
            col_prep1, col_prep2 = st.columns(2)
            with col_prep1:
                extra_monthly_payment = st.number_input(f"Extra Monthly Payment ({currency_symbol}):", min_value=0.0, step=loan_step, key="w_extra_monthly_payment", help="Add this extra amount to your monthly payment starting from Month 1.")
            with col_prep2:
                lump_sum_payment = st.number_input(f"One-Time Lump Sum ({currency_symbol}):", min_value=0.0, step=loan_step, key="w_lump_sum_payment", help="Make a single large payment (e.g., sign-on bonus or tax refund).")
            
            lump_sum_year = st.slider("Lump Sum Timing (Year Post-Grad):", min_value=1, max_value=max(1, int(target_repayment_years)), step=1, key="w_lump_sum_year", help="Select which year after graduation to make the one-time payment.")

        # Save to persistent USD variables
        st.session_state.loan_amount_usd = float(loan_principal_local / exchange_rate) if exchange_rate > 0 else 0.0
        st.session_state.custom_payment_usd = float(custom_monthly_payment / exchange_rate) if exchange_rate > 0 else 0.0
        st.session_state.loan_interest_rate = float(loan_interest_rate)
        st.session_state.target_repayment_years = int(target_repayment_years)
        st.session_state.origination_fee = float(origination_fee)
        st.session_state.grace_period_months = int(grace_period_months)
        st.session_state.extra_monthly_payment_usd = float(extra_monthly_payment / exchange_rate) if exchange_rate > 0 else 0.0
        st.session_state.lump_sum_payment_usd = float(lump_sum_payment / exchange_rate) if exchange_rate > 0 else 0.0
        st.session_state.lump_sum_year = int(lump_sum_year)

        loan_principal_usd = st.session_state.loan_amount_usd
        custom_monthly_payment_usd = st.session_state.custom_payment_usd
        
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
        
    with left_col:
        st.markdown(f"### The Hidden Debt Trap")
        st.markdown("While you are studying, the bank is silently adding fees and interest to your loan. Here is your **TRUE** starting debt when you graduate.")
        
        col_cap1, col_cap2 = st.columns(2)
        with col_cap1: 
            st.metric(label=f"What You Asked For ({currency_symbol})", value=f"{currency_symbol}{loan_principal_local:,.0f}")
            st.metric(label=f"What Bank Loans You ({currency_symbol})", value=f"{currency_symbol}{gross_loan_local:,.0f}", delta=f"+{currency_symbol}{origination_fee_local:,.0f} (Processing Fee)", delta_color="inverse")
        with col_cap2: 
            st.metric(label=f"Your Debt at Graduation ({currency_symbol})", value=f"{currency_symbol}{capitalized_principal_local:,.0f}", delta=f"+{currency_symbol}{moratorium_interest_local:,.0f} (Study Interest)", delta_color="inverse", help=f"This includes the original loan PLUS all the interest that secretly accumulated during your {int(program_duration*12) + grace_period_months} months of studying and job hunting.")
            
        inflation_pct = ((capitalized_principal_usd - loan_principal_usd) / loan_principal_usd * 100) if loan_principal_usd > 0 else 0
        if inflation_pct > 10.0:
            st.warning(f"🚨 **Warning:** Before you even make your first payment, your debt has already grown by **{inflation_pct:.1f}%** because of fees and study-period interest!")
        if grace_period_months >= 6 and job_hunt_penalty_usd > 0:
            st.error(f"⏳ **Job Hunt Cost:** Taking {grace_period_months} months to find a job adds **{currency_symbol}{job_hunt_penalty_local:,.0f}** in extra interest to your debt!")
        
    # Standard baseline (No Prepayments)
    _, base_interest_usd, _, base_history, _ = calculate_amortization(
        principal=capitalized_principal_usd, annual_rate=loan_interest_rate,
        months=target_repayment_years*12, custom_payment=custom_monthly_payment_usd
    )

    # With Prepayments
    lump_sum_month = int((lump_sum_year - 1) * 12) + 12
    actual_payment_usd, total_repayment_interest_usd, extra_interest_usd, baseline_history, shock_history = calculate_amortization(
        principal=capitalized_principal_usd, annual_rate=loan_interest_rate,
        months=target_repayment_years*12, custom_payment=custom_monthly_payment_usd,
        extra_monthly_payment=st.session_state.extra_monthly_payment_usd,
        lump_sum_payment=st.session_state.lump_sum_payment_usd,
        lump_sum_month=lump_sum_month
    )

    # Savings
    interest_saved_usd = max(0.0, base_interest_usd - total_repayment_interest_usd) if not math.isinf(base_interest_usd) else 0.0
    interest_saved_local = interest_saved_usd * exchange_rate
    base_payoff_months = len(base_history) - 1
    prepaid_payoff_months = len(baseline_history) - 1
    months_saved = max(0, base_payoff_months - prepaid_payoff_months)

    total_lifetime_interest_usd = total_repayment_interest_usd + moratorium_interest_usd + origination_fee_usd
        
    with right_col:
        st.markdown("#### How You'll Pay It Back")
        
        monthly_interest_accrual_usd = capitalized_principal_usd * (loan_interest_rate / 100.0 / 12.0)
        monthly_interest_accrual_local = monthly_interest_accrual_usd * exchange_rate
        
        if custom_monthly_payment > 0 and custom_monthly_payment_usd <= monthly_interest_accrual_usd:
            st.error(f"🔥 **Danger!** Your custom payment of **{currency_symbol}{custom_monthly_payment:,.0f}** doesn't even cover the **{currency_symbol}{monthly_interest_accrual_local:,.0f}** in interest charged each month. Your debt will grow forever and never be paid off.")
        
        col_amt1, col_amt2 = st.columns(2)
        payment_label = "Custom Monthly Payment" if custom_monthly_payment > 0 else "Standard Monthly Payment"

        if math.isinf(total_lifetime_interest_usd):
            total_interest_str = "∞ (Infinite Debt)"
        else:
            total_interest_str = f"{currency_symbol}{total_lifetime_interest_usd * exchange_rate:,.0f}"

        with col_amt1: st.metric(label=f"{payment_label} ({currency_symbol})", value=f"{currency_symbol}{actual_payment_usd * exchange_rate:,.0f}", help=f"Your expected monthly cash outflow. Standard assumes your {target_repayment_years}-year target term.")
        with col_amt2: st.metric(label=f"Total Interest Paid to Bank", value=total_interest_str, help="The total amount of pure interest the bank makes off of you.")

        # Show Prepayment Savings Impact if active
        if extra_monthly_payment > 0 or lump_sum_payment > 0:
            st.markdown("##### ⚡ Prepayment Savings Impact")
            col_saved1, col_saved2 = st.columns(2)
            with col_saved1:
                if math.isinf(total_lifetime_interest_usd):
                    st.metric(label="Interest Saved", value="Avoids Infinity")
                else:
                    total_base = base_interest_usd + moratorium_interest_usd + origination_fee_usd
                    pct_saved = (interest_saved_usd / max(1.0, total_base)) * 100
                    st.metric(label="Interest Saved", value=f"{currency_symbol}{interest_saved_local:,.0f}", delta=f"Saved {pct_saved:.1f}%")
            with col_saved2:
                years_saved = months_saved / 12.0
                st.metric(label="Time Saved", value=f"{years_saved:.1f} Years" if years_saved >= 1.0 else f"{months_saved} Months", delta=f"-{months_saved} months")

        repayment_years_actual = len(baseline_history) // 12
        repayment_months_actual = len(baseline_history) % 12
        repayment_text = f"{repayment_years_actual} years" + (f" and {repayment_months_actual} months" if repayment_months_actual > 0 else "")
        total_time_text = f"{int(program_duration)} years studying + {grace_period_months} months job hunting + {repayment_text} of repayment"
        
        st.info(f"💡 **Why is the interest so high?** Student loans are brutal because interest silently accrues while you are studying. This specific calculation spans a total of **{total_time_text}**. By the time you graduate, all the hidden interest from those early years gets added to your principal, meaning you pay *interest on the interest* for the rest of the loan!")

        if capitalized_principal_usd > 0:
            st.markdown("##### Debt Payoff Timeline")
            months_to_plot = min(len(baseline_history), 361)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(months_to_plot)), 
                y=[b * exchange_rate for b in baseline_history[:months_to_plot]], 
                mode='lines', fill='tozeroy', fillcolor='rgba(26, 115, 232, 0.15)',
                name='Prepaid Payoff' if (extra_monthly_payment > 0 or lump_sum_payment > 0) else 'Expected Payoff', 
                line=dict(color='#1a73e8', width=3, shape='spline')
            ))
            
            # Show standard payoff line if prepayments are active
            if extra_monthly_payment > 0 or lump_sum_payment > 0:
                base_months_to_plot = min(len(base_history), 361)
                fig.add_trace(go.Scatter(
                    x=list(range(base_months_to_plot)), 
                    y=[b * exchange_rate for b in base_history[:base_months_to_plot]], 
                    mode='lines', name='Standard Payoff (No Prepay)', 
                    line=dict(color='#94a3b8', width=2, dash='dash')
                ))

            fig.add_trace(go.Scatter(
                x=list(range(months_to_plot)), 
                y=[s * exchange_rate for s in shock_history[:months_to_plot]], 
                mode='lines', fill='tonexty', fillcolor='rgba(217, 48, 37, 0.1)',
                name='Shock Scenario (+2% Rate Hike)', 
                line=dict(color='#d93025', width=2, dash='dot', shape='spline')
            ))
            fig.update_layout(
                xaxis_title="Months", yaxis_title=f"Remaining Balance ({currency_symbol})",
                hovermode="x unified", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("**How does the bank make so much money off me?**"):
            st.markdown("""
            * **Processing Fees:** Banks often charge 1-5% upfront. If you need $100k and the fee is 5%, they loan you $105k but only hand you $100k. You pay interest on the $105k!
            * **Study Interest:** Even if you don't make payments while in school, interest is still silently accumulating every single month. When you graduate, that massive pile of interest gets added to your principal.
            * **Rate Hikes:** Variable interest rates change with the economy. If rates jump just 2%, your monthly payment and total interest paid will skyrocket.
            """)

        st.divider()
        st.markdown("### The Verdict")
        if custom_monthly_payment > 0 and custom_monthly_payment_usd <= monthly_interest_accrual_usd:
            st.error(f"**Debt Crisis:** Your custom payment is too low. You will be trapped in debt forever unless you increase your monthly payment above {format_currency_markdown(currency_symbol, monthly_interest_accrual_local)}.")
        else:
            payoff_years = (len(baseline_history) - 1) / 12.0
            total_monthly_flow = (actual_payment_usd + st.session_state.extra_monthly_payment_usd) * exchange_rate
            st.success(f"**The Bottom Line:** To pay off this degree in {payoff_years:.1f} years, you must secure a job that allows you to easily part with **{format_currency_markdown(currency_symbol, total_monthly_flow)} every single month**.")
            
        st.info(f"**The Golden Rule:** Financial experts advise that your total debt at graduation (**{format_currency_markdown(currency_symbol, capitalized_principal_local)}**) should never be higher than your expected first-year starting salary. Let's see if your dream job meets this rule in **Step 3**!")