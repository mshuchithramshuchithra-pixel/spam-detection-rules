import streamlit as st
import json
import os
import base64
from spam_rules import evaluate_email

# Set page configuration
st.set_page_config(page_title="Rule-Based Spam Detector", page_icon="🛡️", layout="centered")

# ──────────────────────────────────────────────────────────────
# Premium Custom CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0b0b1a;
    --bg-secondary: #12122a;
    --bg-card: rgba(22, 22, 50, 0.65);
    --glass-border: rgba(255,255,255,0.08);
    --glass-shadow: 0 8px 32px rgba(0,0,0,0.45);
    --accent-cyan: #00d4ff;
    --accent-magenta: #ff2d75;
    --accent-green: #00ff88;
    --accent-amber: #ffb347;
    --accent-purple: #a855f7;
    --text-primary: #e8eaed;
    --text-secondary: #9aa0a6;
    --radius: 16px;
}

/* ── Global Overrides ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(160deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, #0d1b2a 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide sidebar completely ── */
[data-testid="stSidebar"],
button[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: none !important;
}
.main .block-container { padding-top: 1rem !important; max-width: 800px !important; }

/* ══════════════════════════════════════════════════════════
   NAVBAR — styled from st.radio(horizontal=True)
   ══════════════════════════════════════════════════════════ */
/* Outer wrapper: center and shape as a pill */
div[data-testid="stRadio"] {
    display: flex !important;
    justify-content: center !important;
    margin-bottom: 1.5rem !important;
}
div[data-testid="stRadio"] > label { display: none !important; }            /* hide "nav" label */
div[data-testid="stRadio"] > div {
    display: flex !important;
    background: var(--bg-card) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 50px !important;
    padding: 0.35rem !important;
    gap: 0.25rem !important;
    box-shadow: var(--glass-shadow) !important;
}
/* each radio option */
div[data-testid="stRadio"] > div > label {
    display: inline-flex !important;
    align-items: center !important;
    padding: 0.5rem 1.4rem !important;
    border-radius: 50px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    gap: 0 !important;
    margin: 0 !important;
    white-space: nowrap !important;
    letter-spacing: 0.2px !important;
}
div[data-testid="stRadio"] > div > label:hover {
    color: var(--text-primary) !important;
    background: rgba(255,255,255,0.04) !important;
}
/* selected / active state */
div[data-testid="stRadio"] > div > label[data-checked="true"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15)) !important;
    color: var(--accent-cyan) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.1) !important;
}
/* hide default radio circles */
div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b1040 40%, #2d1060 70%, #0d1b2a 100%);
    background-size: 300% 300%;
    animation: gradient-shift 8s ease infinite;
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid var(--glass-border);
    box-shadow: var(--glass-shadow), 0 0 60px rgba(168,85,247,0.12);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(0,212,255,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(255,45,117,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero-icon {
    font-size: 3.5rem;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 20px rgba(0,212,255,0.5));
    cursor: pointer;
    transition: transform 0.3s ease, filter 0.3s ease;
}
.hero-icon:hover {
    transform: scale(1.25) rotate(-8deg);
    filter: drop-shadow(0 0 30px rgba(0,212,255,0.8));
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--accent-magenta));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.6rem 0 0.3rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: var(--text-secondary);
    font-size: 0.92rem;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 auto;
}
.hero-sub strong {
    color: var(--accent-cyan);
    -webkit-text-fill-color: var(--accent-cyan);
}

/* ── Glass Card ── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.8rem; margin-bottom: 1.2rem;
    box-shadow: var(--glass-shadow);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(0,212,255,0.18);
    box-shadow: var(--glass-shadow), 0 0 30px rgba(0,212,255,0.06);
}
.card-header { display: flex; align-items: center; gap: 0.65rem; margin-bottom: 1rem; }
.card-header-icon {
    font-size: 1.5rem;
    display: inline-flex; align-items: center; justify-content: center;
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15));
    transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer;
}
.card-header-icon:hover {
    transform: scale(1.15) rotate(5deg);
    box-shadow: 0 0 18px rgba(0,212,255,0.3);
}
.card-header-title { font-size: 1.15rem; font-weight: 700; color: var(--text-primary); }

/* ── Input Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15,15,35,0.8) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stTextInput label, .stTextArea label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
}

/* ── Analyze Button ── */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.3px !important;
    transition: transform 0.2s ease, box-shadow 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(0,212,255,0.25) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,212,255,0.4) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

/* ── Result Badge ── */
.result-badge {
    display: inline-flex; align-items: center; gap: 0.6rem;
    padding: 0.8rem 1.5rem; border-radius: 50px;
    font-size: 1.05rem; font-weight: 700; letter-spacing: 0.5px;
    animation: badge-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.result-badge.safe {
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05));
    color: var(--accent-green); border: 1px solid rgba(0,255,136,0.3);
    box-shadow: 0 0 25px rgba(0,255,136,0.12);
}
.result-badge.suspicious {
    background: linear-gradient(135deg, rgba(255,179,71,0.15), rgba(255,179,71,0.05));
    color: var(--accent-amber); border: 1px solid rgba(255,179,71,0.3);
    box-shadow: 0 0 25px rgba(255,179,71,0.12);
}
.result-badge.spam {
    background: linear-gradient(135deg, rgba(255,45,117,0.15), rgba(255,45,117,0.05));
    color: var(--accent-magenta); border: 1px solid rgba(255,45,117,0.3);
    box-shadow: 0 0 25px rgba(255,45,117,0.12);
}
.result-badge .badge-icon { font-size: 1.4rem; animation: pulse-icon 2s ease-in-out infinite; }

/* ── Score Gauge ── */
.score-gauge { text-align: center; padding: 1.2rem; }
.gauge-value {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1; animation: count-in 0.8s ease-out;
}
.gauge-label {
    font-size: 0.78rem; color: var(--text-secondary);
    text-transform: uppercase; letter-spacing: 2px; margin-top: 0.4rem; font-weight: 600;
}
.score-bar-track {
    width: 100%; height: 8px; background: rgba(255,255,255,0.06);
    border-radius: 4px; margin-top: 1rem; overflow: hidden;
}
.score-bar-fill {
    height: 100%; border-radius: 4px;
    transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 0 12px var(--fill-color);
}

/* ── Rule Card ── */
.rule-card {
    background: rgba(18,18,42,0.6);
    border: 1px solid var(--glass-border);
    border-left: 3px solid var(--accent-purple);
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.65rem;
    transition: transform 0.2s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    animation: slide-in 0.4s ease-out backwards;
}
.rule-card:hover {
    transform: translateX(4px); border-left-color: var(--accent-cyan);
    box-shadow: 0 4px 20px rgba(0,212,255,0.08);
}
.rule-card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem; }
.rule-name { font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 0.5rem; }
.rule-name .rule-icon { transition: transform 0.3s ease; cursor: pointer; }
.rule-name .rule-icon:hover { transform: scale(1.3) rotate(-10deg); }
.rule-score-chip {
    display: inline-flex; align-items: center; padding: 0.2rem 0.7rem; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    background: linear-gradient(135deg, rgba(255,45,117,0.2), rgba(168,85,247,0.2));
    color: var(--accent-magenta); border: 1px solid rgba(255,45,117,0.2);
}
.rule-reason { color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5; }

/* ── Threshold ── */
.threshold-bar {
    display: flex; align-items: center; gap: 1rem;
    padding: 0.8rem 1.2rem; background: rgba(15,15,35,0.5);
    border-radius: 10px; border: 1px solid var(--glass-border);
    margin-top: 1rem; font-size: 0.82rem; color: var(--text-secondary);
}
.threshold-bar .thresh-item { display: flex; align-items: center; gap: 0.35rem; }
.thresh-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.thresh-dot.amber { background: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }
.thresh-dot.red { background: var(--accent-magenta); box-shadow: 0 0 6px var(--accent-magenta); }

/* ── No Rules ── */
.no-rules-card {
    text-align: center; padding: 1.5rem; border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,255,136,0.05), rgba(0,212,255,0.05));
    border: 1px solid rgba(0,255,136,0.15); color: var(--accent-green); font-weight: 500;
}
.no-rules-card .check-icon { font-size: 2rem; display: inline-block; animation: pulse-icon 2s ease-in-out infinite; }

/* ── Profile Card ── */
.profile-card {
    background: var(--bg-card); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border); border-radius: var(--radius);
    padding: 2.5rem 2rem; text-align: center;
    box-shadow: var(--glass-shadow), 0 0 60px rgba(168,85,247,0.08);
    position: relative; overflow: hidden; animation: card-enter 0.6s ease-out;
}
.profile-card::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(0,212,255,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.avatar-ring {
    width: 140px; height: 140px; border-radius: 50%;
    margin: 0 auto 1.2rem; padding: 4px;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--accent-magenta));
    background-size: 200% 200%; animation: ring-rotate 4s linear infinite;
    display: flex; align-items: center; justify-content: center;
}
.avatar-ring img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid var(--bg-primary); }
.avatar-placeholder {
    width: 100%; height: 100%; border-radius: 50%;
    background: var(--bg-secondary); border: 3px solid var(--bg-primary);
    display: flex; align-items: center; justify-content: center; font-size: 3rem;
}
.profile-name {
    font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.3rem;
}
.profile-role { font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 0.2rem; }
.profile-location {
    font-size: 0.82rem; color: var(--text-secondary);
    display: flex; align-items: center; justify-content: center; gap: 0.3rem; margin-bottom: 1.2rem;
}
.social-links { display: flex; justify-content: center; gap: 0.8rem; margin-top: 1rem; flex-wrap: wrap; }
.social-btn {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.5rem 1rem; border-radius: 50px;
    background: rgba(255,255,255,0.04); border: 1px solid var(--glass-border);
    color: var(--text-secondary); font-size: 0.82rem; font-weight: 500;
    text-decoration: none; transition: all 0.3s ease; cursor: pointer;
}
.social-btn:hover {
    border-color: var(--accent-cyan); color: var(--accent-cyan);
    background: rgba(0,212,255,0.08);
    transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,212,255,0.15);
}
.social-btn .s-icon { font-size: 1rem; transition: transform 0.3s ease; }
.social-btn:hover .s-icon { transform: scale(1.2); }

/* ── Glass Section ── */
.glass-section {
    background: var(--bg-card); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border); border-radius: var(--radius);
    padding: 1.8rem; margin-top: 1.2rem; box-shadow: var(--glass-shadow);
    text-align: left; animation: card-enter 0.6s ease-out backwards;
}
.section-header { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1rem; }
.section-icon {
    font-size: 1.4rem; display: inline-flex; align-items: center; justify-content: center;
    width: 40px; height: 40px; border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15));
    transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer;
}
.section-icon:hover { transform: scale(1.15) rotate(5deg); box-shadow: 0 0 18px rgba(0,212,255,0.3); }
.section-title { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }
.section-text { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7; }

/* ── Skill Chips ── */
.skill-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
.skill-chip {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.35rem 0.85rem; border-radius: 50px;
    font-size: 0.78rem; font-weight: 600;
    border: 1px solid var(--glass-border);
    background: rgba(255,255,255,0.03); color: var(--text-secondary);
    transition: all 0.3s ease; cursor: default;
}
.skill-chip:hover {
    border-color: var(--accent-cyan); color: var(--accent-cyan);
    background: rgba(0,212,255,0.06); transform: translateY(-1px);
}
.skill-chip .chip-icon { font-size: 0.9rem; }

/* ── Stats Row ── */
.stats-row { display: flex; gap: 0.8rem; margin-top: 1.2rem; }
.stat-card {
    flex: 1; text-align: center; padding: 1.2rem 0.8rem;
    background: rgba(15,15,35,0.6); border: 1px solid var(--glass-border);
    border-radius: 14px; transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: rgba(0,212,255,0.2); transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}
.stat-value {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label {
    font-size: 0.72rem; color: var(--text-secondary);
    text-transform: uppercase; letter-spacing: 1.5px; margin-top: 0.25rem; font-weight: 600;
}

/* ── Footer ── */
.premium-footer {
    text-align: center; padding: 1.5rem 0 1rem; margin-top: 2rem;
    border-top: 1px solid var(--glass-border);
    color: var(--text-secondary); font-size: 0.78rem;
}
.premium-footer .footer-brand {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 700;
}

/* ── Streamlit Overrides ── */
.stAlert, [data-testid="stAlert"] { display: none; }
div[data-testid="stMetric"] { display: none; }
h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
p, span, li { color: var(--text-primary); }

/* ── Keyframes ── */
@keyframes gradient-shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
@keyframes badge-pop { 0% { opacity: 0; transform: scale(0.7); } 100% { opacity: 1; transform: scale(1); } }
@keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
@keyframes slide-in { 0% { opacity: 0; transform: translateX(-16px); } 100% { opacity: 1; transform: translateX(0); } }
@keyframes count-in { 0% { opacity: 0; transform: scale(0.5); } 100% { opacity: 1; transform: scale(1); } }
@keyframes card-enter { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes ring-rotate { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Navbar  (CSS-styled st.radio — no JS needed)
# ──────────────────────────────────────────────────────────────
page = st.radio("nav", ["🏠  Home", "👤  About Me"], horizontal=True, label_visibility="collapsed")


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def load_sample_inputs():
    file_path = "sample_inputs.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

RULE_ICONS = {
    "Too Many Links": "🔗", "Suspicious Keywords": "🔑",
    "Excessive Uppercase": "🔠", "Excessive Exclamations": "❗",
    "Suspicious Sender Domain": "🌐", "Short Subject + Promo Body": "📝",
    "Missing Subject": "📭", "Urgent Subject": "⚡",
    "Suspicious Attachment Pattern": "📎", "URL Shortener": "🔀",
}


# ══════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
if page == "🏠  Home":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-icon">🛡️</div>
        <div class="hero-title">Email Spam Detection</div>
        <div class="hero-sub">
            Analyze emails with heuristic-powered detection. We score the <strong>sender</strong>,
            <strong>subject</strong>, and <strong>body</strong> to classify messages as
            Safe, Suspicious, or Spam — no machine learning required.
        </div>
    </div>
    """, unsafe_allow_html=True)

    samples = load_sample_inputs()
    sample_options = ["— Manual Entry —"] + [s["name"] for s in samples]

    st.markdown("""
    <div class="card-header">
        <div class="card-header-icon">📁</div>
        <div class="card-header-title">Load Sample Email</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.selectbox("sample", sample_options, label_visibility="collapsed")

    default_sender = default_subject = default_body = ""
    if selected != "— Manual Entry —":
        for s in samples:
            if s["name"] == selected:
                default_sender, default_subject, default_body = s["sender"], s["subject"], s["body"]
                break

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card-header">
        <div class="card-header-icon">📝</div>
        <div class="card-header-title">Email Details</div>
    </div>
    """, unsafe_allow_html=True)

    sender_input = st.text_input("Sender Email Address", value=default_sender, placeholder="e.g., mail@example.com")
    subject_input = st.text_input("Email Subject", value=default_subject, placeholder="e.g., Important update about your account")
    body_input = st.text_area("Email Body", value=default_body, height=180, placeholder="Paste the email content here...")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if st.button("🔍  Analyze Email", type="primary"):
        if not sender_input and not subject_input and not body_input:
            st.markdown("""
            <div class="rule-card" style="border-left-color: var(--accent-amber);">
                <div class="rule-name"><span class="rule-icon">⚠️</span> Please enter at least some email content to analyze.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Analyzing email..."):
                result = evaluate_email(sender_input, subject_input, body_input)

            label, score = result["label"], result["score"]
            badge_cls, badge_icon = ("safe", "✅") if label == "Safe" else ("suspicious", "⚠️") if label == "Suspicious" else ("spam", "🚫")
            bar_pct = min(score / 15 * 100, 100)
            bar_color = "var(--accent-green)" if label == "Safe" else "var(--accent-amber)" if label == "Suspicious" else "var(--accent-magenta)"

            st.markdown("""
            <div class="card-header" style="margin-top:1.5rem;">
                <div class="card-header-icon">📊</div>
                <div class="card-header-title">Analysis Result</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;color:var(--text-secondary);margin-bottom:0.8rem;font-weight:600;">Classification</div>
                    <div class="result-badge {badge_cls}"><span class="badge-icon">{badge_icon}</span> {label}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="score-gauge">
                        <div class="gauge-value">{score}</div>
                        <div class="gauge-label">Spam Score</div>
                        <div class="score-bar-track"><div class="score-bar-fill" style="width:{bar_pct}%;background:{bar_color};--fill-color:{bar_color};"></div></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            num_rules = len(result["triggered_rules"])
            st.markdown(f"""
            <div class="card-header" style="margin-top:0.5rem;">
                <div class="card-header-icon">🚨</div>
                <div class="card-header-title">Triggered Rules ({num_rules})</div>
            </div>""", unsafe_allow_html=True)

            if num_rules == 0:
                st.markdown("""<div class="no-rules-card"><div class="check-icon">✨</div><div style="margin-top:0.5rem;">No suspicious patterns were detected.</div></div>""", unsafe_allow_html=True)
            else:
                for i, rule in enumerate(result["triggered_rules"]):
                    icon = RULE_ICONS.get(rule["rule"], "🔺")
                    st.markdown(f"""
                    <div class="rule-card" style="animation-delay:{i*0.1}s;">
                        <div class="rule-card-header">
                            <div class="rule-name"><span class="rule-icon">{icon}</span> {rule['rule']}</div>
                            <div class="rule-score-chip">+{rule['score']} pts</div>
                        </div>
                        <div class="rule-reason">{rule['reason']}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="threshold-bar">
                <div class="thresh-item"><span class="thresh-dot amber"></span> Suspicious ≥ {result['thresholds']['suspicious']}</div>
                <div class="thresh-item"><span class="thresh-dot red"></span> Spam ≥ {result['thresholds']['spam']}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: ABOUT ME
# ══════════════════════════════════════════════════════════════
elif page == "👤  About Me":

    PROFILE_IMG = os.path.join(os.path.dirname(__file__), "assets", "profile.png")
    PROFILE_JPG = os.path.join(os.path.dirname(__file__), "assets", "profile.jpg")

    profile_img = PROFILE_IMG if os.path.exists(PROFILE_IMG) else PROFILE_JPG if os.path.exists(PROFILE_JPG) else None

    if profile_img:
        with open(profile_img, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        ext = "png" if profile_img.endswith(".png") else "jpeg"
        avatar_html = f'<img src="data:image/{ext};base64,{img_data}" alt="Profile">'
    else:
        avatar_html = '<div class="avatar-placeholder">👤</div>'

    st.markdown(f"""
    <div class="profile-card">
        <div class="avatar-ring">{avatar_html}</div>
        <div class="profile-name">Shuchithra M</div>
        <div class="profile-role">Developer · Data Enthusiast · Builder</div>
        <div class="profile-location">📍 Your Location</div>
        <div class="social-links">
            <a href="https://github.com/mshuchithramshuchithra-pixel" class="social-btn" target="_blank"><span class="s-icon">🐙</span> GitHub</a>
            <a href="https://www.linkedin.com/in/shuchithra-murthy-323b24357?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" class="social-btn" target="_blank"><span class="s-icon">💼</span> LinkedIn</a>
            <a href="mailto:mshuchithramshuchithra@gmail.com" class="social-btn"><span class="s-icon">📧</span> Email</a>
            <a href="https://mshuchithramshuchithra-pixel-spam-detection-rules-app-ktz42f.streamlit.app/" class="social-btn" target="_blank"><span class="s-icon">🚀</span> Live Demo</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-card"><div class="stat-value">10</div><div class="stat-label">Rules Engine</div></div>
        <div class="stat-card"><div class="stat-value">4</div><div class="stat-label">Sample Emails</div></div>
        <div class="stat-card"><div class="stat-value">0%</div><div class="stat-label">ML Required</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-section" style="animation-delay:0.1s;">
        <div class="section-header"><div class="section-icon">🧠</div><div class="section-title">About This Project</div></div>
        <div class="section-text">
            This Email Spam Detection system uses a purely <strong style="color:var(--accent-cyan);">rule-based approach</strong>
            to classify emails as Safe, Suspicious, or Spam. Instead of relying on machine learning models,
            it leverages 10 handcrafted heuristic rules that analyze the sender, subject line, and email body
            to assign penalty scores. This makes the system fully transparent, explainable, and easy to extend.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-section" style="animation-delay:0.2s;">
        <div class="section-header"><div class="section-icon">⚡</div><div class="section-title">Tech Stack</div></div>
        <div class="skill-chips">
            <div class="skill-chip"><span class="chip-icon">🐍</span> Python</div>
            <div class="skill-chip"><span class="chip-icon">🎈</span> Streamlit</div>
            <div class="skill-chip"><span class="chip-icon">🔍</span> Regex</div>
            <div class="skill-chip"><span class="chip-icon">📊</span> Heuristics</div>
            <div class="skill-chip"><span class="chip-icon">🛡️</span> Spam Detection</div>
            <div class="skill-chip"><span class="chip-icon">📐</span> Rule Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-section" style="animation-delay:0.3s;">
        <div class="section-header"><div class="section-icon">🔬</div><div class="section-title">How It Works</div></div>
        <div class="section-text">
            <strong style="color:var(--accent-cyan);">1.</strong> Enter (or select) an email with sender, subject, and body.<br>
            <strong style="color:var(--accent-purple);">2.</strong> The engine runs 10 heuristic rules — checking for suspicious keywords, URL patterns, uppercase ratio, and more.<br>
            <strong style="color:var(--accent-magenta);">3.</strong> Each triggered rule adds penalty points.<br>
            <strong style="color:var(--accent-green);">4.</strong> The total score determines the final classification:
            <strong style="color:var(--accent-green);">Safe</strong>,
            <strong style="color:var(--accent-amber);">Suspicious</strong>, or
            <strong style="color:var(--accent-magenta);">Spam</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Footer (both pages)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="premium-footer">
    Built with ❤️ using <span class="footer-brand">Streamlit</span> · Rule-Based Spam Detection System
</div>
""", unsafe_allow_html=True)
