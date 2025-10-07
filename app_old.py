import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sheets import fetch_sheet_data

# NJIT-inspired styling
st.set_page_config(
    page_title="NJIT Baseball Stats Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for NJIT colors (Navy and Red)
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stTitle {
        color: #dc2626;
        text-align: center;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
    }
    
    .stSubheader {
        color: #ef4444;
        border-bottom: 2px solid #dc2626;
        padding-bottom: 0.5rem;
    }
    
    .stSelectbox > div > div {
        background-color: #1e40af;
        color: white;
        border: 2px solid #dc2626;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #dc2626, #ef4444);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #b91c1c, #dc2626);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(220, 38, 38, 0.4);
    }
    
    .stDataFrame {
        border: 2px solid #dc2626;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #dc2626;
        margin: 0.5rem 0;
    }
    
    .stMetric {
        background: transparent;
    }
    
    h1 {
        color: #dc2626 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e40af, #1e3a8a);
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #1e40af, #1e3a8a);
    }
</style>
""", unsafe_allow_html=True)

# Header with NJIT branding
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #dc2626; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
        ⚾ NJIT Baseball Stats Dashboard ⚾
    </h1>
    <p style="color: #60a5fa; font-size: 1.2rem; margin-top: -1rem;">
        🏆 Highlanders Baseball Analytics 🏆
    </p>
</div>
""", unsafe_allow_html=True)

# Create page navigation
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "📊 Navigate Dashboard",
    ["🏠 Team Overview", "📈 Interactive Charts"],
    key="page_selector"
)
st.sidebar.markdown("---")

# Sidebar with team info and controls
""", unsafe_allow_html=True)

def show_team_overview(data):
    """Display the main team overview page"""
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Total Players", len(data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Data Columns", len(data.columns))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("🔄 Last Updated", "Live Data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("⚾ Season", "2025")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data table section with conditional formatting
    st.subheader("📋 Team Statistics")
    
    # Create a copy of data for styling
    styled_data = data.copy()
    
    # Define stat categories and their ideal values
    # Higher is better stats (green when high)
    higher_better = ['K%', 'K', 'Whiff%', 'Plus%', 'TPLUS%', 'FPS%', 'IP', 'K:BB', 'K:F$', 'k/9', 'Ahead%', 'E+A%']
    
    # Lower is better stats (green when low)  
    lower_better = ['ERA', 'WHIP', 'FWHIP', 'BB%', 'BAA', 'BACON', 'ER', 'BB', 'HBP', 'H', 'bb/9', 'h/9']
    
    # Percentage stats that should be around certain values
    percentage_stats = ['S%', 'FB S%', 'OS S%', 'FB CSW', 'OS CSW', 'SL CSW', 'CH/SPL CSW', 'CB CSW', 'CT CSW', 
                       'FB%', 'Out%', 'Out% RHB', 'Out% LHB', 'ZONE%', 'Swing%', 'FRB%', 'Early%']
    
    def get_color_for_value(column, value):
        """Return color based on stat type and value"""
        try:
            numeric_value = float(str(value).replace('%', ''))
            
            if column in higher_better:
                # Higher values are better (green)
                if numeric_value >= 80:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif numeric_value >= 60:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            elif column in lower_better:
                # Lower values are better (green)
                if numeric_value <= 2.0:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif numeric_value <= 4.0:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            elif column in percentage_stats:
                # Percentage stats - contextual coloring
                if 70 <= numeric_value <= 90:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif 50 <= numeric_value < 70 or 90 < numeric_value <= 95:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            else:
                # Default styling for unknown stats
                return 'color: #60a5fa; font-weight: normal;'  # Light blue text
                
        except (ValueError, TypeError):
            # Non-numeric values get default styling
            return 'color: #e5e7eb; font-weight: normal;'  # Light gray text
    
    # Apply conditional formatting
    def style_dataframe(df):
        styled_df = df.style
        
        # Apply cell-by-cell styling
        for col in df.columns:
            if col not in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']:  # Skip name columns
                styled_df = styled_df.map(
                    lambda x: get_color_for_value(col, x), 
                    subset=[col]
                )
        
        return styled_df
    
    # Display the styled dataframe
    st.dataframe(style_dataframe(styled_data), width=1200, height=400)
    
    # Add legend
    st.markdown("""
    **📊 Color Legend:**
    - <span style="color: #22c55e; font-weight: bold;">🟢 Green Text</span>: Excellent performance
    - <span style="color: #eab308; font-weight: bold;">🟡 Yellow Text</span>: Average/Good performance  
    - <span style="color: #ef4444; font-weight: bold;">🔴 Red Text</span>: Needs improvement
    - <span style="color: #60a5fa;">🔵 Blue Text</span>: Other stats
    - <span style="color: #e5e7eb;">⚪ Gray Text</span>: Player info/Non-numeric
    """, unsafe_allow_html=True)


def show_interactive_charts(data):
    """Display the interactive charts page"""
    st.subheader("📈 Interactive Baseball Charts")
    st.markdown("Create custom visualizations with player names on hover")
    
    # Chart controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Select X-Axis:**")
        columns = [col for col in data.columns if col not in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']]
        x_axis = st.selectbox("X Axis", columns, key="chart_x_axis")
    
    with col2:
        st.markdown("**Select Y-Axis:**")
        y_axis = st.selectbox("Y Axis", columns, key="chart_y_axis")
    
    with col3:
        st.markdown("**Chart Type:**")
        chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart"], key="chart_type")
    
    st.markdown("---")
    
    # Get player name column (first text column)
    player_name_col = None
    for col in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']:
        if col in data.columns:
            player_name_col = col
            break
    
    if st.button("🚀 Generate Interactive Chart", type="primary"):
        st.subheader(f"📊 {chart_type}: {x_axis} vs {y_axis}")
        
        try:
            # Prepare data for plotting
            plot_data = data.copy()
            
            # Convert to numeric, handling non-numeric values
            plot_data[x_axis] = pd.to_numeric(plot_data[x_axis].astype(str).str.replace('%', ''), errors='coerce')
            plot_data[y_axis] = pd.to_numeric(plot_data[y_axis].astype(str).str.replace('%', ''), errors='coerce')
            
            # Remove rows with NaN values
            plot_data = plot_data.dropna(subset=[x_axis, y_axis])
            
            if chart_type == "Scatter Plot":
                fig = px.scatter(
                    plot_data, 
                    x=x_axis, 
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{x_axis} vs {y_axis}",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
                
            elif chart_type == "Bar Chart":
                fig = px.bar(
                    plot_data.head(15),  # Limit to first 15 players for readability
                    x=player_name_col if player_name_col else plot_data.index,
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{y_axis} by Player",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
                fig.update_xaxis(tickangle=45)
                
            elif chart_type == "Line Chart":
                fig = px.line(
                    plot_data,
                    x=x_axis,
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{x_axis} vs {y_axis} Trend",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
            
            # Customize chart appearance with NJIT colors
            fig.update_layout(
                plot_bgcolor='rgba(30, 64, 175, 0.1)',  # Light navy background
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='#dc2626',
                title_font_size=20
            )
            
            # Display the interactive chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Add chart insights
            st.markdown("### 📊 Chart Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                if not plot_data.empty:
                    max_player = plot_data.loc[plot_data[y_axis].idxmax()]
                    st.success(f"🏆 **Highest {y_axis}**: {max_player[player_name_col] if player_name_col else 'Player'} ({max_player[y_axis]:.2f})")
            
            with col2:
                if not plot_data.empty:
                    min_player = plot_data.loc[plot_data[y_axis].idxmin()]
                    st.info(f"📊 **Lowest {y_axis}**: {min_player[player_name_col] if player_name_col else 'Player'} ({min_player[y_axis]:.2f})")
                    
        except Exception as e:
            st.error(f"❌ Error creating chart: {str(e)}")
            st.info("💡 Try selecting different columns or ensure the data is numeric for the selected chart type.")


# Sidebar with team info and controls
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h2 style="color: #dc2626;">🏫 NJIT Highlanders</h2>
        <p style="color: #60a5fa;">New Jersey Institute of Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Dashboard Controls")
    
    # Data refresh button
    if st.button("🔄 Refresh Data", type="secondary"):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Dashboard Features:**
    - 📈 Live Google Sheets integration
    - 📊 Interactive charts and graphs
    - 📋 Real-time team statistics
    - 🎨 NJIT-themed design
    
    **Team Colors:**
    - 🔵 Navy Blue
    - 🔴 Red
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Stats")
    st.info("📊 Stats will appear after data loads")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #60a5fa; font-size: 0.8rem;">
        Built with ❤️ for NJIT Baseball
    </div>
    """, unsafe_allow_html=True)

# Fetch data from Google Sheets
with st.spinner('🔄 Loading baseball stats from Google Sheets...'):
    data = fetch_sheet_data()

if data is not None:
    # Page routing
    if page == "🏠 Team Overview":
        show_team_overview(data)
    elif page == "📈 Interactive Charts":
        show_interactive_charts(data)
else:
    st.error("❌ Failed to load data from Google Sheets.")
    st.info("🔧 Please check your Google Sheets configuration and credentials.")


def show_team_overview(data):
    """Display the main team overview page"""
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Total Players", len(data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Data Columns", len(data.columns))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("🔄 Last Updated", "Live Data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("⚾ Season", "2025")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data table section with conditional formatting
    st.subheader("📋 Team Statistics")
    
    # Create a copy of data for styling
    styled_data = data.copy()
    
    # Define stat categories and their ideal values
    # Higher is better stats (green when high)
    higher_better = ['K%', 'K', 'Whiff%', 'Plus%', 'TPLUS%', 'FPS%', 'IP', 'K:BB', 'K:F$', 'k/9', 'Ahead%', 'E+A%']
    
    # Lower is better stats (green when low)  
    lower_better = ['ERA', 'WHIP', 'FWHIP', 'BB%', 'BAA', 'BACON', 'ER', 'BB', 'HBP', 'H', 'bb/9', 'h/9']
    
    # Percentage stats that should be around certain values
    percentage_stats = ['S%', 'FB S%', 'OS S%', 'FB CSW', 'OS CSW', 'SL CSW', 'CH/SPL CSW', 'CB CSW', 'CT CSW', 
                       'FB%', 'Out%', 'Out% RHB', 'Out% LHB', 'ZONE%', 'Swing%', 'FRB%', 'Early%']
    
    def get_color_for_value(column, value):
        """Return color based on stat type and value"""
        try:
            numeric_value = float(str(value).replace('%', ''))
            
            if column in higher_better:
                # Higher values are better (green)
                if numeric_value >= 80:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif numeric_value >= 60:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            elif column in lower_better:
                # Lower values are better (green)
                if numeric_value <= 2.0:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif numeric_value <= 4.0:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            elif column in percentage_stats:
                # Percentage stats - contextual coloring
                if 70 <= numeric_value <= 90:
                    return 'color: #22c55e; font-weight: bold;'  # Green text
                elif 50 <= numeric_value < 70 or 90 < numeric_value <= 95:
                    return 'color: #eab308; font-weight: bold;'  # Yellow text
                else:
                    return 'color: #ef4444; font-weight: bold;'  # Red text
                    
            else:
                # Default styling for unknown stats
                return 'color: #60a5fa; font-weight: normal;'  # Light blue text
                
        except (ValueError, TypeError):
            # Non-numeric values get default styling
            return 'color: #e5e7eb; font-weight: normal;'  # Light gray text
    
    # Apply conditional formatting
    def style_dataframe(df):
        styled_df = df.style
        
        # Apply cell-by-cell styling
        for col in df.columns:
            if col not in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']:  # Skip name columns
                styled_df = styled_df.map(
                    lambda x: get_color_for_value(col, x), 
                    subset=[col]
                )
        
        return styled_df
    
    # Display the styled dataframe
    st.dataframe(style_dataframe(styled_data), width=1200, height=400)
    
    # Add legend
    st.markdown("""
    **📊 Color Legend:**
    - <span style="color: #22c55e; font-weight: bold;">🟢 Green Text</span>: Excellent performance
    - <span style="color: #eab308; font-weight: bold;">🟡 Yellow Text</span>: Average/Good performance  
    - <span style="color: #ef4444; font-weight: bold;">🔴 Red Text</span>: Needs improvement
    - <span style="color: #60a5fa;">🔵 Blue Text</span>: Other stats
    - <span style="color: #e5e7eb;">⚪ Gray Text</span>: Player info/Non-numeric
    """, unsafe_allow_html=True)


def show_interactive_charts(data):
    """Display the interactive charts page"""
    st.subheader("� Interactive Baseball Charts")
    st.markdown("Create custom visualizations with player names on hover")
    
    # Chart controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Select X-Axis:**")
        columns = [col for col in data.columns if col not in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']]
        x_axis = st.selectbox("X Axis", columns, key="chart_x_axis")
    
    with col2:
        st.markdown("**Select Y-Axis:**")
        y_axis = st.selectbox("Y Axis", columns, key="chart_y_axis")
    
    with col3:
        st.markdown("**Chart Type:**")
        chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart"], key="chart_type")
    
    st.markdown("---")
    
    # Get player name column (first text column)
    player_name_col = None
    for col in ['Column_B', 'Column_C', 'Column_D', 'Column_E', 'Column_F', 'Column_G']:
        if col in data.columns:
            player_name_col = col
            break
    
    if st.button("🚀 Generate Interactive Chart", type="primary"):
        st.subheader(f"� {chart_type}: {x_axis} vs {y_axis}")
        
        try:
            # Prepare data for plotting
            plot_data = data.copy()
            
            # Convert to numeric, handling non-numeric values
            plot_data[x_axis] = pd.to_numeric(plot_data[x_axis].astype(str).str.replace('%', ''), errors='coerce')
            plot_data[y_axis] = pd.to_numeric(plot_data[y_axis].astype(str).str.replace('%', ''), errors='coerce')
            
            # Remove rows with NaN values
            plot_data = plot_data.dropna(subset=[x_axis, y_axis])
            
            if chart_type == "Scatter Plot":
                fig = px.scatter(
                    plot_data, 
                    x=x_axis, 
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{x_axis} vs {y_axis}",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
                
            elif chart_type == "Bar Chart":
                fig = px.bar(
                    plot_data.head(15),  # Limit to first 15 players for readability
                    x=player_name_col if player_name_col else plot_data.index,
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{y_axis} by Player",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
                fig.update_xaxis(tickangle=45)
                
            elif chart_type == "Line Chart":
                fig = px.line(
                    plot_data,
                    x=x_axis,
                    y=y_axis,
                    hover_name=player_name_col if player_name_col else None,
                    title=f"{x_axis} vs {y_axis} Trend",
                    color_discrete_sequence=['#dc2626']  # NJIT red
                )
            
            # Customize chart appearance with NJIT colors
            fig.update_layout(
                plot_bgcolor='rgba(30, 64, 175, 0.1)',  # Light navy background
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='#dc2626',
                title_font_size=20
            )
            
            # Display the interactive chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Add chart insights
            st.markdown("### 📊 Chart Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                if not plot_data.empty:
                    max_player = plot_data.loc[plot_data[y_axis].idxmax()]
                    st.success(f"🏆 **Highest {y_axis}**: {max_player[player_name_col] if player_name_col else 'Player'} ({max_player[y_axis]:.2f})")
            
            with col2:
                if not plot_data.empty:
                    min_player = plot_data.loc[plot_data[y_axis].idxmin()]
                    st.info(f"📊 **Lowest {y_axis}**: {min_player[player_name_col] if player_name_col else 'Player'} ({min_player[y_axis]:.2f})")
                    
        except Exception as e:
            st.error(f"❌ Error creating chart: {str(e)}")
            st.info("� Try selecting different columns or ensure the data is numeric for the selected chart type.")
