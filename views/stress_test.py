import streamlit as st
import pandas as pd
import random
import copy
import plotly.express as px
from core.engine import apply_event, get_regime_type, init_mock_state

def render():
    st.header("🔬 Sub-System Stress Testing")
    st.write("Automatically run your Constitution and current society through a rapid cascade of crisis scenarios to evaluate structural resilience. This does not alter your main timeline.")

    if "history" not in st.session_state:
        st.warning("Simulation state not initialized.")
        return

    current_state = st.session_state.history[-1]

    st.subheader("Config Params")
    scenarios = st.multiselect(
        "Crisis Scenarios to Inject:",
        ["Global Pandemic", "Economic Crash", "Coup", "Civil War", "Border Invasion", "Tech Collapse", "Hyper-Inflation", "Election Fraud"],
        default=["Economic Crash", "Coup", "Global Pandemic"]
    )

    if st.button("Run Simulation Waterfall", type="primary"):
        test_state = copy.deepcopy(current_state)
        
        results = [test_state]
        
        with st.spinner("Processing cascaded events..."):
            for scene in scenarios:
                # Map specific scenario text into base engine events or general detrimental effects
                # We can reuse apply_event but maybe map the names
                if scene in ["Coup", "Civil War"]:
                    test_state = apply_event(test_state, scene)
                elif scene == "Economic Crash":
                    test_state["GDP"] -= 30
                    test_state["Social Trust"] -= 15
                    test_state["Crime Rate"] += 15
                elif scene == "Global Pandemic":
                    test_state["Healthcare Quality"] -= 35
                    test_state["GDP"] -= 20
                    test_state["Happiness Index"] -= 25
                elif scene == "Election Fraud":
                    test_state["Democracy Score"] -= 25
                    test_state["Social Trust"] -= 30
                else: 
                    # generic negative bounds
                    test_state["GDP"] -= 10
                    test_state["Social Trust"] -= 10
                    test_state["Happiness Index"] -= 10
                
                # Make sure constraints hold
                for k, v in test_state.items():
                    if k not in ["Year", "Coup Count", "Amendments Passed"]:
                        test_state[k] = max(0.0, min(100.0, float(v)))
                
                test_state["Year"] += 1
                
                # Snapshot
                results.append(copy.deepcopy(test_state))

        # Calculate Resilience Score
        final_state = results[-1]
        
        # Simple resilience score: average of key stable indicators
        resilience = (final_state["Democracy Score"] + final_state["Social Trust"] + final_state["GDP"] + final_state["Healthcare Quality"]) / 4

        st.success(f"Simulation Complete. 🛡️ Resilience Score: **{resilience:.1f}/100.0**")
        
        # Plot the drop
        df = pd.DataFrame(results)
        df["Step"] = [f"Start"] + scenarios
        
        fig = px.bar(df, x="Step", y=["Democracy Score", "GDP", "Social Trust"], title="Metrics Drop Map", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        st.write(f"Final Regime Classification under extreme stress: **{get_regime_type(final_state)}**")
