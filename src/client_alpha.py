import requests
import matplotlib.pyplot as plt
import json

# api-endpoint
symbol = "QQQ"
URL = "https://www.alphavantage.co/query?function=TIME_SERIES_daiLY_adjusted&symbol=" + symbol + "&outputsize=300&apikey=LS4GR5WN04ICUVTI"

# sending get request and saving the response as response object
r = requests.get(url = URL)

# print(json.loads(r.text)["Time Series (Daily)"])
# extracting data in json format
# data = r.json()
closing_price = []
timeseriesdata = json.loads(r.text)["Time Series (Daily)"]
for day, vals in timeseriesdata.items():
    closing_price.append(vals["6. volume"])
    # closing_price.append(vals["5. adjusted close"])

plt.plot(closing_price)
plt.show()
# print(r.text)

#
# req = {
# "monday": {
#     "closing": 1.0
# },
# "tuesday": {
#
# },
# }
#
# for day in req.items():
#     day["monday"]["closing"]
