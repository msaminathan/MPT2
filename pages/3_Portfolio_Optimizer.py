import streamlit as st
import utils
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Portfolio Optimizer", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stAppHeader { background: linear-gradient(90deg, #1E1E2E 0%, #2D2B55 100%); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #7aa2f7, #99c0d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Portfolio Optimization Engine")

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")
universe = utils.get_stock_universe()
all_tickers = [t for list_t in universe.values() for t in list_t]

selected_tickers = st.sidebar.multiselect(
    "Select Assets for Portfolio",
    options=sorted(list(set(all_tickers))),
    default=["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
)

input_tickers = st.sidebar.text_input("Add Custom Tickers (e.g. SPY, GLD)")
if input_tickers:
    custom_list = [t.strip().upper() for t in input_tickers.split(",")]
    for t in custom_list:
        if t not in selected_tickers:
            selected_tickers.append(t)

risk_free_rate = st.sidebar.slider("Risk Free Rate (%)", 0.0, 10.0, 2.0, step=0.1) / 100.0

if len(selected_tickers) < 2:
    st.warning("Please select at least 2 assets to optimize a portfolio.")
    st.stop()

# --- Analysis Trigger ---
if st.button("Run Optimization"):
    with st.spinner("Downloading Data & Simulating..."):
        # Fetch Data
        df = utils.fetch_stock_data(selected_tickers)
        if df.empty:
            st.error("No data found.")
            st.stop()
            
        daily_returns = utils.calculate_daily_returns(df)
        mean_ret, cov_matrix = utils.calculate_annualized_metrics(daily_returns)
        
        # Optimize
        max_sharpe, min_vol = utils.optimize_portfolio(mean_ret, cov_matrix, risk_free_rate)
        
        # Efficient Frontier Simulation
        results, weights_record = utils.generate_efficient_frontier(mean_ret, cov_matrix, num_portfolios=2000, risk_free_rate=risk_free_rate)
        
        # Calculate Efficient Frontier Line (Envelope)
        ef_returns, ef_volatilities = utils.calculate_efficient_frontier_line(mean_ret, cov_matrix)
        
        # Max Sharpe Results
        max_sharpe_ret, max_sharpe_vol = utils.portfolio_performance(max_sharpe.x, mean_ret, cov_matrix)
        
        # Min Vol Results
        min_vol_ret, min_vol_vol = utils.portfolio_performance(min_vol.x, mean_ret, cov_matrix)

    # --- Display Results ---
    
    # 1. Efficient Frontier & CAL Plot
    st.subheader("Efficient Frontier & Capital Allocation Line")
    
    # Scatter of simulated portfolios
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=results[0,:], 
        y=results[1,:],
        mode='markers',
        marker=dict(
            color=results[2,:], 
            colorscale='Viridis', 
            showscale=True,
            colorbar=dict(title="Sharpe Ratio")
        ),
        name='Simulated Portfolios'
    ))

    # Efficient Frontier Line
    fig.add_trace(go.Scatter(
        x=ef_volatilities, y=ef_returns,
        mode='lines', line=dict(color='#6BFFB8', width=2), # Specific green distinct from others
        name='Efficient Frontier'
    ))
    
    # Max Sharpe Point
    fig.add_trace(go.Scatter(
        x=[max_sharpe_vol], y=[max_sharpe_ret],
        mode='markers', marker=dict(color='red', size=14, symbol='star'),
        name='Max Sharpe Ratio'
    ))
    
    # Min Vol Point
    fig.add_trace(go.Scatter(
        x=[min_vol_vol], y=[min_vol_ret],
        mode='markers', marker=dict(color='blue', size=14, symbol='circle'),
        name='Min Volatility'
    ))
    
    # CAL Line
    # Point 1: Risk Free Rate (Vol=0, Ret=Rf)
    # Point 2: Max Sharpe Portfolio (Vol=max_sharpe_vol, Ret=max_sharpe_ret)
    # Extend line a bit
    cal_x = [0, max_sharpe_vol * 1.5]
    slope = (max_sharpe_ret - risk_free_rate) / max_sharpe_vol
    cal_y = [risk_free_rate, risk_free_rate + slope * (max_sharpe_vol * 1.5)]
    
    fig.add_trace(go.Scatter(
        x=cal_x, y=cal_y, mode='lines', line=dict(color='#99c0d9', dash='dash', width=2),
        name='Capital Allocation Line (CAL)'
    ))

    # Add Risk Free Asset Marker
    fig.add_trace(go.Scatter(
        x=[0], y=[risk_free_rate],
        mode='markers+text', 
        marker=dict(color='#99c0d9', size=10, symbol='diamond'),
        text=['Rf'], textposition="top right",
        name='Risk Free Rate'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Annualized Volatility (Risk)", rangemode="tozero"),
        yaxis=dict(title="Annualized Return"),
        height=600,
        legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. Portfolio Weights
    st.subheader("Optimal Portfolio Composition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Max Sharpe Portfolio**")
        st.write(f"Return: `{max_sharpe_ret:.2%}` | Volatility: `{max_sharpe_vol:.2%}` | Sharpe: `{results[2,:].max():.2f}`")
        
        # Clean weights < 1%
        ms_weights = pd.Series(max_sharpe.x, index=selected_tickers)
        ms_weights = ms_weights[ms_weights > 0.01]
        
        fig_pie1 = px.pie(values=ms_weights.values, names=ms_weights.index, title="Max Sharpe Weights", template="plotly_dark")
        st.plotly_chart(fig_pie1, use_container_width=True)
        
    with col2:
        st.markdown("**Min Volatility Portfolio**")
        st.write(f"Return: `{min_vol_ret:.2%}` | Volatility: `{min_vol_vol:.2%}`")
        
        mv_weights = pd.Series(min_vol.x, index=selected_tickers)
        mv_weights = mv_weights[mv_weights > 0.01]
        
        fig_pie2 = px.pie(values=mv_weights.values, names=mv_weights.index, title="Min Volatility Weights", template="plotly_dark")
        st.plotly_chart(fig_pie2, use_container_width=True)

else:
    st.info("Select tickers from the sidebar and click **Run Optimization** to begin.")
