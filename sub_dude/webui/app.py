import requests_cache
import streamlit as st

from sub_dude.webui.chooser import chooser
from sub_dude.webui.manipulate_transcription import manipulate
from sub_dude.webui.transcribe import transcribe

STATES = {
    'chooser': chooser,
    'transcribe': transcribe,
    'manipulate': manipulate,
}

requests_cache.install_cache("sub_dude.sqlite", expire_after=3600)


def app():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="Sub Dude",
        page_icon="🤖",
        layout="wide"
    )

    if 'STATE' not in st.session_state:
        st.session_state['STATE'] = 'chooser'  # start on page 1

    # Display the current page
    STATES[st.session_state['STATE']]()

    # it takes time so display spinner
    with st.spinner('Loading...'):
        requests_cache.install_cache("ai_news.sqlite", expire_after=3600)


if __name__ == "__main__":
    app()
