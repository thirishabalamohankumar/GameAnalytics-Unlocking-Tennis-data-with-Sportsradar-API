import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db import run_query

def main():
    st.title("👤 Competitor Profile & Rankings")

    # Dropdown for competitors
    competitors = run_query("SELECT DISTINCT name FROM competitors ORDER BY name;")
    competitor_list = competitors["name"].tolist() if not competitors.empty else []

    if competitor_list:
        selected = st.selectbox("Select a Competitor", competitor_list)
    else:
        st.warning("⚠️ No competitors available in database.")
        return

    # Fetch competitor ranking
    q = f"""
        SELECT name, country, rank, points, movement
        FROM competitors
        WHERE name = '{selected}';
    """
    df = run_query(q)

    if df.empty:
        st.warning("⚠️ No ranking data available for this competitor.")
        return

    comp = df.iloc[0]

    # --- Profile Card ---
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:20px; border-radius:12px; margin-bottom:20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 style="margin:0; color:#fff;">{comp['name']}</h2>
            <p style="margin:0; color:#f0f0f0; font-size:16px;">{comp['country']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Stats Row (Rank, Points, Movement) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Rank", int(comp["rank"]))
    with col2:
        st.metric("🏆 Points", int(comp["points"]))
    with col3:
        st.metric("🔄 Movement", comp["movement"])

    st.markdown("---")

    # --- Performance Comparison Analysis ---
    st.subheader("🎯 Performance vs Country Average")

    q_country_avg = f"""
        SELECT 
            AVG(points) as avg_points,
            AVG(rank) as avg_rank,
            COUNT(*) as total_players
        FROM competitors
        WHERE country = '{comp['country']}' AND points IS NOT NULL AND rank IS NOT NULL;
    """
    df_country_avg = run_query(q_country_avg)

    if not df_country_avg.empty:
        country_avg = df_country_avg.iloc[0]

        categories = ['Points Ratio', 'Rank Performance']
        player_values = [
            comp['points'] / country_avg['avg_points'] if country_avg['avg_points'] > 0 else 1,
            country_avg['avg_rank'] / comp['rank'] if comp['rank'] > 0 else 1
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=player_values,
            theta=categories,
            fill='toself',
            name=comp['name'],
            line_color='rgb(102, 126, 234)'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=[1, 1],
            theta=categories,
            fill='toself',
            name='Country Average',
            line_color='rgb(255, 165, 0)',
            opacity=0.6
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(player_values + [1.5])])
            ),
            height=350,
            title=f"vs {comp['country']} Average"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # --- Global Rank vs Points ---
    st.subheader("📊 Global Rank vs Points Analysis")

    q_global = """
        SELECT name, country, rank, points
        FROM competitors
        WHERE rank IS NOT NULL AND points IS NOT NULL
        ORDER BY points DESC
        LIMIT 200;
    """
    df_global = run_query(q_global)

    if not df_global.empty:
        fig_global = px.scatter(
            df_global,
            x="rank",
            y="points",
            color="country",
            hover_data=["name", "country"],
            title="Rank vs Points (Top 200 Players)"
        )

        selected_row = df_global[df_global['name'] == comp['name']]
        if not selected_row.empty:
            fig_global.add_annotation(
                x=selected_row['rank'].iloc[0],
                y=selected_row['points'].iloc[0],
                text=comp['name'],
                showarrow=True,
                arrowhead=2,
                arrowcolor="red"
            )

        fig_global.update_layout(height=400)
        st.plotly_chart(fig_global, use_container_width=True)

    # --- Country Peer Comparison ---
    st.markdown("---")
    st.subheader(f"🇨🇮 Competitor vs Peers from {comp['country']}")

    q_country_peers = f"""
        SELECT name, points
        FROM competitors
        WHERE country = '{comp['country']}' AND points IS NOT NULL
        ORDER BY points DESC
        LIMIT 10;
    """
    df_country_peers = run_query(q_country_peers)

    if not df_country_peers.empty:
        colors = ['#FF6B6B' if n == comp['name'] else '#4ECDC4' for n in df_country_peers['name']]

        fig_country = px.bar(
            df_country_peers,
            x="points",
            y="name",
            orientation="h",
            title=f"Top Players from {comp['country']}",
            color=colors,
            color_discrete_map="identity",
            text="points"
        )
        fig_country.update_traces(textposition="outside")
        fig_country.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_country, use_container_width=True)

    # --- Regional Competition Analysis ---
    st.markdown("---")
    st.subheader("🌍 Regional Competition Landscape")

    col6, col7 = st.columns(2)

    with col6:
        q_region = f"""
            SELECT name, points, rank
            FROM competitors
            WHERE country = '{comp['country']}' AND points IS NOT NULL
            ORDER BY points DESC
            LIMIT 15;
        """
        df_region = run_query(q_region)

        if not df_region.empty:
            colors = ['#FF6B6B' if name == comp['name'] else '#4ECDC4' for name in df_region['name']]

            fig_scatter = px.scatter(
                df_region,
                x="rank",
                y="points",
                hover_data=["name"],
                title=f"Players from {comp['country']}",
                color=colors,
                color_discrete_map="identity"
            )

            selected_row = df_region[df_region['name'] == comp['name']]
            if not selected_row.empty:
                fig_scatter.add_annotation(
                    x=selected_row['rank'].iloc[0],
                    y=selected_row['points'].iloc[0],
                    text=comp['name'],
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="red"
                )

            fig_scatter.update_layout(height=350)
            st.plotly_chart(fig_scatter, use_container_width=True)

    with col7:
        q_movement = """
            SELECT movement, COUNT(*) as count
            FROM competitors
            WHERE movement IS NOT NULL
            GROUP BY movement
            ORDER BY movement;
        """
        df_movement = run_query(q_movement)

        if not df_movement.empty:
            fig_movement = px.histogram(
                df_movement,
                x="movement",
                nbins=20,
                title="Global Movement Distribution",
                color_discrete_sequence=['#3498db']
            )

            if pd.notna(comp['movement']):
                try:
                    movement_val = float(comp['movement'])
                    fig_movement.add_vline(
                        x=movement_val,
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"{comp['name']}"
                    )
                except ValueError:
                    st.info(f"⚠️ Movement value '{comp['movement']}' is not numeric, cannot highlight on chart.")

            fig_movement.update_layout(height=350)
            st.plotly_chart(fig_movement, use_container_width=True)
