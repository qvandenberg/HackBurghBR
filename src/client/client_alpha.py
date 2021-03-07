import requests
import matplotlib.pyplot as plt
import json
import numpy as np
import difflib

symbols = ["QQQ"]

# # api-endpoint
# symbol = "QQQ"
# URL = "https://www.alphavantage.co/query?function=TIME_SERIES_weekLY_adjusted&symbol=" + symbol + "&outputsize=compact&apikey=LS4GR5WN04ICUVTI"
#
# # sending get request and saving the response as response object
# r = requests.get(url = URL)
#
# # print(json.loads(r.text)["Time Series (Daily)"])
# # extracting data in json format
# # data = r.json()
# closing_price = []
# timeseriesdata = json.loads(r.text)["Weekly Adjusted Time Series"]
# for day, vals in timeseriesdata.items():
#     # closing_price.append(float(vals["6. volume"]))
#     closing_price.append(float(vals["5. adjusted close"]))
# print(closing_price)
# plt.plot(closing_price)
# plt.show()



def download_market_data(symbols):
    for symbol in symbols:
        market_data[symbol] = get_weekly_closing_price(symbol)

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
    plt.plot(price_series)
    plt.show()
    pct_changes = np.diff(price_series) / price_series[:-1]
    log_returns = np.log(1 + pct_changes)
    mean_return = log_returns.mean()
    var = log_returns.var()
    return { "return_rate": 52.0 * mean_return,
            "return_variance": 52.0 * var,
            "dividend": dividend
        }

def main():
    print(compute_stock_parameters("QQQ"))

if __name__ == "__main__":
    main()
