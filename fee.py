from math import ceil
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

    def check_cart_value(self):
        if self._cart_value < 1000:
            self._surcharge += abs(1000-self._cart_value)
    
    def check_distance(self):
        #Add 2 euros as the initial distance cost
        self._delivery_fee += 200

        if self._distance > 1000:
            remaining = self._distance - 1000
            self._delivery_fee += ceil(remaining/500)*100
    
    def check_items(self):
        if self._no_of_items >= 5:
            remaining = self._no_of_items - 4
            self._surcharge += remaining * 50

            if self._no_of_items > 12:
                self._surcharge += 120

    def check_time(self):
        time = self._time.strip("Z")

        time = datetime.datetime.fromisoformat(time)

        rush_start, rush_end = datetime.time(15, 0, 0), datetime.time(19, 0, 0)

        #Check if the day is a Friday and if the time.time() part 
        if datetime.datetime.weekday(time) == 4:
            if time.time() >= rush_start and time.time() < rush_end:
                self._total_fee *= 1.2

    def total_fee(self):
        #Check if cart value is greater than 200 euros
        if self._cart_value >=   DeliveryFee.max_cart_value:
            return 0
        
        #Run checks for cart value, distance, and item count
        self.check_cart_value()
        self.check_distance()
        self.check_items()

        self._total_fee = self._delivery_fee + self._surcharge
    
        #Check for Friday rush hour
        self.check_time()

        #Return 1500 if total is greater
        return min(DeliveryFee.max_total_fee, int(self._total_fee))