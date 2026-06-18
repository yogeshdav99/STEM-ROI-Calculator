import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import calculate_roi_metrics, calculate_irr, STEM_DEGREES, STEM_JOBS, DEGREE_JOB_MAPPING, run_monte_carlo_roi

def render(true_economic_cost_local, currency_symbol, exchange_rate):
    st.markdown("### Career & ROI Forecaster")
    
    col_text, col_slider = st.columns([1.5, 1], gap="large")
    with col_text:
        st.markdown("Compare two different post-graduation career tracks side-by-side. See how quickly you can pay off your loans and build actual wealth.")
    with col_slider:
        discount_rate = st.slider("Discount Rate (Inflation & Risk %)", min_value=1.0, max_value=15.0, value=7.0, step=0.5, help="This accounts for inflation and investment risk. Money tomorrow is worth less than money today.")
        
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
                "Job_Title": ["Data Scientist", "Software Engineer", "Mechanical Engineer", "Business Analyst", "Data Scientist", "Software Engineer"],
                "Degree_Level": ["Master's", "Master's", "Master's", "Master's", "Master's", "Master's"],
                "Country": ["USA", "USA", "USA", "USA", "UK", "UK"],
                "Starting_Salary_USD": [105000.0, 115000.0, 85000.0, 80000.0, 65000.0, 75000.0],
                "Source_Name": ["Glassdoor", "Levels.fyi", "BLS.gov", "Glassdoor", "Glassdoor", "Levels.fyi"],
                "Source_URL": ["https://glassdoor.com", "https://levels.fyi", "https://bls.gov", "https://glassdoor.com", "https://glassdoor.co.uk", "https://levels.fyi"]
            })
            
    df_careers = load_career_data()
    df_defaults = load_defaults_data()
    
    sub_tab_a, sub_tab_b = st.tabs(["Scenario A", "Scenario B"])
    
    def render_scenario_ui(scenario_key: str, default_country_idx: int, discount_rate: float):
        left_panel, right_panel = st.columns([1, 1.3], gap="large")
            
        with left_panel:
            col_sel1, col_sel2 = st.columns(2)
            with col_sel1: degree_level = st.selectbox(f"Degree Level ({scenario_key})", options=["Bachelor's", "Master's", "PhD"], index=0, key=f"deg_{scenario_key}")
            with col_sel2: stream = st.selectbox(f"Degree / Stream ({scenario_key})", options=STEM_DEGREES, index=None, placeholder="e.g. Mechanical Engineering", key=f"stream_{scenario_key}")
            
            available_jobs = DEGREE_JOB_MAPPING.get(stream, STEM_JOBS) if stream else STEM_JOBS
            
            col_sel3, col_sel4 = st.columns(2)
            with col_sel3: role = st.selectbox(f"Target Job ({scenario_key})", options=available_jobs, index=None, placeholder="e.g. Mechanical Engineer", key=f"role_{scenario_key}")
            with col_sel4: country = st.selectbox(f"Target Country ({scenario_key})", options=df_careers["Country"].unique(), index=default_country_idx, key=f"country_{scenario_key}")
                
            country_data = df_careers[df_careers["Country"] == country].iloc[0]
            display_role = role if role else "STEM Professional"
            display_stream = f" ({stream})" if stream else ""
            
            # Match against specific career defaults in the selected country, fallback to global role average or country average
            match = df_defaults.copy()
            if "Country" in match.columns:
                match = match[(match["Job_Title"] == role) & (match["Degree_Level"] == degree_level) & (match["Country"] == country)]
                if match.empty:
                    match = df_defaults[(df_defaults["Job_Title"] == role) & (df_defaults["Degree_Level"] == degree_level)]
            else:
                match = match[(match["Job_Title"] == role) & (match["Degree_Level"] == degree_level)]
                
            base_salary_usd = match.iloc[0]["Starting_Salary_USD"] if not match.empty else country_data['Average_STEM_Salary_USD']
            source_text = f"Source: [{match.iloc[0]['Source_Name']}]({match.iloc[0]['Source_URL']})" if not match.empty else "Source: Baseline Country Estimate"
            
            local_salary = base_salary_usd * exchange_rate
            
            with st.container(border=True):
                st.markdown(f"#### Profile: {display_role}{display_stream} in {country}")
                
                col_over1, col_over2 = st.columns(2)
                with col_over1: 
                    custom_salary_local = st.number_input(f"Override Starting Salary ({currency_symbol})", value=int(local_salary), step=5000, help=f"Base Reference: ${base_salary_usd:,.0f} USD", key=f"custom_salary_{scenario_key}")
                    st.session_state[f"saved_salary_{scenario_key}"] = custom_salary_local
                    st.caption(f"*{source_text}*")
                with col_over2: 
                    custom_growth_rate = st.number_input("Override Expected Growth Rate (%)", value=float(country_data['Growth_Rate_Pct']), step=0.5, help="Expected annual salary increase.", key=f"custom_growth_{scenario_key}")
                    st.session_state[f"saved_growth_{scenario_key}"] = custom_growth_rate
                    
            st.markdown("#### Visa & Immigration Realities")
            st.markdown(f"**Immigration Route:** {country_data['Visa_Route']}")
            
            friction = int(country_data['Visa_Friction_Score'])
            st.write(f"**Visa Difficulty Score:** {friction}/10")
            st.progress(friction / 10.0)
            
            if friction >= 8: st.error(f"**High Risk:** The {country_data['Visa_Route']} has high barriers (e.g., lotteries, caps). Note for Indian Students: You face severe backlogs (often decades) for permanent residency/Green Cards in countries like the US. Factor this stress into your decision!")
            elif friction >= 5: st.warning(f"**Moderate Risk:** The {country_data['Visa_Route']} is viable but requires finding an employer willing to sponsor you or meeting strict points criteria. Start networking early!")
            else: st.success(f"**Low Risk:** The {country_data['Visa_Route']} is highly structured and relatively accessible for international graduates, offering a clear pathway to post-study work and PR.")
                
        npv_local, break_even, cash_flows = calculate_roi_metrics(starting_salary=custom_salary_local, growth_rate=custom_growth_rate, discount_rate=discount_rate, year_0_cost=true_economic_cost_local)
        irr_value = calculate_irr(cash_flows)
            
        with right_panel:
            st.markdown("#### 10-Year Wealth Projection")
            
            roi_col1, roi_col2 = st.columns(2)
            with roi_col1: st.metric("10-Year Net Value (NPV)", f"{currency_symbol}{npv_local:,.0f}", help="Net Present Value (NPV): We take all the extra money you'll make over 10 years, subtract the cost of the degree, and reduce it to account for inflation.")
            with roi_col2: st.metric("Internal Rate of Return (IRR)", f"{irr_value:.1f}%", help="IRR treats your degree like a financial asset. Compare this to the stock market (~8%)!")
            
            be_text = f"Year {break_even}" if break_even else "10+ Years"
            st.metric("Break-Even Point", be_text, help="The exact year after graduation when your cumulative earnings finally cover the total upfront cost of your degree.")
            
            with st.expander("Year-by-Year Breakdown"):
                df_cf = pd.DataFrame({"Year": ["Year 0 (Cost)"] + [f"Year {i}" for i in range(1, 11)], "Cash Flow": [f"{currency_symbol}{cf:,.0f}" for cf in cash_flows]})
                st.dataframe(df_cf, hide_index=True, use_container_width=True)

            with st.expander("**Two-Way Sensitivity Matrix**"):
                st.markdown("This matrix shows your NPV if your starting salary and growth rates change by ±10%.")
                
                salaries = [custom_salary_local * 0.9, custom_salary_local, custom_salary_local * 1.1]
                growths = [custom_growth_rate - 1.5, custom_growth_rate, custom_growth_rate + 1.5]
                
                matrix = []
                for s in salaries:
                    row = []
                    for g in growths:
                        n, _, _ = calculate_roi_metrics(s, g, discount_rate, true_economic_cost_local)
                        row.append(f"{currency_symbol}{n:,.0f}")
                    matrix.append(row)
                
                df_sens = pd.DataFrame(matrix, columns=[f"Growth {g:.1f}%" for g in growths], index=[f"Salary {currency_symbol}{s:,.0f}" for s in salaries])
                st.dataframe(df_sens, use_container_width=True)

        st.session_state[f"scenario_label_{scenario_key}"] = f"{display_role} in {country}"
        return cash_flows, f"{display_role} in {country}"

    with sub_tab_a:
        cf_a, label_a = render_scenario_ui("A", 0, discount_rate)
    with sub_tab_b:
        cf_b, label_b = render_scenario_ui("B", 1, discount_rate)

    st.divider()
    st.markdown("### Scenario Comparison")
    
    cum_cf_a = [sum(cf_a[:i+1]) for i in range(len(cf_a))]
    cum_cf_b = [sum(cf_b[:i+1]) for i in range(len(cf_b))]
    years = [i for i in range(11)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cum_cf_a, mode='lines+markers', name=f"Scenario A: {label_a}"))
    fig.add_trace(go.Scatter(x=years, y=cum_cf_b, mode='lines+markers', name=f"Scenario B: {label_b}"))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-Even", annotation_position="top left")
    fig.update_layout(
        title="10-Year Cumulative Earnings Comparison",
        xaxis_title="Years Post-Graduation (0 = Cost at Graduation)",
        yaxis_title=f"Cumulative Cash Flow ({currency_symbol})",
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)