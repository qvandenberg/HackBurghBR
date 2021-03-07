import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

# Derive these from Alpha Vantage data
INTEREST_RATE = 0.01
ANNUAL_DIVIDEND = 0.01 # fractional
STOCK_RETURN = 0.03
STOCK_RETURN_VAR = 0.01



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

@app.route('/api/v1/prognosis', methods=['GET'])
def prognosis():
    # if len(request.args)==0:
    #     return "Error: No data fields provided."

    # Create an empty list for our results
    results = {}

    # Extract data from get request
    # dt = request.

    # compute prognosis and package in request
    mid, low, up = calculate_total_return(10, 1000, 100.0, 0.01, 0.15, 0.08, 0.005)
    results['mid'] = mid.tolist()
    results['low'] = low.tolist()
    results['up'] = up.tolist()
    print(results)
    return jsonify(results)


def main():
    # mid, low, up = stock_etf_yield(10, 0.05, 0.03)
    # mid, low, up = calculate_total_return(10, 1000, 100.0, 0.01, 0.15, 0.08, 0.005)
    # plot_returns(mid, low, up)

    app.run()

if __name__ == "__main__":
    main()
