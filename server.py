import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from flask import Flask

app = Flask(__name__)




def savings_return(dt, interest_rate): # t in years, annual interest rate as fraction
    return np.power(1. + interest_rate, dt)

def bonds_yield(dt, interest_rate):
    return np.power(1. + interest_rate, dt)

def stock_etf_yield(dt, mean_return, return_variance):
    # calculate drift and volatility figures from kaggle
    num_iterations = 1000 # Monte Carlo iterations
    drift = mean_return - 0.5 * return_variance
    stdev = np.sqrt(return_variance)
    annual_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(int(dt), num_iterations)))
    # print(annual_returns)
    price_list = np.zeros_like(annual_returns)
    low_bound, up_bound, mid = np.ones(annual_returns.shape[0]), np.ones(annual_returns.shape[0]), np.ones(annual_returns.shape[0])
    price_list[0] = 1.0
    #Applies Monte Carlo simulation in ETF
    for t in range(1, int(dt)):
        price_list[t] = price_list[t - 1] * annual_returns[t]
        price_list[t].sort()
        print(price_list)
        mid[t] = price_list[t].mean()
        low_bound[t] = price_list[t][int(0.2*num_iterations)]
        up_bound[t] = price_list[t][int(0.8*num_iterations)]
    return mid, low_bound, up_bound

def plot_returns(mid, low_bound, up_bound):
    plt.figure(figsize=(10,6))
    plt.plot(mid, label='mid')
    plt.plot(low_bound, label='low')
    plt.plot(up_bound, label='up')
    plt.legend()
    plt.show()

def main():
    mid, low, up = stock_etf_yield(10, 0.05, 0.03)
    plot_returns(mid, low, up)

if __name__ == "__main__":
    main()
