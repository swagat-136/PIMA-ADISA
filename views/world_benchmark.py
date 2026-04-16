import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.world_governance import WORLD_COUNTRIES, REGIONS
from core.engine import METRIC_KEYS

# Metrics where lower is better (will be inverted for radar display)
LOWER_IS_BETTER = ["Crime Rate", "Income Inequality", "Corruption Index", "Coup Count"]

def normalize_for_radar(state_dict, invert_bad=True):
    """Returns a dict of metric -> score, inverting bad metrics so higher=better always."""
    result = {}
    for k in METRIC_KEYS:
        v = state_dict.get(k, 50)
        if invert_bad and k in LOWER_IS_BETTER:
            result[k] = 100 - v
        else:
            result[k] = v
    return result


def render():
    st.header("🌍 World Governance Benchmarking")
    st.write(
        "Compare your simulated nation against **20 real-world countries** across all governance metrics. "
        "Data is normalized from Freedom House, World Bank, UN HDI, Transparency International, and the EIU Democracy Index (2023)."
    )

    if "history" not in st.session_state or not st.session_state.history:
        st.warning("Simulation state not initialized.")
        return

    current_state = st.session_state.history[-1]

    # ─── Sidebar-style filters in columns ───────────────────────────────────
    st.divider()
    c_left, c_right = st.columns([2, 2])
    with c_left:
        region_filter = st.selectbox(
            "Filter by Region / Group",
            ["All Countries"] + list(REGIONS.keys())
        )
    with c_right:
        compare_metric = st.selectbox(
            "Primary Comparison Metric",
            METRIC_KEYS,
            index=METRIC_KEYS.index("Democracy Score")
        )

    # Build filtered country list
    if region_filter == "All Countries":
        country_pool = list(WORLD_COUNTRIES.keys())
    else:
        country_pool = REGIONS.get(region_filter, list(WORLD_COUNTRIES.keys()))

    # ─── Tab Layout ──────────────────────────────────────────────────────────
    tab_rank, tab_radar, tab_scatter, tab_heat, tab_table = st.tabs([
        "📊 Global Rankings",
        "🕸️ Radar Comparison",
        "🔵 Scatter Analysis",
        "🌡️ Heatmap Matrix",
        "📋 Data Table"
    ])

    # Build dataframe with simulation included
    records = []
    sim_normalized = normalize_for_radar(current_state)
    sim_row = {**{k: current_state.get(k, 0) for k in METRIC_KEYS}, "Country": "🖥️ Your Simulation", "Is_Sim": True}
    records.append(sim_row)

    for country in country_pool:
        cdata = WORLD_COUNTRIES[country]
        row = {**{k: cdata.get(k, 0) for k in METRIC_KEYS}, "Country": country, "Is_Sim": False}
        records.append(row)

    df = pd.DataFrame(records)

    # ── Tab 1: Rankings ────────────────────────────────────────────────────
    with tab_rank:
        st.subheader(f"Global Ranking by: {compare_metric}")

        # Sort (handle lower-is-better)
        ascending = compare_metric in LOWER_IS_BETTER
        df_sorted = df.sort_values(compare_metric, ascending=ascending).reset_index(drop=True)
        df_sorted["Rank"] = df_sorted.index + 1

        # Color: highlight simulation
        colors = ["#FF6B6B" if r else "#4ECDC4" for r in df_sorted["Is_Sim"]]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_sorted["Country"],
            y=df_sorted[compare_metric],
            marker_color=colors,
            text=[f"{v:.1f}" for v in df_sorted[compare_metric]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>" + compare_metric + ": %{y:.1f}<extra></extra>"
        ))
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            xaxis=dict(tickangle=-40, gridcolor="#333"),
            yaxis=dict(range=[0, 110], gridcolor="#333"),
            title=f"{compare_metric} — Your Simulation vs. World",
            height=480,
            margin=dict(b=120)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Find your rank
        sim_rank = df_sorted[df_sorted["Is_Sim"] == True]["Rank"].values[0]
        total = len(df_sorted)
        pct = (sim_rank / total) * 100
        st.info(f"🖥️ Your nation ranks **#{sim_rank} of {total}** on {compare_metric} ({pct:.0f}th percentile)")

        # Closest peer
        non_sim = df_sorted[df_sorted["Is_Sim"] == False]
        closest = non_sim.iloc[(non_sim[compare_metric] - current_state.get(compare_metric, 50)).abs().argsort()[:1]]
        st.success(f"🔗 Closest real-world peer on this metric: **{closest['Country'].values[0]}** ({closest[compare_metric].values[0]:.1f})")

    # ── Tab 2: Radar Chart ─────────────────────────────────────────────────
    with tab_radar:
        st.subheader("Radar Comparison — All Metrics (higher = better, bad metrics inverted)")

        compare_countries = st.multiselect(
            "Select countries to overlay:",
            country_pool,
            default=country_pool[:3] if len(country_pool) >= 3 else country_pool
        )

        radar_metrics = [m for m in METRIC_KEYS if m not in ["Coup Count", "Amendments Passed"]]

        fig_radar = go.Figure()

        # Add simulation trace
        sim_vals = [normalize_for_radar(current_state)[m] for m in radar_metrics]
        fig_radar.add_trace(go.Scatterpolar(
            r=sim_vals + [sim_vals[0]],
            theta=radar_metrics + [radar_metrics[0]],
            fill="toself",
            name="🖥️ Your Simulation",
            line=dict(color="#FF6B6B", width=2.5),
            fillcolor="rgba(255, 107, 107, 0.15)"
        ))

        palette = ["#4ECDC4", "#FFE66D", "#A8E6CF", "#FF8B94", "#C3B1E1", "#FFA07A"]
        for i, country in enumerate(compare_countries):
            cdata = WORLD_COUNTRIES.get(country, {})
            norm = normalize_for_radar(cdata)
            vals = [norm.get(m, 50) for m in radar_metrics]
            color = palette[i % len(palette)]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=radar_metrics + [radar_metrics[0]],
                fill="toself",
                name=country,
                line=dict(color=color, width=1.5),
                fillcolor=f"rgba({int(color[1:3],16)}, {int(color[3:5],16)}, {int(color[5:7],16)}, 0.08)"
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#444", tickfont=dict(size=9)),
                angularaxis=dict(gridcolor="#444")
            ),
            showlegend=True,
            height=550,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            legend=dict(bgcolor="rgba(30,30,30,0.8)", bordercolor="#555", borderwidth=1)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Note: Crime Rate, Income Inequality, and Corruption Index are inverted so higher values always represent better governance.")

    # ── Tab 3: Scatter ─────────────────────────────────────────────────────
    with tab_scatter:
        st.subheader("Governance Scatter Analysis")
        sc1, sc2 = st.columns(2)
        with sc1:
            x_axis = st.selectbox("X-axis", METRIC_KEYS, index=METRIC_KEYS.index("GDP"), key="sc_x")
        with sc2:
            y_axis = st.selectbox("Y-axis", METRIC_KEYS, index=METRIC_KEYS.index("Democracy Score"), key="sc_y")

        fig_sc = px.scatter(
            df,
            x=x_axis, y=y_axis,
            text="Country",
            color="Is_Sim",
            color_discrete_map={True: "#FF6B6B", False: "#4ECDC4"},
            labels={"Is_Sim": ""},
            title=f"{x_axis} vs {y_axis}",
            hover_data={k: True for k in METRIC_KEYS},
            size=[14 if s else 10 for s in df["Is_Sim"]]
        )
        fig_sc.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#222")))
        fig_sc.update_layout(
            plot_bgcolor="rgba(20,20,30,0.8)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0f0f0"),
            xaxis=dict(gridcolor="#333"),
            yaxis=dict(gridcolor="#333"),
            height=520,
            showlegend=False
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Tab 4: Heatmap ─────────────────────────────────────────────────────
    with tab_heat:
        st.subheader("Full Governance Heatmap")

        heat_metrics = st.multiselect(
            "Metrics to include:",
            METRIC_KEYS,
            default=["Democracy Score", "GDP", "Social Trust", "Crime Rate",
                     "Press Freedom", "Income Inequality", "Corruption Index", "Happiness Index"]
        )

        if heat_metrics:
            # Build matrix
            heat_df = df[["Country"] + heat_metrics].set_index("Country")
            # Normalize each column 0-100
            heat_norm = heat_df.copy()
            for col in heat_metrics:
                rng = heat_norm[col].max() - heat_norm[col].min()
                if rng > 0:
                    heat_norm[col] = ((heat_norm[col] - heat_norm[col].min()) / rng) * 100
                if col in LOWER_IS_BETTER:
                    heat_norm[col] = 100 - heat_norm[col]

            fig_heat = px.imshow(
                heat_norm.T,
                color_continuous_scale="RdYlGn",
                aspect="auto",
                title="Normalized Governance Scores (Green = Better)",
                labels=dict(color="Score")
            )
            fig_heat.update_layout(
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0f0f0"),
                coloraxis_colorbar=dict(tickfont=dict(color="#f0f0f0"))
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("Select at least one metric.")

    # ── Tab 5: Data Table ──────────────────────────────────────────────────
    with tab_table:
        st.subheader("Raw Comparative Data")
        display_cols = ["Country"] + METRIC_KEYS
        st.dataframe(
            df[display_cols].style.background_gradient(cmap="RdYlGn", subset=METRIC_KEYS),
            use_container_width=True,
            height=600
        )
        csv = df[display_cols].to_csv(index=False)
        st.download_button("⬇️ Download as CSV", data=csv, file_name="governance_comparison.csv", mime="text/csv")
