import json
from pathlib import Path

import openai
import streamlit as st

from sub_dude.text_parse import word_wrap
from sub_dude.webui.config import transcribe_sidebar
from sub_dude.webui.navigation import navigation_buttons


def transcription_path(ext) -> Path:
    """Return the path to the json folder"""
    return (
        Path(st.session_state.transcriptions_path) / st.session_state.chooser_file
    ).with_suffix(ext)


def transcribe_audio(response_format):
    """Transcribe audio"""
    with open(st.session_state.downloads_path / st.session_state.chooser_file, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            st.session_state["whisper_model"],
            audio_file,
            # this helps to recognize those words in the audio
            prompt=st.session_state.prompt,
            response_format=response_format,
        )

    with open(transcription_path(f".{response_format}"), "w") as f:
        if response_format == "json" or response_format == "verbose_json":
            f.write(json.dumps(transcription))
        else:
            f.write(transcription)

    return transcription


def transcribe():
    """Transcription page"""
    transcribe_sidebar()

    st.title("Transcribe")

    navigation_buttons(position="top", back="chooser", back_label="Choosing file")

    st.markdown(f"##### Audio file: `{st.session_state.chooser_file}`")

    transcription_formats = [
        # "json",
        "text",
        "srt",
        # "verbose_json",
        # "vtt",
    ]
    st.session_state["transcription_format"] = response_format = st.selectbox(
        "Transcription format",
        transcription_formats,
        index=transcription_formats.index(st.session_state.get("transcription_format", "srt")),
    )

    if not transcription_path(f".{response_format}").exists():
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcription = transcribe_audio(response_format=response_format)
                st.experimental_rerun()
    else:
        with open(transcription_path(f".{response_format}")) as f:
            transcription = f.read()
            if response_format == "json" or response_format == "verbose_json":
                transcription = json.dumps(json.loads(transcription), indent=4)
            st.session_state.transcription = transcription

            display_transcription()

    navigation_buttons(
        position="bottom",
        back="chooser",
        back_label="Choosing file",
        forward="manipulate"
        if transcription_path(f".{response_format}").exists()
        and st.session_state.transcription_format != "verbose_json"
        else None,
        forward_label="Use transcription",
    )


def display_transcription():
    """Display transcription in the overflow box"""
    if st.session_state.transcription_format == "text":
        transcription = word_wrap(st.session_state.transcription, 100)
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
