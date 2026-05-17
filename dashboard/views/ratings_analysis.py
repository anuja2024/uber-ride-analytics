import streamlit as st
import plotly.graph_objects as go
from components.metrics import kpi_card, section_header, page_header


def show(data, kpis):
    page_header("Ratings Analysis", "Driver and customer satisfaction scores by vehicle")

    rdf = data["ratings"]

    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Avg Driver Rating",   f"{kpis['avg_driver_rating']}",  "out of 5.0")
    kpi_card(k2, "Avg Customer Rating", f"{kpis['avg_customer_rating']}", "out of 5.0")
    kpi_card(k3, "Best Rated Vehicle",  rdf.iloc[0]["vehicle_type"],      "by customer")
    kpi_card(k4, "Vehicles Tracked",    f"{len(rdf)}",                    "categories")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Ratings by Vehicle Type")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name="Driver Rating",
            x=rdf["vehicle_type"], y=rdf["avg_driver_rating"],
            marker_color="#4d9fff",
            marker_line=dict(color="#0a0a0f", width=1),
            text=rdf["avg_driver_rating"],
            textposition="outside",
            textfont=dict(color="#4d9fff", size=11),
        ))
        fig1.add_trace(go.Bar(
            name="Customer Rating",
            x=rdf["vehicle_type"], y=rdf["avg_customer_rating"],
            marker_color="#00d4aa",
            marker_line=dict(color="#0a0a0f", width=1),
            text=rdf["avg_customer_rating"],
            textposition="outside",
            textfont=dict(color="#00d4aa", size=11),
        ))
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=360,
            barmode="group",
            xaxis=dict(gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title="Rating", range=[4.0, 4.6],
                       gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            legend=dict(orientation="h", y=1.12,
                        font=dict(size=12, color="#8891a8")),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        section_header("Radar Chart — Ratings by Vehicle")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(
            r=rdf["avg_customer_rating"], theta=rdf["vehicle_type"],
            fill="toself", fillcolor="rgba(0,212,170,0.15)",
            line=dict(color="#00d4aa", width=2), name="Customer",
            marker=dict(size=8, color="#00d4aa"),
        ))
        fig2.add_trace(go.Scatterpolar(
            r=rdf["avg_driver_rating"], theta=rdf["vehicle_type"],
            fill="toself", fillcolor="rgba(77,159,255,0.12)",
            line=dict(color="#4d9fff", width=2), name="Driver",
            marker=dict(size=8, color="#4d9fff"),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=360,
            polar=dict(
                bgcolor="#0d0e1a",
                radialaxis=dict(visible=True, range=[4.0, 4.6],
                    gridcolor="#1a1a2e", linecolor="#1a1a2e",
                    tickfont=dict(color="#8891a8", size=10)),
                angularaxis=dict(gridcolor="#1a1a2e", linecolor="#1a1a2e",
                    tickfont=dict(color="#8891a8", size=11)),
            ),
            legend=dict(orientation="h", y=1.1,
                        font=dict(size=12, color="#8891a8")),
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(family="Inter", color="#8891a8"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    section_header("Detailed Ratings Table")
    display = rdf.copy()
    display["avg_driver_rating"]   = display["avg_driver_rating"].apply(lambda x: f"{x} / 5.0")
    display["avg_customer_rating"] = display["avg_customer_rating"].apply(lambda x: f"{x} / 5.0")
    display["total_rides"]         = display["total_rides"].apply(lambda x: f"{x:,}")
    display.columns = ["Vehicle Type", "Driver Rating", "Customer Rating", "Total Rides"]
    st.dataframe(display, use_container_width=True, hide_index=True)