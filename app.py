import streamlit as st

from styles.css import inject_css
from components.home import render_home
from components.booking import render_booking

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Handy – Home Services",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject global styles ──────────────────────────────────────────────────────
inject_css()

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = None
if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False


# ── Navigation helper ─────────────────────────────────────────────────────────
def go_to(page: str, provider=None):
    st.session_state.page = page
    if provider:
        st.session_state.selected_provider = provider
    st.session_state.booking_confirmed = False


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home(go_to)

elif st.session_state.page == "booking":
    render_booking(go_to)
