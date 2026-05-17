import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components.metrics import kpi_card, section_header, page_header, insight_box
from components.charts import COLORS


def show(data, kpis):
    page_header("Cancellation Analysis", "Understanding why rides are cancelled")

    status_df    = data["status"]
    total_all    = status_df["total"].sum()
    completed    = status_df[status_df["booking_status"] == "Completed"]["total"].sum()
    cancelled    = status_df[status_df["booking_status"].str.contains("Cancelled")]["total"].sum()
    cancel_rate  = round(cancelled / total_all * 100, 1)
    success_rate = round(completed / total_all * 100, 1)
    cdf          = data["cancel"]
    cust_c       = int(cdf[cdf["cancelled_by"] == "Customer"]["total"].iloc[0])
    drv_c        = int(cdf[cdf["cancelled_by"] == "Driver"]["total"].iloc[0])

    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Total Bookings",   f"{int(total_all):,}", "all time")
    kpi_card(k2, "Success Rate",     f"{success_rate}%",    "completed")
    kpi_card(k3, "Cancel Rate",      f"{cancel_rate}%",     "of all bookings")
    kpi_card(k4, "Customer Cancels", f"{cust_c:,}",         "rides")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Customer vs Driver Cancellations")
        fig1 = go.Figure(go.Bar(
            x=cdf["cancelled_by"], y=cdf["total"],
            marker=dict(color=["#ff6b6b", "#ffd166"],
                        line=dict(color="#0a0a0f", width=1)),
            text=cdf["total"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color="#8891a8", size=13),
            hovertemplate="<b>%{x}</b><br>Cancellations: %{y:,}<extra></extra>",
        ))
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=40, b=10),
            height=340,
            showlegend=False,
            xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title="Cancellations", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        section_header("Booking Status Overview")
        fig2 = px.pie(
            status_df, names="booking_status", values="total",
            color_discrete_sequence=COLORS, hole=0.55,
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
            legend=dict(font=dict(color="#8891a8", size=10),
                        orientation="h", y=-0.2),
        )
        st.plotly_chart(fig2, use_container_width=True)

    section_header("Key Insights")
    c1, c2 = st.columns(2)
    with c1:
        insight_box("Completion Rate",
            f"<b style='color:#00d4aa;font-size:20px;'>{success_rate}%</b> "
            f"of {total_all:,} total bookings completed successfully.")
        insight_box("Cancellation Split",
            f"Customers cancelled <b style='color:#ff6b6b;'>{cust_c:,}</b> rides · "
            f"Drivers cancelled <b style='color:#ffd166;'>{drv_c:,}</b> rides.")
    with c2:
        insight_box("Cancel Rate",
            f"Overall cancellation rate is <b style='color:#ff6b6b;'>{cancel_rate}%</b> "
            f"of all bookings.")
        insight_box("Total Cancelled",
            f"<b style='color:#ffd166;'>{int(cancelled):,}</b> rides cancelled "
            f"out of <b style='color:#ffffff;'>{int(total_all):,}</b> total bookings.")