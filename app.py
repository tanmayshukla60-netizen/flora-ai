import streamlit as st
from model import PlantRecommendationModel
from serial_reader import read_sensor_data

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Flora AI",
    page_icon="🌱",
    layout="centered"
)

# =========================================================
# GLOBAL STYLE
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* ── Base ── */
.stApp {
    background: #0d1117;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    position: relative;
    overflow: hidden;
    background: #111a14;
    border: 0.5px solid #1e3326;
    border-radius: 20px;
    padding: 28px 24px 22px;
    margin-bottom: 18px;
    color: white;
}
.hero-watermark {
    position: absolute;
    top: -18px; right: -18px;
    font-size: 130px;
    opacity: 0.05;
    pointer-events: none;
    line-height: 1;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(74,222,128,0.08);
    border: 0.5px solid rgba(74,222,128,0.2);
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 14px;
}
.hero-pulse {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
.hero h1 {
    margin: 0 0 5px;
    font-size: 28px;
    font-weight: 600;
    color: #e8f5ee;
    letter-spacing: -0.3px;
}
.hero p {
    margin: 0;
    font-size: 14px;
    color: rgba(255,255,255,0.38);
    line-height: 1.5;
}

/* ── Hero stat strip ── */
.hero-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 18px;
}
.hero-stat {
    background: rgba(255,255,255,0.04);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px 14px;
}
.hero-stat .val {
    font-size: 19px;
    font-weight: 600;
    color: #c8e6c9;
}
.hero-stat .lbl {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    margin-top: 2px;
}

/* ── Eco pills row ── */
.eco-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.eco-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(45,106,79,0.2);
    border: 0.5px solid rgba(45,106,79,0.4);
    border-radius: 20px;
    padding: 5px 13px;
    font-size: 12px;
    color: #6fcf97;
    font-weight: 500;
}
.eco-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
}

/* ── Section cards ── */
.card {
    background: #111a14;
    border: 0.5px solid #1e3326;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: none;
}

/* ── Card header ── */
.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}
.card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: rgba(45,106,79,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
}
.card-title {
    font-size: 15px;
    font-weight: 600;
    color: #c8e6c9;
    margin-bottom: 2px;
}
.card-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.35);
}

/* ── Sensor display cards ── */
.sensor-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 14px;
}
.sensor-card {
    background: #0d1a10;
    border: 0.5px solid #1e3326;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}
.sensor-val {
    font-size: 26px;
    font-weight: 600;
    color: #a5d6a7;
    line-height: 1;
    margin-bottom: 4px;
}
.sensor-unit {
    font-size: 13px;
    color: rgba(255,255,255,0.3);
    font-weight: 400;
}
.sensor-lbl {
    font-size: 12px;
    color: rgba(255,255,255,0.3);
    margin-top: 3px;
}

/* ── Custom selectbox ── */
.stSelectbox > div > div {
    border-radius: 10px !important;
    border-color: #2d5a3d !important;
    background: #0d1a10 !important;
    color: #a5d6a7 !important;
}

/* ── Sliders ── */
.stSlider > div > div > div > div {
    background: #2d6a4f !important;
}
.stSlider [data-baseweb="slider"] {
    padding-top: 4px;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: #1e3d2a !important;
    color: #a5d6a7 !important;
    border-radius: 12px !important;
    padding: 13px 20px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border: 0.5px solid #2d6a4f !important;
    letter-spacing: 0.1px;
    transition: background 0.15s, transform 0.1s;
}
div[data-testid="stButton"] > button:hover {
    background: #243f2f !important;
    transform: translateY(-1px);
}
div[data-testid="stButton"] > button:active {
    transform: scale(0.98);
}

/* ── Result box ── */
.result-box {
    background: #0d1a10;
    border: 0.5px solid #2d5a3d;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    margin-top: 14px;
    animation: fadeSlide 0.35s ease;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0);   }
}
.result-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 6px;
}
.result-plant {
    font-size: 28px;
    font-weight: 600;
    color: #c8e6c9;
    margin-bottom: 6px;
    letter-spacing: -0.3px;
}
.result-desc {
    font-size: 13px;
    color: rgba(255,255,255,0.38);
    margin-bottom: 14px;
    line-height: 1.5;
}
.result-pills {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
}
.result-pill {
    background: rgba(45,106,79,0.2);
    border: 0.5px solid #2d5a3d;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #6fcf97;
    font-weight: 500;
}

/* ── Success/info messages ── */
.stSuccess {
    border-radius: 12px !important;
    border-left-color: #2d6a4f !important;
    background: #0d1a10 !important;
    color: #a5d6a7 !important;
}
.stError {
    border-radius: 12px !important;
    background: #1a0d0d !important;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 0.5px solid #1e3326;
    margin: 4px 0 16px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 12px;
    color: rgba(255,255,255,0.2);
    margin-top: 24px;
    padding-top: 16px;
    border-top: 0.5px solid #1a2a1e;
}
.footer a { color: #4ade80; text-decoration: none; }

/* ── Slider label text ── */
.stSlider label, .stSlider p {
    color: rgba(255,255,255,0.5) !important;
}

/* ── General text ── */
.stMarkdown p {
    color: rgba(255,255,255,0.6);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MODEL
# =========================================================
if "model" not in st.session_state:
    st.session_state.model = PlantRecommendationModel()

model = st.session_state.model


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-watermark">🌿</div>
    <div class="hero-badge">
        <span class="hero-pulse"></span>
        IoT + Machine Learning
    </div>
    <h1>🌱 Flora AI</h1>
    <p>Smart plant recommendation — live sensor data meets intelligent prediction</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="val">50+</div>
            <div class="lbl">Plant species</div>
        </div>
        <div class="hero-stat">
            <div class="val">97%</div>
            <div class="lbl">Accuracy</div>
        </div>
        <div class="hero-stat">
            <div class="val">Live</div>
            <div class="lbl">Sensor feed</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# ECO PILLS
# =========================================================
st.markdown("""
<div class="eco-strip">
    <span class="eco-pill"><span class="eco-dot"></span>Sustainable AI</span>
    <span class="eco-pill"><span class="eco-dot"></span>IoT-enabled</span>
    <span class="eco-pill"><span class="eco-dot"></span>Final year project</span>
    <span class="eco-pill"><span class="eco-dot"></span>Eco-smart farming</span>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DATA SOURCE CARD
# =========================================================
st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="card-icon">📡</div>
        <div>
            <div class="card-title">Data source</div>
            <div class="card-sub">Choose how to supply environmental readings</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

mode = st.selectbox("", ["Manual Input", "Live Arduino Sensor"], label_visibility="collapsed")


# =========================================================
# DEFAULTS
# =========================================================
st.session_state.setdefault("temp", 25.0)
st.session_state.setdefault("moist", 500)


# =========================================================
# INPUT CARD
# =========================================================
st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="card-icon">🌡️</div>
        <div>
            <div class="card-title">Environmental readings</div>
            <div class="card-sub">Current temperature and soil moisture levels</div>
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

if mode == "Live Arduino Sensor":
    st.write("Click below to fetch real-time sensor data from your Arduino")
    if st.button("📡 Read Live Sensor"):
        temp, moist = read_sensor_data()
        if temp is not None:
            st.session_state.temp = temp
            st.session_state.moist = moist
            st.success(f"✅  Sensor updated — {temp} °C  |  Moisture: {moist}")
        else:
            st.error("⚠️  Sensor not detected. Check your connection and try again.")

else:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.temp = st.slider(
            "🌡️ Temperature (°C)",
            0.0, 50.0,
            st.session_state.temp,
            0.5
        )
    with col2:
        st.session_state.moist = st.slider(
            "💧 Soil Moisture",
            0, 1023,
            int(st.session_state.moist),
            5
        )

# Live display cards
st.markdown(f"""
<div class="sensor-grid">
    <div class="sensor-card">
        <div class="sensor-val">{st.session_state.temp:.1f}<span class="sensor-unit"> °C</span></div>
        <div class="sensor-lbl">Temperature</div>
    </div>
    <div class="sensor-card">
        <div class="sensor-val">{int(st.session_state.moist)}<span class="sensor-unit"> raw</span></div>
        <div class="sensor-lbl">Soil moisture</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PREDICTION CARD
# =========================================================
st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="card-icon">🌿</div>
        <div>
            <div class="card-title">Recommendation engine</div>
            <div class="card-sub">ML model predicts the best plant for your environment</div>
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

if st.button("🌱 Find Best Plant"):
    plant = model.predict(st.session_state.temp, st.session_state.moist)

    # Determine moisture label
    m = int(st.session_state.moist)
    if m < 300:
        moist_label = "Dry soil"
    elif m < 600:
        moist_label = "Moderate moisture"
    else:
        moist_label = "High moisture"

    st.markdown(f"""
    <div class="result-box">
        <div style="font-size:36px;margin-bottom:8px;">🌱</div>
        <div class="result-eyebrow">Recommended plant</div>
        <div class="result-plant">{plant}</div>
        <div class="result-desc">
            Optimal for your current conditions — adapt watering and light as needed.
        </div>
        <div class="result-pills">
            <span class="result-pill">🌡️ {st.session_state.temp:.1f} °C</span>
            <span class="result-pill">💧 {moist_label}</span>
            <span class="result-pill">✅ ML matched</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    🌍 Flora AI &nbsp;·&nbsp; IoT + Machine Learning &nbsp;·&nbsp; Final Year Project<br>
    <span style="font-size:11px;opacity:0.7;">Building smarter, greener environments — one plant at a time</span>
</div>
""", unsafe_allow_html=True)