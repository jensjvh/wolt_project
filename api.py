import fee
from flask import Flask,json, request

#Create a Flask app
app = Flask(__name__)

#POST request handler
@app.route('/', methods=['POST'])
def api():
    """
    Handle the main POST request to return a response containing
    the delivery fee.

    Expected JSON payload:
    {
        "cart_value": float,
        "delivery_distance": float,
        "number_of_items": int,
        "time": str
    }

    Returns:
    JSON response containing the calculated delivery fee.
    """

    #Check for errors in the request payload by checking for KeyError
    try:
        values = request.get_json()
        cart_value = values['cart_value']
        delivery_distance = values['delivery_distance']
        number_of_items = values['number_of_items']
        time = values['time']

    #Return error response if payload is invalid
    except KeyError:
        return app.response_class(response="error: Invalid request format",
                                  status=400,)
    
    #Calculate delivery fee with fee.py
    delivery_fee = fee.DeliveryFee(values['cart_value'],
                                  values['delivery_distance'],
                                  values['number_of_items'],
                                  values['time'])
    

    response = app.response_class(response=json.dumps({"delivery_fee":delivery_fee.total_fee()}),
                                  status=200,
                                  mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)