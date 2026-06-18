# 🗺️ MASTER ROADMAP: STEM ROI CALCULATOR

## 📌 PHASE 1: The Cost Projection Calculator (Weeks 1 & 2)

*Goal: Help students understand the absolute true cost of their degree under multiple financial scenarios.*

### 🧱 Step 1.1: Direct Costs & Opportunity Cost (Current State)

* **UI Inputs:** Sliders for annual tuition, annual living expenses, and program duration (1, 1.5, 2 years).
* **The Logic:** Calculate Total Direct Cost.
* **The "Anxiety" Feature:** Add a slider for "Current Annual Salary." Calculate lost income over the duration of the degree.
* **UI Output:** Display metric cards for **Total Direct Cost**, **Total Opportunity Cost**, and **True Economic Cost**.

### 📉 Step 1.2: The Loan & Interest Engine

* **UI Inputs:** Slider for "% of degree funded by loans" and a slider for "Expected Loan Interest Rate" (e.g., 5% to 9%).
* **The Logic:**
* Calculate principal loan balance upon graduation.
* Build an amortization function to simulate standard 10-year repayment vs. a variable rate shock scenario (+2% increase).


* **UI Output:** An interactive line chart (`st.line_chart` or `plotly`) showing total debt payoff over time vs. total interest paid.

### 🛡️ Step 1.3: Post-Graduation Grace Period & Emergency Mode

* **UI Inputs:** "Months to find a job after graduation" slider (0 to 12 months).
* **The Logic:** Accumulate daily/monthly compounding interest during the grace period while salary is $0.
* **UI Output:** Alert boxes (`st.warning`) showing how much extra the loan grows if it takes 6+ months to find a role.

---

## 💼 PHASE 2: The Career Pathway Analyzer (Weeks 2 & 3)

*Goal: Contrast different global career tracks, calculate dynamic ROI metrics, and evaluate sponsorship odds.*

### 📊 Step 2.1: Multi-Scenario Architecture

* **UI Structure:** Implement Streamlit tabs (`st.tabs(["Scenario A", "Scenario B"])`) so users can compare two completely different paths (e.g., *Scenario A: MSBA in New Zealand* vs. *Scenario B: MSDS in the US*).
* **Data Integration:** Create a small local dataset (`careers.csv` or an Excel file) using Gemini containing typical starting salaries, 5-year growth rates, and baseline visa cap numbers.

### 🧮 Step 2.2: Hard Finance Metrics (NPV & Break-Even)

* **The Logic:**
* Project cash flows out for 10 years post-graduation.
* Calculate **Net Present Value (NPV)** using a standard discount rate (e.g., 6% or 8%).
* Calculate the exact **Break-Even Year** (the cross-over point where cumulative career earnings surpass total degree costs).


* **UI Output:** A side-by-side comparison table using `st.dataframe` or a formatted table.

### 🌍 Step 2.3: International Sponsorship Index

* **UI Inputs:** Dropdown menu for Target Country (US, UK, Canada, Australia, NZ).
* **The Logic:** Assign a **Sponsorship Difficulty Score (1-10)** based on structural data (e.g., US H1B lottery odds vs. NZ Green List pathways).
* **UI Output:** A color-coded status indicator (`st.info`, `st.success`, `st.error`) estimating visa friction.

---

## 🎨 PHASE 3: Polish, Refactor & Deployment (Week 4)

*Goal: Turn functional code into a pristine, user-friendly production app for your portfolio.*

### 🧹 Step 3.1: Code Optimization via R / Python Refactoring

* **Data Verification:** Use an Excel sheet to run parallel calculations to audit your Python math, ensuring NPV and amortization schedules match to the penny.
* **Code Clean-up:** Use Gemini inside VS Code to refactor your code into clean, modular Python functions with robust error handling (e.g., handling $0 inputs gracefully).

### 💅 Step 3.2: Advanced UI/UX Enhancements

* **Visuals:** Replace basic Streamlit charts with interactive **Plotly** charts that display hover data.
* **Contextual Help:** Add tooltips (`help="This factors in inflation..."`) to every slider so undergrads understand financial terms.

### 🚀 Step 3.3: Global Cloud Deployment

* **Version Control:** Push your finalized code repository to **GitHub**.
* **Live App:** Link your repository to **Streamlit Community Cloud** to generate a live, shareable public URL.
* **Documentation:** Write a professional GitHub `README.md` complete with an architecture diagram, making it a stellar highlight for your resume.
