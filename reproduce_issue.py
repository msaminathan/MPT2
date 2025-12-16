
import utils
import pandas as pd

# Test 1: Robustness check - passing a list with the bad ticker 'PXD'
print("--- Test 1: Robustness with 'PXD' ---")
tickers_with_bad = ["XOM", "CVX", "PXD"] # PXD is delisted
df = utils.fetch_stock_data(tickers_with_bad, period="1y")

if "PXD" not in df.columns and "XOM" in df.columns:
    print("SUCCESS: PXD was dropped and XOM remains.")
else:
    print(f"FAILURE: Columns are {df.columns}")

if df.empty:
    print("FAILURE: DataFrame is empty!")
else:
    print(f"DataFrame shape: {df.shape}")


# Test 2: Default Energy Sector check
print("\n--- Test 2: Default Energy Sector ---")
universe = utils.get_stock_universe()
energy_tickers = universe["Energy"]
print(f"Energy Tickers: {energy_tickers}")

if "PXD" in energy_tickers:
    print("FAILURE: PXD is still in the universe definition!")
else:
    print("SUCCESS: PXD is removed from universe.")

df_energy = utils.fetch_stock_data(energy_tickers, period="1y")
if df_energy.empty:
    print("FAILURE: Energy sector data is empty!")
else:
    print(f"SUCCESS: Energy sector data fetched. Shape: {df_energy.shape}")
