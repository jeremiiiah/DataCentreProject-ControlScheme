from src.simulation.loop import run_simulation_simple

if __name__ == "__main__":
    print("Starting AI Cooling System Simulation...")
    history = run_simulation_simple()

    print("\n--- FINAL OUTPUT ---")
    for entry in history[-10:]:
        t, Q_IT, mdot_liq, mdot_air, T = entry
        print(f"t={t:4d}s | Q_IT={Q_IT:5.1f} kW | "
              f"m_liq={mdot_liq:.3f} kg/s | m_air={mdot_air:.3f} kg/s | "
              f"T_cpu={T:.2f} °C")
