import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from db import run_query

def main():
    # Enhanced header
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; margin: 0;">🏟️ Tennis Venues Analytics</h1>
            <p style="color: #34495e; margin: 10px 0 0 0;">Exploring Tennis Infrastructure & Facilities</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        # Check what tables and columns actually exist first
        try:
            # Test basic venue table
            df = run_query("SELECT * FROM venues LIMIT 10;")
            st.success("✅ Successfully connected to venues table")
            
            # Get column info
            columns_info = list(df.columns) if not df.empty else []
            st.info(f"Available columns: {', '.join(columns_info)}")
            
        except Exception as e:
            st.error(f"❌ Cannot access venues table: {e}")
            st.markdown("### 📋 Expected Database Structure")
            st.code("""
            Tables needed:
            1. venues (venue_id, venue_name, complex_id, ...)
            2. complexes (complex_id, complex_name, ...)
            """)
            return

        # Basic venue metrics (safe queries)
        try:
            total_venues = run_query("SELECT COUNT(*) as total FROM venues;")
            unique_complexes = run_query("SELECT COUNT(DISTINCT complex_id) as total FROM venues WHERE complex_id IS NOT NULL;")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏟️ Total Venues", int(total_venues["total"][0]))
            with col2:
                if not unique_complexes.empty and unique_complexes["total"][0] > 0:
                    st.metric("🏢 Unique Complexes", int(unique_complexes["total"][0]))
                else:
                    st.metric("🏢 Unique Complexes", "N/A")
            with col3:
                if not unique_complexes.empty and unique_complexes["total"][0] > 0:
                    venues_per_complex = int(total_venues["total"][0]) / int(unique_complexes["total"][0])
                    st.metric("📊 Venues per Complex", f"{venues_per_complex:.1f}")
                else:
                    st.metric("📊 Venues per Complex", "N/A")

        except Exception as e:
            st.warning(f"Could not calculate metrics: {e}")

        st.markdown("---")

        # Main content area
        col4, col5 = st.columns([1.2, 0.8])
        
        with col4:
            st.subheader("🏛️ Venue Directory")
            
            if not df.empty:
                # Display available data
                display_df = df.head(15)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=400
                )
            else:
                st.warning("No venue data available")

        with col5:
            st.subheader("📈 Venue Distribution")
            
            try:
                # Safe query for complex distribution
                q_complex_dist = """
                SELECT 
                    complex_id,
                    COUNT(*) as venue_count
                FROM venues
                WHERE complex_id IS NOT NULL
                GROUP BY complex_id
                ORDER BY venue_count DESC;
                """
                df_complex_dist = run_query(q_complex_dist)
                
                if not df_complex_dist.empty:
                    fig_dist = px.histogram(
                        df_complex_dist,
                        x="venue_count",
                        nbins=10,
                        title="Venues per Complex Distribution",
                        color_discrete_sequence=['#3498db'],
                        labels={"venue_count": "Number of Venues", "count": "Number of Complexes"}
                    )
                    fig_dist.update_layout(height=400)
                    st.plotly_chart(fig_dist, use_container_width=True)
                else:
                    st.info("No complex distribution data available")
            except Exception as e:
                st.warning(f"Distribution analysis unavailable: {e}")

        st.markdown("---")

        # Try to get venue-complex relationships if complexes table exists
        try:
            # Test if complexes table exists and join works
            q_test_join = """
            SELECT v.*, cx.complex_name
            FROM venues v
            LEFT JOIN complexes cx ON v.complex_id = cx.complex_id
            LIMIT 5;
            """
            df_test = run_query(q_test_join)
            
            if not df_test.empty:
                st.success("✅ Complex data available")
                
                # Full venue-complex relationship
                q1 = """
                SELECT v.venue_name, cx.complex_name, v.complex_id
                FROM venues v
                LEFT JOIN complexes cx ON v.complex_id = cx.complex_id
                ORDER BY cx.complex_name, v.venue_name
                LIMIT 50;
                """
                df1 = run_query(q1)
                
                col6, col7 = st.columns(2)
                
                with col6:
                    st.subheader("🏢 Venues with Complexes")
                    st.dataframe(df1.head(20), use_container_width=True, height=350)

                with col7:
                    st.subheader("🎯 Complex Network Analysis")
                    
                    # Create treemap
                    if 'complex_name' in df1.columns:
                        complex_summary = df1.groupby('complex_name').agg({
                            'venue_name': 'count',
                            'complex_id': 'first'
                        }).reset_index()
                        complex_summary.rename(columns={'venue_name': 'venue_count'}, inplace=True)
                        
                        # Remove null complex names
                        complex_summary = complex_summary.dropna(subset=['complex_name'])
                        
                        if not complex_summary.empty:
                            fig_treemap = px.treemap(
                                complex_summary.head(15),
                                path=[px.Constant("All Complexes"), 'complex_name'],
                                values='venue_count',
                                title="Complex Hierarchy by Venue Count",
                                color='venue_count',
                                color_continuous_scale='viridis'
                            )
                            fig_treemap.update_layout(height=350)
                            st.plotly_chart(fig_treemap, use_container_width=True)
                        else:
                            st.info("No complex hierarchy data available")

        except Exception as e:
            st.warning("⚠️ Complex relationship analysis unavailable")
            st.info("This usually means the 'complexes' table doesn't exist or the join failed")
            
            # Show basic venue analysis instead
            col6, col7 = st.columns(2)
            
            with col6:
                st.subheader("📊 Basic Venue Analysis")
                st.dataframe(df.head(20), use_container_width=True, height=350)

            with col7:
                st.subheader("📈 Venue ID Distribution")
                if 'venue_id' in df.columns and not df.empty:
                    fig_ids = px.histogram(
                        df.head(100),  # Limit for performance
                        x="venue_id",
                        title="Venue ID Distribution",
                        color_discrete_sequence=['#e74c3c']
                    )
                    fig_ids.update_layout(height=350)
                    st.plotly_chart(fig_ids, use_container_width=True)
                else:
                    st.info("No venue ID data available for analysis")

        st.markdown("---")

        # Advanced Analytics Section (Simplified)
        st.subheader("🔍 Venue Insights")
        
        col8, col9 = st.columns(2)
        
        with col8:
            # Venue count by complex (if available)
            try:
                complex_analysis = run_query("""
                SELECT 
                    complex_id,
                    COUNT(*) as venue_count
                FROM venues 
                WHERE complex_id IS NOT NULL
                GROUP BY complex_id
                ORDER BY venue_count DESC
                LIMIT 10;
                """)
                
                if not complex_analysis.empty:
                    fig_complex = px.bar(
                        complex_analysis,
                        x="complex_id",
                        y="venue_count",
                        title="Top Complexes by Venue Count",
                        color="venue_count",
                        color_continuous_scale="blues"
                    )
                    fig_complex.update_layout(height=400)
                    st.plotly_chart(fig_complex, use_container_width=True)
                else:
                    st.info("No complex analysis data available")
            except Exception as e:
                st.info("Complex analysis unavailable")

        with col9:
            # Simple venue statistics
            if not df.empty:
                venue_stats = {
                    "Total Venues": len(df),
                    "Unique Complex IDs": df['complex_id'].nunique() if 'complex_id' in df.columns else 0,
                    "Venues with Complex ID": df['complex_id'].notna().sum() if 'complex_id' in df.columns else 0,
                    "Venues without Complex": df['complex_id'].isna().sum() if 'complex_id' in df.columns else 0
                }
                
                # Create a simple metrics display
                st.write("**Venue Statistics:**")
                for stat, value in venue_stats.items():
                    st.metric(stat, value)
            else:
                st.info("No venue statistics available")

        # Data Quality Check
        st.markdown("---")
        st.subheader("🔧 Data Quality Check")
        
        if not df.empty:
            col10, col11 = st.columns(2)
            
            with col10:
                st.write("**Column Information:**")
                for col in df.columns:
                    non_null_count = df[col].notna().sum()
                    null_count = df[col].isna().sum()
                    st.write(f"- {col}: {non_null_count} non-null, {null_count} null")
                    
            with col11:
                st.write("**Sample Data:**")
                st.dataframe(df.head(5), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading venue data: {e}")
        st.markdown("### 🔧 Troubleshooting")
        st.write("""
        This error typically occurs when:
        1. The 'venues' table doesn't exist
        2. The 'complexes' table doesn't exist (for joins)
        3. Database connection issues
        4. Column names don't match expectations
        
        **Next steps:**
        1. Check your database tables exist
        2. Verify column names match your schema
        3. Ensure database connection is working
        """)