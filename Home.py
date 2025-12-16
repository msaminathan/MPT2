import streamlit as st
import utils
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MPT Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Vibrant Theme ---
st.markdown("""
<style>
    /* Gradient Background for top container */
    .stAppHeader {
        background: linear-gradient(90deg, #1E1E2E 0%, #2D2B55 100%);
    }
    
    /* Global Text Styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        color: #F8F8F2 !important;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #7aa2f7, #99c0d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Info Cards */
    .info-card {
        background-color: #2D2B55;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #4B4B6B;
        margin-bottom: 20px;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #99c0d9;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #7aa2f7 0%, #89b4fa 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# --- Main Content ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Modern Portfolio Theory")
    st.markdown("### <span style='color: #A6ACCD'>Build, Analyze, and Optimize your Wealth.</span>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <p style="font-size: 1.1em; color: #F8F8F2;">
        Welcome to the <b>Premium MPT Analyzer</b>. This application leverages the power of data science to help you construct the mathematically optimal stock portfolio.
        Whether you are a novice looking to understand diversification or an expert seeking the Efficient Frontier, this tool is designed for you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### What can you do here?")
    st.info("📚 **Learn**: Master the math behind Risk & Return.")
    st.info("🔍 **Explore**: Visualize historical performance of Top Tech, Finance, and Healthcare stocks.")
    st.info("🚀 **Optimize**: Run Monte Carlo simulations to find the best portfolio weights.")

with col2:
    # A quick look at a random vibrant chart
    st.markdown("### Market Pulse (Demo)")
    df_demo = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Price': pd.Series(range(100)) + pd.Series(range(100)).apply(lambda x: x * 0.1 + (x%10))
    })
    fig = px.line(df_demo, x='Date', y='Price', template="plotly_dark")
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.update_traces(line_color='#7aa2f7', line_width=4)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("""
<div style="text-align: center; color: #6272A4;">
    <p>Get started by navigating to the <b>Theory & Background</b> page or jump straight to the <b>Market Explorer</b>.</p>
</div>
""", unsafe_allow_html=True)
