import streamlit as st
from PIL import Image
import os


def render_sidebar():
    # Check if navigation was triggered from home page buttons
    if "nav" in st.session_state:
        nav_value = st.session_state["nav"]
    else:
        nav_value = "Home"

    pages = ["Home", "Overview", "Vehicle Type",
             "Revenue", "Cancellation", "Ratings"]

    with st.sidebar:
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets", "uver_logo.jpg"
        )
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, width=80)

        st.markdown("""
        <div style="padding:0.5rem 1rem 1rem;">
            <div style="color:#00d4aa; font-size:30px;
                        letter-spacing:0.2em; font-weight:500;
                        text-transform:uppercase; margin-bottom:1rem;">
                Analytics Platform
            </div>
            <div style="color:#6b7399; font-size:10px;
                        letter-spacing:0.2em; text-transform:uppercase;
                        margin-bottom:0.5rem; font-weight:600;">
                Navigation
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Get index of current page
        if nav_value in pages:
            idx = pages.index(nav_value)
        else:
            idx = 0

        page = st.radio(
            "nav",
            pages,
            index=idx,
            label_visibility="collapsed",
        )

        # Clear session state nav after use
        if "nav" in st.session_state:
            del st.session_state["nav"]

        # st.markdown("""
        # <div style="padding:1.2rem; margin-top:2rem;
        #             border-top:1px solid #1a1a2e;">
        #     <div style="color:#6b7399; font-size:10px;
        #                 letter-spacing:0.15em; text-transform:uppercase;
        #                 margin-bottom:0.8rem; font-weight:600;">Dataset</div>
        #     <div style="color:#8891a8; font-size:13px; line-height:2.2;">
        #         150,000 rides<br>
        #         Full Year 2024<br>
        #         India<br>
        #         6 vehicle types<br>
        #         5 payment methods<br>
        #         PostgreSQL
        #     </div>
        # </div>
        # """, unsafe_allow_html=True)

    return page