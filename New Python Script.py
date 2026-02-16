import streamlit as st

st.set_page_config(page_title="Agri Drone Speed Calculator", layout="centered")
st.title("🚁 Drone Speed Required for 1 Acre Coverage")
st.caption("Fixed 2% loss per turn | Flow = 10 kg/min | Swath = 7.5 m")

st.divider()

# -----------------------
# Constants
# -----------------------
FLOW = 10.0          # kg/min
SWATH = 7.5          # meters
TURN_LOSS = 0.02     # 2%
ACRE_M2 = 4046.86    # 1 acre in m²

# -----------------------
# Inputs
# -----------------------
dispense = st.number_input(
    "Total dispense weight per acre (kg)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=0.5
)

N = st.number_input(
    "Number of turns (N)",
    min_value=0,
    max_value=200,
    value=12,
    step=1
)

st.divider()

# -----------------------
# Calculations
# -----------------------

# Real area fixed at 1 acre
A_real = 1.0

# Ideal area required
A_ideal = A_real / ((1 - TURN_LOSS) ** N)

# Spray time (seconds)
t_spray = (dispense / FLOW) * 60

# Required speed (m/s)
v_required = (A_ideal * ACRE_M2) / (SWATH * t_spray)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Result")

st.metric("Required Speed (m/s)", f"{v_required:.3f}")

st.caption(
    "Model used:\n"
    "1 acre = A_ideal × (0.98)^N\n"
    "Speed = (A_ideal × 4046.86) / (Swath × SprayTime)"
)
