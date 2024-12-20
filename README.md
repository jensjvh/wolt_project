# Wolt API app

An app featuring an HTTP API to calculate a delivery fee. A submission for Wolt internship application, implemented using Python and Flask. Tests are done using Pytest, and the API testing using either Postman or `requests` library.

### Features
* Hosting the API on a local server as a Flask app.
* Calculate and return a delivery fee as a HTTP response JSON payload from a given HTTP POST request JSON payload using a Flask API.
* Check the request payload for negative values, invalid time strings or missing keys.

### Dependencies
* Python 3.10.0 or newer
* Flask 3.0.1
* pytest 6.2.5 (for testing)
* requests 2.25.1 (for sending a POST request payload, the POST request testing was also done using Postman)

### Installing dependencies
Use the command `pip install -r requirements.txt`

### How to test and run

#### Testing
* Pytest can be invoked to test the functionality of the API with the command `python3 -m pytest test_api.py`

#### Running
1. Launch the local server with the command `python3 api.py`. 
2. API testing can be done on an API platform such as Postman. Alternatively, to send a request payload with the included file `post_request.py`, use the command `python3 post_request.py` in a new terminal session. Sending a POST request payload (json) to `http://localhost:5000` returns a response payload (json) with the calculated delivery fee.

### JSON payload formats
* Request example

```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

* Request details

| Field             | Type  | Description                                                               | Example value                             |
|:---               |:---   |:---                                                                       |:---                                       |
|cart_value         |Integer|Value of the shopping cart __in cents__.                                   |__790__ (790 cents = 7.90€)                |
|delivery_distance  |Integer|The distance between the store and customer’s location __in meters__.      |__2235__ (2235 meters = 2.235 km)          |
|number_of_items    |Integer|The __number of items__ in the customer's shopping cart.                   |__4__ (customer has 4 items in the cart)   |
|time               |String |Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). |__2024-01-15T13:00:00Z__                   |

* Response example

```json
{"delivery_fee": 710}
```

* Response details

| Field         | Type  | Description                           | Example value             |
|:---           |:---   |:---                                   |:---                       |
|delivery_fee   |Integer|Calculated delivery fee __in cents__.  |__710__ (710 cents = 7.10€)|
