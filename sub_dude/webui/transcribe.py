import json

import streamlit as st

from sub_dude.text_parse import word_wrap
from sub_dude.transcribe import transcribe_audio, transcription_path
from sub_dude.webui.config import transcribe_sidebar
from sub_dude.webui.navigation import navigation_buttons


def transcribe():
    """Transcription page"""
    transcribe_sidebar()

    st.title("Transcribe")

    navigation_buttons(position="top", back="chooser", back_label="Choosing audio file")

    st.markdown(f"##### Audio file: `{st.session_state.chooser_file}`")

    transcription_formats = [
        # "json",
        "text",
        "srt",
        # "verbose_json",
        # "vtt",
    ]
    st.session_state["transcription_format"] = transcription_format = st.selectbox(
        "Transcription format",
        transcription_formats,
        index=transcription_formats.index(st.session_state.get("transcription_format", "srt")),
    )

    if not transcription_path(transcription_format).exists():
        transcribe_audio()
    else:
        with open(transcription_path(transcription_format)) as f:
            transcription = f.read()
            if transcription_format == "json" or transcription_format == "verbose_json":
                transcription = json.dumps(json.loads(transcription), indent=4)
            st.session_state.transcription = transcription

            display_transcription()

    navigation_buttons(
        position="bottom",
        back="chooser",
        back_label="Choosing audio file",
        forward="manipulate"
        if transcription_path(transcription_format).exists()
           and st.session_state.transcription_format != "verbose_json"
        else None,
        forward_label="Use transcription",
    )


def display_transcription():
    """Display transcription in the overflow box"""
    if st.session_state.transcription_format == "text":
        transcription = word_wrap(st.session_state.transcription, 88)
    else:
        transcription = st.session_state.transcription

    st.markdown(
        f"""<div style="height: 23em; overflow-y: auto; margin-bottom: 1.25em;">

```{st.session_state.transcription_format}
{transcription}
```
</div>
""",
        unsafe_allow_html=True,
    )
