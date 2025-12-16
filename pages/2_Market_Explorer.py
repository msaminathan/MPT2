import streamlit as st
import utils
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Market Explorer", page_icon="🔍", layout="wide")

# Custom CSS
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

st.title("🔍 Market Explorer")

# --- Sidebar Controls ---
st.sidebar.header("Data Selection")
universe = utils.get_stock_universe()

# Flatten the universe for easy searching
all_tickers = []
for sector, tickers in universe.items():
    all_tickers.extend(tickers)

# Category selection helper
selected_sector = st.sidebar.selectbox("Select Sector (Quick Add)", ["None"] + list(universe.keys()))
default_tickers = universe[selected_sector] if selected_sector != "None" else ["AAPL", "MSFT", "GOOGL"]

selected_tickers = st.sidebar.multiselect(
    "Select Tickers",
    options=sorted(list(set(all_tickers))), # Unique and sorted
    default=default_tickers
)

input_tickers = st.sidebar.text_input("Add Custom Tickers (comma separated, e.g. NVDA, TSLA)")

if input_tickers:
    custom_list = [t.strip().upper() for t in input_tickers.split(",")]
    # Add to selected if not already there to avoid duplicates
    for t in custom_list:
        if t not in selected_tickers:
            selected_tickers.append(t)

period = st.sidebar.selectbox("Time Period", ["1y", "2y", "5y", "10y", "max"], index=1)

if not selected_tickers:
    st.warning("Please select at least one ticker to view data.")
    st.stop()

# --- Data Fetching ---
with st.spinner("Fetching Market Data..."):
    df = utils.fetch_stock_data(selected_tickers, period=period)

if df.empty:
    st.error("No data found for the selected tickers.")
    st.stop()

# --- Visualizations ---

# Normalized Price Chart (Rebased to 100)
st.subheader("📈 Normalized Price History (Base = 100)")
normalized_df = df / df.iloc[0] * 100
fig_price = px.line(normalized_df, x=normalized_df.index, y=normalized_df.columns, template="plotly_dark")
fig_price.update_layout(height=500, xaxis_title="Date", yaxis_title="Normalized Price")
st.plotly_chart(fig_price, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Statistics")
    daily_returns = utils.calculate_daily_returns(df)
    mean_ret, cov = utils.calculate_annualized_metrics(daily_returns)
    volatility = daily_returns.std() * (252**0.5)
    
    stats_df = pd.DataFrame({
        "Annualized Return": mean_ret,
        "Annualized Volatility": volatility
    })
    st.dataframe(stats_df.style.format("{:.2%}"), use_container_width=True)

with col2:
    st.subheader("📉 Correlation Matrix")
    corr_matrix = df.pct_change().corr()
    st.dataframe(corr_matrix.style.format("{:.2f}"), use_container_width=True)

with st.expander("View Raw Data"):
    st.dataframe(df)
