import streamlit as st

st.set_page_config(page_title="Agri Drone Speed Calculator", layout="centered")
st.title("🚁 Drone Speed Required for 1 Acre Coverage")
st.caption("Fixed 2% turn loss | 1 Acre Coverage Model")

st.divider()

# -----------------------
# Constants
# -----------------------
FLOW = 10.0          # kg/min (constant)
SWATH = 7.5          # meters (constant)
TURN_LOSS = 0.02     # 2% per turn
ACRE_M2 = 4046.86    # 1 acre in m²

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

# Ideal area needed considering turn loss
A_ideal = A_real / ((1 - TURN_LOSS) ** N)

# Spray time (seconds)
t_spray = (dispense / FLOW) * 60

# Required speed (m/s)
v_required = (A_ideal * ACRE_M2) / (SWATH * t_spray)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Required Speed (m/s)", f"{v_required:.3f}")
    st.metric("Required Speed (km/h)", f"{v_required * 3.6:.2f}")

with c2:
    st.metric("Flow Rate (kg/min)", f"{FLOW}")
    st.metric("Swath Width (m)", f"{SWATH}")

st.caption(
    "Model used:\n"
    "1 acre = A_ideal × (0.98)^N\n"
    "Speed = (A_ideal × 4046.86) / (Swath × SprayTime)\n\n"
    "Turn loss fixed at 2% per turn."
)
