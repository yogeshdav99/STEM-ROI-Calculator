import streamlit as st
import plotly.graph_objects as go
from utils import run_monte_carlo_roi

def render(true_economic_cost_local, currency_symbol, exchange_rate):
    st.info("💡 **Why does this matter?** In Step 3, we assumed you would get exactly your target salary and standard raises every year. But real life is messy. What if there's a recession? What if you get promoted faster? This step runs **1,000 different simulated lifetimes** to show you the real odds of success.")
    
    left_col, right_col = st.columns([1, 1.5], gap="large")

    with left_col:
        st.markdown("### Stress-Test Your Plan")
        st.markdown("Click below to test your *Dream Job* and *Backup Plan* against 1,000 unpredictable economic realities (inflation, market crashes, pay cuts, and promotions).")
        
        discount_rate = st.session_state.get("discount_rate", 7.0)
        
        # Check if Task 3 data is available
        if "salary_usd_A" not in st.session_state or "salary_usd_B" not in st.session_state:
            st.warning("Please complete **Step 3: Will It Pay Off?** first to set up your career plans.")
            return

        run_sim = st.button("Run 1,000 Lifetimes", type="primary")
        
    if run_sim or "mc_results_a" in st.session_state:
        true_economic_cost_usd = true_economic_cost_local / exchange_rate if exchange_rate > 0 else true_economic_cost_local
        
        if run_sim:
            # Run simulations in USD (currency-neutral) so they persist across currency switches
            salary_a = st.session_state.get("salary_usd_A", 0.0)
            growth_a = st.session_state.get("growth_rate_A", 4.0)
            salary_b = st.session_state.get("salary_usd_B", 0.0)
            growth_b = st.session_state.get("growth_rate_B", 4.0)
            
            st.session_state.mc_results_a = run_monte_carlo_roi(
                salary_a, growth_a, discount_rate, true_economic_cost_usd
            )
            st.session_state.mc_results_b = run_monte_carlo_roi(
                salary_b, growth_b, discount_rate, true_economic_cost_usd
            )

        mc_results_a = st.session_state.mc_results_a
        mc_results_b = st.session_state.mc_results_b
        
        # Scale USD simulation results to the active display currency
        worst_case_a_local = mc_results_a['worst_case_5th'] * exchange_rate
        worst_case_b_local = mc_results_b['worst_case_5th'] * exchange_rate
        npvs_a_local = mc_results_a['npvs'] * exchange_rate
        npvs_b_local = mc_results_b['npvs'] * exchange_rate
        
        with left_col:
            st.divider()
            st.markdown("#### Your Odds of Success")
            
            st.markdown(f"**Dream Job:** {st.session_state.get('scenario_label_A', 'Option A')}")
            col_a1, col_a2 = st.columns(2)
            col_a1.metric("Chance of Profit", f"{mc_results_a['prob_positive']:.1f}%", help="Out of 1,000 lifetimes, how many times did you make more money than the degree cost?")
            col_a2.metric("Absolute Worst Case", f"{currency_symbol}{worst_case_a_local:,.0f}", help="If you have terrible luck (bottom 5%), how much money will you lose over 10 years?")
            
            st.markdown(f"**Backup Plan:** {st.session_state.get('scenario_label_B', 'Option B')}")
            col_b1, col_b2 = st.columns(2)
            col_b1.metric("Chance of Profit", f"{mc_results_b['prob_positive']:.1f}%", help="Out of 1,000 lifetimes, how many times did you make more money than the degree cost?")
            col_b2.metric("Absolute Worst Case", f"{currency_symbol}{worst_case_b_local:,.0f}", help="If you have terrible luck (bottom 5%), how much money will you lose over 10 years?")

            st.divider()
            st.markdown("### The Verdict")
            if mc_results_a['prob_positive'] > 85.0:
                st.success("✅ **Safe Bet:** Your Dream Job has an excellent chance of paying off, even if the economy struggles.")
            elif mc_results_a['prob_positive'] > 50.0:
                st.warning("⚠️ **Coin Toss:** Your Dream Job is risky. You have a decent chance of profit, but you might lose money if the economy turns against you.")
            else:
                st.error("🚨 **High Risk:** In most scenarios, your Dream Job will NOT pay back your degree. You need to rely on your Backup Plan or rethink the cost.")

        with right_col:
            # Create overlaid histogram
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=npvs_a_local, 
                name=f"Dream Job: {st.session_state.get('scenario_label_A', 'Option A')}", 
                nbinsx=50, opacity=0.75, 
                marker_color='#1a73e8', marker_line_width=1, marker_line_color='rgba(255,255,255,0.2)'
            ))
            fig_mc.add_trace(go.Histogram(
                x=npvs_b_local, 
                name=f"Backup Plan: {st.session_state.get('scenario_label_B', 'Option B')}", 
                nbinsx=50, opacity=0.6, 
                marker_color='#8a2be2', marker_line_width=1, marker_line_color='rgba(255,255,255,0.2)'
            ))
            
            fig_mc.update_layout(
                barmode='overlay',
                title="How 1,000 Alternate Lifetimes Played Out",
                xaxis_title=f"Wealth After 10 Years ({currency_symbol})",
                yaxis_title="Number of Simulated Lifetimes",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_mc.add_vline(x=0, line_dash="dash", line_color="gray", annotation_text="Break-Even (Loss vs Profit)")
            st.plotly_chart(fig_mc, use_container_width=True)
            
            with st.expander("How do I read this chart?"):
                st.markdown("""
                * Everything to the **right of the Break-Even line** means you made a profit.
                * Everything to the **left of the Break-Even line** means you lost money on the degree.
                * The taller the bars are in a certain area, the more likely that outcome is. A big cluster of bars on the right means you're almost guaranteed to succeed!
                """)