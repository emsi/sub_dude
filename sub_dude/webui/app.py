import streamlit as st

from sub_dude.webui.chooser import chooser
from sub_dude.webui.manipulate_transcription import manipulate
from sub_dude.webui.project import project
from sub_dude.webui.transcribe import transcribe

STATES = {
    "project": project,
    "chooser": chooser,
    "transcribe": transcribe,
    "manipulate": manipulate,
}


def app():
    """Main Streamlit app"""
    st.set_page_config(page_title="Sub Dude", page_icon="🤖", layout="wide")

    if "STATE" not in st.session_state:
        st.session_state["STATE"] = list(STATES)[0]  # start on page 1

    # Display the current page
    STATES[st.session_state["STATE"]]()


if __name__ == "__main__":
    app()
