import os
from pathlib import Path

import streamlit as st


def _downloads_path() -> Path:
    """Return the path to the downloads folder"""
    return Path(st.session_state.data_folder) / 'downloads'


def sidebar():
    """Configuration sidebar"""
    st.sidebar.title("🤖Sub Dude Config")

    if st.sidebar.text_input(
        "Data folder",
        st.session_state.get("data_folder", "./data"),
        key="data_folder",
    ):
        os.makedirs(_downloads_path(), exist_ok=True)

    st.session_state.downloads_path = _downloads_path().resolve()
