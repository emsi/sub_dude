import streamlit as st


def navigation_buttons(
    back=None, forward=None, position="bottom", forward_label="Next", back_label="Back"
):
    """Navigation buttons for the fetch page"""
    back_col, forth, _ = st.columns([0.14, 0.14, 0.8])

    if back and back_col.button(f"← {back_label}", key=f"back_{position}"):
        st.session_state["STATE"] = back
        st.experimental_rerun()

    if forward and forth.button(f"{forward_label} →", key=f"forward_{position}"):
        st.session_state["STATE"] = forward
        st.experimental_rerun()
