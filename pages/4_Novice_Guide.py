import streamlit as st

st.set_page_config(page_title="Novice Guide", page_icon="🧭", layout="wide")

st.markdown("""
<style>
    .stAppHeader { background: linear-gradient(90deg, #1E1E2E 0%, #2D2B55 100%); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 {
        color: #F8F8F2 !important;
        background: -webkit-linear-gradient(45deg, #7aa2f7, #99c0d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .step-card {
        background-color: #2D2B55;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #7aa2f7;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧭 Novice User Guide")
st.markdown("### How to conduct an analysis in 4 easy steps")

st.markdown("""
<div class="step-card">
    <h3>Step 1: Understand the Basics</h3>
    <p>Read the <b>Theory & Background</b> page first. Understand what <i>Risk</i> (Volatility) and <i>Reward</i> (Return) mean. Remember: High return usually comes with high risk.</p>
</div>

<div class="step-card">
    <h3>Step 2: Explore the Market</h3>
    <p>Go to the <b>Market Explorer</b>. Select the "Tech" category. Look at the <i>Correlation Matrix</i>. You want to find stocks that don't move exactly together (low correlation) to build a safer portfolio.</p>
</div>

<div class="step-card">
    <h3>Step 3: Run the Optimizer</h3>
    <p>Navigate to <b>Portfolio Optimizer</b>. Select 5-10 stocks you like. Click "Run Optimization". The app will simulate thousands of possibilities for you.</p>
</div>

<div class="step-card">
    <h3>Step 4: Pick your Portfolio</h3>
    <p>Look for the <b>Star</b> (Max Sharpe Ratio). This is the mathematically "best" portfolio for risk-adjusted returns. Look at the pie chart below it to see how much money you should put in each stock.</p>
</div>
""", unsafe_allow_html=True)
