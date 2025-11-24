import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

from faang_calculations import (
    faang_data,
    daily_returns,
    cum_returns,
    annual_mean_returns,
    annual_cov_matrix,
    ef,
    weights,
    correlation_risk
    )

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# PLOT 1: Cumulative Returns 
for c in cum_returns.columns:
    axes[0, 0].plot(cum_returns.index, cum_returns[c], label=c, linewidth=2)
axes[0, 0].set_title('Cumulative Returns (Growth of $1)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Multiplier')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# PLOT 2: Correlation Heatmap 
sns.heatmap(correlation_risk, annot=True, cmap='coolwarm', ax=axes[0, 1], vmin=-1, vmax=1)
axes[0, 1].set_title('Correlation Matrix', fontsize=12, fontweight='bold')

# PLOT 3: Efficient Frontier Simulation
# We simulate the frontier here for visualization
n_portfolios = 5000
all_weights = np.zeros((n_portfolios, len(daily_returns.columns)))
ret_arr = np.zeros(n_portfolios)
vol_arr = np.zeros(n_portfolios)
sharpe_arr = np.zeros(n_portfolios)

for i in range(n_portfolios):
    weights = np.array(np.random.random(len(daily_returns.columns)))
    weights = weights / np.sum(weights)
    all_weights[i,:] = weights
    ret_arr[i] = np.sum(annual_mean_returns * weights)
    vol_arr[i] = np.sqrt(np.dot(weights.T, np.dot(annual_cov_matrix, weights)))
    sharpe_arr[i] = ret_arr[i] / vol_arr[i]

sc = axes[1, 0].scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis', s=10, alpha=0.5)
axes[1, 0].set_title('Efficient Frontier (Risk vs Return)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Annualized Volatility')
axes[1, 0].set_ylabel('Annualized Return')
plt.colorbar(sc, ax=axes[1, 0], label='Sharpe Ratio')

#PLOT 4: Histogram of Daily Returns (Distribution) 
# This shows if the stock returns follow a "Normal Distribution"
for c in daily_returns.columns:
    sns.kdeplot(daily_returns[c], ax=axes[1, 1], label=c, fill=False)
axes[1, 1].set_title('Return Distribution (Density)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Daily Return')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Save and Show
plt.suptitle('FAANG Portfolio Analysis Dashboard', fontsize=16)
print("Generating Dashboard")
plt.show()










