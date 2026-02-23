import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

from data.providers import SAMPLE_REVIEWS, HOURS_MAP, TIME_SLOTS
from utils.matching import get_score_breakdown


DAY_MAP = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def _next_date_for_day(day_label: str) -> datetime:
    """Return the next calendar date that falls on the given weekday label."""
    today = datetime.today()
    target = DAY_MAP[day_label]
    days_ahead = (target - today.weekday()) % 7 or 7
    return today + timedelta(days=days_ahead)


def render_booking(go_to):
    p = st.session_state.selected_provider

    if st.button("← Back to search"):
        go_to("home")
        st.rerun()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero">
        <h1>{p['avatar']} Book {p['name']}</h1>
        <p>
            {p['category']} · {p['experience']} years experience ·
            {p['distance']} km away ·
            <span style="color:#e8c547;">€{p['price']}/hr</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    # ── Left: customer details ────────────────────────────────────────────────
    with col1:
        st.markdown('<div class="section-title">Your Details</div>', unsafe_allow_html=True)

        name     = st.text_input("Your full name")
        address  = st.text_input("Service address")
        _        = st.text_input("Phone number")
        job_desc = st.text_area(
            "Describe the job",
            placeholder="e.g. Fix a leaking pipe under the kitchen sink…",
            height=100,
        )
        job_size = st.select_slider(
            "Estimated job size",
            options=list(HOURS_MAP.keys()),
        )

        est_hours = HOURS_MAP[job_size]
        est_cost  = est_hours * p["price"]
        st.metric("Estimated cost", f"€{est_cost}", f"~{est_hours}h × €{p['price']}/hr")

    # ── Right: slot picker + AI breakdown ────────────────────────────────────
    with col2:
        st.markdown('<div class="section-title">Pick a Slot</div>', unsafe_allow_html=True)

        selected_day = st.radio("Available days", p["availability"], horizontal=True)
        booking_date = _next_date_for_day(selected_day)
        st.caption(f"Next available: **{booking_date.strftime('%A, %d %B %Y')}**")

        # Simulate some taken slots
        random.seed(p["id"])
        taken           = random.sample(TIME_SLOTS, 3)
        available_slots = [t for t in TIME_SLOTS if t not in taken]
        selected_time   = st.select_slider("Choose a time slot", options=available_slots)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**AI Match Summary**")
        st.progress(int(p["score"]) / 100, text=f"⚡ {p['score']}% match for your request")

        breakdown    = get_score_breakdown(p, max_price=60, max_distance=5, preferred_day=selected_day)
        breakdown_df = pd.DataFrame.from_dict(breakdown, orient="index", columns=["Score"])
        st.bar_chart(breakdown_df)

        st.markdown("**Provider reviews**")
        for reviewer, review in SAMPLE_REVIEWS:
            st.markdown(f'> *\u201c{review}\u201d* \u2014 **{reviewer}**')

    # ── Confirm button ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Confirm Booking", use_container_width=True, type="primary"):
        if name and address and job_desc:
            st.session_state.booking_confirmed = True
        else:
            st.warning("Please fill in your name, address and job description.")

    if st.session_state.get("booking_confirmed"):
        st.markdown(f"""
        <div class="confirm-box">
            <div style="font-size:2.5rem;">🎉</div>
            <h3>Booking Confirmed!</h3>
            <p style="color:#a0a0b8;">
                Your booking with <strong style="color:white;">{p['name']}</strong> is confirmed for
                <strong style="color:#e8c547;">{booking_date.strftime('%A, %d %B')} at {selected_time}</strong>.
            </p>
            <p style="color:#a0a0b8; font-size:0.9rem;">
                A confirmation has been sent. Estimated cost:
                <strong style="color:white;">€{est_cost}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to home", use_container_width=True):
            go_to("home")
            st.rerun()
