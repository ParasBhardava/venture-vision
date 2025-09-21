"""S
"""

from typing import Dict, Any
import streamlit as st
import requests
import json
from config.settings import API_BASE_URL

# Configure page    
st.set_page_config(
    page_title="Venture Vision - Company Evaluator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 3rem;
    }
    
    .evaluation-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .error-message {
        background: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    
    .success-message {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🚀 Venture Vision</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Company Evaluation Platform</p>', unsafe_allow_html=True)

# API Configuration
API_ENDPOINT = f"{API_BASE_URL}/api/v1/evaluate"

def make_api_request(company_name: str) -> Dict[str, Any]:
    """Make API request to evaluate company."""
    try:
        payload = {"company_name": company_name}
        headers = {"Content-Type": "application/json"}
        
        with st.spinner(f"🔍 Analyzing {company_name}... This may take a few moments."):
            response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API. Please ensure the server is running.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The analysis is taking longer than expected.")
        return None
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return None

def display_analysis_section(title: str, content: str, icon: str):
    """Display an analysis section with consistent formatting."""
    st.markdown(f"### {icon} {title}")
    
    if content and content.strip() and content != "No results found":
        # Try to parse as JSON first (in case it's structured data)
        try:
            if content.startswith('{') and content.endswith('}'):
                data = json.loads(content)
                if isinstance(data, dict):
                    # Display as structured data
                    for key, value in data.items():
                        if isinstance(value, (dict, list)):
                            st.json(value)
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.markdown(content)
            else:
                st.markdown(content)
        except json.JSONDecodeError:
            # If not JSON, display as markdown
            st.markdown(content)
    else:
        st.warning("No analysis available for this section.")

# Company input section
st.markdown("## 📝 Enter Company Information")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    company_name = st.text_input(
        "Company Name",
        placeholder="Enter company name (e.g., Tesla, OpenAI, Stripe)",
        help="Enter the name of the company you want to evaluate"
    )
    
    analyze_button = st.button(
        "🚀 Analyze Company",
        type="primary",
        use_container_width=True
    )

# Initialize session state
if 'evaluation_data' not in st.session_state:
    st.session_state.evaluation_data = None
if 'last_company' not in st.session_state:
    st.session_state.last_company = ""

# Handle analysis request
if analyze_button and company_name:
    st.session_state.evaluation_data = make_api_request(company_name)
    st.session_state.last_company = company_name

# Display results if available
if st.session_state.evaluation_data:
    api_response = st.session_state.evaluation_data
    
    # Check if the response has the expected structure
    if 'result' in api_response and 'data' in api_response['result']:
        evaluation_data = api_response['result']['data']
        
        st.markdown(f"## 📊 Analysis Results for **{st.session_state.last_company}**")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Executive Summary", 
            "👥 Founders & Team", 
            "🎯 Market & Problem", 
            "⚡ Competitive Edge", 
            "📈 Traction & Metrics",
            "📄 Complete Report"
        ])
        
        with tab1:
            st.markdown("### 📋 Executive Summary & Final Report")
            if 'final_report' in evaluation_data:
                display_analysis_section(
                    "Final Report", 
                    evaluation_data['final_report'], 
                    "📋"
                )
            else:
                st.warning("Executive summary not available.")
        
        with tab2:
            display_analysis_section(
                "Founders & Team Assessment", 
                evaluation_data.get('founders_profile_agent_response', 'No data available'), 
                "👥"
            )
        
        with tab3:
            display_analysis_section(
                "Market Opportunity & Problem Validation", 
                evaluation_data.get('problem_market_size_agent_response', 'No data available'), 
                "🎯"
            )
        
        with tab4:
            display_analysis_section(
                "Competitive Advantage & Differentiation", 
                evaluation_data.get('unique_differentiator_agent_response', 'No data available'), 
                "⚡"
            )
        
        with tab5:
            display_analysis_section(
                "Traction & Business Metrics", 
                evaluation_data.get('traction_metrics_agent_response', 'No data available'), 
                "📈"
            )
        
        with tab6:
            st.markdown("### 📄 Complete Evaluation Report")
            st.markdown("---")
            
            # Display all sections in a comprehensive format
            sections = [
                ("📋 Final Report", evaluation_data.get('final_report', 'N/A')),
                ("👥 Founders & Team", evaluation_data.get('founders_profile_agent_response', 'N/A')),
                ("🎯 Market & Problem", evaluation_data.get('problem_market_size_agent_response', 'N/A')),
                ("⚡ Competitive Edge", evaluation_data.get('unique_differentiator_agent_response', 'N/A')),
                ("📈 Traction & Metrics", evaluation_data.get('traction_metrics_agent_response', 'N/A'))
            ]
            
            for section_title, section_content in sections:
                with st.expander(section_title, expanded=False):
                    if section_content and section_content != 'N/A' and section_content != 'No results found':
                        st.markdown(section_content)
                    else:
                        st.warning("No data available for this section.")
            
            # Download option
            if st.button("💾 Download Complete Report as JSON"):
                report_json = json.dumps(evaluation_data, indent=2)
                st.download_button(
                    label="Download JSON Report",
                    data=report_json,
                    file_name=f"{st.session_state.last_company}_evaluation_report.json",
                    mime="application/json"
                )
    else:
        st.error("❌ Unexpected response format from API")
        st.json(api_response)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🚀 Venture Vision | AI-Powered Company Evaluation Platform</p>
        <p>Built with Streamlit | Powered by Advanced AI Agents</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Sidebar with instructions
with st.sidebar:
    st.markdown("## 🔧 How to Use")
    st.markdown("""
    1. **Enter Company Name**: Type the name of the company you want to analyze
    2. **Click Analyze**: Hit the analyze button to start the evaluation
    3. **View Results**: Explore the 6 tabs to see different aspects of the analysis:
       - **Executive Summary**: Overall assessment
       - **Founders & Team**: Leadership evaluation
       - **Market & Problem**: Market opportunity analysis
       - **Competitive Edge**: Differentiation factors
       - **Traction & Metrics**: Business performance
       - **Complete Report**: All sections combined
    """)
    
    st.markdown("## ⚙️ Configuration")
    st.markdown(f"**API Endpoint**: `{API_ENDPOINT}`")
    
    # API status check
    try:
        health_response = requests.get(f"{API_BASE_URL}/api/v1/health/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API is online")
        else:
            st.error("❌ API is not responding")
    except:
        st.error("❌ Cannot reach API")
    
    st.markdown("## 💡 Tips")
    st.info("""
    - Use well-known company names for better results
    - Analysis may take 30-60 seconds to complete
    - Each analysis provides comprehensive insights across multiple dimensions
    """) 