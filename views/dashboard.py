import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core.engine import apply_event, get_regime_type, METRIC_KEYS, get_pillar_scores, PILLAR_MAP, get_status_details

LOWER_IS_BETTER = ["Crime Rate", "Income Inequality", "Corruption Index", "Coup Count"]

METRIC_DESCRIPTIONS = {
    "GDP": "Gross Domestic Product index — economic output & productivity",
    "Social Trust": "Citizens' trust in institutions, neighbors, and government",
    "Education Index": "Quality and access of public education system",
    "Crime Rate": "Prevalence of crime, lower is better",
    "Democracy Score": "Electoral fairness, rule of law, and civil liberties",
    "Coup Count": "Number of successful or attempted government overthrows",
    "Amendments Passed": "Constitutional amendments enacted (institutional reform activity)",
    "Healthcare Quality": "Quality and access of healthcare system",
    "Press Freedom": "Independence of media from government control",
    "Income Inequality": "Gap between richest and poorest citizens, lower is better",
    "Tech Innovation": "R&D investment, tech sector growth, and digital infrastructure",
    "Environment Health": "Air/water quality, biodiversity, and ecological sustainability",
    "Military Power": "Defense capacity and strategic strength",
    "Infrastructure": "Roads, power, internet, and public services quality",
    "Corruption Index": "Transparency International-style corruption level, lower is better",
    "Happiness Index": "Citizens' self-reported life satisfaction and wellbeing",
    "Accuracy": "Precision of the nation's core AI decision-making models",
    "Fairness": "Demographic parity and bias mitigation in algorithmic outputs",
    "Privacy Risk": "Potential for sensitive data exposure or leakage (lower is better)",
    "Governance Trust": "Public confidence in algorithmic governance and state transparency",
    "AI Legitimacy": "Societal acceptance of automated institutional decisions",
    "Bias Risk": "Likelihood of systematic prejudice in data processing (lower is better)",
    "Citizen Satisfaction": "Real-time approval rating of state digital policies",
    "Surveillance Level": "Intensity of state digital monitoring and data collection"
}

EVENT_DESCRIPTIONS = {
    "Standard Year Progression": "Normal year passes. Metrics evolve naturally.",
    "Coup": "Military seizes power. Democracy collapses. Trust evaporates.",
    "Civil War": "Internal armed conflict. Infrastructure and GDP collapse.",
    "Election Reform": "Free and fair elections institutionalized. Trust grows.",
    "Tech Revolution": "Technology boom. Economy surges. Inequality may rise.",
    "Amnesty": "Political prisoners freed. Social healing begins.",
    "Green New Deal": "Massive environmental investment. Costly but healing.",
    "Anti-Corruption Drive": "Systemic anti-corruption reforms. GDP and trust improve.",
    "Universal Healthcare": "Healthcare expanded to all citizens. Happiness surges.",
    "Education Revolution": "Education system overhauled. Long-term growth catalyst.",
    "Foreign Invasion": "External military threat. Military rises, economy falls.",
    "Market Crash": "Financial crisis. GDP and equality crisis.",
    "Peace Treaty": "End of conflict. Trust and infrastructure rebuild."
}


def render():
    st.header("⚖️ Governance Dashboard & Timeline")

    if "history" not in st.session_state:
        st.warning("Simulation state not initialized.")
        return

    hist = st.session_state.history
    current_state = hist[-1]
    regime = get_regime_type(current_state)

    # ── Top KPI Row ──────────────────────────────────────────────────────────
    prev_state = hist[-2] if len(hist) > 1 else current_state

    def delta(key):
        d = current_state[key] - prev_state[key]
        return f"{d:+.1f}" if d != 0 else None

    regime_line = f"### Current Regime: **{regime}** &nbsp;|&nbsp; Year {current_state['Year']}"
    if len(hist) > 1:
        regime_line += f" &nbsp;|&nbsp; Turn {len(hist)-1}"
    st.markdown(regime_line)

    # ── Pillar Status Cards ──────────────────────────────────────────────────
    pillars = get_pillar_scores(current_state)
    prev_pillars = get_pillar_scores(prev_state)
    
    p_cols = st.columns(len(pillars))
    for i, (name, score) in enumerate(pillars.items()):
        label, color, icon = get_status_details(score)
        
        with p_cols[i]:
            st.markdown(f"""
                <div style='text-align:center; padding:10px; border-radius:10px; border:1px solid {color}33; background:{color}11'>
                    <div style='font-size:0.85em; font-weight:600; color:#aaa'>{name.upper()}</div>
                    <div style='font-size:1.2em; font-weight:800; color:{color}'>{icon} {label}</div>
                    <div style='font-size:1.0em; font-weight:600;'>{score:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

    # ── Crisis Advice Logic ──────────────────────────────────────────────────
    critical_pillars = [n for n, s in pillars.items() if s < 41]
    if critical_pillars:
        st.write("")
        with st.container(border=True):
            st.error(f"🚨 **Urgent Notice**: Your nation is experiencing a crisis in: {', '.join(critical_pillars)}")
            pillar = critical_pillars[0]
            if "Money" in pillar:
                st.info("💡 **Crisis Advice**: Consider a **Tech Revolution** or **Anti-Corruption Drive** to boost the economy.")
            elif "Freedom" in pillar:
                st.info("💡 **Crisis Advice**: **Election Reform** or **Amnesty** could help restore democratic trust.")
            elif "Happiness" in pillar:
                st.info("💡 **Crisis Advice**: **Universal Healthcare** or **Education Revolution** will improve wellbeing.")
            elif "Safety" in pillar:
                st.info("💡 **Crisis Advice**: **Peace Treaty** or **Anti-Corruption Drive** is needed to restore order.")
            elif "AI" in pillar:
                st.info("💡 **Crisis Advice**: Invest in **Oversight** via the Policy Engine or perform **Unlearning** to restore AI Health.")

    st.divider()
    
    # ── Drill-down Expanders ─────────────────────────────────────────────────
    with st.expander("🔍 View Detailed Metrics by Category"):
        d_cols = st.columns(len(PILLAR_MAP))
        for i, (p_name, m_keys) in enumerate(PILLAR_MAP.items()):
            with d_cols[i]:
                st.markdown(f"**{p_name}**")
                for k in m_keys:
                    st.caption(f"{k}: **{current_state[k]:.1f}**")

    # ── Main Content Tabs ──────────────────────────────────────────────────
    tab_events, tab_timeline, tab_ai_stability, tab_ledger, tab_radar, tab_metrics = st.tabs([
        "⚡ Event Engine",
        "📈 Timeline",
        "🤖 AI Stability",
        "📜 Governance Ledger",
        "🕸️ Radar Profile",
        "📊 All Metrics"
    ])

    # ── Event Engine Tab ───────────────────────────────────────────────────
    with tab_events:
        st.subheader("⚡ Event Engine — Trigger Historical Forces")

        event_options = list(EVENT_DESCRIPTIONS.keys())
        c_a, c_b = st.columns([3, 1])
        with c_a:
            event_choice = st.selectbox("Select Event to Trigger", event_options)

        with c_b:
            st.write("")
            st.write("")
            trigger = st.button("🚀 Trigger Event / Next Year", type="primary", use_container_width=True)

        # Event description card
        st.info(f"**{event_choice}**: {EVENT_DESCRIPTIONS.get(event_choice, '')}")

        if trigger:
            new_state = apply_event(current_state, event_choice)
            # Add to ledger
            if "ledger" not in st.session_state: st.session_state.ledger = []
            st.session_state.ledger.append({
                "Year": new_state["Year"],
                "Entity": "⚖️ National Event",
                "Action": event_choice,
                "Detail": EVENT_DESCRIPTIONS.get(event_choice, "")
            })
            st.session_state.history.append(new_state)
            st.rerun()

        st.divider()
        st.subheader("🎛️ Manual Metric Override")
        st.caption("Fine-tune individual metrics directly — simulates specific policy decisions.")

        override_cols = st.columns(4)
        override_metric = override_cols[0].selectbox("Metric", METRIC_KEYS, key="override_metric")
        override_val = override_cols[1].slider(
            "New Value", 0.0, 100.0,
            value=float(current_state.get(override_metric, 50)),
            step=1.0, key="override_val"
        )
        override_cols[2].write("")
        override_cols[2].write("")
        if override_cols[2].button("✏️ Apply Override", use_container_width=True):
            import copy
            ns = copy.deepcopy(current_state)
            ns[override_metric] = override_val
            ns["Year"] += 1
            st.session_state.history.append(ns)
            st.rerun()

    # ── Timeline Tab ───────────────────────────────────────────────────────
    with tab_timeline:
        st.subheader("📈 Timeline Metrics")
        df = pd.DataFrame(hist)

        selected_metrics = st.multiselect(
            "Select Metrics to Plot", METRIC_KEYS,
            default=["Democracy Score", "GDP", "Social Trust", "Crime Rate", "Happiness Index"]
        )

        chart_type = st.radio("Chart Type", ["Line", "Area", "Bar"], horizontal=True)

        if selected_metrics:
            if chart_type == "Line":
                fig = px.line(df, x="Year", y=selected_metrics, markers=True,
                              title="Society Metrics Over Time")
            elif chart_type == "Area":
                fig = px.area(df, x="Year", y=selected_metrics,
                              title="Society Metrics Over Time (Area)")
            else:
                fig = px.bar(df, x="Year", y=selected_metrics, barmode="group",
                             title="Society Metrics Over Time (Bar)")

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f0f0"),
                xaxis=dict(gridcolor="#333"),
                yaxis=dict(range=[0, 110], gridcolor="#333"),
                yaxis_title="Score (0-100)",
                xaxis_title="Simulation Year",
                hovermode="x unified",
                height=480,
                legend=dict(bgcolor="rgba(30,30,30,0.8)", bordercolor="#555", borderwidth=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least one metric to visualize.")

        with st.expander("📋 Raw Timeline Data"):
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Timeline CSV", data=csv, file_name="simulation_timeline.csv")

    # ── AI Stability Tab ───────────────────────────────────────────────────
    with tab_ai_stability:
        st.subheader("🤖 Algorithmic & AI Stability Index")
        ai_metrics = ["Accuracy", "Fairness", "AI Legitimacy", "Bias Risk", "Privacy Risk"]
        
        # Invert Bias and Privacy risk for better visual comparison in a bar chart if needed
        # But for AI Health, let's just show them as is in a group
        ai_df = pd.DataFrame([
            {"Metric": m, "Score": current_state[m], "Status": "Good" if current_state[m] > 70 else "Warning" if current_state[m] > 40 else "Critical"}
            for m in ai_metrics
        ])
        
        fig_ai = px.bar(ai_df, x="Metric", y="Score", color="Status",
                        color_discrete_map={"Good": "#00C897", "Warning": "#F9D423", "Critical": "#FF4B4B"},
                        title="ADISA Core Stability Metrics")
        fig_ai.update_layout(yaxis_range=[0, 100], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0f0f0"))
        st.plotly_chart(fig_ai, use_container_width=True)
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("#### 🛡️ ADISA Privacy Ledger")
            st.progress(current_state["Privacy Risk"] / 100)
            st.caption(f"Current Privacy Exposure: {current_state['Privacy Risk']:.1f}%")
        with c_p2:
            st.markdown("#### ⚖️ Fairness Coefficient")
            st.progress(current_state["Fairness"] / 100)
            st.caption(f"Current Bias Mitigation: {current_state['Fairness']:.1f}%")

    # ── Governance Ledger Tab ──────────────────────────────────────────────
    with tab_ledger:
        st.subheader("📜 Governance Ledger — Institutional Record")
        st.caption("A chronological record of all major state decisions, crises, and policy pulses.")
        
        if "ledger" not in st.session_state or not st.session_state.ledger:
            st.info("No records in the ledger yet. Trigger an event or commit a policy to begin.")
        else:
            # Show ledger in reverse chronological order
            for log in reversed(st.session_state.ledger):
                with st.expander(f"📅 Year {log['Year']}: {log['Action']}", expanded=False):
                    c1, c2 = st.columns([1, 3])
                    c1.markdown(f"**Entity:** {log['Entity']}")
                    c2.markdown(f"**Outcome:** {log['Detail']}")
                    
            if st.button("🗑️ Clear Ledger", use_container_width=True):
                st.session_state.ledger = []
                st.rerun()

    # ── Radar Tab ──────────────────────────────────────────────────────────
    with tab_radar:
        st.subheader("🕸️ Nation Governance Radar Profile")

        radar_metrics = [m for m in METRIC_KEYS if m not in ["Coup Count", "Amendments Passed"]]

        def safe_score(state, key):
            v = state.get(key, 50)
            return 100 - v if key in LOWER_IS_BETTER else v

        fig_r = go.Figure()

        if len(hist) > 1:
            # Show initial vs current
            start_vals = [safe_score(hist[0], m) for m in radar_metrics]
            fig_r.add_trace(go.Scatterpolar(
                r=start_vals + [start_vals[0]],
                theta=radar_metrics + [radar_metrics[0]],
                fill="toself", name=f"Year {hist[0]['Year']} (Start)",
                line=dict(color="#4ECDC4", width=1.5, dash="dash"),
                fillcolor="rgba(78, 205, 196, 0.1)"
            ))

        curr_vals = [safe_score(current_state, m) for m in radar_metrics]
        fig_r.add_trace(go.Scatterpolar(
            r=curr_vals + [curr_vals[0]],
            theta=radar_metrics + [radar_metrics[0]],
            fill="toself", name=f"Year {current_state['Year']} (Current)",
            line=dict(color="#FF6B6B", width=2.5),
            fillcolor="rgba(255, 107, 107, 0.2)"
        ))

        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#444"),
                angularaxis=dict(gridcolor="#444")
            ),
            showlegend=True, height=550,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            legend=dict(bgcolor="rgba(30,30,30,0.8)")
        )
        st.plotly_chart(fig_r, use_container_width=True)
        st.caption("Note: Crime Rate, Income Inequality, and Corruption Index are inverted — higher = better governance.")

    # ── All Metrics Tab ────────────────────────────────────────────────────
    with tab_metrics:
        st.subheader("📊 Full Metrics Snapshot")

        metric_data = []
        for k in METRIC_KEYS:
            v = current_state.get(k, 0)
            prev_v = prev_state.get(k, 0)
            change = v - prev_v
            good_dir = "↓ better" if k in LOWER_IS_BETTER else "↑ better"
            metric_data.append({
                "Metric": k,
                "Current": round(v, 1),
                "Previous": round(prev_v, 1),
                "Change": round(change, 1),
                "Direction": good_dir,
                "Description": METRIC_DESCRIPTIONS.get(k, "")
            })

        metrics_df = pd.DataFrame(metric_data)

        def color_change(val):
            if val > 0:
                return "color: #00C897"
            elif val < 0:
                return "color: #FF4B4B"
            return ""

        st.dataframe(
            metrics_df.style.applymap(color_change, subset=["Change"])
            .background_gradient(cmap="RdYlGn", subset=["Current"]),
            use_container_width=True,
            height=580
        )

        # Gauge-style mini chart for any single metric
        st.divider()
        gauge_metric = st.selectbox("Gauge View for Metric:", METRIC_KEYS, key="gauge_sel")
        gval = current_state.get(gauge_metric, 50)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=gval,
            delta={"reference": prev_state.get(gauge_metric, gval)},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#FF6B6B"},
                "steps": [
                    {"range": [0, 33], "color": "#2d1b1b"},
                    {"range": [33, 66], "color": "#2d2a1b"},
                    {"range": [66, 100], "color": "#1b2d1e"}
                ],
                "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.75, "value": gval}
            },
            title={"text": gauge_metric, "font": {"color": "#f0f0f0"}}
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0f0f0"), height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
