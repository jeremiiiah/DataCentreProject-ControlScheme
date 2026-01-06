import streamlit as st

#model saftey
try:
    from src.physics.rack import Rack
    from src.control.ai_controller import AIController
except Exception as e:
    # If imports fail, show the error instead of a black screen
    st.set_page_config(page_title="AI Cooling Dashboard - Import Error", layout="wide")
    st.title("❌ Import error in dashboard.py")
    st.write("I couldn't import Rack or AIController. Check your src/ structure.")
    st.exception(e)
    st.stop()


#  Session helpers 

def init_state():
    """Initialise all simulation state the first time the app runs."""
    if "initialised" in st.session_state:
        return

    st.session_state.rack = Rack(T_init=25.0)
    st.session_state.ai = AIController()

    st.session_state.t = 0  # time in seconds

    # Scenario variables
    st.session_state.Q_IT = 50.0          # kW
    st.session_state.ambient = 18.0       # °C
    st.session_state.price_standard = 0.20      # €/kWh
    st.session_state.price_adjusted = 0.20      # €/kWh 
    st.session_state.wind_share = 0.8     # fraction 0–1

    # results hisotry
    st.session_state.history = []

    st.session_state.initialised = True


def step_simulation(n_steps: int = 1):
    """advance the simulation forward n_steps seconds."""
    rack = st.session_state.rack
    ai = st.session_state.ai

    for _ in range(n_steps):
        mdot_liq, mdot_air = ai.decide(
            T_rack=rack.T,
            Q_IT=st.session_state.Q_IT,
            wind_share=st.session_state.wind_share,
            price=st.session_state.price_adjusted,
            ambient_temp=st.session_state.ambient,
        )

        state = rack.step(
            Q_IT=st.session_state.Q_IT,
            mdot_liq=mdot_liq,
            mdot_air=mdot_air,
            ambient_temp=st.session_state.ambient,  
        )

        st.session_state.t += 1

        st.session_state.t += 1

        # Log one row of history
        st.session_state.history.append(
            {
                "t": st.session_state.t,
                "T_rack": round(state["T_rack"], 3),
                "Q_IT": st.session_state.Q_IT,
                "mdot_liq": round(mdot_liq, 4),
                "mdot_air": round(mdot_air, 4),
                "price_standard": st.session_state.price_standard,
                "price_adjusted": st.session_state.price_adjusted,
                "ambient": st.session_state.ambient,
                "wind_share": st.session_state.wind_share,
            }
        )


# Main GUI------------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="AI Cooling Control Dashboard", layout="wide")
    init_state()

    # Clean styling for metrics
    st.markdown("""<style>div[data-testid="stMetric"] {border: 1px solid rgba(49, 51, 63, 0.1); border-radius: 0.5rem; padding: 1rem;}</style>""", unsafe_allow_html=True)

    st.title("AI Data Centre Cooling – Control Dashboard")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("Simulation Control")
        step_size = st.selectbox("Step Size (seconds)", options=[1, 5, 10, 30], index=1)
        if st.button("▶ Step Simulation", key="step_btn", use_container_width=True):
            step_simulation(n_steps=int(step_size))

        st.markdown("---")
        with st.expander("🌡️ Environmental Factors", expanded=True):
            st.session_state.Q_IT = st.slider("Total Rack Thermal Load (kW)", 10.0, 100.0, float(st.session_state.Q_IT))
            st.session_state.ambient = st.slider("Ambient Temperature (°C)", -5.0, 40.0, float(st.session_state.ambient))
            st.session_state.wind_share = st.slider("Renewable Wind Share", 0.0, 1.0, float(st.session_state.wind_share))

        with st.expander("💸 Economic Factors"):
            st.session_state.price_standard = st.slider("Standard Grid Price (€/kWh)", 0.05, 0.80, float(st.session_state.price_standard))
            st.session_state.price_adjusted = st.slider("Test Price (€/kWh)", 0.05, 1.00, float(st.session_state.price_adjusted))

        st.markdown("---")
        st.subheader("Quick Disturbances")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("IT +10 kW", key="spike_it"): st.session_state.Q_IT += 10.0
        with c2:
            if st.button("Set Amb 5°C", key="set_cold"): st.session_state.ambient = 5.0
        
        if st.button("Reset All Data", key="reset_btn", use_container_width=True):
            for key in list(st.session_state.keys()): del st.session_state[key]
            init_state()
            st.rerun()

    # --- DYNAMIC STATUS BANNER ---
    curr_t = st.session_state.rack.T
    curr_p = st.session_state.price_adjusted
    if curr_t > 26.0:
        st.warning(f"⚠️ High Thermal Load ({curr_t:.2f}°C): AI Increasing Cooling Response.")
    elif curr_p > 0.35:
        st.info(f"♻️ Energy Recovery Mode: AI Throttling cooling power to optimize costs (€{curr_p:.2f}/kWh).")
    elif 24.0 <= curr_t <= 26.0:
        st.success("✅ Nominal Operation: System running within optimized thermal band (24-26°C).")
    else:
        st.info("❄️ Optimization Active: AI reducing flow to return to target 25°C range.")

    # --- KPI METRICS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Thermal State")
        st.metric("T_cpu (°C)", f"{curr_t:.2f}", delta=f"{curr_t - 25.0:.2f} vs Target", delta_color="inverse")
    with col2:
        st.subheader("Cooling Flows (kg/s)")
        if st.session_state.history:
            last = st.session_state.history[-1]
            st.metric("Liquid (GPU/CPU)", f"{last['mdot_liq']:.4f}")
            st.metric("Air (Ancillary)", f"{last['mdot_air']:.4f}")
    with col3:
        st.subheader("External Conditions")
        status = "SUSTAINABLE" if st.session_state.wind_share > 0.5 else "GRID-HEAVY"
        st.metric("Grid Status", status, delta=f"{st.session_state.wind_share*100:.0f}% Wind")

    st.markdown("---")

    # --- ANALYSIS CHARTS ---
    if st.session_state.history:
        st.subheader("📊 Thermal Performance & Cooling Response")
        h = st.session_state.history
        chart_data = {
            "Time (s)": [x["t"] for x in h],
            "Rack Temp (°C)": [x["T_rack"] for x in h],
            "IT Load (kW)": [x["Q_IT"] for x in h],
            "Liquid Flow (kg/s)": [x["mdot_liq"] for x in h],
            "Air Flow (kg/s)": [x["mdot_air"] for x in h]
        }
        pc1, pc2 = st.columns(2)
        with pc1: st.line_chart(data=chart_data, x="Time (s)", y=["Rack Temp (°C)", "IT Load (kW)"])
        with pc2: st.line_chart(data=chart_data, x="Time (s)", y=["Liquid Flow (kg/s)", "Air Flow (kg/s)"])

    # --- TELEMETRY LOG ---
    with st.expander("📜 View Raw Telemetry History"):
        if st.session_state.history: st.table(st.session_state.history[-15:])

if __name__ == "__main__":
    main()
