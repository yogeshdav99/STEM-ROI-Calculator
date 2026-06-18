import streamlit as st
import plotly.graph_objects as go
from utils import run_monte_carlo_roi

def render(true_economic_cost_local, currency_symbol):
    left_col, right_col = st.columns([1, 1.5], gap="large")

    with left_col:
        st.markdown("### Risk Analysis (Monte Carlo)")
        st.markdown("Real-world careers aren't perfect straight lines. This engine simulates **1,000 alternate realities** (factor in recessions, promotions, and market volatility) to determine the statistical probability that your degree actually pays off.")
        
        discount_rate = st.session_state.get("discount_rate", 7.0)
        
        # Check if Task 3 data is available
        if "saved_salary_A" not in st.session_state or "saved_salary_B" not in st.session_state:
            st.warning("Please complete **Task 3: Career & ROI** first to set up your career scenarios.")
            return

        # Regular sized button to save space
        run_sim = st.button("Run Comparative Simulation", type="primary")
        
    if run_sim or "mc_results_a" in st.session_state:
        if run_sim:
            # Run and save simulations in session state so they persist
            st.session_state.mc_results_a = run_monte_carlo_roi(
                st.session_state.get("saved_salary_A"), 
                st.session_state.get("saved_growth_A"), 
                discount_rate, true_economic_cost_local
            )
            st.session_state.mc_results_b = run_monte_carlo_roi(
                st.session_state.get("saved_salary_B"), 
                st.session_state.get("saved_growth_B"), 
                discount_rate, true_economic_cost_local
            )

        mc_results_a = st.session_state.mc_results_a
        mc_results_b = st.session_state.mc_results_b
        
        with left_col:
            st.divider()
            st.markdown("#### Comparative Risk Metrics")
            
            st.markdown(f"**Scenario A: {st.session_state.get('scenario_label_A', 'Option A')}**")
            col_a1, col_a2 = st.columns(2)
            col_a1.metric("Probability of Profit", f"{mc_results_a['prob_positive']:.1f}%")
            col_a2.metric("Worst Case (5th %ile)", f"{currency_symbol}{mc_results_a['worst_case_5th']:,.0f}")
            
            st.markdown(f"**Scenario B: {st.session_state.get('scenario_label_B', 'Option B')}**")
            col_b1, col_b2 = st.columns(2)
            col_b1.metric("Probability of Profit", f"{mc_results_b['prob_positive']:.1f}%")
            col_b2.metric("Worst Case (5th %ile)", f"{currency_symbol}{mc_results_b['worst_case_5th']:,.0f}")

        with right_col:
            # Create overlaid histogram
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(x=mc_results_a['npvs'], name=st.session_state.get('scenario_label_A', 'Scenario A'), nbinsx=50, opacity=0.7))
            fig_mc.add_trace(go.Histogram(x=mc_results_b['npvs'], name=st.session_state.get('scenario_label_B', 'Scenario B'), nbinsx=50, opacity=0.7))
            
            fig_mc.update_layout(
                barmode='overlay',
                title="Distribution of Potential Financial Outcomes",
                xaxis_title=f"Net Present Value ({currency_symbol})",
                yaxis_title="Number of Simulated Outcomes",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_mc.add_vline(x=0, line_dash="dash", line_color="gray", annotation_text="Break-Even")
            st.plotly_chart(fig_mc, use_container_width=True)