import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import requests

# Derive these from Alpha Vantage data
INTEREST_RATE = 0.01
ANNUAL_DIVIDEND = 0.01 # fractional
STOCK_RETURN = 0.03
STOCK_RETURN_VAR = 0.01


def savings_return(dt, interest_rate): # t in years, annual interest rate as fraction
    return np.power(1. + interest_rate, dt)

def stock_etf_yield(dt, mean_return, return_variance):
    # calculate drift and volatility figures from kaggle
    num_iterations = 1000 # Monte Carlo iterations
    drift = mean_return - 0.5 * return_variance
    stdev = np.sqrt(return_variance)
    annual_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(int(dt), num_iterations)))
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

def calc_time_array(dt):
    return np.linspace(0, dt, int(dt)+1)

def savings_fraction(dt):
    times = calc_time_array(dt)
    initial_split = min(0.2, 1.0 - 0.1 * dt)
    slope = (1. - initial_split)/(1.0 * dt)
    saving_fraction = slope * times + initial_split
    return saving_fraction

def calculate_total_return(dt, starting_savings, monthly_saving, interest_rate, return_rate, return_variance, dividend):
    times = calc_time_array(dt)
    savings_frac = savings_fraction(dt)

    num_iterations = 1000 # Monte Carlo iterations
    drift = (return_rate - 0.5 * return_variance + dividend) * (1.0-savings_frac) + savings_frac * interest_rate
    drift = np.tile(drift, (num_iterations,1)).T # prepare for Monte Carlo sampling
    stdev = np.sqrt(return_variance) * (1.0-savings_frac)
    stdev = np.tile(stdev, (num_iterations,1)).T
    annual_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(len(times), num_iterations)))
    total_money = np.zeros_like(annual_returns)
    low_bound, up_bound, mid = np.ones(annual_returns.shape[0]), np.ones(annual_returns.shape[0]), np.ones(annual_returns.shape[0])
    total_money[0] = starting_savings

    for t in range(1, len(times)):
        total_money[t] = total_money[t - 1] * annual_returns[t] + 12.0 * monthly_saving
        total_money[t].sort()
        print(total_money)
        mid[t] = total_money[t].mean()
        low_bound[t] = total_money[t][int(0.2*num_iterations)]
        up_bound[t] = total_money[t][int(0.8*num_iterations)]
    return mid, low_bound, up_bound


def plot_returns(mid, low_bound, up_bound):
    plt.figure(figsize=(10,6))
    plt.plot(mid, label='mid')
    plt.plot(low_bound, label='low')
    plt.plot(up_bound, label='up')
    plt.legend()
    plt.show()

def main():
    # mid, low, up = stock_etf_yield(10, 0.05, 0.03)
    mid, low, up = calculate_total_return(10, 1000, 100.0, 0.01, 0.15, 0.08, 0.005)
    plot_returns(mid, low, up)

if __name__ == "__main__":
    main()
