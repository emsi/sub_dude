from typing import Optional

import streamlit as st


def file_choose(filename: Optional[str] = None) -> str:
    """Select a file"""

    # use glob to match the pattern '.mp4' and list the files
    files = {
        file.name: file.resolve().as_posix()
        for file in st.session_state.downloads_path.glob("audio_*.mp4")
    }

    filename = filename or st.session_state.get("chooser_file")

    # Create the multi-select box with the friendly names
    st.session_state.chooser_file = st.selectbox(
        "Choose a file to transcribe",
        files.keys(),
        disabled=len(files) == 0,
        index=list(files.keys()).index(filename) if filename else 0,
    )
    return st.session_state.chooser_file


def transcript_choose(filename: Optional[str] = None) -> str:
    """Select a transcript file"""

    # use glob to match the pattern '.mp4' and list the files
    files = {
        file.name: file.resolve().as_posix()
        for file in st.session_state.downloads_path.glob("*.srt")
    }

    filename = filename or st.session_state.get("transcription_file")

    # Create the multi-select box with the friendly names
    st.session_state.transcription_file = st.selectbox(
        "Choose a transcription file",
        files.keys(),
        disabled=len(files) == 0,
        index=list(files.keys()).index(filename) if filename else 0,
    )
    st.session_state.transcription_format = "srt"
    if st.session_state.transcription_file:
        with open(st.session_state.downloads_path / st.session_state.transcription_file) as f:
            st.session_state.transcription = f.read()
    return st.session_state.transcription_file
