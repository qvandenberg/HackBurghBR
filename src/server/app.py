import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import requests
from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)
app.config["DEBUG"] = True

# Store market data in cache to avoid repeated API calls to Alpha Vantage
symbols = ["QQQ"]
market_data = {} # symbol : [prices]



# Derive these from Alpha Vantage data
INTEREST_RATE = 0.01
ANNUAL_DIVIDEND = 0.01 # fractional
STOCK_RETURN = 0.03
STOCK_RETURN_VAR = 0.01

def get_closing_price_and_dividend(symbol, max_weeks):
    # URL = "https://www.alphavantage.co/query?function=TIME_SERIES_daiLY_adjusted&symbol=" + symbol + "&outputsize=compact&apikey=LS4GR5WN04ICUVTI"
    URL = "https://www.alphavantage.co/query?function=TIME_SERIES_weekLY_adjusted&symbol=" + symbol + "&outputsize=compact&apikey=LS4GR5WN04ICUVTI"
    # URL = "https://www.alphavantage.co/query?function=TIME_SERIES_monthLY_adjusted&symbol=QQQ&apikey=LS4GR5WN04ICUVTI"
    r = requests.get(url = URL)
    closing_price = []
    dividends = []
    # timeseriesdata = json.loads(r.text)["Time Series (Daily)"]
    timeseriesdata = json.loads(r.text)["Weekly Adjusted Time Series"]
    # timeseriesdata = json.loads(r.text)["Monthly Adjusted Time Series"]
    for day, vals in timeseriesdata.items():
        if (len(closing_price) <= max_weeks):
            closing_price.append(float(vals["5. adjusted close"]))
            if float(vals["7. dividend amount"]) > 0.0:
                dividends.append(float(vals["7. dividend amount"]))
        else:
            break
    closing_price.reverse() # so latest month comes last in list
    return closing_price, np.array(dividends).mean()

def compute_stock_parameters(symbol):
    symbol = difflib.get_close_matches(symbol, symbols)[0]
    price_series, dividend = get_closing_price_and_dividend(symbol, 100)
    print(price_series)
    # plt.plot(price_series)
    # plt.show()
    pct_changes = np.diff(price_series) / price_series[:-1]
    log_returns = np.log(1 + pct_changes)
    mean_return = log_returns.mean()
    var = log_returns.var()
    return { "return_rate": 52.0 * mean_return,
            "return_variance": 52.0 * var,
            "dividend": dividend/100.0
        }

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
    low_bound, up_bound, mid = starting_savings * np.ones(annual_returns.shape[0]), starting_savings * np.ones(annual_returns.shape[0]), starting_savings * np.ones(annual_returns.shape[0])
    total_money[0] = starting_savings

    for t in range(1, len(times)):
        total_money[t] = total_money[t - 1] * annual_returns[t] + 12.0 * monthly_saving
        total_money[t].sort()
        print(total_money)
        mid[t] = total_money[t].mean()
        low_bound[t] = total_money[t][int(0.2*num_iterations)]
        up_bound[t] = total_money[t][int(0.8*num_iterations)]
    return mid, low_bound, up_bound

def calculate_savings_return(dt, current_savings, monthly_saving, interest_rate):
    times = calc_time_array(dt)
    moneys = np.zeros_like(times)
    moneys[0] = current_savings
    for idx in range(1, len(times)):
        moneys[idx] = moneys[idx-1]*(1+interest_rate) + 12.0 * monthly_saving
    return moneys

def plot_returns(mid, low_bound, up_bound):
    plt.figure(figsize=(10,6))
    plt.plot(mid, label='mid')
    plt.plot(low_bound, label='low')
    plt.plot(up_bound, label='up')
    plt.legend()
    plt.show()

@app.route('/api/v1/prognosis', methods=['GET'])
def prognosis():
    if len(request.args)==0:
        return "Error: No data fields provided."

    stock_symbol = "QQQ"
    return_params = compute_stock_parameters(stock_symbol)
    # Create an empty list for our results
    results = {}

    # Extract data from get request
    dt = float(request.args['time'])
    current_savings = float(request.args['current_savings'])
    monthly_savings = float(request.args['monthly_savings'])
    bank_interest = 0.001

    # compute prognosis and package in request
    mid, low, up = calculate_total_return(dt, current_savings, monthly_savings, bank_interest, return_params["return_rate"], return_params["return_variance"], return_params["dividend"])
    results['mid'] = mid.tolist()
    results['low'] = low.tolist()
    results['up'] = up.tolist()
    results['savings_only'] = calculate_savings_return(dt, current_savings, monthly_savings, bank_interest).tolist()
    # print(results)
    return jsonify(results)


def main():
    # mid, low, up = calculate_total_return(10, 1000, 100.0, 0.001, 0.27, 0.06, 0.0047)
    # plot_returns(mid, low, up)

    app.run()

if __name__ == "__main__":
    main()
