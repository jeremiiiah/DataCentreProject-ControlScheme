from src.scenario import profiles

class ScenarioManager:
    def __init__(self):
        self.Q_IT = 50.0
        self.ambient = 18.0
        self.price = 0.2
        self.adjusted_price = 0.2
        self.wind_share = 0.8

    def update(self, t):
        self.Q_IT = profiles.base_IT_profile(t)
        self.ambient = profiles.base_weather_profile(t)
        self.price = profiles.base_price_profile(t)
