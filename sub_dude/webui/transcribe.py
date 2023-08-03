import json
from pathlib import Path

import openai
import streamlit as st

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
            "whisper-1",
            audio_file,
            # this helps to recognize those words in the audio
            prompt="DALL·E, GPT-3, ChatGPT, GPT-4, OpenAI, Midjourney",
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

    st.session_state["transcription_format"] = response_format = st.selectbox(
        "Transcription format",
        ["json", "text", "srt", "verbose_json", "vtt"],
        index=2,
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

            st.markdown(
                f"""<div style="height: 18.75em; overflow-y: auto; margin-bottom: 1.25em;">
                
```{response_format}
{transcription}
```

</div>
""",
                unsafe_allow_html=True,
            )

    navigation_buttons(
        position="bottom",
        back="chooser",
        back_label="Choosing file",
        forward="manipulate"
        if transcription_path(f".{response_format}").exists()
        else None,
        forward_label="Use transcription",
    )
