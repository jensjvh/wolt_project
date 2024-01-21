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

    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)