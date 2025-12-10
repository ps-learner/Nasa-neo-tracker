import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from project_sql_queries import QUERIES

# Page config
st.set_page_config(
    page_title="NASA NEO Tracker",
    page_icon=r"C:\Users\praty\OneDrive\Pictures\Screenshots\Screenshot 2025-12-11 001034.png",
    layout="wide"
)

# Custom CSS - Enhanced
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #667eea;
        padding: 20px;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .metric-card {
        background: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Color scheme
COLORS = {
    'primary': '#667eea',
    'danger': '#ef4444',
    'safe': '#10b981',
    'warning': '#f59e0b',
    'info': '#3b82f6'
}

# Database connection
@st.cache_resource
def get_db():
    return sqlite3.connect(r"C:\Users\praty\OneDrive\Desktop\Personal projects\Mini project1 - NASA NEOT\nasa_neo.db", check_same_thread=False)

def run_query(query):
    try:
        return pd.read_sql(query, get_db()), None
    except Exception as e:
        return None, str(e)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image(r"C:\Users\praty\OneDrive\Pictures\Screenshots\Screenshot 2025-12-11 002303.png", width=275)
with col2:
    st.markdown('<h1 class="main-header">NASA Near-Earth Object Tracker</h1>', unsafe_allow_html=True)

st.markdown("**Advanced Intelligence System for Asteroid Monitoring**")
st.markdown("---")

# Get stats with trends
@st.cache_data(ttl=600)
def get_stats():
    conn = get_db()
    total_asteroids = pd.read_sql("SELECT COUNT(*) as c FROM asteroids", conn)['c'][0]
    total_approaches = pd.read_sql("SELECT COUNT(*) as c FROM close_approach", conn)['c'][0]
    hazardous = pd.read_sql("SELECT COUNT(*) as c FROM asteroids WHERE is_potentially_hazardous_asteroid=1", conn)['c'][0]
    
    # Get most dangerous
    most_dangerous = pd.read_sql("""
        SELECT name, estimated_diameter_max_km 
        FROM asteroids 
        WHERE is_potentially_hazardous_asteroid=1 
        ORDER BY estimated_diameter_max_km DESC LIMIT 1
    """, conn)
    
    return total_asteroids, total_approaches, hazardous, most_dangerous

stats = get_stats()

# Enhanced Stats cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌑 Total Asteroids", f"{stats[0]:,}", help="Total tracked near-Earth objects")
col2.metric("📊 Close Approaches", f"{stats[1]:,}", help="Recorded approach events")
col3.metric("⚠️ Hazardous", f"{stats[2]:,}", help="Potentially dangerous asteroids")
col4.metric("🎯 Hazard Rate", f"{(stats[2]/stats[0]*100):.1f}%", 
            delta=f"{stats[2]} active threats", delta_color="inverse")

# Featured Insight
if len(stats[3]) > 0:
    st.markdown(f"""
    <div class="insight-box">
        <h3>💡 Featured Threat</h3>
        <p>Largest hazardous asteroid: <strong>{stats[3]['name'].iloc[0]}</strong> 
        ({stats[3]['estimated_diameter_max_km'].iloc[0]:.2f} km diameter)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar with filters
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["📊 Overview", "🔍 SQL Queries", "🎛️ Advanced Filters", "📈 Analytics", "🏆 Top Threats"]
)

# Add global filters
st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Global Filters")
show_hazardous_only = st.sidebar.checkbox("Show Only Hazardous", value=False)

# PAGE 1: OVERVIEW - ENHANCED
if page == "📊 Overview":
    st.header("📊 Database Overview")
    
    # Row 1: Two main charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Hazard Classification")
        df, _ = run_query(QUERIES["13. Hazardous vs Non-Hazardous"])
        if df is not None:
            # Donut chart instead of pie
            fig = px.pie(df, values='count', names='category',
                        color='category', hole=0.4,
                        color_discrete_map={'Hazardous': COLORS['danger'], 
                                          'Non-Hazardous': COLORS['safe']})
            fig.update_traces(textposition='inside', textinfo='percent+label',
                            textfont_size=14)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Monthly Activity Trends")
        df, _ = run_query(QUERIES["11. Monthly Approach Count"])
        if df is not None:
            # Area chart with better styling
            fig = px.area(df, x='month', y='count',
                         color_discrete_sequence=[COLORS['primary']])
            fig.update_traces(fill='tozeroy')
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Approach Count",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: Top 10 Fastest with improved visualization
    st.subheader("⚡ Top 10 Fastest Asteroids")
    df, _ = run_query(QUERIES["3. Top 10 Fastest Asteroids"])
    if df is not None:
        # Horizontal bar chart for better readability
        fig = px.bar(df, y='name', x='max_velocity', orientation='h',
                     color='max_velocity', color_continuous_scale='Plasma',
                     text='max_velocity')
        fig.update_traces(texttemplate='%{text:,.0f} km/h', textposition='outside')
        fig.update_layout(
            showlegend=False,
            xaxis_title="Maximum Velocity (km/h)",
            yaxis_title="Asteroid Name",
            yaxis={'categoryorder':'total ascending'}
        )
        fig.add_vline(x=50000, line_dash="dash", line_color="red",
                     annotation_text="High Speed Threshold (50k km/h)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Size distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📏 Size Distribution")
        df, _ = run_query(QUERIES["BONUS: Size Categories"])
        if df is not None:
            fig = px.bar(df, x='size_category', y='count',
                        color='count', color_continuous_scale='Viridis',
                        text='count')
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌙 Lunar Distance Analysis")
        df, _ = run_query(QUERIES["14. Closer Than Moon (<1 LD)"])
        if df is not None and len(df) > 0:
            fig = px.scatter(df, x='close_approach_date', y='lunar_distance',
                           hover_name='name', size='lunar_distance',
                           color='lunar_distance', 
                           color_continuous_scale='Reds_r')
            fig.add_hline(y=1, line_dash="dash", 
                         annotation_text="Moon's Distance (1 LD)")
            fig.update_layout(yaxis_title="Distance (Lunar Distance)")
            st.plotly_chart(fig, use_container_width=True)

# PAGE 2: SQL QUERIES - ENHANCED
elif page == "🔍 SQL Queries":
    st.header("🔍 SQL Query Explorer")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        query_name = st.selectbox("Select Query", list(QUERIES.keys()))
    with col2:
        auto_viz = st.checkbox("Auto-visualize results", value=True)
    
    with st.expander("📝 View SQL Code", expanded=False):
        st.code(QUERIES[query_name], language='sql')
    
    if st.button("▶️ Execute Query", type="primary"):
        with st.spinner('Executing query...'):
            df, error = run_query(QUERIES[query_name])
        
        if error:
            st.error(f"❌ Error: {error}")
        else:
            st.success(f"✅ Query returned {len(df)} rows")
            
            # Show data
            st.dataframe(df, use_container_width=True, height=400)
            
            # Download options
            col1, col2 = st.columns([1, 4])
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"results_{query_name}.csv",
                    "text/csv"
                )
            
            # Smart auto-visualization
            if auto_viz and len(df) > 0:
                st.subheader("📊 Visualization")
                
                # Determine best chart type
                if len(df.columns) == 2 and len(df) <= 50:
                    col_types = df.dtypes
                    
                    # If one column is numeric
                    if pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                        # Horizontal bar for better readability
                        fig = px.bar(df, y=df.columns[0], x=df.columns[1], 
                                   orientation='h',
                                   color=df.columns[1],
                                   color_continuous_scale='Viridis')
                        fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    else:
                        fig = px.line(df, x=df.columns[0], y=df.columns[1], 
                                    markers=True)
                    
                    st.plotly_chart(fig, use_container_width=True)

# PAGE 3: FILTERS - ENHANCED
elif page == "🎛️ Advanced Filters":
    st.header("🎛️ Advanced Asteroid Filtering")
    
    st.info("💡 Adjust the filters below to find asteroids matching specific criteria")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        velocity_min = st.slider("Min Velocity (km/h)", 0, 150000, 0, 1000,
                                help="Filter by minimum approach velocity")
        diameter_min = st.slider("Min Diameter (km)", 0.0, 10.0, 0.0, 0.1,
                                help="Filter by minimum estimated diameter")
    
    with col2:
        lunar_max = st.slider("Max Lunar Distance (LD)", 0.0, 50.0, 50.0, 0.5,
                             help="1 LD = Distance from Earth to Moon")
        hazardous = st.selectbox("Hazard Status", 
                                ["All", "Hazardous Only", "Non-Hazardous Only"])
    
    with col3:
        sort_by = st.selectbox("Sort By", 
                              ["Velocity", "Distance", "Diameter"])
        limit = st.number_input("Max Results", min_value=10, max_value=1000, 
                               value=100, step=10)
    
    hazard_filter = ""
    if hazardous == "Hazardous Only":
        hazard_filter = "AND a.is_potentially_hazardous_asteroid = 1"
    elif hazardous == "Non-Hazardous Only":
        hazard_filter = "AND a.is_potentially_hazardous_asteroid = 0"
    
    sort_mapping = {
        "Velocity": "c.relative_velocity_kmph",
        "Distance": "c.miss_distance_lunar",
        "Diameter": "a.estimated_diameter_max_km"
    }
    
    query = f"""
    SELECT 
        a.name,
        c.close_approach_date as date,
        c.relative_velocity_kmph as velocity,
        c.miss_distance_lunar as distance_LD,
        a.estimated_diameter_max_km as diameter,
        CASE WHEN a.is_potentially_hazardous_asteroid = 1 THEN 'Yes' ELSE 'No' END as hazardous
    FROM asteroids a
    JOIN close_approach c ON a.id = c.neo_reference_id
    WHERE c.relative_velocity_kmph >= {velocity_min}
    AND a.estimated_diameter_max_km >= {diameter_min}
    AND c.miss_distance_lunar <= {lunar_max}
    {hazard_filter}
    ORDER BY {sort_mapping[sort_by]} DESC
    LIMIT {limit}
    """
    
    col1, col2 = st.columns([1, 4])
    with col1:
        apply_filter = st.button("🔍 Apply Filters", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Reset Filters"):
            st.rerun()
    
    if apply_filter:
        with st.spinner("Searching database..."):
            df, error = run_query(query)
        
        if df is not None and len(df) > 0:
            st.success(f"✅ Found {len(df)} matching asteroids")
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Velocity", f"{df['velocity'].mean():,.0f} km/h")
            col2.metric("Avg Distance", f"{df['distance_LD'].mean():.2f} LD")
            col3.metric("Hazardous Count", df[df['hazardous']=='Yes'].shape[0])
            
            st.dataframe(df, use_container_width=True, height=400)
            
            # Visualization
            st.subheader("📊 Results Visualization")
            fig = px.scatter(df, x='distance_LD', y='velocity',
                           size='diameter', color='hazardous',
                           hover_name='name',
                           color_discrete_map={'Yes': COLORS['danger'], 
                                             'No': COLORS['safe']})
            fig.update_layout(
                xaxis_title="Miss Distance (Lunar Distance)",
                yaxis_title="Velocity (km/h)",
                title="Asteroid Characteristics"
            )
            st.plotly_chart(fig, use_container_width=True)
        elif df is not None:
            st.warning("⚠️ No asteroids match your criteria. Try adjusting the filters.")

# PAGE 4: ANALYTICS - ENHANCED
elif page == "📈 Analytics":
    st.header("📈 Advanced Analytics Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Risk Analysis", "📅 Trends", 
                                       "📏 Size Distribution", "🔥 Comparisons"])
    
    with tab1:
        st.subheader("🎯 Top Risk Score Analysis")
        df, _ = run_query(QUERIES["BONUS: Risk Score Analysis"])
        if df is not None:
            # Add risk levels
            df['risk_level'] = pd.cut(df['risk_score'], 
                                     bins=[0, 100, 500, 1000, float('inf')],
                                     labels=['Low', 'Medium', 'High', 'Critical'])
            
            fig = px.bar(df.head(15), x='name', y='risk_score',
                        color='risk_level',
                        color_discrete_map={'Low': COLORS['safe'], 
                                          'Medium': COLORS['warning'],
                                          'High': COLORS['danger'], 
                                          'Critical': '#991b1b'},
                        text='risk_score')
            fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            fig.update_xaxes(tickangle=45)
            fig.update_layout(xaxis_title="Asteroid", yaxis_title="Risk Score")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df.head(15), use_container_width=True)
    
    with tab2:
        st.subheader("📅 Year-over-Year Activity Trends")
        df, _ = run_query(QUERIES["BONUS: Year-over-Year Trends"])
        if df is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['year'], y=df['total_approaches'],
                mode='lines+markers',
                line=dict(color=COLORS['primary'], width=3),
                marker=dict(size=10)
            ))
            
            # Highlight max year
            max_idx = df['total_approaches'].idxmax()
            fig.add_annotation(
                x=df.loc[max_idx, 'year'],
                y=df.loc[max_idx, 'total_approaches'],
                text=f"Peak: {df.loc[max_idx, 'total_approaches']} approaches",
                showarrow=True,
                arrowhead=2
            )
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Total Approaches",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("📏 Size Category Distribution")
        
        col1, col2 = st.columns(2)
        df, _ = run_query(QUERIES["BONUS: Size Categories"])
        
        if df is not None:
            with col1:
                fig = px.pie(df, values='count', names='size_category',
                           hole=0.4, color_discrete_sequence=px.colors.sequential.Viridis)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(df, x='size_category', y='count',
                           color='count', color_continuous_scale='Viridis',
                           text='count')
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🔥 Velocity vs Distance Analysis")
        df, _ = run_query("""
            SELECT 
                a.name,
                c.relative_velocity_kmph as velocity,
                c.miss_distance_lunar as distance,
                a.estimated_diameter_max_km as size,
                a.is_potentially_hazardous_asteroid as hazardous
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_reference_id
            LIMIT 500
        """)
        
        if df is not None:
            fig = px.scatter(df, x='distance', y='velocity',
                           size='size', color='hazardous',
                           hover_name='name',
                           color_continuous_scale='Reds',
                           labels={'distance': 'Miss Distance (LD)',
                                  'velocity': 'Velocity (km/h)',
                                  'hazardous': 'Hazard Level'})
            st.plotly_chart(fig, use_container_width=True)

# PAGE 5: TOP THREATS - NEW
elif page == "🏆 Top Threats":
    st.header("🏆 Most Dangerous Asteroids")
    st.warning("⚠️ These asteroids pose the highest potential risk based on size, velocity, and proximity")
    
    # Get top 10 most dangerous
    df, _ = run_query("""
        SELECT 
            a.name,
            a.estimated_diameter_max_km as diameter,
            c.relative_velocity_kmph as velocity,
            c.miss_distance_lunar as distance,
            c.close_approach_date as next_approach,
            ROUND(a.estimated_diameter_max_km * c.relative_velocity_kmph / 
                  CASE WHEN c.miss_distance_lunar > 0 THEN c.miss_distance_lunar ELSE 1 END, 2) as threat_score
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE a.is_potentially_hazardous_asteroid = 1
        ORDER BY threat_score DESC
        LIMIT 10
    """)
    
    if df is not None:
        for idx, row in df.iterrows():
            with st.expander(f"#{idx+1}: {row['name']} - Threat Score: {row['threat_score']:,.0f}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💎 Diameter", f"{row['diameter']:.3f} km")
                col2.metric("⚡ Velocity", f"{row['velocity']:,.0f} km/h")
                col3.metric("📏 Distance", f"{row['distance']:.2f} LD")
                col4.metric("📅 Next Approach", row['next_approach'])

# Footer
st.markdown("---")
st.markdown("**Data Source:** NASA NeoWs API | **Dashboard:** Built with Streamlit & Plotly")