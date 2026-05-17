import streamlit as st


def kpi_card(col, label, value, sub):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)


def section_header(title):
    st.markdown(
        f'<div class="section-header">{title}</div>',
        unsafe_allow_html=True,
    )


def page_header(title, subtitle=""):
    st.markdown(
        f'<div class="page-title">{title}</div>'
        f'<div class="page-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def insight_box(title, content):
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">{title}</div>
        <div class="insight-text">{content}</div>
    </div>""", unsafe_allow_html=True)