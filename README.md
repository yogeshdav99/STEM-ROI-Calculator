# STEM ROI Calculator: Advanced Educational Investment Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Data_Visualization-3F4F75?logo=plotly&logoColor=white)

## Executive Summary
The **STEM ROI Calculator** is a Master's-level Business Analytics web application designed to evaluate the true financial footprint and risk-adjusted return on investment (ROI) of international STEM degrees. 

Moving beyond simple deterministic calculators ($A + B = C$), this application utilizes advanced corporate finance methodologies (NPV, IRR) and probabilistic modeling (Monte Carlo Simulations) to help prospective students stress-test multi-thousand dollar educational investments against real-world volatility.

## Key Analytics Features

* **True Cost & Opportunity Cost Engine:** Calculates both direct out-of-pocket educational expenses and the compounding lost income (opportunity cost) incurred while studying.
* **Advanced Loan Amortization:** Simulates the "Capitalization Trap" (how study-period and grace-period interest inflates starting balances), origination fee dilution, and variable interest rate shock premiums.
* **Data-Driven Career Forecaster:** Maps dynamic, real-world starting salaries based on degree level and geographic market, cross-referencing reliable datasets.
* **Corporate Finance Valuation (NPV & IRR):** Calculates 10-year Net Present Value (NPV), precise Break-Even Horizons, and the Internal Rate of Return (IRR) of the degree asset.
* **Sensitivity Matrix:** Generates two-way data tables testing how sensitive the final NPV is to simultaneous ±10% shifts in starting salary and growth rate assumptions.
* **Risk Analytics (Monte Carlo Simulation):** Runs 1,000 statistical permutations of career pathways using Normal Distributions to generate a definitive "Probability of Profit."

## Technical Architecture

The application is built on a modular, React-inspired Python architecture using Streamlit.

* **Frontend:** Streamlit, Custom HTML/CSS injection (Glassmorphism, Responsive Grid, Micro-animations), Plotly Interactive Charts.
* **Backend Engine:** Pure Python, leveraging `numpy` for stochastic simulations and `pandas` for data manipulation.
* **Live API Integration:** Fetches real-time global currency exchange rates via `frankfurter.dev`, securely caching the network requests to optimize load times.

### Directory Structure
```text
STEM ROI Calculator/
├── .streamlit/
│   └── config.toml             # Custom Light-mode SaaS Theme
├── app.py                      # Main Application Router & Wizard State
├── tab_cost.py                 # Module: Step 1 (Investment & Opportunity Cost)
├── tab_loan.py                 # Module: Step 2 (Amortization & Debt Risk)
├── tab_career.py               # Module: Step 3 (Valuation & Monte Carlo)
├── developer_profile.py        # Module: Animated Developer Profile UI
├── utils.py                    # Core Math Engine & Global CSS Injector
├── careers.csv                 # Country baseline market data
├── career_defaults.csv         # Specific role & degree starting salaries
└── requirements.txt            # Cloud deployment dependencies
```

## Local Installation & Usage

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/STEM-ROI-Calculator.git
   cd STEM-ROI-Calculator
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

## Live Deployment
This application is fully optimized for cloud deployment and is currently hosted live on Streamlit Community Cloud.

**View the Live Application Here**
*(Note: Update this link once you deploy your app to Streamlit Cloud!)*

## Author
**Yogesh Patel**  
*Business Intelligence & Analytics*  
* LinkedIn
* Portfolio

---
*Disclaimer: This tool is designed for educational and strategic planning purposes. Always consult with a certified financial advisor or official loan servicer before making binding financial decisions.*
