import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import calculate_roi_metrics, calculate_irr, STEM_DEGREES, STEM_JOBS, DEGREE_JOB_MAPPING, calculate_capitalized_principal, calculate_amortization

def render(true_economic_cost_local, currency_symbol, exchange_rate):
    st.info(f"💡 **The Story So Far:** You're about to spend **{currency_symbol}{true_economic_cost_local:,.0f}** in real cash and lost salary. Now, let's see if the job you get AFTER graduation actually pays that back.")
    
    col_text, col_slider = st.columns([1.5, 1], gap="large")
    with col_text:
        st.markdown("Compare two different post-graduation career paths. Let's see how long it takes to break even and start building actual wealth.")
    with col_slider:
        if "w_discount_rate" not in st.session_state:
            st.session_state.w_discount_rate = float(st.session_state.get("discount_rate", 7.0))
            
        discount_rate = st.slider(
            "Inflation & Risk Adjustment (%)", min_value=1.0, max_value=15.0, step=0.5, 
            key="w_discount_rate",
            help="Money tomorrow is worth less than money today. A 7% rate means we assume inflation and investment risks reduce the value of your future salary by 7% a year."
        )
        st.session_state.discount_rate = discount_rate
        
    st.divider()
    
    @st.cache_data
    def load_career_data():
        try:
            return pd.read_csv("careers.csv")
        except FileNotFoundError:
            return pd.DataFrame({
                "Country": ["USA", "Canada", "UK", "Australia", "New Zealand", "Germany"],
                "Average_STEM_Salary_USD": [90_000.0, 70_000.0, 65_000.0, 80_000.0, 60_000.0, 65_000.0],
                "Growth_Rate_Pct": [5.0, 4.5, 3.5, 4.5, 4.0, 4.0],
                "Visa_Route": ["H1B Lottery / STEM OPT", "Express Entry / Tech Pilot", "Skilled Worker Visa", "TSS / Skilled Independent", "Green List / Post-Study Work", "EU Blue Card / Job Seeker Visa"],
                "Visa_Friction_Score": [8, 4, 6, 5, 3, 2]
            })
            
    @st.cache_data
    def load_defaults_data():
        try:
            return pd.read_csv("career_defaults.csv")
        except FileNotFoundError:
            return pd.DataFrame({
                "Job_Title": ["Data Scientist", "Software Engineer"],
                "Degree_Level": ["Master's", "Master's"],
                "Country": ["USA", "USA"],
                "Starting_Salary_USD": [105000.0, 115000.0],
                "Source_Name": ["Glassdoor", "Levels.fyi"],
                "Source_URL": ["https://glassdoor.com", "https://levels.fyi"]
            })
            
    df_careers = load_career_data()
    df_defaults = load_defaults_data()
    
    # Recalculate monthly loan payment if loan exists (for safety margin)
    monthly_loan_payment_local = 0.0
    loan_amount_usd = st.session_state.get("loan_amount_usd", 0.0)
    if loan_amount_usd > 0:
        loan_ir = st.session_state.get("loan_interest_rate", 6.5)
        repay_years = st.session_state.get("target_repayment_years", 10)
        orig_fee = st.session_state.get("origination_fee", 1.5)
        prog_dur = st.session_state.get("program_duration", 4.0)
        grace_m = st.session_state.get("grace_period_months", 6)
        
        gross_loan = loan_amount_usd / (1.0 - (orig_fee / 100.0)) if orig_fee < 100 else loan_amount_usd
        cap_principal, _ = calculate_capitalized_principal(total_loan=gross_loan, annual_rate=loan_ir, program_duration=prog_dur, grace_months=grace_m)
        
        extra_mp = st.session_state.get("extra_monthly_payment_usd", 0.0)
        custom_p = st.session_state.get("custom_payment_usd", 0.0)
        act_payment, _, _, _, _ = calculate_amortization(principal=cap_principal, annual_rate=loan_ir, months=repay_years*12, custom_payment=custom_p, extra_monthly_payment=extra_mp)
        monthly_loan_payment_local = (act_payment + extra_mp) * exchange_rate
    
    sub_tab_a, sub_tab_b = st.tabs(["🌟 Your Dream Job", "🛡️ Your Backup Plan"])
    
    def render_scenario_ui(scenario_key: str, default_country_idx: int, discount_rate: float, tab_title: str):
        left_panel, right_panel = st.columns([1, 1.3], gap="large")
            
        with left_panel:
            prev_deg = st.session_state.get(f"deg_{scenario_key}")
            prev_stream = st.session_state.get(f"stream_{scenario_key}")
            prev_role = st.session_state.get(f"role_{scenario_key}")
            prev_country = st.session_state.get(f"country_{scenario_key}")

            col_sel1, col_sel2 = st.columns(2)
            with col_sel1: 
                deg_options = ["Bachelor's", "Master's", "PhD"]
                deg_idx = deg_options.index(st.session_state[f"deg_{scenario_key}"]) if st.session_state[f"deg_{scenario_key}"] in deg_options else 1
                degree_level = st.selectbox(f"Degree Level", options=deg_options, index=deg_idx, key=f"w_deg_{scenario_key}")
                
            with col_sel2: 
                stream_idx = STEM_DEGREES.index(st.session_state[f"stream_{scenario_key}"]) if st.session_state[f"stream_{scenario_key}"] in STEM_DEGREES else None
                stream = st.selectbox(f"Degree / Stream", options=STEM_DEGREES, index=stream_idx, placeholder="e.g. Mechanical Engineering", key=f"w_stream_{scenario_key}")
            
            available_jobs = DEGREE_JOB_MAPPING.get(stream, STEM_JOBS) if stream else STEM_JOBS
            
            col_sel3, col_sel4 = st.columns(2)
            with col_sel3: 
                role_idx = available_jobs.index(st.session_state[f"role_{scenario_key}"]) if st.session_state[f"role_{scenario_key}"] in available_jobs else None
                role = st.selectbox(f"Target Job", options=available_jobs, index=role_idx, placeholder="e.g. Mechanical Engineer", key=f"w_role_{scenario_key}")
                
            with col_sel4: 
                country_options = list(df_careers["Country"].unique())
                country_idx = country_options.index(st.session_state[f"country_{scenario_key}"]) if st.session_state[f"country_{scenario_key}"] in country_options else default_country_idx
                country = st.selectbox(f"Target Country", options=country_options, index=country_idx, key=f"w_country_{scenario_key}")
                
            # If key selectors changed, reset custom salary so it recalculates from defaults
            if (degree_level != prev_deg or stream != prev_stream or role != prev_role or country != prev_country):
                st.session_state[f"salary_usd_{scenario_key}"] = 0.0
                if f"w_salary_{scenario_key}" in st.session_state:
                    del st.session_state[f"w_salary_{scenario_key}"]

            country_data = df_careers[df_careers["Country"] == country].iloc[0]
            display_role = role if role else "STEM Professional"
            display_stream = f" ({stream})" if stream else ""
            
            # Multi-country salary default lookup with dynamic scaling fallback
            match = df_defaults[(df_defaults["Job_Title"] == role) & (df_defaults["Degree_Level"] == degree_level) & (df_defaults["Country"] == country)]
            if match.empty:
                usa_match = df_defaults[(df_defaults["Job_Title"] == role) & (df_defaults["Degree_Level"] == degree_level) & (df_defaults["Country"] == "USA")]
                if not usa_match.empty:
                    usa_salary = usa_match.iloc[0]["Starting_Salary_USD"]
                    usa_avg = df_careers[df_careers["Country"] == "USA"].iloc[0]["Average_STEM_Salary_USD"]
                    country_avg = country_data["Average_STEM_Salary_USD"]
                    base_salary_usd = usa_salary * (country_avg / usa_avg)
                    source_text = f"Source: Scaled from US [{usa_match.iloc[0]['Source_Name']}]"
                else:
                    base_salary_usd = country_data['Average_STEM_Salary_USD']
                    source_text = "Source: Baseline Country Estimate"
            else:
                base_salary_usd = match.iloc[0]["Starting_Salary_USD"]
                source_text = f"Source: [{match.iloc[0]['Source_Name']}]({match.iloc[0]['Source_URL']})"
                
            local_salary = base_salary_usd * exchange_rate
            
            w_salary_key = f"w_salary_{scenario_key}"
            if w_salary_key not in st.session_state:
                if st.session_state.get(f"salary_usd_{scenario_key}", 0.0) > 0.0:
                    st.session_state[w_salary_key] = float(st.session_state[f"salary_usd_{scenario_key}"] * exchange_rate)
                else:
                    st.session_state[w_salary_key] = float(local_salary)

            w_growth_key = f"w_growth_{scenario_key}"
            if w_growth_key not in st.session_state:
                st.session_state[w_growth_key] = float(st.session_state.get(f"growth_rate_{scenario_key}", country_data['Growth_Rate_Pct']))

            with st.container(border=True):
                st.markdown(f"#### Profile: {display_role}{display_stream} in {country}")
                
                col_over1, col_over2 = st.columns(2)
                with col_over1: 
                    custom_salary_local = st.number_input(f"Starting Salary ({currency_symbol})", min_value=0.0, step=5000.0, key=w_salary_key, help=f"Base Reference: ${base_salary_usd:,.0f} USD")
                    st.caption(f"*{source_text}*")
                with col_over2: 
                    custom_growth_rate = st.number_input("Expected Yearly Raise (%)", min_value=0.0, step=0.5, key=w_growth_key, help="How much your salary grows each year.")

            # Save back to persistent state
            st.session_state[f"deg_{scenario_key}"] = degree_level
            st.session_state[f"stream_{scenario_key}"] = stream
            st.session_state[f"role_{scenario_key}"] = role
            st.session_state[f"country_{scenario_key}"] = country
            st.session_state[f"salary_usd_{scenario_key}"] = float(custom_salary_local / exchange_rate) if exchange_rate > 0 else 0.0
            st.session_state[f"growth_rate_{scenario_key}"] = float(custom_growth_rate)
            st.session_state[f"saved_salary_{scenario_key}"] = custom_salary_local
            st.session_state[f"saved_growth_{scenario_key}"] = custom_growth_rate
            
            # Post-Graduation Tax & Disposable Income
            TAX_RATES = {"USA": 25.0, "Canada": 22.0, "UK": 22.0, "Australia": 25.0, "New Zealand": 20.0, "Germany": 35.0}
            tax_rate = TAX_RATES.get(country, 25.0)
            annual_tax_local = custom_salary_local * (tax_rate / 100.0)
            net_annual_salary_local = custom_salary_local - annual_tax_local
            
            student_living_local = st.session_state.get("living_usd", 20000.0) * exchange_rate
            
            w_factor_key = f"w_living_factor_{scenario_key}"
            if w_factor_key not in st.session_state:
                st.session_state[w_factor_key] = float(st.session_state.get("post_grad_living_factor", 1.5))
                
            post_grad_living_factor = st.slider("Post-Grad Living Multiplier (vs. Student Living):", min_value=1.0, max_value=3.0, step=0.1, key=w_factor_key, help="Factor in higher expenses after graduation.")
            st.session_state.post_grad_living_factor = post_grad_living_factor
            
            post_grad_living_local = student_living_local * post_grad_living_factor
            monthly_net_salary = net_annual_salary_local / 12.0
            monthly_living = post_grad_living_local / 12.0
            monthly_disposable_income = max(0.0, monthly_net_salary - monthly_living)

            st.markdown("#### The Reality of Visas")
            st.markdown(f"**Immigration Route:** {country_data['Visa_Route']}")
            
            friction = int(country_data['Visa_Friction_Score'])
            st.progress(friction / 10.0)
            
            if friction >= 8: st.error(f"**High Risk:** The {country_data['Visa_Route']} has high barriers (like lotteries). Remember: if you don't get the visa, you go home with foreign debt but a local salary. Factor this stress into your decision!")
            elif friction >= 5: st.warning(f"**Moderate Risk:** The {country_data['Visa_Route']} is viable but requires finding an employer willing to sponsor you. Start networking early!")
            else: st.success(f"**Low Risk:** The {country_data['Visa_Route']} is highly structured and relatively accessible for international graduates, offering a clear pathway to work.")
                
        npv_local, break_even, cash_flows = calculate_roi_metrics(starting_salary=custom_salary_local, growth_rate=custom_growth_rate, discount_rate=discount_rate, year_0_cost=true_economic_cost_local)
        irr_value = calculate_irr(cash_flows)
            
        with right_panel:
            st.markdown("#### 10-Year Wealth Projection")
            
            roi_col1, roi_col2 = st.columns(2)
            with roi_col1: st.metric("Extra Wealth After 10 Years", f"{currency_symbol}{npv_local:,.0f}", help="If you add up all the money you'll earn for 10 years, subtract the degree cost, and adjust for inflation — this is what's left.")
            with roi_col2: st.metric("Degree's Rate of Return", f"{irr_value:.1f}%", help="Treat your degree like a stock market investment. The stock market averages an 8% return. Does your degree beat that?")
            
            be_text = f"Year {break_even}" if break_even else "Never (10+ Years)"
            st.metric("When Do You Break Even?", be_text, help="The exact year after graduation when your cumulative earnings finally cover the total upfront cost of your degree.")
            
            # Net Take-Home & Safety Margin
            st.markdown("#### 👤 Net Take-Home & Safety Margin")
            tax_col1, tax_col2 = st.columns(2)
            with tax_col1: st.metric(label="Est. Monthly Taxes", value=f"{currency_symbol}{annual_tax_local / 12.0:,.0f}", help=f"Estimated tax based on {country}'s average STEM tax rate of {tax_rate}%.")
            with tax_col2: st.metric(label="Net Monthly Take-Home", value=f"{currency_symbol}{monthly_net_salary:,.0f}", help="Your gross monthly salary minus estimated taxes.")
                
            disp_col1, disp_col2 = st.columns(2)
            with disp_col1: st.metric(label="Monthly Disposable Income", value=f"{currency_symbol}{monthly_disposable_income:,.0f}", help="What is left after paying taxes and post-graduation living expenses.")
            with disp_col2:
                if monthly_loan_payment_local > 0:
                    margin_pct = (monthly_disposable_income / monthly_loan_payment_local) * 100
                    delta_color = "normal" if monthly_disposable_income >= monthly_loan_payment_local else "inverse"
                    st.metric(label="Loan Repayment Margin", value=f"{margin_pct:.0f}%", delta=f"{currency_symbol}{monthly_disposable_income - monthly_loan_payment_local:,.0f} Safety", delta_color=delta_color, help="Your disposable income relative to your monthly loan payment. Values over 150% are recommended.")
                else:
                    st.metric(label="Loan Repayment Margin", value="N/A (No Loan)", help="Setup a loan in Step 2 to compute this metric.")

            if monthly_loan_payment_local > 0 and monthly_disposable_income < monthly_loan_payment_local:
                st.error("🚨 **Repayment Deficit:** Your monthly disposable income is not enough to cover your student loan payment!")
            elif monthly_loan_payment_local > 0 and monthly_disposable_income < monthly_loan_payment_local * 1.5:
                st.warning("⚠️ **Tight Repayment Margin:** You can cover the loan, but you have very little cushion left for emergencies or savings.")
            elif monthly_loan_payment_local > 0:
                st.success("✅ **Healthy Repayment Margin:** You have plenty of safety cushion after making your monthly loan payments.")

            st.divider()
            st.markdown("### The Verdict")
            if break_even is None:
                st.error(f"❌ **Bad Investment:** Even after 10 years of working, this job will not pay back the **{currency_symbol}{true_economic_cost_local:,.0f}** cost of your degree.")
            elif npv_local > 0 and irr_value > 8.0:
                st.success(f"✅ **Great Investment:** Your degree pays for itself by **Year {break_even}**. After 10 years, you'll be **{currency_symbol}{npv_local:,.0f}** richer. A {irr_value:.1f}% return beats the stock market!")
            else:
                st.warning(f"⚠️ **Risky Investment:** You break even in **Year {break_even}**, but your overall return ({irr_value:.1f}%) is fairly low compared to the massive debt risk.")

            with st.expander("Show me the year-by-year cash flow"):
                df_cf = pd.DataFrame({"Timeline": ["Graduation Day (Cost)"] + [f"End of Year {i}" for i in range(1, 11)], "Your Cash Flow": [f"{currency_symbol}{cf:,.0f}" for cf in cash_flows]})
                st.dataframe(df_cf, hide_index=True, use_container_width=True)

        st.session_state[f"scenario_label_{scenario_key}"] = f"{display_role} in {country}"
        return cash_flows, f"{display_role} in {country}"

    with sub_tab_a:
        cf_a, label_a = render_scenario_ui("A", 0, discount_rate, "Dream Job")
    with sub_tab_b:
        cf_b, label_b = render_scenario_ui("B", 1, discount_rate, "Backup Plan")

    st.divider()
    st.markdown("### Career Paths Compared")
    
    cum_cf_a = [sum(cf_a[:i+1]) for i in range(len(cf_a))]
    cum_cf_b = [sum(cf_b[:i+1]) for i in range(len(cf_b))]
    years = list(range(11))
    
    # "Stay in Current Job (No Degree)" baseline
    current_sal_local = st.session_state.get("current_salary_usd", 0.0) * exchange_rate
    growth_rate = st.session_state.get("salary_growth", 3.0) / 100.0
    program_dur = st.session_state.get("program_duration", 4.0)
    
    stay_cf = [0.0]
    running_sum = 0.0
    for t in range(1, 11):
        salary_t = current_sal_local * ((1 + growth_rate) ** (program_dur + t - 1))
        running_sum += salary_t
        stay_cf.append(running_sum)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=cum_cf_a, mode='lines', fill='tozeroy', fillcolor='rgba(26, 115, 232, 0.15)',
        name=f"Dream Job: {label_a}", line=dict(color='#1a73e8', width=3, shape='spline')
    ))
    fig.add_trace(go.Scatter(
        x=years, y=cum_cf_b, mode='lines', fill='tozeroy', fillcolor='rgba(138, 43, 226, 0.1)',
        name=f"Backup Plan: {label_b}", line=dict(color='#8a2be2', width=3, shape='spline', dash='dot')
    ))
    
    if current_sal_local > 0:
        fig.add_trace(go.Scatter(
            x=years, y=stay_cf, mode='lines',
            name="Stay in Current Job (No Degree)",
            line=dict(color='#94a3b8', width=2.5, dash='dash')
        ))
        
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-Even", annotation_position="top left")
    fig.update_layout(
        title="10-Year Cumulative Earnings Comparison",
        xaxis_title="Years Post-Graduation (0 = Graduation Day)",
        yaxis_title=f"Cumulative Cash Flow ({currency_symbol})",
        hovermode="x unified", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)