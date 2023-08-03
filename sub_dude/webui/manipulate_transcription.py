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