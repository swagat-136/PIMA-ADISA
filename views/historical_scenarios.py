import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import copy
from data.historical_scenarios import HISTORICAL_SCENARIOS, CATEGORY_COLORS, CATEGORY_ICONS
from core.engine import apply_event, get_regime_type, METRIC_KEYS, init_mock_state

LOWER_IS_BETTER = ["Crime Rate", "Income Inequality", "Corruption Index", "Coup Count"]

RESILIENCE_LABELS = {
    (0, 25): ("💀 Collapsed State", "#FF4B4B"),
    (25, 45): ("🔴 Fragile State", "#FF7043"),
    (45, 60): ("🟡 Hybrid / Volatile", "#FFB300"),
    (60, 75): ("🟢 Stable State", "#66BB6A"),
    (75, 90): ("🔵 Resilient Democracy", "#42A5F5"),
    (90, 101): ("⭐ Exemplary Governance", "#AB47BC"),
}

def get_resilience_label(score):
    for (lo, hi), (label, color) in RESILIENCE_LABELS.items():
        if lo <= score < hi:
            return label, color
    return ("Unknown", "#888")


def apply_historical_event(state, event_name, deltas):
    """Apply a historical event's delta dict to a state."""
    ns = copy.deepcopy(state)
    ns["Year"] += 1
    for k, v in deltas.items():
        if k in ns:
            ns[k] = ns.get(k, 50) + v
    for k, v in ns.items():
        if k not in ["Year", "Coup Count", "Amendments Passed"]:
            ns[k] = max(0.0, min(100.0, float(v)))
    return ns


def render():
    st.header("📜 Historical Constitutional Scenarios")
    st.write(
        "Explore **8 pivotal real-world constitutional moments** — from the Weimar Republic's collapse to "
        "Rwanda's recovery. Load any scenario as your simulation starting point, or play it back step-by-step "
        "to see how historical forces shaped governance outcomes."
    )

    # ── Category Filter ──────────────────────────────────────────────────────
    st.divider()
    all_categories = list(set(v["category"] for v in HISTORICAL_SCENARIOS.values()))
    selected_cats = st.multiselect(
        "Filter by Category:",
        all_categories,
        default=all_categories,
        format_func=lambda c: f"{CATEGORY_ICONS.get(c, '📌')} {c}"
    )

    filtered_scenarios = {
        k: v for k, v in HISTORICAL_SCENARIOS.items()
        if v["category"] in selected_cats
    }

    tab_explore, tab_playback, tab_compare, tab_lessons = st.tabs([
        "🗺️ Explore Scenarios",
        "▶️ Step-by-Step Playback",
        "📊 Comparative Analysis",
        "📖 Historical Lessons"
    ])

    # ── Tab 1: Card Grid ─────────────────────────────────────────────────────
    with tab_explore:
        st.subheader("Scenario Library")

        cols = st.columns(2)
        for i, (name, data) in enumerate(filtered_scenarios.items()):
            cat_color = CATEGORY_COLORS.get(data["category"], "#888")
            resilience_label, res_color = get_resilience_label(data["resilience_score"])

            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(
                        f"### {data['icon']} {name}"
                    )
                    st.caption(f"📅 {data['era']} &nbsp;|&nbsp; 🌍 {data['region']}")

                    # Category badge
                    st.markdown(
                        f"<span style='background:{cat_color};color:white;padding:3px 10px;"
                        f"border-radius:12px;font-size:12px;font-weight:600'>{data['category']}</span>",
                        unsafe_allow_html=True
                    )
                    st.write("")
                    st.write(data["description"])

                    # Resilience bar
                    score = data["resilience_score"]
                    st.markdown(f"**Resilience Score:** {resilience_label} ({score}/100)")
                    st.progress(score / 100)

                    st.markdown(f"**Historical Outcome:** `{data['final_outcome']}`")

                    c_load, c_playback = st.columns(2)
                    if c_load.button(f"📥 Load Starting State", key=f"load_{name}", use_container_width=True):
                        new_start = copy.deepcopy(data["starting_state"])
                        st.session_state.history = [new_start]
                        st.success(f"✅ Loaded '{name}' as new simulation starting point!")
                        st.rerun()

                    if c_playback.button(f"▶️ Play Full Scenario", key=f"play_{name}", use_container_width=True):
                        st.session_state["playback_scenario"] = name
                        st.session_state["playback_step"] = 0
                        st.rerun()

    # ── Tab 2: Step-by-Step Playback ─────────────────────────────────────────
    with tab_playback:
        st.subheader("Interactive Step-by-Step Scenario Playback")

        scenario_names = list(filtered_scenarios.keys())
        if not scenario_names:
            st.info("No scenarios match the selected categories.")
        else:
            selected_scenario = st.selectbox("Choose a Scenario:", scenario_names, key="pb_select")
            sc_data = HISTORICAL_SCENARIOS[selected_scenario]

            # Initialize playback state
            pb_key = f"pb_{selected_scenario}"
            if pb_key not in st.session_state:
                st.session_state[pb_key] = [copy.deepcopy(sc_data["starting_state"])]

            pb_hist = st.session_state[pb_key]
            current_step = len(pb_hist) - 1
            max_steps = len(sc_data["event_sequence"])

            # Info header
            st.info(
                f"**{sc_data['icon']} {selected_scenario}** | "
                f"Step {current_step}/{max_steps} | "
                f"Year: {pb_hist[-1]['Year']}"
            )

            # Navigation
            nav_c1, nav_c2, nav_c3 = st.columns([1, 1, 2])
            with nav_c1:
                if st.button("⏮️ Reset", use_container_width=True, key=f"reset_{selected_scenario}"):
                    st.session_state[pb_key] = [copy.deepcopy(sc_data["starting_state"])]
                    st.rerun()

            with nav_c2:
                if current_step < max_steps:
                    next_event_name, next_deltas = sc_data["event_sequence"][current_step]
                    if st.button(f"⏭️ Next: {next_event_name}", use_container_width=True, key=f"next_{selected_scenario}"):
                        new_state = apply_historical_event(pb_hist[-1], next_event_name, next_deltas)
                        st.session_state[pb_key].append(new_state)
                        st.rerun()
                else:
                    st.button("✅ Scenario Complete", use_container_width=True, disabled=True, key=f"done_{selected_scenario}")

            with nav_c3:
                if st.button("📥 Import to Main Simulation", use_container_width=True, key=f"import_{selected_scenario}"):
                    st.session_state.history = list(pb_hist)
                    st.success("✅ Imported playback state into main simulation!")

            st.divider()

            # Show the event sequence
            st.markdown("**Event Timeline:**")
            for step_i, (ev_name, ev_deltas) in enumerate(sc_data["event_sequence"]):
                if step_i < current_step:
                    icon = "✅"
                elif step_i == current_step:
                    icon = "▶️"
                else:
                    icon = "⏳"
                delta_str = ", ".join([f"{k}: {'+' if v>0 else ''}{v}" for k, v in ev_deltas.items()])
                st.markdown(f"{icon} **Step {step_i+1}:** {ev_name} — `{delta_str}`")

            st.divider()

            # Line chart of playback history
            if len(pb_hist) > 1:
                pb_df = pd.DataFrame(pb_hist)
                sel_metrics = st.multiselect(
                    "Metrics to visualize:",
                    METRIC_KEYS,
                    default=["Democracy Score", "GDP", "Social Trust", "Happiness Index", "Crime Rate"],
                    key="pb_metrics"
                )
                if sel_metrics:
                    # Step labels
                    step_labels = ["Start"] + [e[0] for e in sc_data["event_sequence"][:current_step]]
                    pb_df_plot = pb_df.copy()
                    pb_df_plot["Event"] = step_labels
                    fig_pb = px.line(
                        pb_df_plot, x="Event", y=sel_metrics,
                        markers=True,
                        title=f"{selected_scenario} — Metric Trajectory"
                    )
                    fig_pb.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#f0f0f0"),
                        xaxis=dict(gridcolor="#333", tickangle=-25),
                        yaxis=dict(range=[0, 110], gridcolor="#333"),
                        hovermode="x unified",
                        height=420
                    )
                    st.plotly_chart(fig_pb, use_container_width=True)

                # Current regime
                regime = get_regime_type(pb_hist[-1])
                res_label, res_color = get_resilience_label(
                    (pb_hist[-1]["Democracy Score"] + pb_hist[-1]["Social Trust"] +
                     pb_hist[-1]["GDP"] + pb_hist[-1]["Healthcare Quality"]) / 4
                )
                st.markdown(f"**Current Regime:** {regime} &nbsp;&nbsp; **Resilience:** {res_label}")
            else:
                st.info("Click '⏭️ Next' to begin playback")

    # ── Tab 3: Comparative Analysis ───────────────────────────────────────────
    with tab_compare:
        st.subheader("Compare Starting vs. Ending States Across Scenarios")

        # Build ending states by simulating all events
        compare_rows = []
        for sc_name, sc_data in filtered_scenarios.items():
            start_state = copy.deepcopy(sc_data["starting_state"])
            end_state = copy.deepcopy(start_state)
            for ev_name, ev_deltas in sc_data["event_sequence"]:
                end_state = apply_historical_event(end_state, ev_name, ev_deltas)

            compare_rows.append({
                "Scenario": sc_name[:35] + "..." if len(sc_name) > 35 else sc_name,
                "Phase": "Start",
                "Resilience Score": sc_data["resilience_score"],
                **{k: start_state.get(k, 0) for k in METRIC_KEYS}
            })
            final_resilience = (end_state["Democracy Score"] + end_state["Social Trust"] +
                                end_state["GDP"] + end_state["Healthcare Quality"]) / 4
            compare_rows.append({
                "Scenario": sc_name[:35] + "..." if len(sc_name) > 35 else sc_name,
                "Phase": "End",
                "Resilience Score": final_resilience,
                **{k: end_state.get(k, 0) for k in METRIC_KEYS}
            })

        cmp_df = pd.DataFrame(compare_rows)

        cmp_metric = st.selectbox("Metric to compare:", METRIC_KEYS, key="cmp_metric",
                                  index=METRIC_KEYS.index("Democracy Score"))

        fig_cmp = px.bar(
            cmp_df, x="Scenario", y=cmp_metric, color="Phase",
            barmode="group",
            color_discrete_map={"Start": "#4ECDC4", "End": "#FF6B6B"},
            title=f"{cmp_metric}: Before vs. After Historical Events",
        )
        fig_cmp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            xaxis=dict(gridcolor="#333", tickangle=-25),
            yaxis=dict(range=[0, 110], gridcolor="#333"),
            height=480, margin=dict(b=130)
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Resilience bubble chart
        st.subheader("Resilience Score Comparison")
        bubble_df = cmp_df[cmp_df["Phase"] == "End"].copy()
        fig_bub = px.scatter(
            bubble_df,
            x="Scenario", y="Resilience Score",
            size="Resilience Score",
            color="Resilience Score",
            color_continuous_scale="RdYlGn",
            title="Final Resilience Score by Historical Scenario",
            size_max=50,
        )
        fig_bub.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            xaxis=dict(tickangle=-25),
            height=380,
            margin=dict(b=120)
        )
        st.plotly_chart(fig_bub, use_container_width=True)

    # ── Tab 4: Lessons ────────────────────────────────────────────────────────
    with tab_lessons:
        st.subheader("📖 Distilled Historical Lessons")
        st.write("Extract policy wisdom from each scenario:")

        for sc_name, sc_data in filtered_scenarios.items():
            cat_color = CATEGORY_COLORS.get(sc_data["category"], "#888")
            with st.expander(f"{sc_data['icon']} {sc_name} ({sc_data['era']})"):
                st.markdown(
                    f"<span style='background:{cat_color};color:white;padding:2px 10px;"
                    f"border-radius:10px;font-size:12px'>{sc_data['category']}</span>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.write(sc_data["description"])
                st.markdown("**Key Policy Lessons:**")
                for lesson in sc_data["lessons"]:
                    st.markdown(f"• {lesson}")
                res_label, res_color = get_resilience_label(sc_data["resilience_score"])
                st.markdown(
                    f"**Final Outcome:** `{sc_data['final_outcome']}` &nbsp;|&nbsp; "
                    f"**Resilience:** {res_label} ({sc_data['resilience_score']}/100)"
                )

                # Apply to simulation button
                if st.button(f"🚀 Load this scenario into Simulation", key=f"lesson_load_{sc_name}"):
                    st.session_state.history = [copy.deepcopy(sc_data["starting_state"])]
                    st.success(f"✅ Loaded '{sc_name}' as new simulation starting point!")
                    st.rerun()
