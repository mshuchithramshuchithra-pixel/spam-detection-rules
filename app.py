import streamlit as st
import json
import os
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

[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,15,35,0.95) 0%, rgba(10,10,25,0.98) 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
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
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--glass-shadow);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(0,212,255,0.18);
    box-shadow: var(--glass-shadow), 0 0 30px rgba(0,212,255,0.06);
}
.card-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
}
.card-header-icon {
    font-size: 1.5rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15));
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.card-header-icon:hover {
    transform: scale(1.15) rotate(5deg);
    box-shadow: 0 0 18px rgba(0,212,255,0.3);
}
.card-header-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
}

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
.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ── Result Badge ── */
.result-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    animation: badge-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.result-badge.safe {
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05));
    color: var(--accent-green);
    border: 1px solid rgba(0,255,136,0.3);
    box-shadow: 0 0 25px rgba(0,255,136,0.12);
}
.result-badge.suspicious {
    background: linear-gradient(135deg, rgba(255,179,71,0.15), rgba(255,179,71,0.05));
    color: var(--accent-amber);
    border: 1px solid rgba(255,179,71,0.3);
    box-shadow: 0 0 25px rgba(255,179,71,0.12);
}
.result-badge.spam {
    background: linear-gradient(135deg, rgba(255,45,117,0.15), rgba(255,45,117,0.05));
    color: var(--accent-magenta);
    border: 1px solid rgba(255,45,117,0.3);
    box-shadow: 0 0 25px rgba(255,45,117,0.12);
}
.result-badge .badge-icon {
    font-size: 1.4rem;
    animation: pulse-icon 2s ease-in-out infinite;
}

/* ── Score Gauge ── */
.score-gauge {
    text-align: center;
    padding: 1.2rem;
}
.gauge-value {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    animation: count-in 0.8s ease-out;
}
.gauge-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.4rem;
    font-weight: 600;
}
.score-bar-track {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 4px;
    margin-top: 1rem;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 0 12px var(--fill-color);
}

/* ── Rule Card ── */
.rule-card {
    background: rgba(18,18,42,0.6);
    border: 1px solid var(--glass-border);
    border-left: 3px solid var(--accent-purple);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.65rem;
    transition: transform 0.2s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    animation: slide-in 0.4s ease-out backwards;
}
.rule-card:hover {
    transform: translateX(4px);
    border-left-color: var(--accent-cyan);
    box-shadow: 0 4px 20px rgba(0,212,255,0.08);
}
.rule-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.4rem;
}
.rule-name {
    font-weight: 600;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.rule-name .rule-icon {
    transition: transform 0.3s ease;
    cursor: pointer;
}
.rule-name .rule-icon:hover {
    transform: scale(1.3) rotate(-10deg);
}
.rule-score-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    background: linear-gradient(135deg, rgba(255,45,117,0.2), rgba(168,85,247,0.2));
    color: var(--accent-magenta);
    border: 1px solid rgba(255,45,117,0.2);
}
.rule-reason {
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.5;
}

/* ── Threshold Info ── */
.threshold-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem 1.2rem;
    background: rgba(15,15,35,0.5);
    border-radius: 10px;
    border: 1px solid var(--glass-border);
    margin-top: 1rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
}
.threshold-bar .thresh-item {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.thresh-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.thresh-dot.amber { background: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }
.thresh-dot.red { background: var(--accent-magenta); box-shadow: 0 0 6px var(--accent-magenta); }

/* ── Footer ── */
.premium-footer {
    text-align: center;
    padding: 1.5rem 0 1rem;
    margin-top: 2rem;
    border-top: 1px solid var(--glass-border);
    color: var(--text-secondary);
    font-size: 0.78rem;
}
.premium-footer .footer-brand {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* ── Sidebar Info Card ── */
.sidebar-info-card {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.6;
}
.sidebar-info-card .info-icon {
    font-size: 1.2rem;
    transition: transform 0.3s ease;
    cursor: pointer;
    display: inline-block;
}
.sidebar-info-card .info-icon:hover {
    transform: scale(1.3);
}

/* ── No Rules Card ── */
.no-rules-card {
    text-align: center;
    padding: 1.5rem;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,255,136,0.05), rgba(0,212,255,0.05));
    border: 1px solid rgba(0,255,136,0.15);
    color: var(--accent-green);
    font-weight: 500;
}
.no-rules-card .check-icon {
    font-size: 2rem;
    display: inline-block;
    animation: pulse-icon 2s ease-in-out infinite;
}

/* ── Streamlit Overrides ── */
.stAlert, [data-testid="stAlert"] { display: none; }
div[data-testid="stMetric"] { display: none; }
.stDivider { border-color: var(--glass-border) !important; }
h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
p, span, li { color: var(--text-primary); }

/* Hide default streamlit elements we replace */
.main .block-container { padding-top: 2rem !important; }

/* ── Streamlit Expander Override ── */
.streamlit-expanderHeader {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
details {
    background: rgba(18,18,42,0.5) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

/* ── Keyframes ── */
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
@keyframes badge-pop {
    0% { opacity: 0; transform: scale(0.7); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes pulse-icon {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.15); }
}
@keyframes slide-in {
    0% { opacity: 0; transform: translateX(-16px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes count-in {
    0% { opacity: 0; transform: scale(0.5); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────
def load_sample_inputs():
    """Loads sample emails from the JSON file."""
    file_path = "sample_inputs.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []


RULE_ICONS = {
    "Too Many Links": "🔗",
    "Suspicious Keywords": "🔑",
    "Excessive Uppercase": "🔠",
    "Excessive Exclamations": "❗",
    "Suspicious Sender Domain": "🌐",
    "Short Subject + Promo Body": "📝",
    "Missing Subject": "📭",
    "Urgent Subject": "⚡",
    "Suspicious Attachment Pattern": "📎",
    "URL Shortener": "🔀",
}


# ──────────────────────────────────────────────────────────────
# Hero Banner
# ──────────────────────────────────────────────────────────────
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


# ──────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────
samples = load_sample_inputs()
sample_options = ["— Manual Entry —"] + [sample["name"] for sample in samples]

st.sidebar.markdown("""
<div style="text-align:center; margin-bottom:1rem;">
    <div class="hero-icon" style="font-size:2.5rem;">📁</div>
    <div style="font-size:1.1rem; font-weight:700; margin-top:0.4rem; color:var(--text-primary);">
        Sample Emails
    </div>
    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.2rem;">
        Quick-load pre-built test cases
    </div>
</div>
""", unsafe_allow_html=True)

selected_sample_name = st.sidebar.selectbox("Choose a sample:", sample_options, label_visibility="collapsed")

# Pre-fill data if a sample is selected
default_sender = ""
default_subject = ""
default_body = ""

if selected_sample_name != "— Manual Entry —":
    for sample in samples:
        if sample["name"] == selected_sample_name:
            default_sender = sample["sender"]
            default_subject = sample["subject"]
            default_body = sample["body"]
            break

st.sidebar.markdown("""
<div class="sidebar-info-card">
    <span class="info-icon">💡</span> <strong>How it works</strong><br>
    10 heuristic rules analyze your email content and assign penalty scores.
    The total score determines the final classification.
    <br><br>
    <span class="info-icon">🎯</span> <strong>Thresholds</strong><br>
    Score ≥ 4 → Suspicious &nbsp;|&nbsp; Score ≥ 5 → Spam
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Input Form
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="card-header">
    <div class="card-header-icon">📝</div>
    <div class="card-header-title">Email Details</div>
</div>
""", unsafe_allow_html=True)

sender_input = st.text_input("Sender Email Address", value=default_sender, placeholder="e.g., mail@example.com")
subject_input = st.text_input("Email Subject", value=default_subject, placeholder="e.g., Important update about your account")
body_input = st.text_area("Email Body", value=default_body, height=180, placeholder="Paste the email content here...")

st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Analyze Button & Results
# ──────────────────────────────────────────────────────────────
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

        label = result["label"]
        score = result["score"]

        # ── Classification badge + Score gauge ──
        if label == "Safe":
            badge_cls = "safe"
            badge_icon = "✅"
        elif label == "Suspicious":
            badge_cls = "suspicious"
            badge_icon = "⚠️"
        else:
            badge_cls = "spam"
            badge_icon = "🚫"

        # Score bar percentage (max out at 15 for visual)
        bar_pct = min(score / 15 * 100, 100)
        if label == "Safe":
            bar_color = "var(--accent-green)"
        elif label == "Suspicious":
            bar_color = "var(--accent-amber)"
        else:
            bar_color = "var(--accent-magenta)"

        # Results section header
        st.markdown("""
        <div class="card-header" style="margin-top: 1.5rem;">
            <div class="card-header-icon">📊</div>
            <div class="card-header-title">Analysis Result</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; color:var(--text-secondary); margin-bottom:0.8rem; font-weight:600;">Classification</div>
                <div class="result-badge {badge_cls}">
                    <span class="badge-icon">{badge_icon}</span>
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <div class="score-gauge">
                    <div class="gauge-value">{score}</div>
                    <div class="gauge-label">Spam Score</div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill" style="width:{bar_pct}%; background:{bar_color}; --fill-color:{bar_color};"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Triggered Rules ──
        num_rules = len(result["triggered_rules"])

        st.markdown(f"""
        <div class="card-header" style="margin-top: 0.5rem;">
            <div class="card-header-icon">🚨</div>
            <div class="card-header-title">Triggered Rules ({num_rules})</div>
        </div>
        """, unsafe_allow_html=True)

        if num_rules == 0:
            st.markdown("""
            <div class="no-rules-card">
                <div class="check-icon">✨</div>
                <div style="margin-top:0.5rem;">No suspicious patterns were detected in this email.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, rule in enumerate(result["triggered_rules"]):
                icon = RULE_ICONS.get(rule["rule"], "🔺")
                delay = i * 0.1
                st.markdown(f"""
                <div class="rule-card" style="animation-delay: {delay}s;">
                    <div class="rule-card-header">
                        <div class="rule-name">
                            <span class="rule-icon">{icon}</span>
                            {rule['rule']}
                        </div>
                        <div class="rule-score-chip">+{rule['score']} pts</div>
                    </div>
                    <div class="rule-reason">{rule['reason']}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Threshold bar ──
        st.markdown(f"""
        <div class="threshold-bar">
            <div class="thresh-item"><span class="thresh-dot amber"></span> Suspicious ≥ {result['thresholds']['suspicious']}</div>
            <div class="thresh-item"><span class="thresh-dot red"></span> Spam ≥ {result['thresholds']['spam']}</div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="premium-footer">
    Built with ❤️ using <span class="footer-brand">Streamlit</span> · Rule-Based Spam Detection System
</div>
""", unsafe_allow_html=True)
