def it_spike(current_Q, amount=10):
    return current_Q + amount

def cold_weather_event():
    return 5.0   # °C

def price_spike(current_price, factor=2.0):
    return current_price * factor
