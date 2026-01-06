from src.physics.rack import Rack
from src.control.ai_controller import AIController
from src.scenario.scenario_manager import ScenarioManager
from src.simulation.logger import Logger
from src.simulation.config import SIM_DURATION

def run_simulation_simple():

    rack = Rack()
    ai = AIController()
    scenario = ScenarioManager()
    logger = Logger()

    for t in range(SIM_DURATION):

        scenario.update(t)

        mdot_liq, mdot_air = ai.decide(
            T_rack=rack.T,
            Q_IT=scenario.Q_IT,
            wind_share=scenario.wind_share,
            price=scenario.price,
            ambient_temp=scenario.ambient
        )

        state = rack.step(
            Q_IT=scenario.Q_IT,
            mdot_liq=mdot_liq,
            mdot_air=mdot_air
        )

        logger.log(t, scenario.Q_IT, mdot_liq, mdot_air, state["T_rack"])

    return logger.get()
