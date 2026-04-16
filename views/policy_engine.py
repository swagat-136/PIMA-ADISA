import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.engine import apply_policy_impact

def render():
    st.header("🛡️ ADISA Policy Engine")
    st.markdown("""
    The **ADISA (Algorithmic Decision-making & Institutional Stability Analysis)** engine allows you to tune 
    active governance parameters. These settings simulate continuous policy pressure exerted on the nation.
    """)

    if "history" not in st.session_state:
        st.warning("Simulation state not initialized.")
        return

    hist = st.session_state.history
    current_state = hist[-1]

    # Initialize policies in session state if not present
    if "active_policies" not in st.session_state:
        st.session_state.active_policies = {
            "Transparency": 50,
            "Surveillance": 20,
            "Oversight": 50,
            "Health Digitization": 50,
            "Media Regulation": 30,
            "Civic Participation": 50,
            "Education Investment": 50
        }

    col_ctrl, col_viz = st.columns([1, 1])

    with col_ctrl:
        st.subheader("🎛️ Governance Controls")
        
        policies = st.session_state.active_policies
        
        # Policy Sliders
        policies["Transparency"] = st.slider(
            "🏛️ System Transparency", 0, 100, policies["Transparency"],
            help="High transparency reduces corruption but can lead to political volatility."
        )
        
        policies["Surveillance"] = st.slider(
            "👁️ Surveillance Level", 0, 100, policies["Surveillance"],
            help="High surveillance reduces crime but severely impacts social trust and privacy."
        )
        
        policies["Oversight"] = st.slider(
            "⚖️ AI Oversight & Ethics", 0, 100, policies["Oversight"],
            help="Rigorous oversight reduces bias risk and increases AI legitimacy."
        )
        
        policies["Health Digitization"] = st.slider(
            "🏥 Health Digitization", 0, 100, policies["Health Digitization"],
            help="Digitizing records improves healthcare quality but raises privacy risks."
        )
        
        policies["Civic Participation"] = st.slider(
            "🗳️ Civic Participation", 0, 100, policies["Civic Participation"],
            help="Empowering citizens improves democracy score and social trust."
        )

        policies["Education Investment"] = st.slider(
            "🎓 Education Investment", 0, 100, policies["Education Investment"],
            help="Massive long-term ROI for GDP and Tech Innovation."
        )

        st.divider()
        if st.button("🚀 Commit Policy Pulse (Next Year)", type="primary", use_container_width=True):
            new_state = apply_policy_impact(current_state, policies)
            # Add to ledger
            if "ledger" not in st.session_state: st.session_state.ledger = []
            
            # Create a summary of policy changes
            summary = []
            if policies["Surveillance"] > 50: summary.append("Increased surveillance")
            if policies["Transparency"] > 50: summary.append("Enhanced transparency")
            if policies["Oversight"] > 50: summary.append("Rigorous AI oversight")
            
            st.session_state.ledger.append({
                "Year": new_state["Year"],
                "Entity": "🛡️ Policy Engine",
                "Action": "Policy Pulse",
                "Detail": f"Adjusted governance parameters: {', '.join(summary) if summary else 'Minor adjustments'}"
            })
            
            st.session_state.history.append(new_state)
            st.success("Policies committed. Year advanced.")
            st.rerun()

    with col_viz:
        st.subheader("📊 Projected Impact")
        
        # Show a summary card of current decision
        trust_impact = (policies["Transparency"] - 50) * 0.2
        privacy_impact = (policies["Surveillance"] - 20) * 0.4 + (policies["Health Digitization"] - 50) * 0.1
        
        st.info(f"**Policy Brief:** Your current stance is focused on **{'Stability' if policies['Surveillance'] > 50 else 'Liberty'}**. Trust impact is projected at {trust_impact:+.1f} points.")
        
        # Gauges for critical AI Governance metrics
        g1, g2 = st.columns(2)
        
        def create_mini_gauge(label, value, color):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': label, 'font': {'size': 18}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                }
            ))
            fig.update_layout(height=180, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
            return fig

        g1.plotly_chart(create_mini_gauge("Governance Trust", current_state.get("Governance Trust", 65), "#4ECDC4"), use_container_width=True)
        g2.plotly_chart(create_mini_gauge("Privacy Risk", current_state.get("Privacy Risk", 30), "#FF6B6B"), use_container_width=True)
        
        st.markdown("### 📜 System Narrative")
        if policies["Surveillance"] > 70:
            st.warning("⚠️ **Mass Surveillance Alert**: Social trust is eroding fast. Citizens feel watched.")
        if policies["Transparency"] > 80:
            st.success("✅ **Radical Openness**: Government legitimacy is at an all-time high.")
        if policies["Education Investment"] > 80:
            st.info("📈 **Knowledge Economy**: Long-term tech innovation is surging.")
        if current_state.get("Privacy Risk", 0) > 60:
            st.error("🚨 **Privacy Breach Warning**: Data exposure risks are critical. Regulation needed.")

if __name__ == "__main__":
    render()
