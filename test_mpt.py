import utils
import pandas as pd
import numpy as np

def test_mpt():
    print("Testing MPT Utils...")
    
    # 1. Test Data Fetching
    print("1. Fetching data for AAPL, MSFT...")
    try:
        df = utils.fetch_stock_data(["AAPL", "MSFT", "GOOGL"], period="1mo")
        if df.empty:
            print("ERROR: Dataframe is empty.")
            return
        print(f"   Success. Shape: {df.shape}")
    except Exception as e:
        print(f"   ERROR: {e}")
        return

    # 2. Test Math
    print("2. Calculating metrics...")
    daily_returns = utils.calculate_daily_returns(df)
    mean, cov = utils.calculate_annualized_metrics(daily_returns)
    print("   Success.")

    # 3. Test Optimization
    print("3. Running Optimization...")
    try:
        max_sharpe, min_vol = utils.optimize_portfolio(mean, cov)
        print(f"   Max Sharpe Success: {max_sharpe.success}")
        print(f"   Min Vol Success: {min_vol.success}")
        print(f"   Weights Sum: {np.sum(max_sharpe.x):.2f}")
    except Exception as e:
        print(f"   ERROR in optimization: {e}")

if __name__ == "__main__":
    test_mpt()
