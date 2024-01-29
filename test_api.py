import json
import pytest
import fee
from flask.testing import FlaskClient
from api import app

@pytest.fixture
def client():
    return app.test_client()

def test_api_correct_value(client: FlaskClient):
    """
    Test for checking that the API returns the correct value for inputs
    """
    payload = {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'delivery_fee' in data
    assert data['delivery_fee'] == 710

def test_api_valid_request(client: FlaskClient):
    payload = {
        "cart_value": 1000,
        "delivery_distance": 1500,
        "number_of_items": 3,
        "time": "2024-01-21T12:00:00Z"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'delivery_fee' in data

def test_api_invalid_request(client: FlaskClient):
    # Send an invalid request with a missing key
    payload = {
        "cart_value": 1000,
        "delivery_distance": 1500,
        "number_of_items": 3,
        # 'time' key is missing
    }

    response = client.post('/', json=payload)

    assert response.status_code == 400
    assert b"error: Invalid request format" in response.data

def test_negative_values(client: FlaskClient):
    #Test for response with status code 400 if any of the values is negative
    payload = {
        "cart_value": -3,
        "delivery_distance": 1500,
        "number_of_items": 3,
        "time": "2024-01-21T12:00:00Z"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 400
    assert b"error: Invalid request format" in response.data

def test_invalid_time(client: FlaskClient):
    #Test for response with status code 400 if time format is invalid
    payload = {
        "cart_value": 4,
        "delivery_distance": 1500,
        "number_of_items": 3,
        #Z is missing
        "time": "2024-01-21T12:00:00"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 400
    assert b"error: Invalid request format" in response.data

def test_api_maximum_cart_value(client: FlaskClient):
    # Test when the cart value exceeds 200 euros
    payload = {
        "cart_value": 25000,
        "delivery_distance": 1500,
        "number_of_items": 3,
        "time": "2024-01-21T12:00:00Z"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'delivery_fee' in data
    assert data['delivery_fee'] == 0  # Assuming that the delivery fee is set to 0 when cart value exceeds 200

def test_api_rush_hour_discount(client: FlaskClient):
    # Test applying rush hour discount
    payload = {
        "cart_value": 1000,
        "delivery_distance": 1500,
        "number_of_items": 3,
        "time": "2024-01-19T18:00:00Z"  # Time set to be within the Friday rush period
    }

    response = client.post('/', json=payload)

    calculated_fee = fee.DeliveryFee(payload["cart_value"],
                             payload["delivery_distance"],
                             payload["number_of_items"],
                             payload["time"])
    
    #Execute the calculation
    calculated_fee.total_fee()

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'delivery_fee' in data
    # Assuming that the rush hour discount multiplies the delivery fee by 1.2
    assert data['delivery_fee'] == 1.2 * (calculated_fee.delivery_fee + calculated_fee.surcharge)

def test_api_maximum_total_fee(client: FlaskClient):
    # Test if the total fee is correctly limited to 15 euros
    payload = {
        "cart_value": 10000,
        "delivery_distance": 15000,
        "number_of_items": 20,
        "time": "2024-01-21T12:00:00Z"
    }

    response = client.post('/', json=payload)

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'delivery_fee' in data
    assert data['delivery_fee'] == 1500  # Assuming that the total fee is capped at 1500
