import streamlit as st

from sub_dude.webui.config import sidebar
from sub_dude.webui.download import download
from sub_dude.webui.file_chooser import file_choose


def chooser():
    """Chooser"""
    sidebar()

    st.title("Choose a file")

    st.text_input(
        "Enter Youtube URL",
        st.session_state.get("yt_url", ""),
        key="yt_url",
    )
    downloaded_files = None
    if st.session_state.yt_url and st.button("Download"):
        downloaded_files = download(st.session_state.yt_url)

    file_choose(downloaded_files)
