import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import random
from db import run_query


def get_time_based_greeting():
    """Generate time-based greeting messages"""
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        greetings = [
            "Good Morning, Tennis Enthusiast!",
            "Rise and Serve! Ready for Analytics?",
            "Morning Champion! Let's ace this data!"
        ]
    elif 12 <= current_hour < 17:
        greetings = [
            "Good Afternoon! Game, Set, Analytics!",
            "Ready to smash through some data?",
            "Afternoon Ace! Let's serve up insights!"
        ]
    elif 17 <= current_hour < 21:
        greetings = [
            "Good Evening! Time for Victory Analytics!",
            "Evening Champion! Let's dominate the data!",
            "Ready for your evening training session?"
        ]
    else:
        greetings = [
            "Late Night Analytics Session!",
            "Burning the midnight oil? Let's go!",
            "Night Owl Mode: Data Championship!"
        ]
    
    return random.choice(greetings)


def create_hero_section():
    """Beautiful, compact hero section"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1.2rem;
        background: linear-gradient(120deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    .main-header h1 {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }
    .main-header h2 {
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 0.8rem;
        opacity: 0.95;
    }
    .main-header p {
        font-size: 0.9rem;
        margin: 0.2rem 0;
        opacity: 0.9;
    }
    .tennis-ball {
        position: absolute;
        top: -20px;
        right: -20px;
        width: 70px;
        height: 70px;
        background: radial-gradient(circle at 30% 30%, #ffeb3b, #fbc02d);
        border-radius: 50%;
        box-shadow: inset -5px -5px 10px rgba(0,0,0,0.25);
        animation: floatBall 4s ease-in-out infinite;
    }
    @keyframes floatBall {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(10px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    


def create_stats_ticker():
    """Modern, compact stats ticker"""
    st.markdown("""
    <style>
    .ticker {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: glowPulse 3s infinite;
    }
    @keyframes glowPulse {
        0% { box-shadow: 0 0 8px rgba(30,60,114,0.6); }
        50% { box-shadow: 0 0 18px rgba(42,82,152,0.9); }
        100% { box-shadow: 0 0 8px rgba(30,60,114,0.6); }
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        
        total_competitors = run_query("SELECT COUNT(*) as total FROM competitors;")["total"][0]
        countries = run_query("SELECT COUNT(DISTINCT country) as total FROM competitors WHERE country IS NOT NULL;")["total"][0]
        top_points = run_query("SELECT MAX(points) as max FROM competitors WHERE points IS NOT NULL;")["max"][0]
        
        st.markdown(f"""
        <div class="ticker">
            ⏱️ Last Update: <b>{current_time}</b> | 
            👥 <b>{total_competitors}</b> Players | 
            🌍 <b>{countries}</b> Countries | 
            🏆 Highest Points: <b>{int(top_points):,}</b> | 
            📡 Status: <span style="color:#4caf50; font-weight:bold;">ONLINE</span>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception:
        st.markdown("""
        <div class="ticker">
            🔄 Loading live data stream...
        </div>
        """, unsafe_allow_html=True)


def main():
    # Hero + ticker
    create_hero_section()
    create_stats_ticker()

    # Dashboard title
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📈 Championship Dashboard Overview</h2>", unsafe_allow_html=True)

    # === Metrics Section ===
    try:
        df1 = run_query("SELECT COUNT(*) AS total_competitors FROM competitors;")
        df2 = run_query("SELECT COUNT(DISTINCT country) AS countries FROM competitors WHERE country IS NOT NULL;")
        df3 = run_query("SELECT MAX(points) AS highest_points FROM competitors WHERE points IS NOT NULL;")
        df4 = run_query("SELECT AVG(points) AS avg_points FROM competitors WHERE points IS NOT NULL;")

        st.markdown("""
        <style>
        .metric-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 0.3rem;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🏃‍♂️ Total Athletes</div>
                <div class="metric-value">{int(df1['total_competitors'][0]):,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🌍 Countries</div>
                <div class="metric-value">{int(df2['countries'][0])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🏆 Highest Points</div>
                <div class="metric-value">{int(df3['highest_points'][0]):,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">📊 Average Points</div>
                <div class="metric-value">{int(df4['avg_points'][0]):,}</div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading metrics: {e}")

    st.divider()

    # === Leaderboard Section ===
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🎾 Championship Leaderboard 🏆</h2>", unsafe_allow_html=True)
    try:
        df_top = run_query("""
            SELECT name, points, country, rank
            FROM competitors
            WHERE points IS NOT NULL
            ORDER BY points DESC
            LIMIT 8;
        """)

        if not df_top.empty:
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.subheader("🏅 Elite Championship Rankings")
                fig = px.bar(
                    df_top,
                    x="name",
                    y="points",
                    text="points",
                    color="points",
                    color_continuous_scale="Viridis",
                    title=""
                )
                fig.update_traces(
                    texttemplate='%{text:,}',
                    textposition="outside"
                )
                fig.update_layout(
                    height=400,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    margin=dict(l=30, r=30, t=30, b=30),
                    plot_bgcolor="white"
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                st.subheader("🎯 Top 3 Champions")
                st.markdown("""
                <style>
                .champ-card {
                    background: linear-gradient(135deg, #ff9966, #ff5e62);
                    color: white;
                    padding: 1rem;
                    border-radius: 12px;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                </style>
                """, unsafe_allow_html=True)

                for idx, (_, player) in enumerate(df_top.head(3).iterrows()):
                    medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉"
                    st.markdown(f"""
                    <div class="champ-card">
                        <b>{medal} #{idx+1} {player['name']}</b><br>
                        🎾 {int(player['points']):,} pts | 🌍 {player['country']}
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"Could not load top players: {e}")

    st.divider()

    # === World Map Section ===
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🌍 Global Tennis Network</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d;'>Discover tennis talent across the globe</p>", unsafe_allow_html=True)

    try:
        df_countries = run_query("""
            SELECT country AS country_name, 
                   COUNT(*) AS total_competitors,
                   AVG(points) as avg_points,
                   MAX(points) as max_points
            FROM competitors
            WHERE country IS NOT NULL AND points IS NOT NULL
            GROUP BY country
            ORDER BY total_competitors DESC;
        """)

        if not df_countries.empty:
            col_map, col_stats = st.columns([2, 1])
            
            with col_map:
                fig_map = px.choropleth(
                    df_countries,
                    locations="country_name",
                    locationmode="country names",
                    color="total_competitors",
                    hover_name="country_name",
                    hover_data={"avg_points": ":.0f", "max_points": ":.0f"},
                    color_continuous_scale="Viridis"
                )
                fig_map.update_layout(
                    height=400,
                    geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig_map, use_container_width=True)

            with col_stats:
                st.subheader("🌟 Top 5 Countries")
                st.markdown("""
                <style>
                .country-card {
                    background: linear-gradient(135deg, #36d1dc, #5b86e5);
                    color: white;
                    padding: 1rem;
                    border-radius: 12px;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                </style>
                """, unsafe_allow_html=True)

                top_countries = df_countries.head(5)
                for idx, (_, country) in enumerate(top_countries.iterrows()):
                    st.markdown(f"""
                    <div class="country-card">
                        <b>#{idx+1} {country['country_name']}</b><br>
                        👥 {int(country['total_competitors'])} players<br>
                        📊 Avg: {int(country['avg_points']):,} pts
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"Could not load world map: {e}")

    # === Footer ===
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 15px;'>
        <h2>🚀 Ready to Dive Deeper?</h2>
        <p>Explore detailed analytics, competitor profiles, and championship insights!</p>
        <p>🏆 Leaderboards | 👥 Player Profiles | 🌍 Country Analysis | 🏟️ Venues & Tournaments</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
