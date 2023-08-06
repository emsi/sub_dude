import streamlit as st

from sub_dude.webui.config import manipulate_sidebar
from sub_dude.webui.navigation import navigation_buttons
from sub_dude.webui.transcribe import display_transcription


def manipulate():
    """Translate"""
    manipulate_sidebar()

    st.title("Manipulate transcription")
    navigation_buttons(back="transcribe", back_label="Transcribe")

    display_transcription()

    if st.session_state.transcription_format == "srt" and st.button("Translate"):
        if not st.session_state.target_language:
            st.error("Please enter a target language in options")
            return

    if st.session_state.transcription_format == "text" and st.button("Summarize"):
        ...
