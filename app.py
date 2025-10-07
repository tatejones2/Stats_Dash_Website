import streamlit as st
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
    
    # Data table section
    st.subheader("📋 Team Statistics")
    st.dataframe(data, width=1200, height=400)
    
    st.markdown("---")
    
    # Chart creation section
    st.subheader("📊 Create Interactive Charts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Select X-Axis:**")
        columns = data.columns.tolist()
        x_axis = st.selectbox("X Axis", columns, key="x_axis")
    
    with col2:
        st.markdown("**Select Y-Axis:**")
        y_axis = st.selectbox("Y Axis", columns, key="y_axis")
    
    with col3:
        st.markdown("**Chart Type:**")
        chart_type = st.selectbox("Chart Type", ["Scatter", "Bar", "Line"], key="chart_type")
    
    st.markdown("---")
    
    if st.button("🚀 Generate Chart", type="primary"):
        st.subheader(f"📈 {chart_type} Chart: {x_axis} vs {y_axis}")
        
        # Create chart based on selection
        try:
            if chart_type == "Scatter":
                st.scatter_chart(data.set_index(x_axis)[y_axis])
            elif chart_type == "Bar":
                st.bar_chart(data.set_index(x_axis)[y_axis])
            elif chart_type == "Line":
                st.line_chart(data.set_index(x_axis)[y_axis])
        except Exception as e:
            st.error(f"❌ Error creating chart: {str(e)}")
            st.info("💡 Try selecting different columns or ensure the data is numeric for the selected chart type.")

else:
    st.error("❌ Failed to load data from Google Sheets.")
    st.info("🔧 Please check your Google Sheets configuration and credentials.")
