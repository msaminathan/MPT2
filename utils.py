import yfinance as yf
import pandas as pd
import numpy as np
import scipy.optimize as sco

def get_stock_universe():
    """
    Returns a dictionary of sectors and their representative tickers.
    """
    return {
        "High Tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AMD", "INTC", "CSCO"],
        "Finance": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "V", "MA", "AXP"],
        "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK", "TMO", "LLY", "AMGN", "BMY", "GILD"],
        "Consumer Goods": ["PG", "KO", "PEP", "COST", "WMT", "NKE", "MCD", "SBUX", "EL", "CL"],
        "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY"]
    }

def get_ticker_name_mapping():
    """
    Returns a dictionary mapping tickers to company names.
    """
    return {
        # High Tech
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corporation", "GOOGL": "Alphabet Inc.", 
        "AMZN": "Amazon.com Inc.", "NVDA": "NVIDIA Corporation", "TSLA": "Tesla Inc.", 
        "META": "Meta Platforms Inc.", "AMD": "Advanced Micro Devices", "INTC": "Intel Corporation", 
        "CSCO": "Cisco Systems",
        # Finance
        "JPM": "JPMorgan Chase & Co.", "BAC": "Bank of America", "WFC": "Wells Fargo & Co.", 
        "C": "Citigroup Inc.", "GS": "Goldman Sachs Group", "MS": "Morgan Stanley", 
        "BLK": "BlackRock Inc.", "V": "Visa Inc.", "MA": "Mastercard Inc.", "AXP": "American Express",
        # Healthcare
        "JNJ": "Johnson & Johnson", "PFE": "Pfizer Inc.", "UNH": "UnitedHealth Group", 
        "ABBV": "AbbVie Inc.", "MRK": "Merck & Co.", "TMO": "Thermo Fisher Scientific", 
        "LLY": "Eli Lilly and Co.", "AMGN": "Amgen Inc.", "BMY": "Bristol-Myers Squibb", 
        "GILD": "Gilead Sciences",
        # Consumer Goods
        "PG": "Procter & Gamble", "KO": "Coca-Cola Company", "PEP": "PepsiCo Inc.", 
        "COST": "Costco Wholesale", "WMT": "Walmart Inc.", "NKE": "NIKE Inc.", 
        "MCD": "McDonald's Corp", "SBUX": "Starbucks Corp", "EL": "Estee Lauder Cos", 
        "CL": "Colgate-Palmolive",
        # Energy
        "XOM": "Exxon Mobil Corp", "CVX": "Chevron Corp", "COP": "ConocoPhillips", 
        "SLB": "Schlumberger Ltd", "EOG": "EOG Resources", "MPC": "Marathon Petroleum", 
        "PSX": "Phillips 66", "VLO": "Valero Energy", "OXY": "Occidental Petroleum"
    }

def fetch_stock_data(tickers, period="5y"):
    """
    Fetches historical adjusted close prices for the given tickers.
    """
    if not tickers:
        return pd.DataFrame()
    
    # Download data
    # auto_adjust=True is now default, so we use 'Close' which is adjusted.
    df = yf.download(tickers, period=period, progress=False)
    
    # Extract just the Close prices
    # If MultiIndex (Price, Ticker), this gets the Close level
    if isinstance(df.columns, pd.MultiIndex):
        data = df['Close']
    else:
        # If single level, it might be just columns if we asked for one ticker?
        # But yf.download usually returns multiindex for multiple tickers or just one.
        # Let's inspect safely.
        if 'Close' in df.columns:
            data = df['Close']
        else:
             # Fallback if structure is different
             data = df
    
    # If single ticker and no list passed, it might be a Series or 1-col DF
    # Ensure it's a DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame()
        data.columns = tickers
    
    # Drop columns that are entirely NaN (e.g., delisted tickers)
    data = data.dropna(axis=1, how='all')

    # Handle missing data if any (rows)
    data = data.dropna()
    
    return data

def calculate_daily_returns(data):
    return data.pct_change().dropna()

def calculate_annualized_metrics(daily_returns):
    """
    Returns annualized mean returns and covariance matrix.
    Assuming 252 trading days.
    """
    mean_returns = daily_returns.mean() * 252
    cov_matrix = daily_returns.cov() * 252
    return mean_returns, cov_matrix

def portfolio_performance(weights, mean_returns, cov_matrix):
    """
    Calculates portfolio return and volatility.
    """
    returns = np.sum(mean_returns * weights)
    std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, std_dev

def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
    p_ret, p_var = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def minimize_volatility_func(weights, mean_returns, cov_matrix):
    p_ret, p_var = portfolio_performance(weights, mean_returns, cov_matrix)
    return p_var

def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate=0.02):
    """
    Finds the Max Sharpe Ratio portfolio and Min Volatility portfolio.
    """
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0.0, 1.0) for asset in range(num_assets))
    
    # Max Sharpe Ratio
    result_max_sharpe = sco.minimize(negative_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                                     method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Min Volatility
    args_min_vol = (mean_returns, cov_matrix)
    result_min_vol = sco.minimize(minimize_volatility_func, num_assets*[1./num_assets,], args=args_min_vol,
                                  method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result_max_sharpe, result_min_vol

def generate_efficient_frontier(mean_returns, cov_matrix, num_portfolios=5000, risk_free_rate=0.02):
    """
    Generates random portfolios to visualize the efficient frontier.
    """
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        portfolio_return, portfolio_std_dev = portfolio_performance(weights, mean_returns, cov_matrix)
        
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
        
    return results, weights_record

def calculate_efficient_frontier_line(mean_returns, cov_matrix, num_points=100):
    """
    Calculates the actual Efficient Frontier line by minimizing volatility for a range of target returns.
    """
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    bounds = tuple((0.0, 1.0) for asset in range(num_assets))
    
    # 1. Find Min Volatility Portfolio (Global Minimum)
    constraints_min_vol = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    result_min_vol = sco.minimize(minimize_volatility_func, num_assets*[1./num_assets,], args=args,
                                  method='SLSQP', bounds=bounds, constraints=constraints_min_vol)
    min_vol_ret, min_vol_vol = portfolio_performance(result_min_vol.x, mean_returns, cov_matrix)
    
    # 2. Find Max Return Portfolio (Just the asset with max return)
    # Actually, we can just iterate up to the max asset return.
    max_ret = np.max(mean_returns)
    
    # 3. Create target returns range
    target_returns = np.linspace(min_vol_ret, max_ret, num_points)
    
    frontier_volatility = []
    
    for t_ret in target_returns:
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: portfolio_performance(x, mean_returns, cov_matrix)[0] - t_ret}
        )
        
        result = sco.minimize(minimize_volatility_func, num_assets*[1./num_assets,], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            frontier_volatility.append(result.fun)
        else:
            # Fallback if optimization fails (rare but possible at boundaries)
            frontier_volatility.append(np.nan)
            
    return target_returns, frontier_volatility
