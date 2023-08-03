import streamlit as st

from sub_dude.webui.navigation import navigation_buttons


def translate():
    """Translate"""
    st.title("Translate")
    navigation_buttons(back="transcribe", back_label="Transcribe")

    st.write(st.session_state.transcription_format)