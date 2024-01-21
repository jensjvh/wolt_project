import datetime

class DeliveryFee():
    """
    A class for handling all the data in the request payload.
    Used for calculating the total fee in cents.

    Parameters
    ----------
    cart_value : int
        Value of the shopping cart in cents.
    distance : int
        The distance between the store and customer's location in meters.
    no_of_items : int
        The number of items in the customer's shopping cart.
    time : str
        Order time in UTC in ISO format.
    """

    #Constants as class attributes
    max_cart_value = 20000
    max_total_fee = 1500
    
    def __init__(self, cart_value: int,
                 distance: int,
                 no_of_items: int,
                 time: str):
        self._cart_value = cart_value
        self._distance = distance
        self._no_of_items = no_of_items
        self._time = time
        self._delivery_fee = 0 #Variable to keep track of delivery fee
        self._surcharge = 0 #Variable to keep track of surcharge
        self._total_fee = 0