import streamlit as st


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f7f5f0;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Force all widget labels to be dark and visible ── */
label,
div[data-testid="stWidgetLabel"] p,
.stRadio p,
.stSelectbox p,
.stSlider p,
.stRadio div[role="radiogroup"] label,
div[data-testid="stMarkdownContainer"] p {
    color: #1a1a2e !important;
}

.stTextInput > label,
.stTextArea > label,
.stSelectbox > label,
.stSlider > label,
.stRadio > label,
.stNumberInput > label,
.stMultiSelect > label {
    color: #1a1a2e !important;
    font-weight: 500;
}

/* ── Hero ── */
.hero {
    background: #1a1a2e;
    border-radius: 20px;
    padding: 52px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, #e8c547 0%, transparent 70%);
    opacity: 0.15;
    border-radius: 50%;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    color: #ffffff;
    margin: 0 0 8px 0;
    line-height: 1.15;
}
.hero p { color: #a0a0b8; font-size: 1.1rem; margin: 0; }
.hero span { color: #e8c547; }

/* ── Provider card ── */
.provider-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.provider-card:hover {
    border-color: #e8c547;
    box-shadow: 0 4px 20px rgba(232,197,71,0.2);
}

/* ── Badges & tags ── */
.match-badge {
    background: #e8c547;
    color: #1a1a2e;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-block;
}
.tag {
    background: #f0ede6;
    color: #444;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    display: inline-block;
    margin: 2px;
}

/* ── Typography helpers ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    color: #1a1a2e;
    margin-bottom: 4px;
}
.subtitle {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 24px;
}

/* ── Stat boxes ── */
.stat-box {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-num  { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; }
.stat-label { font-size: 0.8rem; color: #888; }

/* ── Booking confirmation ── */
.confirm-box {
    background: #1a1a2e;
    border-radius: 16px;
    padding: 28px;
    color: white;
    text-align: center;
}
.confirm-box h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    margin-bottom: 8px;
}

/* ── AI parsed params display ── */
.ai-parse-box {
    background: #eef6ff;
    border: 1.5px solid #b3d4ff;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}
.ai-label {
    font-weight: 600;
    color: #1a5fb4;
    font-size: 0.85rem;
    margin-right: 4px;
}
.ai-chip {
    background: #dbeafe;
    color: #1e40af;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

/* ── AI match explanation box ── */
.ai-explain-box {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d50 100%);
    border: 1.5px solid #e8c547;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
}
.ai-explain-title {
    font-weight: 700;
    color: #e8c547;
    font-size: 0.9rem;
    margin-bottom: 6px;
}
.ai-explain-body {
    color: #d0d0e8;
    font-size: 0.9rem;
    line-height: 1.55;
}

/* ── AI enhance box (booking page) ── */
.ai-enhance-box {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 10px;
    padding: 10px 14px 4px 14px;
    margin-bottom: 4px;
}
.ai-enhance-title {
    font-weight: 600;
    color: #15803d;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)
