import streamlit as st

st.set_page_config(page_title="Agri Drone Spreading Calculator", layout="centered")
st.title("🚁 Spreader dispense settings")
st.caption("Automatic configuration based on material selection")

st.divider()

# -----------------------
# Constants
# -----------------------
TURN_LOSS = 0.02
ACRE_M2 = 4046.86

# Reference tables
DISCHARGE_TABLE = {
    30: 10.0  # 30% valve → 10 kg/min
}

SWATH_TABLE = {
    1500: 7.5  # 1500 PWM → 7.5 m
}

# -----------------------
# Inputs
# -----------------------

material = st.selectbox(
    "Spreading Material",
    ["Urea", "DAP", "Potash"]
)

dispense = st.number_input(
    "Total dispense weight per acre (kg)",
    min_value=1.0,
    max_value=200.0,
    value=25.0,
    step=1.0
)

turns = st.number_input(
    "Number of turns (N)",
    min_value=0,
    max_value=200,
    value=12,
    step=1
)

st.divider()

# -----------------------
# Automatic Configuration
# -----------------------

# Default settings (currently same for all materials)
# DAP explicitly fixed per your requirement
valve_setting = 30
pwm_setting = 1500

discharge_rate = DISCHARGE_TABLE[valve_setting]
swath_width = SWATH_TABLE[pwm_setting]

# -----------------------
# Calculations
# -----------------------

A_real = 1.0
A_ideal = A_real / ((1 - TURN_LOSS) ** turns)

t_spray = (dispense / discharge_rate) * 60

v_required = (A_ideal * ACRE_M2) / (swath_width * t_spray)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

st.metric("Required Speed (m/s)", f"{v_required:.3f}")
st.metric("Valve Open Setting (%)", f"{valve_setting}%")
st.metric("PWM Setting", f"{pwm_setting}")

st.caption(
    "Model:\n"
    "1 acre = A_ideal × (1 - 0.02)^N\n"
    "Speed = (A_ideal × 4046.86) / (Swath × SprayTime)\n\n"
    "Valve & PWM auto-configured for selected material."
)
