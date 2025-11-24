import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import seaborn as sns

# load the dataset 

try: #this is the native path
    faang_data = pd.read_csv('FAANG dataset- finance.csv')
except FileNotFoundError:
    # This is the specific path on my local computer
    faang_data = pd.read_csv('C:/Users/DELL/Documents/PROJECT FOR DATA ANALYSIS/PROJECT- PYTHON/data/FAANG dataset- finance.csv')
print("\n" + "="*40)
print("SHORT SUMMARY OF DATA")
print("="*40)
print(faang_data.head())

#convert Date column to a datetime object that python can understand
faang_data['Date'] = pd.to_datetime(faang_data['Date'])

# set Date column as the index(the "row labels")
faang_data.set_index('Date', inplace = True)

# now we want to know the daily percentage change in the stock prices
daily_returns = faang_data.pct_change().dropna()
print("\n" + "="*40)
print("1.DAILY RETURNS")
print("="*40)
print(daily_returns.head(3))

#calculate cumulative returns
cum_returns = daily_returns.cumprod()
print("\n" + "="*40)
print("2.CUMULATIVE RETURNS")
print("="*40)
print(cum_returns.head(2))

len_assets = len(daily_returns)
print("\n" + "="*40)
print("3. NUMBER OF ASSETS")
print("="*40)
print(f"Total Assets: {len_assets}")

# expected annual return of each stocks : we have 252 trading days
annual_mean_returns = daily_returns.mean() *252
print("\n" + "="*40)
print("4.ANNUAL MEAN RETURNS")
print("="*40)
print(annual_mean_returns)


#Portfolio weights
portfolio_weights = 5*[0.2]
portfolio_returns = daily_returns.dot(portfolio_weights) #portfolio returns of the 1/n portfolio
exp_portfolio_return  = portfolio_returns.mean()


#Risk: we're kind of measuring the relationship between risk and return
annual_cov_matrix = daily_returns.cov()*252
print("\n" + "="*40)
print("5.ANNUALIZED COVARIANCE MATRIX")
print("="*40)
print(annual_cov_matrix)

annual_std_dev = daily_returns.std()*252
print("\n" + "="*40)
print("6.ANNUAL_VOLATILITY(STD DEVIATION)")
print("="*40)
print(annual_std_dev)

correlation_risk = daily_returns.corr()
print("\n" + "="*40)
print("7. CORRELATION MATRIX")
print("="*40)
print(correlation_risk) 

#Efficient frontier: shows a curve that shows returns on all efficient portfolios
ef = EfficientFrontier(annual_mean_returns , annual_cov_matrix)
print("\n" + "="*40)
print("8. MAX SHARPE RATIO")
print("="*40)
print(ef) 

#weights that maximises sharpe ratio
weights = ef.min_volatility()
my_portfolio = pd.Series(weights)
print("\n" + "="*40)
print("9. MAX SHARPE RATIO")
print("="*40)
print(my_portfolio.head(5))

#weights that minimizes volatility i.e up and down movement of stocks
volatile_portfolio= ef.portfolio_performance(risk_free_rate=0)[1]
print("\n" + "="*40)
print("10. MINIMUM VOLATILITY PORTFOLIO")
print("="*40)
print(volatile_portfolio)  






