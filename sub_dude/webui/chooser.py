import streamlit as st
from youtube_transcript_api import TranscriptsDisabled

from sub_dude.webui.download import download, DownloadType, download_transcripts
from sub_dude.webui.file_chooser import file_choose, transcript_choose
from sub_dude.webui.navigation import navigation_buttons


def chooser():
    """Chooser"""

    st.title("Choose a source material")

    st.text_input(
        "Enter Youtube URL",
        st.session_state.get("yt_url", ""),
        key="yt_url",
    )
    st.session_state.downloaded_file = st.session_state.get("downloaded_file", None)
    if st.session_state.yt_url:
        col1, col2, col3, _ = st.columns([0.15, 0.2, 0.2, 0.6])
        if col1.button("Download audio"):
            st.session_state.downloaded_file = download(st.session_state.yt_url)
        if col2.button("Download audio & video"):
            st.session_state.downloaded_file = download(st.session_state.yt_url, DownloadType.BOTH)
        try:
            download_transcripts(st.session_state.yt_url)
        except TranscriptsDisabled:
            st.error("There is no manual transcript available for this video")

    if file_choose(st.session_state.downloaded_file):
        navigation_buttons(forward="transcribe", forward_label="Transcribe")

    if transcript_choose():
        navigation_buttons(
            position="bottom2",
            forward="manipulate",
            forward_label="Use transcription",
        )
