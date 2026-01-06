class Logger:
    def __init__(self):
        self.data = []

    def log(self, t, Q_IT, mdot_liq, mdot_air, T_rack):
        self.data.append((t, Q_IT, mdot_liq, mdot_air, T_rack))

    def get(self):
        return self.data