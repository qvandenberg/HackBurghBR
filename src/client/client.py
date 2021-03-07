import requests

# api-endpoint
URL = "http://127.0.0.1:5000/api/v1/prognosis"


# defining a params dict for the parameters to be sent to the API
PARAMS = {'initial_savings': 1000.0}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
# data = r.json()

print(r)


req = {
"monday": {
    "closing": 1.0
},
"tuesday": {

},
}

for day in req.items():
    day["monday"]["closing"]