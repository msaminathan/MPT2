import streamlit as st

st.set_page_config(page_title="References", page_icon="📖", layout="wide")

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
</style>
""", unsafe_allow_html=True)

st.title("📖 References")

st.markdown("""
### Core Reading
1. **Markowitz, H. (1952).** Portfolio Selection. *The Journal of Finance*, 7(1), 77-91.
2. **Sharpe, W. F. (1964).** Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk. *The Journal of Finance*, 19(3), 425-442.

### Textbooks
- **Bodie, Z., Kane, A., & Marcus, A. J.** *Investments*. McGraw-Hill Education.
- **Fabozzi, F. J., Gupta, F., & Markowitz, H. M.** *The Theory and Practice of Investment Management*. Wiley.

### Libraries & Tools
- [Streamlit](https://streamlit.io/)
- [Yahoo Finance (yfinance)](https://pypi.org/project/yfinance/)
- [Plotly](https://plotly.com/python/)
- [SciPy](https://scipy.org/)
""")
