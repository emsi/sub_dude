import streamlit as st

from sub_dude.webui.config import chooser_sidebar
from sub_dude.webui.download import download, DownloadType
from sub_dude.webui.file_chooser import file_choose
from sub_dude.webui.navigation import navigation_buttons


def chooser():
    """Chooser"""
    chooser_sidebar()

    st.title("Choose a file")

    st.text_input(
        "Enter Youtube URL",
        st.session_state.get("yt_url", ""),
        key="yt_url",
    )
    st.session_state.downloaded_file = st.session_state.get("downloaded_file", None)
    if st.session_state.yt_url:
        col1, col2, _ = st.columns([0.1, 0.15, 0.8])
        if col1.button("Download audio"):
            st.session_state.downloaded_file = download(st.session_state.yt_url)
        if col2.button("Download audio & video"):
            st.session_state.downloaded_file = download(st.session_state.yt_url, DownloadType.BOTH)

    if file_choose(st.session_state.downloaded_file):
        navigation_buttons(back="transcribe", back_label="Transcribe")
