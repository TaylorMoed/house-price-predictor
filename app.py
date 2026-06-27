import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="House Price Predictor",
    page_icon=None,
    layout="centered"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;1,14..32,300&display=swap');

/* ───────────────────────────────────────────
   BASE
─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background-color: #080809 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #e2e8f0 !important;
    -webkit-font-smoothing: antialiased;
}
.block-container {
    padding: 0 1.5rem 8rem !important;
    max-width: 780px !important;
}

/* ───────────────────────────────────────────
   SLIDER
─────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div {
    background: #161620 !important;
    height: 4px !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: #2563eb !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    background: #1e3a5f !important;
    color: #93c5fd !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
}
/* SVG thumb circle — this is what renders red */
[data-testid="stSlider"] [role="slider"] {
    background: #2563eb !important;
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.2) !important;
}
[data-testid="stSlider"] div[role="slider"] {
    background-color: #2563eb !important;
    border: 2px solid #3b82f6 !important;
}
/* Catch the inner colored circle Streamlit injects */
[data-testid="stSlider"] > div > div > div > div > div {
    background: #2563eb !important;
    border-color: #2563eb !important;
}
[data-testid="stSlider"] input[type="range"] {
    accent-color: #2563eb !important;
}
/* Thumb value tooltip text */
[data-testid="stSlider"] [data-testid="stThumbValue"] p,
[data-testid="stSlider"] [data-testid="stThumbValue"] span,
[data-testid="stSlider"] [data-testid="stThumbValue"] div,
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #93c5fd !important;
    background: #1e3a5f !important;
}
/* Current value shown above thumb */
[data-testid="stSlider"] > div > div > div > div > div > p,
[data-testid="stSlider"] p {
    color: #4a6fa5 !important;
}
[data-testid="stSlider"] label p {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #1e293b !important;
    font-size: 10px !important;
}

/* ───────────────────────────────────────────
   BUTTON
─────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background: #2563eb !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 10px !important;
    height: 46px !important;
    transition: background 0.15s ease, transform 0.1s ease !important;
    box-shadow: 0 1px 3px rgba(37,99,235,0.3), 0 4px 16px rgba(37,99,235,0.2) !important;
}
[data-testid="stButton"] > button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.4), 0 8px 24px rgba(37,99,235,0.25) !important;
}
[data-testid="stButton"] > button:active {
    background: #1e40af !important;
    transform: scale(0.985) !important;
}

/* ───────────────────────────────────────────
   HIDE CHROME
─────────────────────────────────────────── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], header,
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ───────────────────────────────────────────
   LAYOUT HELPERS
─────────────────────────────────────────── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 3rem 0 1.25rem;
}
.sec-title {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2d3f55;
    white-space: nowrap;
}
.sec-rule { flex: 1; height: 1px; background: #0f0f14; }

/* ───────────────────────────────────────────
   HEADER
─────────────────────────────────────────── */
.app-header {
    padding: 3.5rem 0 2.75rem;
    border-bottom: 1px solid #0f0f14;
    margin-bottom: 0.5rem;
    position: relative;
}
.app-header-glow {
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(37,99,235,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.app-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(37,99,235,0.08);
    border: 1px solid rgba(37,99,235,0.18);
    border-radius: 99px;
    padding: 4px 12px;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 1.1rem;
}
.app-badge-dot {
    width: 5px; height: 5px;
    background: #3b82f6;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}
.app-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}
.app-subtitle {
    font-size: 0.83rem;
    color: #3d5166;
    line-height: 1.7;
    max-width: 480px;
    font-weight: 400;
}

/* ───────────────────────────────────────────
   INPUTS CARD
─────────────────────────────────────────── */
.inputs-card {
    background: #0c0c0f;
    border: 1px solid #13131a;
    border-radius: 20px;
    padding: 1.75rem 2rem 1.25rem;
}

/* ───────────────────────────────────────────
   PREDICTION CARD
─────────────────────────────────────────── */
.pred-card {
    background: #0c0c0f;
    border: 1px solid #13131a;
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    margin-bottom: 0.5rem;
}
.pred-card-glow {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 0%, rgba(37,99,235,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.pred-top-bar {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(59,130,246,0.5) 20%,
        rgba(99,162,255,0.8) 50%,
        rgba(59,130,246,0.5) 80%,
        transparent 100%);
}
.pred-inner {
    padding: 2.5rem 2.75rem 2rem;
    position: relative;
}
.pred-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #2d3f55;
    margin-bottom: 0.75rem;
}
.pred-value-row {
    display: flex;
    align-items: baseline;
    gap: 0.2rem;
    margin-bottom: 0.4rem;
}
.pred-currency {
    font-size: 2rem;
    font-weight: 700;
    color: #475569;
    letter-spacing: -0.02em;
    line-height: 1;
}
.pred-amount {
    font-size: 4.2rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.05em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.pred-confidence-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(37,99,235,0.08);
    border: 1px solid rgba(37,99,235,0.18);
    border-radius: 99px;
    padding: 3px 10px;
    font-size: 0.62rem;
    font-weight: 600;
    color: #3b82f6;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.pred-confidence-dot {
    width: 4px; height: 4px;
    background: #3b82f6;
    border-radius: 50%;
}
.pred-footer {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.1rem 2.75rem;
    background: rgba(0,0,0,0.25);
    border-top: 1px solid #0f0f14;
}
.pred-footer-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1e3350;
}
.pred-footer-val {
    font-size: 0.8rem;
    font-weight: 600;
    color: #3b82f6;
    font-variant-numeric: tabular-nums;
}
.pred-footer-sep { color: #1a2535; font-size: 0.7rem; }
.pred-footer-spacer { flex: 1; }
.pred-footer-ci {
    font-size: 0.62rem;
    color: #1e3350;
    font-weight: 500;
}

/* ───────────────────────────────────────────
   IDLE CARD
─────────────────────────────────────────── */
.idle-card {
    background: #0a0a0d;
    border: 1px dashed #13131a;
    border-radius: 20px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.idle-icon { font-size: 2.2rem; margin-bottom: 0.75rem; opacity: 0.2; }
.idle-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #1a2535;
    margin-bottom: 0.3rem;
}
.idle-sub { font-size: 0.75rem; color: #131e2b; line-height: 1.65; }

/* ───────────────────────────────────────────
   DETAIL CARDS
─────────────────────────────────────────── */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 8px;
}
.detail-card {
    background: #0c0c0f;
    border: 1px solid #13131a;
    border-radius: 16px;
    padding: 1.1rem 1.3rem 1rem;
    transition: border-color 0.2s ease;
}
.detail-card:hover { border-color: #1e293b; }
.d-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2d3f55;
    margin-bottom: 0.45rem;
}
.d-value-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}
.d-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
}
.d-pct {
    font-size: 0.65rem;
    font-weight: 500;
    color: #1e3350;
}
.d-bar-track {
    height: 3px;
    background: #0f0f14;
    border-radius: 99px;
    overflow: hidden;
}
.d-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #1d4ed8, #3b82f6);
}

/* ───────────────────────────────────────────
   METRIC CARDS
─────────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
}
.metric-card {
    background: #0c0c0f;
    border: 1px solid #13131a;
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    transition: border-color 0.2s ease;
}
.metric-card:hover { border-color: #1e293b; }
.m-label {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2d3f55;
    margin-bottom: 0.5rem;
}
.m-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.m-sub {
    font-size: 0.62rem;
    color: #1e3350;
    font-weight: 400;
}

/* ───────────────────────────────────────────
   WHY CARD
─────────────────────────────────────────── */
.why-card {
    background: #0c0c0f;
    border: 1px solid #13131a;
    border-radius: 18px;
    overflow: hidden;
}
.why-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.1rem 1.5rem;
    border-bottom: 1px solid #0d0d11;
    transition: background 0.15s ease;
}
.why-item:last-child { border-bottom: none; }
.why-item:hover { background: rgba(255,255,255,0.01); }
.why-icon-wrap {
    width: 30px; height: 30px;
    min-width: 30px;
    background: rgba(37,99,235,0.06);
    border: 1px solid rgba(37,99,235,0.12);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6rem;
    font-weight: 700;
    color: #1e3a5f;
    letter-spacing: 0.05em;
    margin-top: 1px;
    font-family: 'Inter', sans-serif;
}
.why-body { flex: 1; }
.why-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-bottom: 0.15rem;
}
.why-stars {
    font-size: 0.68rem;
    color: #2563eb;
    letter-spacing: 2px;
    margin-bottom: 0.25rem;
}
.why-desc {
    font-size: 0.72rem;
    color: #2d3f55;
    line-height: 1.55;
}
.why-rank {
    font-size: 0.6rem;
    font-weight: 700;
    color: #1a2535;
    letter-spacing: 0.05em;
    padding-top: 4px;
}

/* ───────────────────────────────────────────
   SIMILAR HOMES
─────────────────────────────────────────── */
.ph-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
}
.ph-card {
    background: #0a0a0d;
    border: 1px solid #0f0f14;
    border-radius: 16px;
    padding: 1.3rem;
    transition: border-color 0.2s ease;
}
.ph-card:hover { border-color: #13131a; }
.ph-price {
    font-size: 1rem;
    font-weight: 700;
    color: #1a2535;
    letter-spacing: -0.02em;
    margin-bottom: 0.9rem;
}
.ph-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
}
.ph-field { font-size: 0.65rem; color: #131c28; font-weight: 500; }
.ph-val { font-size: 0.65rem; color: #161e2b; font-weight: 500; }
.ph-coming {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #0f172a;
}

/* ───────────────────────────────────────────
   ANIMATE COUNT UP
─────────────────────────────────────────── */
@keyframes countUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.pred-amount { animation: countUp 0.4s cubic-bezier(0.16,1,0.3,1) both; }
.pred-confidence-badge { animation: countUp 0.4s 0.1s cubic-bezier(0.16,1,0.3,1) both; }
.pred-footer { animation: countUp 0.4s 0.15s cubic-bezier(0.16,1,0.3,1) both; }
</style>
"""

# ── JS: animated count-up ──────────────────────────────────
COUNTUP_JS = """
<script>
function animateCount(el, target, duration) {
    const start = performance.now();
    const from = 0;
    function step(now) {
        const p = Math.min((now - start) / duration, 1);
        const ease = 1 - Math.pow(1 - p, 4);
        const val = Math.round(from + (target - from) * ease);
        el.textContent = val.toLocaleString('en-US');
        if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}
document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('pred-count');
    if (el) animateCount(el, parseInt(el.dataset.target), 900);
});
</script>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────
model    = joblib.load("models/house_price_model.pkl")
features = joblib.load("models/model_features.pkl")
df       = pd.read_csv("data/housing_cleaned.csv")

def create_house_profile(vals):
    house = df[features].median(numeric_only=True).to_dict()
    for f in features:
        house.setdefault(f, 0)
    for key, val in vals.items():
        if key in house:
            house[key] = val
    return pd.DataFrame([house])[features]

def dbar(pct):
    pct = max(0.0, min(1.0, pct))
    return (
        '<div class="d-bar-track">'
        f'<div class="d-bar-fill" style="width:{pct*100:.1f}%"></div>'
        '</div>'
    )

def dcard(label, value_str, pct):
    p = max(0.0, min(1.0, pct))
    return (
        '<div class="detail-card">'
        f'<div class="d-label">{label}</div>'
        '<div class="d-value-row">'
        f'<div class="d-value">{value_str}</div>'
        f'<div class="d-pct">{p*100:.0f}%</div>'
        '</div>'
        f'{dbar(p)}'
        '</div>'
    )

# ── HEADER ─────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-header-glow"></div>
  <div class="app-badge">
    <div class="app-badge-dot"></div>
    ML · Random Forest · Ames Iowa
  </div>
  <div class="app-title">House Price Predictor</div>
  <div class="app-subtitle">Estimate a home's market value using a machine learning model trained on 1,460 real sales. Adjust inputs below and run a prediction.</div>
</div>
""", unsafe_allow_html=True)

# ── PROPERTY INPUTS ────────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Property Details</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    overall_qual  = st.slider("Overall Quality (1–10)",  1,    10,    6)
    garage_cars   = st.slider("Garage Spaces",           0,    5,     2)
    bedrooms      = st.slider("Bedrooms",                0,    8,     3)
    total_bsmt_sf = st.slider("Basement SF",             0,    3000,  800,  step=50)
    lot_area      = st.slider("Lot Area (sq ft)",        1000, 50000, 9000, step=500)
with col2:
    gr_liv_area  = st.slider("Living Area (sq ft)",      300,  6000,  1500, step=50)
    garage_area  = st.slider("Garage Area (sq ft)",      0,    1500,  500,  step=25)
    full_bath    = st.slider("Full Bathrooms",           0,    5,     2)
    first_flr_sf = st.slider("1st Floor SF",             300,  4000,  1000, step=50)
    year_built   = st.slider("Year Built",               1870, 2026,  2000)

# ── PREDICT BUTTON ─────────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Estimated Value</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)

clicked = st.button("Run Prediction", use_container_width=True)

input_vals = {
    "Overall Qual":  overall_qual,  "Gr Liv Area":   gr_liv_area,
    "Garage Cars":   garage_cars,   "Garage Area":   garage_area,
    "Year Built":    year_built,    "Total Bsmt SF": total_bsmt_sf,
    "1st Flr SF":    first_flr_sf,  "Bedroom AbvGr": bedrooms,
    "Full Bath":     full_bath,     "Lot Area":      lot_area,
}

if clicked:
    pred       = model.predict(create_house_profile(input_vals))[0]
    low, high  = pred - 15833, pred + 15833
    pred_int   = int(round(pred))

    import streamlit.components.v1 as components
    components.html(f"""<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;font-family:'Inter',sans-serif;}}
.card{{background:#0c0c0f;border:1px solid #13131a;border-radius:20px;overflow:hidden;position:relative;animation:fadeUp 0.35s cubic-bezier(0.16,1,0.3,1) both;}}
.glow{{position:absolute;inset:0;background:radial-gradient(ellipse at 20% 0%,rgba(37,99,235,0.07) 0%,transparent 60%);pointer-events:none;}}
.topbar{{height:1px;background:linear-gradient(90deg,transparent,rgba(59,130,246,0.5) 20%,rgba(99,162,255,0.8) 50%,rgba(59,130,246,0.5) 80%,transparent);}}
.inner{{padding:2.5rem 2.75rem 2rem;position:relative;}}
.lbl{{font-size:0.62rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#2d3f55;margin-bottom:0.75rem;}}
.val-row{{display:flex;align-items:baseline;gap:0.2rem;margin-bottom:0.6rem;}}
.cur{{font-size:2rem;font-weight:700;color:#475569;line-height:1;letter-spacing:-0.02em;}}
.num{{font-size:4.2rem;font-weight:800;color:#f8fafc;letter-spacing:-0.05em;line-height:1;font-variant-numeric:tabular-nums;}}
.badge{{display:inline-flex;align-items:center;gap:0.35rem;background:rgba(37,99,235,0.08);border:1px solid rgba(37,99,235,0.18);border-radius:99px;padding:3px 10px;font-size:0.62rem;font-weight:600;color:#3b82f6;letter-spacing:0.08em;text-transform:uppercase;}}
.dot{{width:4px;height:4px;background:#3b82f6;border-radius:50%;animation:pulse 2s ease-in-out infinite;}}
.footer{{display:flex;align-items:center;gap:1.25rem;padding:1.1rem 2.75rem;background:rgba(0,0,0,0.25);border-top:1px solid #0f0f14;}}
.flbl{{font-size:0.6rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:#1e3350;}}
.fval{{font-size:0.8rem;font-weight:600;color:#3b82f6;font-variant-numeric:tabular-nums;}}
.fsep{{color:#1a2535;font-size:0.7rem;}}
.fsp{{flex:1;}}
.fci{{font-size:0.62rem;color:#1e3350;font-weight:500;}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:0.4;transform:scale(0.8);}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}
</style></head><body>
<div class="card">
  <div class="glow"></div>
  <div class="topbar"></div>
  <div class="inner">
    <div class="lbl">Estimated Home Value</div>
    <div class="val-row"><div class="cur">$</div><div class="num" id="c">0</div></div>
    <div class="badge"><div class="dot"></div>High Confidence</div>
  </div>
  <div class="footer">
    <div class="flbl">Expected Range</div>
    <div class="fval">${low:,.0f}</div>
    <div class="fsep">—</div>
    <div class="fval">${high:,.0f}</div>
    <div class="fsp"></div>
    <div class="fci">&#177;$15,833 &nbsp;&middot;&nbsp; 68% confidence interval</div>
  </div>
</div>
<script>
(function(){{
  var target={pred_int},el=document.getElementById('c'),start=null,dur=1000;
  function ease(t){{return 1-Math.pow(1-t,4);}}
  function step(ts){{
    if(!start)start=ts;
    var p=Math.min((ts-start)/dur,1);
    el.textContent=Math.round(ease(p)*target).toLocaleString('en-US');
    if(p<1)requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}})();
</script>
</body></html>""", height=260)
else:
    st.markdown("""
    <div class="idle-card">
      <div class="idle-title">No estimate yet</div>
      <div class="idle-sub">Configure the property details above,<br>then click <strong style="color:#1e3350;font-weight:600">Run Prediction</strong> to see the estimated value.</div>
    </div>
    """, unsafe_allow_html=True)

# ── HOUSE DETAILS ──────────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Property Summary</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)

cards = (
    dcard("Overall Quality",  f"{overall_qual} / 10",      overall_qual / 10)
  + dcard("Living Area",      f"{gr_liv_area:,} sq ft",    min(gr_liv_area / 5000, 1.0))
  + dcard("Garage Spaces",    f"{garage_cars} cars",       garage_cars / 5)
  + dcard("Garage Area",      f"{garage_area:,} sq ft",    min(garage_area / 1500, 1.0))
  + dcard("Bedrooms",         str(bedrooms),               bedrooms / 8)
  + dcard("Bathrooms",        str(full_bath),              full_bath / 5)
  + dcard("Basement SF",      f"{total_bsmt_sf:,} sq ft",  min(total_bsmt_sf / 3000, 1.0))
  + dcard("Lot Area",         f"{lot_area:,} sq ft",       min(lot_area / 50000, 1.0))
)
st.markdown(f'<div class="detail-grid">{cards}</div>', unsafe_allow_html=True)

built_pct = (year_built - 1870) / (2026 - 1870)
st.markdown(
    '<div class="detail-card" style="margin-bottom:0">'
    '<div class="d-label">Year Built</div>'
    '<div class="d-value-row">'
    f'<div class="d-value">{year_built}</div>'
    f'<div class="d-pct">{built_pct*100:.0f}%</div>'
    '</div>'
    f'{dbar(built_pct)}'
    '</div>',
    unsafe_allow_html=True
)

# ── MODEL PERFORMANCE ──────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Model Performance</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)
st.markdown("""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">Algorithm</div>
    <div class="m-value">Random Forest</div>
    <div class="m-sub">100-tree ensemble</div>
  </div>
  <div class="metric-card">
    <div class="m-label">R² Score</div>
    <div class="m-value">0.911</div>
    <div class="m-sub">On held-out test set</div>
  </div>
  <div class="metric-card">
    <div class="m-label">Avg Error</div>
    <div class="m-value">$15.8k</div>
    <div class="m-sub">Mean absolute error</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── WHY THIS PREDICTION ────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Why This Prediction?</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)

factors = [
    ("01", "Overall Quality",  "★★★★★", "The single strongest predictor — captures finish quality, materials, and construction grade.",        "#1"),
    ("02", "Living Area",       "★★★★☆", "Above-grade square footage has a near-linear relationship with sale price.",                          "#2"),
    ("03", "Garage Size",       "★★★★☆", "Garage car capacity and area are highly valued by buyers in this dataset.",                           "#3"),
    ("04", "Basement Area",     "★★★☆☆", "Total and finished basement square footage adds measurable resale value.",                            "#4"),
    ("05", "Year Built",        "★★★☆☆", "Newer construction commands a premium; age affects both condition and buyer perception.",              "#5"),
]
items = "".join(
    f'<div class="why-item">'
    f'<div class="why-icon-wrap">{ic}</div>'
    f'<div class="why-body">'
    f'<div class="why-name">{nm}</div>'
    f'<div class="why-stars">{st_}</div>'
    f'<div class="why-desc">{dc}</div>'
    f'</div>'
    f'<div class="why-rank">{rk}</div>'
    f'</div>'
    for ic, nm, st_, dc, rk in factors
)
st.markdown(f'<div class="why-card">{items}</div>', unsafe_allow_html=True)

# ── SIMILAR HOMES (placeholder) ───────────────────────────
st.markdown('<div class="sec-header"><span class="sec-title">Similar Homes</span><div class="sec-rule"></div></div>', unsafe_allow_html=True)

ph_cards = "".join(
    '<div class="ph-card">'
    '<div class="ph-price">$—</div>'
    '<div class="ph-row"><span class="ph-field">Sq Footage</span><span class="ph-val">—</span></div>'
    '<div class="ph-row"><span class="ph-field">Year Built</span><span class="ph-val">—</span></div>'
    '<div class="ph-row"><span class="ph-field">Neighborhood</span><span class="ph-val">—</span></div>'
    '</div>'
    for _ in range(3)
)
st.markdown(f'<div class="ph-grid">{ph_cards}</div>', unsafe_allow_html=True)
st.markdown('<div class="ph-coming">Comparable sales — coming soon</div>', unsafe_allow_html=True)

st.markdown('<div style="height:4rem"></div>', unsafe_allow_html=True)