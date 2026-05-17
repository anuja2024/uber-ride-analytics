import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components.metrics import kpi_card, section_header, page_header
from components.charts import COLORS


def show(data, kpis):
    page_header("Revenue Analysis", "Revenue trends, payment methods and fare breakdown")

    rev = int(kpis["total_revenue"])
    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Total Revenue", f"Rs.{rev/1e6:.2f}M",                      "completed")
    kpi_card(k2, "Avg Fare",      f"Rs.{kpis['avg_fare']}",                  "per ride")
    kpi_card(k3, "Daily Avg",     f"Rs.{rev/365:,.0f}",                      "per day")
    kpi_card(k4, "Top Payment",   data["payment"].iloc[0]["payment_method"],  "by revenue")

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("Monthly Revenue Trend")
    mdf = data["monthly"]
    fig1 = go.Figure(go.Bar(
        x=mdf["month"],
        y=mdf["monthly_revenue"],
        marker=dict(
            color=mdf["monthly_revenue"],
            colorscale=[[0, "#1a3a4a"], [0.5, "#4d9fff"], [1, "#00d4aa"]],
            showscale=False,
            line=dict(color="#0a0a0f", width=1),
        ),
        text=mdf["monthly_revenue"].apply(lambda x: f"Rs.{x/1e6:.1f}M"),
        textposition="outside",
        textfont=dict(color="#8891a8", size=10),
        hovertemplate="<b>%{x}</b><br>Revenue: Rs.%{y:,.0f}<extra></extra>",
    ))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0d0e1a",
        font=dict(family="Inter", color="#8891a8", size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        height=300,
        xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        yaxis=dict(title="Revenue (Rs.)", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
    )
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Revenue by Payment Method")
        pdf = data["payment"]
        fig2 = go.Figure(go.Bar(
            x=pdf["revenue"],
            y=pdf["payment_method"],
            orientation="h",
            marker=dict(
                color=pdf["revenue"],
                colorscale=[[0, "#1a2a4a"], [0.5, "#4d9fff"], [1, "#00d4aa"]],
                showscale=False,
                line=dict(color="#0a0a0f", width=1),
            ),
            text=pdf["revenue"].apply(lambda x: f"Rs.{x/1e6:.1f}M"),
            textposition="outside",
            textfont=dict(color="#8891a8", size=11),
            hovertemplate="<b>%{y}</b><br>Revenue: Rs.%{x:,.0f}<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=320,
            xaxis=dict(title="Revenue (Rs.)", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        section_header("Revenue Share by Vehicle")
        vdf = data["vehicle"]
        fig3 = px.pie(
            vdf,
            names="vehicle_type",
            values="total_revenue",
            color_discrete_sequence=COLORS,
            hole=0.5,
        )
        fig3.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont=dict(size=11, color="#ffffff"),
            marker=dict(line=dict(color="#0a0a0f", width=2)),
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=320,
            legend=dict(
                font=dict(color="#8891a8", size=11),
                orientation="h",
                y=-0.15,
            ),
        )
        st.plotly_chart(fig3, use_container_width=True)