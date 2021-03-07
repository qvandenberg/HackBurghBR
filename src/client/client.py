import requests

# api-endpoint
# URL = "http://127.0.0.1:5000/api/v1/prognosis"
URL = "https://investment-time-series-i3uvcztkyq-uw.a.run.app:8080/api/v1/prognosis"
# defining a params dict for the parameters to be sent to the API
PARAMS = { 'time' : 10.0,
            'current_savings': 1000.0,
            'monthly_savings': 100.0
            }

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
# data = r.json()

print(r.text)
