import streamlit as st
from data.providers import PROVIDERS, CATEGORIES, DAYS
from utils.matching import filter_and_rank


def render_home(go_to):
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <h1>Find trusted help,<br><span>right when you need it.</span></h1>
        <p>Handy connects you with vetted local professionals — powered by smart matching.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("1,240+", "Verified Providers"),
        ("4.8★",   "Avg. Rating"),
        ("98%",    "Satisfaction Rate"),
        ("< 2h",   "Avg. Response Time"),
    ]
    for col, (num, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(
                f'<div class="stat-box"><div class="stat-num">{num}</div>'
                f'<div class="stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters + Results ─────────────────────────────────────────────────────
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown('<div class="section-title">🔍 Smart Search</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Tell us what you need — our AI finds the best match.</div>', unsafe_allow_html=True)

        category      = st.selectbox("Service category", CATEGORIES)
        preferred_day = st.select_slider("Preferred day", options=DAYS, value="Mon")
        urgency       = st.radio("When do you need it?", ["ASAP (today/tomorrow)", "This week", "Flexible"])
        max_price     = st.slider("Max hourly rate (€)", 20, 100, 60, step=5)
        min_rating    = st.slider("Minimum rating", 4.0, 5.0, 4.5, step=0.1)
        max_distance  = st.slider("Max distance (km)", 1, 10, 5)

    with right:
        st.markdown('<div class="section-title">Top Providers</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Ranked by our AI matching score based on your preferences.</div>', unsafe_allow_html=True)

        results = filter_and_rank(
            PROVIDERS, category, max_price, min_rating, max_distance, preferred_day, urgency
        )

        if not results:
            st.info("No providers match your current filters. Try adjusting your criteria.")
        else:
            for p in results:
                _render_provider_card(p)
                if st.button(f"Book {p['name']}", key=f"book_{p['id']}", use_container_width=True):
                    go_to("booking", provider=p)
                    st.rerun()

    # ── Provider registration ─────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    _render_registration_form()


def _render_provider_card(p):
    avail_str = " · ".join(p["availability"])
    tags_html = " ".join([f'<span class="tag">{t}</span>' for t in p["tags"]])
    stars = "★" * int(p["rating"]) + ("½" if p["rating"] % 1 >= 0.5 else "")

    st.markdown(f"""
    <div class="provider-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div style="display:flex; gap:14px; align-items:center;">
                <div style="font-size:2rem;">{p['avatar']}</div>
                <div>
                    <div style="font-weight:700; font-size:1.05rem; color:#1a1a2e;">{p['name']}</div>
                    <div style="color:#888; font-size:0.85rem;">
                        {p['category']} · {p['experience']} yrs exp · {p['distance']} km away
                    </div>
                    <div style="margin-top:6px;">{tags_html}</div>
                </div>
            </div>
            <div style="text-align:right;">
                <div class="match-badge">⚡ {p['score']}% match</div>
                <div style="font-size:1.1rem; font-weight:700; color:#1a1a2e; margin-top:6px;">€{p['price']}/hr</div>
                <div style="color:#e8a020; font-size:0.85rem;">{stars} {p['rating']} ({p['reviews']})</div>
            </div>
        </div>
        <div style="color:#555; font-size:0.85rem; margin-top:10px;">{p['bio']}</div>
        <div style="color:#aaa; font-size:0.78rem; margin-top:6px;">Available: {avail_str}</div>
    </div>
    """, unsafe_allow_html=True)


def _render_registration_form():
    with st.expander("📋 Are you a professional? Register as a provider"):
        st.markdown("**Join Handy and reach hundreds of customers in your area.**")
        r1, r2 = st.columns(2)

        with r1:
            prov_name  = st.text_input("Full name")
            prov_cat   = st.selectbox("Your service", CATEGORIES[1:], key="reg_cat")
            prov_exp   = st.number_input("Years of experience", 0, 50, 1)
            prov_price = st.number_input("Hourly rate (€)", 10, 200, 30)
        with r2:
            prov_avail = st.multiselect("Available days", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], default=["Mon","Wed","Fri"])
            prov_bio   = st.text_area("Short bio (max 200 chars)", max_chars=200)
            _          = st.text_input("Skills / tags (comma separated)")

        if st.button("Submit registration", type="primary"):
            if prov_name and prov_bio:
                st.success(f"Thanks {prov_name}! Your profile is under review. We'll notify you within 24 hours. 🎉")
            else:
                st.warning("Please fill in at least your name and bio.")
