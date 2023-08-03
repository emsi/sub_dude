import glob
import os
from pathlib import Path
from typing import Optional

import streamlit as st


def file_choose(filename: Optional[str] = None) -> str:
    """Select a file"""

    # use glob to match the pattern '.mp4' and list the files
    files = {
        file.name: file.resolve().as_posix()
        for file in st.session_state.downloads_path.glob("*.mp4")
    }

    # Create the multi-select box with the friendly names
    st.session_state.chooser_file = st.selectbox(
        "Or choose a file",
        files.keys(),
        disabled=len(files) == 0,
        index=list(files.keys()).index(filename) if filename else 0,
    )
    return st.session_state.chooser_file
