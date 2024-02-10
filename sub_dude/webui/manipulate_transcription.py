import streamlit as st

from sub_dude.srt_parse import srt_dump
from sub_dude.translate import translate_srt
from sub_dude.webui.config import manipulate_sidebar
from sub_dude.webui.navigation import navigation_buttons
from sub_dude.webui.render import render
from sub_dude.transcribe import transcription_path


def manipulate():
    """Translate"""
    manipulate_sidebar()

    st.title("Manipulate transcription")
    navigation_buttons(back="transcribe", back_label="Transcribe")

    translation_path = transcription_path(
        st.session_state.transcription_format,
        translation_language=st.session_state.target_language,
    )

    source, translated = st.columns([0.5, 0.5])
    if st.session_state.transcription_format == "srt":
        source.text_area("Source", st.session_state.transcription, height=500)

        if source.button("Translate"):
            if not st.session_state.target_language:
                st.error("Please enter a target language in options")
                return

            translating_header = translated.markdown("Translating...")
            translating = translated.empty()

            status = st.empty()
            status.progress(0)
            full_response = ""

            def streaming_callback(response):
                nonlocal full_response
                full_response += response
                translating.markdown(
                    # f"{st.session_state.target_language} translation",
                    full_response,
                    # height=680
                )
                if response.endswith("\n"):
                    full_response = ""

            def chunk_callback(progress):
                status.progress(progress)

            str_list = translate_srt(
                st.session_state.transcription,
                target_language=st.session_state.target_language,
                extra_prompt_instruction=st.session_state.extra_prompt_instruction,
                model=st.session_state.gpt_model,
                temperature=st.session_state.manipulate_temperature,
                streaming_callback=streaming_callback,
                chunk_callback=chunk_callback,
                srt_filename=translation_path,
            )
            srt_dump(srt_list=str_list, srt_filename=translation_path)
            translating.empty()
            translating_header.empty()
            status.empty()

        if translation_path.exists():
            with open(translation_path) as f:
                translation = f.read()
                translated.text_area(
                    f"{st.session_state.target_language} translation", translation, height=500
                )
            if translated.button("Render"):
                render(translated)


    if st.session_state.transcription_format == "text" and st.button("Summarize"):
        ...
