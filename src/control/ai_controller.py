from src.physics.rack import (
    CP_LIQ, CP_AIR, DT_LIQ, 
    MDOT_LIQ_MAX, MDOT_AIR_MAX
)

class AIController:
    def decide(self, T_rack, Q_IT, wind_share, price, ambient_temp):
        Q_ancillary = 6.0 
        Q_high_power = max(0, Q_IT - Q_ancillary)

        MAX_EXHAUST_TEMP = 45.0
        available_dt_air = max(5.0, MAX_EXHAUST_TEMP - ambient_temp)
        mdot_air_min = Q_ancillary / (CP_AIR * available_dt_air)
        
        IS_PRICE_SPIKE = (price > 0.35)

        target_temp = 20.0 + ((Q_IT / 80.0) * 6.0)
        target_temp = max(18.0, min(target_temp, 26.0))

        high_load_factor = 1.0 + (max(0, Q_IT - 50.0) / 100.0) 

        if Q_IT < 30.0:
            low_load_boost = 1.5
        else:
            low_load_boost = 1.0

        if T_rack > target_temp + 0.5:
            temp_mod = 1.20  # Stronger reaction to rising temp
        elif T_rack < target_temp - 0.5:
            temp_mod = 0.90
        else:
            temp_mod = (0.95 if IS_PRICE_SPIKE else 1.0)

        # Calculate base thermal requirement
        Q_high_power_target = Q_high_power * high_load_factor * low_load_boost * temp_mod

        # --- Calculate Liquid Flow ---
        if IS_PRICE_SPIKE:
            mdot_liq = Q_high_power_target / (CP_LIQ * DT_LIQ)
            mdot_air = mdot_air_min
        elif wind_share < 0.5:
            mdot_liq = (Q_high_power_target * 0.8) / (CP_LIQ * DT_LIQ)
            extra_air_q = Q_high_power_target * 0.2
            mdot_air = mdot_air_min + (extra_air_q / (CP_AIR * available_dt_air))
        else:
            mdot_liq = Q_high_power_target / (CP_LIQ * DT_LIQ)
            mdot_air = mdot_air_min
        

        MIN_FLOW_LIQ = MDOT_LIQ_MAX * 0.25
        
        mdot_liq = max(MIN_FLOW_LIQ, min(mdot_liq, MDOT_LIQ_MAX))
        mdot_air = max(0, min(mdot_air, MDOT_AIR_MAX))

        return mdot_liq, mdot_air