import streamlit as st
import os

st.set_page_config(page_title="About Me", page_icon="👤", layout="centered")

# ──────────────────────────────────────────────────────────────
# Premium Custom CSS  (shared palette with main app)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

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

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(160deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, #0d1b2a 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,15,35,0.95) 0%, rgba(10,10,25,0.98) 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
p, span, li { color: var(--text-primary); }
.main .block-container { padding-top: 2rem !important; }

/* ── Profile Card ── */
.profile-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: var(--glass-shadow), 0 0 60px rgba(168,85,247,0.08);
    position: relative;
    overflow: hidden;
    animation: card-enter 0.6s ease-out;
}
.profile-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(0,212,255,0.07) 0%, transparent 60%);
    pointer-events: none;
}

/* ── Avatar ── */
.avatar-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    margin: 0 auto 1.2rem;
    padding: 4px;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--accent-magenta));
    background-size: 200% 200%;
    animation: ring-rotate 4s linear infinite;
    display: flex;
    align-items: center;
    justify-content: center;
}
.avatar-ring img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--bg-primary);
}
.avatar-placeholder {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: var(--bg-secondary);
    border: 3px solid var(--bg-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}

.profile-name {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.profile-role {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-bottom: 0.2rem;
}
.profile-location {
    font-size: 0.82rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.3rem;
    margin-bottom: 1.2rem;
}

/* ── Social Links ── */
.social-links {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.social-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--glass-border);
    color: var(--text-secondary);
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
}
.social-btn:hover {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    background: rgba(0,212,255,0.08);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,212,255,0.15);
}
.social-btn .s-icon {
    font-size: 1rem;
    transition: transform 0.3s ease;
}
.social-btn:hover .s-icon {
    transform: scale(1.2);
}

/* ── Glass Section ── */
.glass-section {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.8rem;
    margin-top: 1.2rem;
    box-shadow: var(--glass-shadow);
    text-align: left;
    animation: card-enter 0.6s ease-out backwards;
}
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.section-icon {
    font-size: 1.4rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15));
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.section-icon:hover {
    transform: scale(1.15) rotate(5deg);
    box-shadow: 0 0 18px rgba(0,212,255,0.3);
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}
.section-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.7;
}

/* ── Skill Chips ── */
.skill-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.85rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    border: 1px solid var(--glass-border);
    background: rgba(255,255,255,0.03);
    color: var(--text-secondary);
    transition: all 0.3s ease;
    cursor: default;
}
.skill-chip:hover {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    background: rgba(0,212,255,0.06);
    transform: translateY(-1px);
}
.skill-chip .chip-icon {
    font-size: 0.9rem;
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-top: 1.2rem;
}
.stat-card {
    flex: 1;
    text-align: center;
    padding: 1.2rem 0.8rem;
    background: rgba(15,15,35,0.6);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: rgba(0,212,255,0.2);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}
.stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.25rem;
    font-weight: 600;
}

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

/* ── Keyframes ── */
@keyframes card-enter {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes ring-rotate {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Profile Picture Path
# ──────────────────────────────────────────────────────────────
# 👉 PUT YOUR PROFILE PICTURE HERE:
#    Save your photo as "profile.png" (or .jpg) inside:
#      d:\spam-detection\rules-based-approach\assets\profile.png
#
#    The avatar ring will automatically display it.
# ──────────────────────────────────────────────────────────────

PROFILE_IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "profile.png")
PROFILE_IMAGE_JPG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "profile.jpg")


def get_profile_image():
    """Check for profile image in assets folder."""
    if os.path.exists(PROFILE_IMAGE_PATH):
        return PROFILE_IMAGE_PATH
    elif os.path.exists(PROFILE_IMAGE_JPG):
        return PROFILE_IMAGE_JPG
    return None


# ──────────────────────────────────────────────────────────────
# Profile Card
# ──────────────────────────────────────────────────────────────
profile_img = get_profile_image()

if profile_img:
    import base64
    with open(profile_img, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    ext = "png" if profile_img.endswith(".png") else "jpeg"
    avatar_html = f'<img src="data:image/{ext};base64,{img_data}" alt="Profile">'
else:
    avatar_html = '<div class="avatar-placeholder">👤</div>'

st.markdown(f"""
<div class="profile-card">
    <div class="avatar-ring">
        {avatar_html}
    </div>
    <div class="profile-name">Your Name</div>
    <div class="profile-role">Developer · Data Enthusiast · Builder</div>
    <div class="profile-location">📍 Your Location</div>
    <div class="social-links">
        <a href="#" class="social-btn"><span class="s-icon">🐙</span> GitHub</a>
        <a href="#" class="social-btn"><span class="s-icon">💼</span> LinkedIn</a>
        <a href="#" class="social-btn"><span class="s-icon">🐦</span> Twitter</a>
        <a href="#" class="social-btn"><span class="s-icon">📧</span> Email</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Stats Row
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value">10</div>
        <div class="stat-label">Rules Engine</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">4</div>
        <div class="stat-label">Sample Emails</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">0%</div>
        <div class="stat-label">ML Required</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# About Section
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-section" style="animation-delay: 0.1s;">
    <div class="section-header">
        <div class="section-icon">🧠</div>
        <div class="section-title">About This Project</div>
    </div>
    <div class="section-text">
        This Email Spam Detection system uses a purely <strong style="color: var(--accent-cyan);">rule-based approach</strong>
        to classify emails as Safe, Suspicious, or Spam. Instead of relying on machine learning models,
        it leverages 10 handcrafted heuristic rules that analyze the sender, subject line, and email body
        to assign penalty scores. This makes the system fully transparent, explainable, and easy to extend.
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Skills / Tech Stack
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-section" style="animation-delay: 0.2s;">
    <div class="section-header">
        <div class="section-icon">⚡</div>
        <div class="section-title">Tech Stack</div>
    </div>
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


# ──────────────────────────────────────────────────────────────
# How It Works
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-section" style="animation-delay: 0.3s;">
    <div class="section-header">
        <div class="section-icon">🔬</div>
        <div class="section-title">How It Works</div>
    </div>
    <div class="section-text">
        <strong style="color: var(--accent-cyan);">1.</strong> Enter (or select) an email with sender, subject, and body.<br>
        <strong style="color: var(--accent-purple);">2.</strong> The engine runs 10 heuristic rules — checking for suspicious keywords, URL patterns, uppercase ratio, and more.<br>
        <strong style="color: var(--accent-magenta);">3.</strong> Each triggered rule adds penalty points.<br>
        <strong style="color: var(--accent-green);">4.</strong> The total score determines the final classification: <strong style="color: var(--accent-green);">Safe</strong>, <strong style="color: var(--accent-amber);">Suspicious</strong>, or <strong style="color: var(--accent-magenta);">Spam</strong>.
    </div>
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
