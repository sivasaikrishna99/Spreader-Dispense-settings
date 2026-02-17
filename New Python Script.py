import streamlit as st

st.set_page_config(page_title="Agri Drone Spreading Calculator", layout="centered")
st.title("🚁 Spreader settings")

st.caption("Includes valve setting & PWM reference mapping")

st.divider()

# -----------------------
# Constants
# -----------------------
TURN_LOSS = 0.02
ACRE_M2 = 4046.86

# -----------------------
# Reference Tables
# -----------------------

# Discharge rate reference (kg/min)
DISCHARGE_TABLE = {
    30: 10.0,
    25: 8.0  # Placeholder (update later when tested)
}

# Swath width reference (PWM : width in meters)
SWATH_TABLE = {
    1500: 7.5,
    1750: 10.5
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

# -----------------------
# Conditional Settings
# -----------------------

if material == "DAP":
    valve_setting = 30
    pwm_setting = 1500
else:
    valve_setting = st.selectbox(
        "Spreader Valve Open Setting (%)",
        [30, 25]
    )

    pwm_setting = st.selectbox(
        "PWM Setting",
        [1500, 1750]
    )

# Fetch mapped values
discharge_rate = DISCHARGE_TABLE[valve_setting]
swath_width = SWATH_TABLE[pwm_setting]

st.divider()

# -----------------------
# Calculations
# -----------------------

# Real area fixed at 1 acre
A_real = 1.0

# Ideal area considering turn loss
A_ideal = A_real / ((1 - TURN_LOSS) ** turns)

# Spray time (seconds)
t_spray = (dispense / discharge_rate) * 60

# Required speed (m/s)
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
    "Discharge & Swath derived from reference settings."
)
