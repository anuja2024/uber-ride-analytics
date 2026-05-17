import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components.metrics import kpi_card, section_header, page_header
from components.charts import COLORS


def show(data, kpis):
    page_header("Vehicle Type Analysis", "Performance breakdown by vehicle category")

    vdf = data["vehicle"]
    top = vdf.iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Top Vehicle",  top["vehicle_type"],               "by revenue")
    kpi_card(k2, "Top Revenue",  f"₹{int(top['total_revenue']):,}", "best vehicle")
    kpi_card(k3, "Top Rides",    f"{int(top['total_rides']):,}",    "best vehicle")
    kpi_card(k4, "Avg Distance", f"{top['avg_distance']} km",       "best vehicle")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Revenue by Vehicle Type")
        fig1 = go.Figure(go.Bar(
            x=vdf["vehicle_type"], y=vdf["total_revenue"],
            marker=dict(
                color=vdf["total_revenue"],
                colorscale=[[0, "#1a3a4a"], [0.5, "#4d9fff"], [1, "#00d4aa"]],
                showscale=False,
                line=dict(color="#0a0a0f", width=1),
            ),
            text=vdf["total_revenue"].apply(lambda x: f"₹{x/1e6:.1f}M"),
            textposition="outside",
            textfont=dict(color="#8891a8", size=11),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ))
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=340,
            xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title="Revenue (₹)", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        section_header("Ride Share by Vehicle Type")
        fig2 = px.pie(
            vdf, names="vehicle_type", values="total_rides",
            color_discrete_sequence=COLORS, hole=0.5,
        )
        fig2.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont=dict(size=11, color="#ffffff"),
            marker=dict(line=dict(color="#0a0a0f", width=2)),
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=340,
            legend=dict(font=dict(color="#8891a8", size=11),
                        orientation="h", y=-0.15),
        )
        st.plotly_chart(fig2, use_container_width=True)

    section_header("Vehicle Performance Table")
    display = vdf.copy()
    display["total_revenue"] = display["total_revenue"].apply(lambda x: f"₹{x:,.0f}")
    display["avg_fare"]      = display["avg_fare"].apply(lambda x: f"₹{x:,.0f}")
    display["avg_distance"]  = display["avg_distance"].apply(lambda x: f"{x} km")
    display["avg_rating"]    = display["avg_rating"].apply(lambda x: f"{x} / 5.0")
    display.columns = ["Vehicle", "Rides", "Revenue", "Avg Fare", "Avg Distance", "Avg Rating"]
    st.dataframe(display, use_container_width=True, hide_index=True)