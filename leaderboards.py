import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from db import run_query

def main():
    # Enhanced header
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;">
            <h1 style="color: white; margin: 0;">🏆 Tennis Leaderboards</h1>
            <p style="color: #ffe6e6; margin: 10px 0 0 0;">Elite Performance Rankings & Analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Control panel
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("⚙️ **Controls**")
        n = st.selectbox(
            "Top N players:",
            options=[5, 10, 15, 20, 25, 30],
            index=1  # default to 10
        )
        
        chart_type = st.radio(
            "Chart Style:",
            ["Line Chart", "Bar Chart", "Area Chart"],
            index=0
        )

    with col2:
        # Quick stats
        total_players = run_query("SELECT COUNT(*) as total FROM competitors WHERE points IS NOT NULL;")
        top_points = run_query("SELECT MAX(points) as max_points FROM competitors;")
        countries = run_query("SELECT COUNT(DISTINCT country) as countries FROM competitors;")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🎾 Total Players", int(total_players["total"][0]))
        with col_b:
            st.metric("🏆 Highest Points", int(top_points["max_points"][0]))
        with col_c:
            st.metric("🌍 Countries", int(countries["countries"][0]))

    st.markdown("---")

    # Main leaderboards section
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(f"🔥 Top {n} Players by Points")
        q_points = f"""
            SELECT name, points, rank, country, tour_type, movement,
                   ROW_NUMBER() OVER (ORDER BY points DESC) as position
            FROM competitors
            WHERE points IS NOT NULL
            ORDER BY points DESC
            LIMIT {n};
        """
        df_points = run_query(q_points)

        if not df_points.empty:
            if chart_type == "Line Chart":
                fig_points = px.line(
                    df_points, 
                    x="position", 
                    y="points", 
                    hover_data=["name", "country", "rank"],
                    markers=True,
                    title=f"Points Progression - Top {n}",
                    color_discrete_sequence=['#ff6b6b']
                )
            elif chart_type == "Area Chart":
                fig_points = px.area(
                    df_points, 
                    x="position", 
                    y="points", 
                    hover_data=["name", "country", "rank"],
                    title=f"Points Distribution - Top {n}",
                    color_discrete_sequence=['#4ecdc4']
                )
            else:  # Bar Chart
                fig_points = px.bar(
                    df_points, 
                    x="position", 
                    y="points", 
                    hover_data=["name", "country", "rank"],
                    title=f"Points Rankings - Top {n}",
                    color="points",
                    color_continuous_scale="viridis"
                )
            
            fig_points.update_layout(height=400)
            st.plotly_chart(fig_points, use_container_width=True)
            
            st.dataframe(df_points[["position", "name", "points", "rank", "country", "tour_type"]], 
                        use_container_width=True, height=300)

    with col4:
        st.subheader(f"🏆 Top {n} Players by Rank")
        q_rank = f"""
            SELECT name, rank, points, country, tour_type, movement,
                   ROW_NUMBER() OVER (ORDER BY rank ASC) as position
            FROM competitors
            WHERE rank IS NOT NULL
            ORDER BY rank ASC
            LIMIT {n};
        """
        df_rank = run_query(q_rank)

        if not df_rank.empty:
            df_rank['rank_inverted'] = df_rank['rank'].max() - df_rank['rank'] + 1
            
            if chart_type == "Line Chart":
                fig_rank = px.line(
                    df_rank, 
                    x="position", 
                    y="rank_inverted", 
                    hover_data=["name", "country", "rank", "points"],
                    markers=True,
                    title=f"Rank Progression - Top {n}",
                    color_discrete_sequence=['#45b7d1']
                )
            elif chart_type == "Area Chart":
                fig_rank = px.area(
                    df_rank, 
                    x="position", 
                    y="rank_inverted", 
                    hover_data=["name", "country", "rank", "points"],
                    title=f"Rank Distribution - Top {n}",
                    color_discrete_sequence=['#96ceb4']
                )
            else:  # Bar Chart
                fig_rank = px.bar(
                    df_rank, 
                    x="position", 
                    y="rank_inverted", 
                    hover_data=["name", "country", "rank", "points"],
                    title=f"Rank Performance - Top {n}",
                    color="points",
                    color_continuous_scale="plasma"
                )
            
            fig_rank.update_layout(height=400, yaxis_title="Rank Performance Score")
            st.plotly_chart(fig_rank, use_container_width=True)
            
            st.dataframe(df_rank[["position", "name", "rank", "points", "country", "tour_type"]], 
                        use_container_width=True, height=300)

    # ----------------------
    # New Analysis Section
    # ----------------------
    st.markdown("---")
    st.subheader("🌍 Country Dominance in Leaderboards")

    q_country_dom = f"""
        SELECT country, COUNT(*) as player_count, AVG(points) as avg_points
        FROM (
            SELECT name, country, points, rank
            FROM competitors
            WHERE rank IS NOT NULL
            ORDER BY rank ASC
            LIMIT {n}
        ) sub
        GROUP BY country
        ORDER BY player_count DESC, avg_points DESC
        LIMIT 10;
    """
    df_country_dom = run_query(q_country_dom)

    if not df_country_dom.empty:
        fig_country_dom = px.bar(
            df_country_dom,
            x="country",
            y="player_count",
            text="player_count",
            color="avg_points",
            color_continuous_scale="Blues",
            title=f"Top {n} Leaderboard Representation by Country"
        )
        fig_country_dom.update_traces(textposition="outside")
        fig_country_dom.update_layout(height=400)
        st.plotly_chart(fig_country_dom, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Consistency & Stability of Players")

    q_consistency = f"""
        SELECT name, rank, points, country, movement
        FROM competitors
        WHERE rank IS NOT NULL AND points IS NOT NULL
        ORDER BY points DESC
        LIMIT {n*3};
    """
    df_consistency = run_query(q_consistency)

    if not df_consistency.empty:
        df_consistency["movement_num"] = pd.to_numeric(df_consistency["movement"], errors="coerce")

        fig_consistency = px.scatter(
            df_consistency,
            x="rank",
            y="points",
            size="movement_num",
            color="movement_num",
            hover_data=["name", "country", "movement"],
            title="Player Stability (Bubble size = Movement)",
            color_continuous_scale="RdYlGn_r"
        )
        fig_consistency.update_layout(height=400)
        st.plotly_chart(fig_consistency, use_container_width=True)

    # ----------------------
    # Movement Analysis - FIXED
    # ----------------------
    st.markdown("---")
    st.subheader("📈 Movement & Momentum Analysis")
    
    col7, col8 = st.columns(2)
    
    with col7:
        try:
            q_movement = """
                SELECT 
                    CASE 
                        WHEN movement ~ '^-?[0-9]+$' THEN CAST(movement AS INTEGER)
                        ELSE NULL 
                    END as movement_int,
                    COUNT(*) as count, 
                    AVG(points) as avg_points
                FROM competitors
                WHERE movement IS NOT NULL AND movement ~ '^-?[0-9]+$'
                GROUP BY movement_int
                ORDER BY movement_int;
            """
            df_movement = run_query(q_movement)
            
            if not df_movement.empty:
                fig_movement = go.Figure()
                
                fig_movement.add_trace(go.Bar(
                    x=df_movement['movement_int'],
                    y=df_movement['count'],
                    name='Player Count',
                    yaxis='y',
                    marker_color='lightblue',
                    opacity=0.8
                ))
                
                fig_movement.add_trace(go.Scatter(
                    x=df_movement['movement_int'],
                    y=df_movement['avg_points'],
                    mode='lines+markers',
                    name='Avg Points',
                    yaxis='y2',
                    line=dict(color='red', width=3)
                ))
                
                fig_movement.update_layout(
                    title="Movement Distribution & Average Points",
                    xaxis_title="Movement",
                    yaxis=dict(title="Number of Players", side="left"),
                    yaxis2=dict(title="Average Points", side="right", overlaying="y"),
                    height=400
                )
                
                st.plotly_chart(fig_movement, use_container_width=True)
            else:
                st.info("No valid movement data available")
        except Exception as e:
            st.warning(f"Movement analysis unavailable: {str(e)}")

    with col8:
        try:
            # FIXED: Cast movement to integer with proper error handling
            q_top_movers = f"""
                SELECT name, movement, points, rank, country,
                       CASE 
                           WHEN movement ~ '^[0-9]+$' THEN CAST(movement AS INTEGER)
                           ELSE 0 
                       END as movement_int
                FROM competitors
                WHERE movement IS NOT NULL 
                  AND movement ~ '^[0-9]+$'
                  AND CAST(movement AS INTEGER) > 0
                ORDER BY CAST(movement AS INTEGER) DESC
                LIMIT {min(n, 10)};
            """
            df_top_movers = run_query(q_top_movers)
            
            if not df_top_movers.empty:
                fig_movers = px.bar(
                    df_top_movers,
                    x="name",
                    y="movement_int",
                    color="points",
                    title="Top Positive Movers",
                    labels={"movement_int": "Ranking Movement", "name": "Player"},
                    color_continuous_scale="greens"
                )
                fig_movers.update_layout(
                    height=400,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_movers, use_container_width=True)
            else:
                st.info("No positive movement data available")
        except Exception as e:
            st.warning(f"Top movers analysis unavailable: {str(e)}")