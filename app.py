import streamlit as st
import importlib
from streamlit_option_menu import option_menu
from datetime import datetime
import random

# ----------------- App Config -----------------
st.set_page_config(
    page_title="🎾 Tennis Analytics Dashboard",
    page_icon="🎾",
    layout="wide"
)


# ----------------- Time-based Greeting -----------------
def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greetings = ["☀️ Good Morning, Champion!", "Rise & Shine 🎾", "Morning Ace, ready to smash data?"]
    elif 12 <= hour < 17:
        greetings = ["🌞 Good Afternoon!", "Let’s serve up insights 🏆", "Afternoon Grind 💪"]
    elif 17 <= hour < 21:
        greetings = ["🌇 Good Evening!", "Evening match analytics 🎾", "Ready for some evening stats?"]
    else:
        greetings = ["🌙 Night Owl Mode!", "Late-night analytics grind 🌌", "Smash data under the stars ⭐"]
    return random.choice(greetings)


# ----------------- Custom Styling -----------------
st.markdown("""
<style>
/* === Title Card Styling === */
.title-card {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); /* Professional dark teal gradient */
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    text-align: center;
    color: white;
}
.title-card h1 {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.title-card p {
    margin: 0.3rem 0;
    font-size: 1rem;
    color: #f1f1f1;
}
</style>
""", unsafe_allow_html=True)


# ----------------- Horizontal Navigation -----------------
page = option_menu(
    None,
    ["homepage", "competitions", "competitors", "country_analysis", "leaderboards", "venues"],
    icons=["house", "trophy", "people", "flag", "bar-chart", "map"],
    orientation="horizontal",
    default_index=0,
    menu_icon="cast"
)


# ----------------- Title Card (Fixed Background) -----------------
st.markdown(f"""
<div class="title-card">
    <h1>🎾 Tennis Analytics Hub</h1>
    <p>{get_time_based_greeting()} Game, Set, Analytics!</p>
    <p>🔑 Powered by SportsRadar API + PostgreSQL + Real-time Analytics</p>
    <p>📊 Live Tennis Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)


# ----------------- Dynamic Import -----------------
try:
    module = importlib.import_module(f"app_pages.{page}")  # If your files are in app_pages/
    if hasattr(module, "main"):
        module.main()
    else:
        st.error(f"⚠️ The page `{page}` does not have a main() function.")
except ModuleNotFoundError as e:
    st.error(f"❌ Could not load page `{page}`. Error: {str(e)}")
