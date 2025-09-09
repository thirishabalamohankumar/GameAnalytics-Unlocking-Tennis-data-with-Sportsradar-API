import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from db import run_query

def main():
    st.title("🏆 Competitions Analysis")

    try:
        # Basic competitions data
        df = run_query("SELECT * FROM competitions LIMIT 10;")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Recent Competitions")
            st.dataframe(df, use_container_width=True)

        with col2:
            # Competitions by category chart
            q_cat = """
            SELECT cat.category_name, COUNT(*) as competition_count
            FROM competitions c
            JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name
            ORDER BY competition_count DESC;
            """
            df_cat = run_query(q_cat)
            
            if not df_cat.empty:
                fig_cat = px.bar(
                    df_cat,
                    x="competition_count",
                    y="category_name",
                    orientation='h',
                    title="Competitions by Category",
                    color="competition_count",
                    color_continuous_scale="viridis"
                )
                fig_cat.update_layout(height=400)
                st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("---")

        # Competition-Category relationship
        q1 = """
        SELECT c.competition_name, cat.category_name
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        LIMIT 20;
        """
        df1 = run_query(q1)
        
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.subheader("🎯 Competitions with Categories")
            st.dataframe(df1, use_container_width=True)

        with col4:
            # Sunburst chart for competition hierarchy
            if not df1.empty:
                fig_sunburst = px.sunburst(
                    df1,
                    path=['category_name', 'competition_name'],
                    title="Competition Hierarchy",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_sunburst.update_layout(height=400)
                st.plotly_chart(fig_sunburst, use_container_width=True)

        st.markdown("---")

        # Additional analytics
        st.subheader("📊 Competition Analytics")
        
        col5, col6 = st.columns(2)
        
        with col5:
            # Competition timeline (if date fields exist)
            try:
                q_timeline = """
                SELECT 
                    cat.category_name,
                    COUNT(*) as total_competitions,
                    COUNT(DISTINCT c.competition_id) as unique_competitions
                FROM competitions c
                JOIN categories cat ON c.category_id = cat.category_id
                GROUP BY cat.category_name
                ORDER BY total_competitions DESC;
                """
                df_timeline = run_query(q_timeline)
                
                if not df_timeline.empty:
                    fig_polar = px.bar_polar(
                        df_timeline,
                        r="total_competitions",
                        theta="category_name",
                        color="unique_competitions",
                        title="Competition Distribution (Polar View)",
                        color_continuous_scale="plasma"
                    )
                    st.plotly_chart(fig_polar, use_container_width=True)
                    
            except Exception as e:
                st.info("Timeline analysis not available with current data structure")

        with col6:
            # Category distribution pie chart
            if not df_cat.empty:
                fig_pie = px.pie(
                    df_cat,
                    values="competition_count",
                    names="category_name",
                    title="Category Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

        # Competition metrics
        col7, col8, col9 = st.columns(3)
        
        total_comps = run_query("SELECT COUNT(*) as total FROM competitions;")
        total_cats = run_query("SELECT COUNT(DISTINCT category_id) as total FROM competitions;")
        
        with col7:
            st.metric("🏆 Total Competitions", int(total_comps["total"][0]))
        
        with col8:
            st.metric("📂 Total Categories", int(total_cats["total"][0]))
            
        with col9:
            avg_per_cat = int(total_comps["total"][0]) / int(total_cats["total"][0]) if int(total_cats["total"][0]) > 0 else 0
            st.metric("📊 Avg per Category", f"{avg_per_cat:.1f}")

    except Exception as e:
        st.error(f"Error: {e}")