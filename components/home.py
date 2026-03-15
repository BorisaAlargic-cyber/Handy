import streamlit as st
from data.providers import PROVIDERS, CATEGORIES, DAYS
from utils.matching import filter_and_rank
from utils.llm import parse_job_request, explain_top_match


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

    # ── AI Natural Language Search ────────────────────────────────────────────
    st.markdown('<div class="section-title">🤖 Describe Your Job</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Tell us what you need in plain English — our AI will understand and find the right match.</div>',
        unsafe_allow_html=True,
    )

    ai_col, _ = st.columns([2, 1])
    with ai_col:
        job_text = st.text_area(
            "What do you need help with?",
            placeholder=(
                'e.g. "My bathroom pipe is leaking badly under the sink, need someone ASAP, '
                'budget around €40/hr, preferably close by"'
            ),
            height=90,
            key="ai_job_input",
            label_visibility="collapsed",
        )

        btn_col1, btn_col2 = st.columns([1, 3])
        with btn_col1:
            search_clicked = st.button("🔍 Find Matches", type="primary", use_container_width=True)
        with btn_col2:
            manual_toggle = st.checkbox("Use manual filters instead", value=False, key="manual_mode")

    # Parse & store results in session state
    if search_clicked and job_text.strip() and not manual_toggle:
        with st.spinner("🤖 Analysing your request..."):
            parsed = parse_job_request(job_text.strip())

        if parsed:
            st.session_state["ai_parsed"] = parsed
            st.session_state["ai_job_text"] = job_text.strip()
        else:
            st.error("Couldn't parse your request. Please try rephrasing or use manual filters.")
            st.session_state.pop("ai_parsed", None)

    # Show parsed params as a nice info box
    if "ai_parsed" in st.session_state and not manual_toggle:
        p = st.session_state["ai_parsed"]
        st.markdown(f"""
        <div class="ai-parse-box">
            <span class="ai-label">🤖 AI understood:</span>
            <span class="ai-chip">📋 {p['category']}</span>
            <span class="ai-chip">⏱ {p['urgency']}</span>
            <span class="ai-chip">💶 Max €{p['max_price']}/hr</span>
            <span class="ai-chip">📍 Within {p['max_distance']} km</span>
            <span class="ai-chip">⭐ Min {p['min_rating']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters + Results ─────────────────────────────────────────────────────
    left, right = st.columns([1, 2], gap="large")

    # Determine which params to use
    use_ai = "ai_parsed" in st.session_state and not manual_toggle
    ai_p   = st.session_state.get("ai_parsed", {})

    with left:
        st.markdown('<div class="section-title">🔧 Filters</div>', unsafe_allow_html=True)

        if use_ai:
            st.markdown('<div class="subtitle">Auto-filled from your request. Adjust if needed.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="subtitle">Set your preferences manually.</div>', unsafe_allow_html=True)

        category      = st.selectbox("Service category", CATEGORIES,
                                     index=CATEGORIES.index(ai_p.get("category", "All")) if use_ai else 0)
        preferred_day = st.select_slider("Preferred day", options=DAYS,
                                         value=ai_p.get("preferred_day", "Mon") if use_ai else "Mon")
        urgency_opts  = ["ASAP (today/tomorrow)", "This week", "Flexible"]
        urgency       = st.radio("When do you need it?", urgency_opts,
                                 index=urgency_opts.index(ai_p.get("urgency", "Flexible")) if use_ai else 2)
        max_price     = st.slider("Max hourly rate (€)", 20, 100,
                                  int(ai_p.get("max_price", 60)) if use_ai else 60, step=5)
        min_rating    = st.slider("Minimum rating", 4.0, 5.0,
                                  float(ai_p.get("min_rating", 4.5)) if use_ai else 4.5, step=0.1)
        max_distance  = st.slider("Max distance (km)", 1, 10,
                                  int(ai_p.get("max_distance", 5)) if use_ai else 5)

    with right:
        st.markdown('<div class="section-title">Top Providers</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Ranked by our AI matching score based on your preferences.</div>', unsafe_allow_html=True)

        results = filter_and_rank(
            PROVIDERS, category, max_price, min_rating, max_distance, preferred_day, urgency
        )

        if not results:
            st.info("No providers match your current filters. Try adjusting your criteria.")
        else:
            # Feature 1b: AI explanation for top match (only when AI search was used)
            if use_ai and results:
                job_summary = ai_p.get("job_summary", st.session_state.get("ai_job_text", ""))
                top = results[0]
                cache_key = f"explain_{top['id']}_{job_summary[:40]}"

                if cache_key not in st.session_state:
                    with st.spinner("✨ Generating personalised recommendation..."):
                        explanation = explain_top_match(job_summary, top)
                    st.session_state[cache_key] = explanation

                explanation = st.session_state.get(cache_key, "")
                if explanation:
                    st.markdown(f"""
                    <div class="ai-explain-box">
                        <div class="ai-explain-title">🤖 Why {top['name']} is your best match</div>
                        <div class="ai-explain-body">{explanation}</div>
                    </div>
                    """, unsafe_allow_html=True)

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
