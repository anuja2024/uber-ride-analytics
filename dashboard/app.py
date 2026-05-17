import streamlit as st
st.set_page_config(
    page_title="Uber Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, DASH)

from components.sidebar import render_sidebar
from components.styles import load_css
from analytics.queries import (
    get_kpis, get_bookings_by_status, get_revenue_by_vehicle,
    get_bookings_over_time, get_payment_method_split,
    get_cancellation_reasons, get_ratings_by_vehicle,
    get_top_routes, get_monthly_stats,
)

st.markdown(load_css(), unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    return {
        "kpis":    get_kpis(),
        "status":  get_bookings_by_status(),
        "vehicle": get_revenue_by_vehicle(),
        "time":    get_bookings_over_time(),
        "payment": get_payment_method_split(),
        "cancel":  get_cancellation_reasons(),
        "ratings": get_ratings_by_vehicle(),
        "routes":  get_top_routes(),
        "monthly": get_monthly_stats(),
    }

data = load_data()
kpis = data["kpis"]
page = render_sidebar().strip()

if page == "Home":
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div style="font-size:5rem; font-weight:800; color:white;
                    letter-spacing:-3px; line-height:1; margin-bottom:12px;
                    font-family:'Inter',sans-serif;">Uber.</div>
        <div style="font-size:1.3rem; color:#6b7399; margin-bottom:24px;">
            Real-Time Ride Analytics · India · 2024
        </div>
        <div style="font-size:1rem; color:#a0aec0; line-height:1.8;
                    margin-bottom:32px; max-width:500px;">
            End-to-end analytics platform built on
            <span style="color:#00d4aa; font-weight:600;">150,000 real rides</span>.
            Powered by PostgreSQL, Python and Streamlit.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Completed Rides", "93,000")
        c2.metric("Total Revenue",   "₹47M")
        c3.metric("Avg Rating",      "4.40")
        c4.metric("Success Rate",    "62%")

    with col2:
        st.markdown("""
        <div style="background:#12131f; border:1px solid #1e2040;
                    border-radius:16px; padding:2rem; margin-top:0.5rem;">
            <div style="color:#00d4aa; font-size:11px; font-weight:600;
                        letter-spacing:0.15em; text-transform:uppercase;
                        margin-bottom:1rem;">What this project demonstrates</div>
            <div style="color:#a0aec0; font-size:14px; line-height:2.4;">
                Real-time data pipelines<br>
                SQL analytics with PostgreSQL<br>
                Python ETL pipeline<br>
                Interactive dashboard engineering<br>
                Multi-page application architecture
            </div>
            <div style="margin-top:1.5rem; color:#00d4aa; font-size:11px;
                        font-weight:600; letter-spacing:0.15em;
                        text-transform:uppercase; margin-bottom:0.8rem;">
                Tech stack
            </div>
            <div style="color:#a0aec0; font-size:14px; line-height:2.4;">
                Python · PostgreSQL · Streamlit · Plotly · Pandas
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Explore the data")
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Overview", "Vehicle Performance", "Quick Stats"])

    with tab1:
        t1, t2, t3 = st.columns(3)
        status_df = data["status"]
        total     = status_df["total"].sum()
        completed = status_df[status_df["booking_status"] == "Completed"]["total"].sum()
        cancelled = status_df[status_df["booking_status"].str.contains("Cancelled")]["total"].sum()
        t1.metric("Total Bookings", f"{int(total):,}")
        t2.metric("Completed",      f"{int(completed):,}", f"{round(completed/total*100,1)}%")
        t3.metric("Cancelled",      f"{int(cancelled):,}", f"-{round(cancelled/total*100,1)}%")

        fig = px.pie(
            status_df,
            names="booking_status",
            values="total",
            color_discrete_sequence=["#00d4aa","#4d9fff","#ff6b6b","#ffd166","#a78bfa"],
            hole=0.6,
        )
        fig.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont=dict(size=11, color="#ffffff"),
            marker=dict(line=dict(color="#0a0a0f", width=2)),
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            legend=dict(orientation="h", y=-0.15,
                        font=dict(color="#8891a8", size=11)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        vdf = data["vehicle"]
        fig2 = go.Figure(go.Bar(
            x=vdf["vehicle_type"],
            y=vdf["total_revenue"],
            marker=dict(
                color=vdf["total_revenue"],
                colorscale=[[0,"#1a3a4a"],[0.5,"#4d9fff"],[1,"#00d4aa"]],
                showscale=False,
                line=dict(color="#0a0a0f", width=1),
            ),
            text=vdf["total_revenue"].apply(lambda x: f"₹{x/1e6:.1f}M"),
            textposition="outside",
            textfont=dict(color="#8891a8", size=11),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0d0e1a",
            font=dict(family="Inter", color="#8891a8", size=12),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            xaxis=dict(title="", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
            yaxis=dict(title="Revenue (₹)", gridcolor="#1a1a2e", linecolor="#1a1a2e"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Avg Fare",        f"₹{kpis['avg_fare']}")
        s2.metric("Avg Distance",    f"{kpis['avg_distance']} km")
        s3.metric("Driver Rating",   f"{kpis['avg_driver_rating']} / 5")
        s4.metric("Customer Rating", f"{kpis['avg_customer_rating']} / 5")

        pay_df = data["payment"]
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Revenue by payment method**")
        for _, row in pay_df.iterrows():
            pct = int(row["revenue"] / pay_df["revenue"].sum() * 100)
            st.progress(
                pct / 100,
                text=f"{row['payment_method']} — ₹{row['revenue']/1e6:.1f}M ({pct}%)"
            )

elif page == "Overview":
    from views.overview import show
    show(data, kpis)

elif page == "Vehicle Type":
    from views.vehicle_analysis import show
    show(data, kpis)

elif page == "Revenue":
    from views.revenue_analysis import show
    show(data, kpis)

elif page == "Cancellation":
    from views.cancellation_analysis import show
    show(data, kpis)

elif page == "Ratings":
    from views.ratings_analysis import show
    show(data, kpis)