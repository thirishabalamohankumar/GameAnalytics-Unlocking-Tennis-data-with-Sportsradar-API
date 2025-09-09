import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from db import run_query

def main():
    # Enhanced title with gradient background
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.1);">
            <h1 style="color: white; margin: 0; font-size: 2.5em;">🌍 Global Tennis Analytics</h1>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 1.2em;">Exploring Tennis Talent Across Nations</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        # Main country data query
        q = """
        SELECT 
            country, 
            COUNT(*) AS competitors,
            AVG(points) as avg_points,
            AVG(rank) as avg_rank,
            MAX(points) as top_points
        FROM competitors
        WHERE country IS NOT NULL AND points IS NOT NULL AND rank IS NOT NULL
        GROUP BY country
        HAVING COUNT(*) >= 1
        ORDER BY competitors DESC;
        """
        df = run_query(q)

        if df.empty:
            st.error("No country data available")
            return

        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_countries = len(df)
            st.metric("🏛️ Countries", total_countries)
            
        with col2:
            total_competitors = df['competitors'].sum()
            st.metric("👥 Total Players", int(total_competitors))
            
        with col3:
            top_country = df.iloc[0]['country']
            st.metric("🥇 Leading Nation", top_country)
            
        with col4:
            avg_per_country = df['competitors'].mean()
            st.metric("📊 Avg per Country", f"{avg_per_country:.1f}")

        st.markdown("---")

        # Main visualization section
        col5, col6 = st.columns([1.2, 0.8])
        
        with col5:
            st.subheader("🎯 Competitors Distribution by Country")
            
            # Enhanced bar chart with country flags concept
            fig_bar = px.bar(
                df.head(15),  # Top 15 countries
                x="competitors",
                y="country",
                orientation='h',
                color="avg_points",
                color_continuous_scale="viridis",
                title="Top 15 Countries by Player Count",
                labels={"avg_points": "Avg Points", "competitors": "Number of Players"},
                text="competitors"
            )
            
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col6:
            st.subheader("💎 Quality vs Quantity")
            
            # Bubble chart: competitors vs avg_points
            fig_bubble = px.scatter(
                df,
                x="competitors",
                y="avg_points",
                size="top_points",
                color="avg_rank",
                hover_name="country",
                hover_data={"competitors": True, "avg_points": ":.1f", "top_points": True},
                title="Country Performance Matrix",
                labels={
                    "competitors": "Number of Players",
                    "avg_points": "Average Points",
                    "avg_rank": "Avg Rank"
                },
                color_continuous_scale="RdYlBu_r"
            )
            
            fig_bubble.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bubble, use_container_width=True)

        st.markdown("---")

        # Performance Analysis Section
        col7, col8 = st.columns(2)
        
        with col7:
            st.subheader("🏆 Elite Performance Analysis")
            
            # Countries with highest average points
            top_performers = df.nlargest(10, 'avg_points')
            
            fig_radar_countries = go.Figure()
            
            # Create radar chart for top 5 performing countries
            for i, (_, country_data) in enumerate(top_performers.head(5).iterrows()):
                fig_radar_countries.add_trace(go.Scatterpolar(
                    r=[
                        country_data['competitors'],
                        country_data['avg_points'] / 100,  # Normalized
                        (1000 - country_data['avg_rank']) / 10,  # Inverted and normalized
                        country_data['top_points'] / 1000  # Normalized
                    ],
                    theta=['Player Count', 'Avg Points (÷100)', 'Rank Quality (÷10)', 'Peak Points (÷1000)'],
                    fill='toself',
                    name=country_data['country'],
                    opacity=0.7
                ))
            
            fig_radar_countries.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(top_performers['competitors'].max(), 50)])
                ),
                height=400,
                title="Top 5 Countries - Multi-dimensional Performance"
            )
            st.plotly_chart(fig_radar_countries, use_container_width=True)

        with col8:
            st.subheader("📈 Distribution Patterns")
            
            # Histogram of competitors per country
            fig_hist = px.histogram(
                df,
                x="competitors",
                nbins=20,
                title="Distribution of Players per Country",
                color_discrete_sequence=['#FF6B6B']
            )
            
            fig_hist.add_vline(
                x=df['competitors'].mean(),
                line_dash="dash",
                line_color="blue",
                annotation_text=f"Average: {df['competitors'].mean():.1f}"
            )
            
            fig_hist.update_layout(
                height=200,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Box plot for points distribution
            st.subheader("🎪 Points Distribution Ranges")
            fig_box = px.box(
                df,
                y="avg_points",
                title="Average Points Distribution Across Countries",
                color_discrete_sequence=['#4ECDC4']
            )
            fig_box.update_layout(
                height=200,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("---")

        # Detailed Country Rankings Table
        st.subheader("📋 Comprehensive Country Rankings")
        
        # Create performance score
        df['performance_score'] = (
            (df['competitors'] / df['competitors'].max()) * 0.3 +
            (df['avg_points'] / df['avg_points'].max()) * 0.4 +
            ((df['avg_rank'].max() - df['avg_rank']) / df['avg_rank'].max()) * 0.3
        ) * 100
        
        df_display = df.copy()
        df_display['avg_points'] = df_display['avg_points'].round(1)
        df_display['avg_rank'] = df_display['avg_rank'].round(1)
        df_display['performance_score'] = df_display['performance_score'].round(1)
        
        # Style the dataframe
        styled_df = df_display[['country', 'competitors', 'avg_points', 'avg_rank', 'top_points', 'performance_score']].head(20)
        
        # Color coding for better visualization
        def highlight_top(val, column):
            if column == 'performance_score':
                if val >= 80:
                    return 'background-color: #90EE90'  # Light green
                elif val >= 60:
                    return 'background-color: #FFE4B5'  # Light orange
            return ''

        st.dataframe(
            styled_df.style.format({
                'avg_points': '{:.1f}',
                'avg_rank': '{:.1f}',
                'performance_score': '{:.1f}'
            }),
            use_container_width=True,
            height=400
        )

        # Interactive Country Selector for Deep Dive
        st.markdown("---")
        st.subheader("🔍 Country Deep Dive")
        
        selected_country = st.selectbox(
            "Select a country for detailed analysis:",
            options=df['country'].tolist(),
            index=0
        )
        
        if selected_country:
            country_data = df[df['country'] == selected_country].iloc[0]
            
            col9, col10, col11 = st.columns(3)
            
            with col9:
                st.metric("👥 Players", int(country_data['competitors']))
                st.metric("🏆 Avg Points", f"{country_data['avg_points']:.1f}")
            
            with col10:
                rank_position = df[df['country'] == selected_country].index[0] + 1
                st.metric("🥇 Global Rank", f"#{rank_position}")
                st.metric("📊 Avg Rank", f"{country_data['avg_rank']:.1f}")
            
            with col11:
                st.metric("⭐ Top Points", int(country_data['top_points']))
                st.metric("🎯 Performance Score", f"{country_data['performance_score']:.1f}")

    except Exception as e:
        st.error(f"Error loading country analysis: {e}")
        st.info("Please check if the database connection is working properly.")