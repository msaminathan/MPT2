import streamlit as st

st.set_page_config(page_title="Theory & Background", page_icon="📚", layout="wide")

# Re-inject the vibrant CSS (Streamlit resets it per page usually)
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
    .latex-container {
        background-color: #2D2B55;
        padding: 15px;
        border-radius: 10px;
        color: #F8F8F2;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 Theory & Background")
st.markdown("### Understanding Modern Portfolio Theory (MPT)")

st.write("""
Modern Portfolio Theory (MPT), pioneered by Harry Markowitz, is a mathematical framework for assembling a portfolio of assets such that the expected return is maximized for a given level of risk. 
It suggests that it is not enough to look at the expected risk and return of one particular stock. By investing in more than one stock, an investor can reap the benefits of **diversification**.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Expected Return")
    st.write("The expected return of a portfolio is the weighted average of the expected returns of the individual assets.")
    
    st.latex(r"E(R_p) = \sum_{i} w_i E(R_i)")
    st.caption("Where $w_i$ is the weight of asset $i$ and $E(R_i)$ is the expected return of asset $i$.")

    st.markdown("### 2. Risk (Volatility)")
    st.write("Risk is commonly measured by the standard deviation (volatility) of returns. For a two-asset portfolio:")

    st.latex(r"\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2w_1 w_2 \sigma_1 \sigma_2 \rho_{1,2}")
    st.caption("Notice the correlation coefficient $\\rho_{1,2}$. If it is less than 1, the portfolio risk is **less** than the weighted average of individual risks.")

    st.markdown("**Matrix Notation**")
    st.write("For a portfolio with $N$ assets, the variance can be compactly written in matrix form:")
    st.latex(r"\sigma_p^2 = w^T \Sigma w")
    st.caption(r"Where $w$ is the column vector of weights and $\Sigma$ is the covariance matrix of asset returns.")

with col2:
    st.markdown("### 3. The Efficient Frontier")
    st.write("""
    The **Efficient Frontier** is the set of optimal portfolios that offer the highest expected return for a defined level of risk.
    Portfolios that lie below the efficient frontier are sub-optimal because they do not provide enough return for the level of risk taken.
    """)
    
    st.markdown("### 4. Sharpe Ratio")
    st.write("The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, like a Treasury bond.")

    st.latex(r"Sharpe = \frac{R_p - R_f}{\sigma_p}")
    st.write("A higher Sharpe ratio indicates better risk-adjusted performance.")

st.divider()

st.markdown("### 5. Capital Allocation Line (CAL)")
st.write("""
The Capital Allocation Line (CAL) is a line created on a graph of all possible portfolios of risk-free and risky assets. 
The graph displays expected return (y-axis) versus risk (x-axis). 
The slope of the CAL is the **Sharpe Ratio** of the risky portfolio. The optimal risky portfolio is found where the CAL is tangent to the Efficient Frontier.
""")
