import streamlit as st
from core.engine import init_mock_state
import views.dashboard as v_dash
import views.ai_analysis as v_ai
import views.stress_test as v_stress
import views.world_benchmark as v_world
import views.historical_scenarios as v_hist
import views.policy_engine as v_policy
import views.unlearning_lab as v_lab

st.set_page_config(
    page_title="PIMA ADISA Governance Simulator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');

    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --accent-glow: 0 0 15px rgba(102, 126, 234, 0.4);
    }

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.5px;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 25, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: var(--accent-glow);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.2);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Plotly Chart Styling */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

def init_sim_state():
    if "history" not in st.session_state:
        st.session_state.history = [init_mock_state()]


def main():
    init_sim_state()

    # Sidebar branding
    st.sidebar.markdown(
        """
        <div style='text-align:center;padding:10px 0 5px 0'>
            <span style='font-size:2.2em'>🏛️</span><br>
            <span style='font-size:1.2em;font-weight:800;letter-spacing:0.5px'>PIMA ADISA</span><br>
            <span style='font-size:0.75em;color:#aaa'>Governance Simulator v3.0 (2026)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    # Quick stats in sidebar
    current = st.session_state.history[-1]
    st.sidebar.markdown("**📊 Live Stats**")
    st.sidebar.metric("Year", int(current["Year"]))
    st.sidebar.metric("Democracy Score", f"{current['Democracy Score']:.1f}")
    st.sidebar.metric("GDP", f"{current['GDP']:.1f}")
    st.sidebar.metric("Turns Simulated", len(st.session_state.history) - 1)

    if len(st.session_state.history) > 1:
        if st.sidebar.button("↩️ Undo Last Turn", use_container_width=True):
            st.session_state.history.pop()
            if "ledger" in st.session_state and st.session_state.ledger:
                st.session_state.ledger.pop()
            st.rerun()

    st.sidebar.divider()



    # Navigation
    page = st.sidebar.radio("🗺️ Where to go?", [
        "📊 Nation Summary",
        "🌍 Compare with World",
        "🛡️ Rulebook & Policies",
        "🧪 Forget Bad Data (AI)",
        "📜 History Book",
        "🤖 AI Analysis & Chat",
        "🔬 Stress Testing"
    ])

    # Render selected page
    if page == "📊 Nation Summary":
        v_dash.render()
    elif page == "🌍 Compare with World":
        v_world.render()
    elif page == "🛡️ Rulebook & Policies":
        v_policy.render()
    elif page == "🧪 Forget Bad Data (AI)":
        v_lab.render()
    elif page == "📜 History Book":
        v_hist.render()
    elif page == "🤖 AI Analysis & Chat":
        v_ai.render()
    elif page == "🔬 Stress Testing":
        v_stress.render()

    st.sidebar.divider()
    if st.sidebar.button("⚠️ Hard Reset Simulation", use_container_width=True):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
