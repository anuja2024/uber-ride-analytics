import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components.metrics import kpi_card, section_header, page_header
from components.charts import DARK, COLORS


def show(data, kpis):
    st.markdown("""
    <div class="live-badge">
        <div class="live-dot"></div>
        Live — updates every 10 seconds
    </div>
    """, unsafe_allow_html=True)
    page_header("Overview", "High-level performance across all rides · 2024")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    rev = int(kpis["total_revenue"])
    kpi_card(k1, "Completed Rides", f"{int(kpis['total_bookings']):,}", "bookings")
    kpi_card(k2, "Total Revenue",   f"₹{rev/1e6:.1f}M",               "all time")
    kpi_card(k3, "Avg Fare",        f"₹{kpis['avg_fare']}",           "per ride")
    kpi_card(k4, "Avg Distance",    f"{kpis['avg_distance']} km",      "per ride")
    kpi_card(k5, "Driver Rating",   f"{kpis['avg_driver_rating']}",    "out of 5")
    kpi_card(k6, "Customer Rating", f"{kpis['avg_customer_rating']}",  "out of 5")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Booking Status Breakdown")
        fig1 = px.pie(
            data["status"], names="booking_status", values="total",
            color_discrete_sequence=COLORS, hole=0.55,
        )
        fig1.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont=dict(size=11, color="#ffffff"),
            marker=dict(line=dict(color="#0a0a0f", width=2)),
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=360,
            legend=dict(font=dict(color="#8891a8", size=11),
                        orientation="h", y=-0.15),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        section_header("Monthly Bookings & Completions")
        mdf = data["monthly"]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=mdf["month"], y=mdf["total_bookings"],
            mode="lines+markers", name="Total",
            line=dict(color="#00d4aa", width=2.5),
            marker=dict(size=7, color="#00d4aa",
                        line=dict(color="#0a0a0f", width=2)),
            fill="tozeroy", fillcolor="rgba(0,212,170,0.06)",
        ))
        fig2.add_trace(go.Scatter(
            x=mdf["month"], y=mdf["completed"],
            mode="lines+markers", name="Completed",
            line=dict(color="#4d9fff", width=1.5, dash="dot"),
            marker=dict(size=5, color="#4d9fff"),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=360,
            xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title="Rides", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            legend=dict(orientation="h", y=1.1,
                        font=dict(size=11, color="#8891a8")),
            hovermode="x unified",
        )
        st.plotly_chart(fig2, use_container_width=True)

    section_header("Daily Revenue & Bookings Over Time")
    tdf = data["time"]
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=tdf["date"], y=tdf["daily_revenue"], name="Revenue",
        line=dict(color="#00d4aa", width=2),
        fill="tozeroy", fillcolor="rgba(0,212,170,0.05)",
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=tdf["date"], y=tdf["total_bookings"], name="Bookings",
        line=dict(color="#4d9fff", width=1.5, dash="dot"),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>",
    ))
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0d0e1a",
        font=dict(family="Inter", color="#8891a8", size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
        xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        yaxis=dict(title="Revenue (₹)", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        yaxis2=dict(title="Bookings", overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)"),
        legend=dict(orientation="h", y=1.12,
                    font=dict(size=11, color="#8891a8")),
        hovermode="x unified",
    )
    st.plotly_chart(fig3, use_container_width=True)