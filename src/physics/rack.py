# Updated constants 
CP_LIQ = 3.875     # kJ/kgK (Water/30% Propylene Glycol) 
CP_AIR = 1.005     # kJ/kgK 

DT_LIQ = 5.0       # °C (Fixed rise for liquid loop) 

# Max flow rates 
MDOT_LIQ_MAX = 2.466   # kg/s 
MDOT_AIR_MAX = 0.272   # kg/s

# Thermal capacitance
# lowered for responsiveness
C_TH = 500.0        # kJ/°C 
DT = 1.0           # seconds

class Rack:
    def __init__(self, T_init=25.0):
        self.T = T_init

    def step(self, Q_IT, mdot_liq, mdot_air, ambient_temp):
        Q_liq = mdot_liq * CP_LIQ * DT_LIQ

        actual_dt_air = max(0, self.T - ambient_temp)
        Q_air = mdot_air * CP_AIR * actual_dt_air

        Q_cool_total = Q_liq + Q_air

        dTdt = (Q_IT - Q_cool_total) / C_TH
        self.T += dTdt * DT

        return {
            "T_rack": self.T,
            "Q_liq": Q_liq,
            "Q_air": Q_air,
            "Q_cool_total": Q_cool_total
        }