import json
from pathlib import Path

import openai
import pysrt
import streamlit as st
from moviepy.audio.io.AudioFileClip import AudioFileClip

from sub_dude.audio_parse import (
    detect_silence_splits_with_ffmpeg,
    split_audio_with_ffmpeg,
    first_split_file,
    n_split_file,
    max_clip_duration,
    check_segments_length,
)
from sub_dude.srt_parse import shift_subtitles


def transcription_path(ext, *, translation_language="") -> Path:
    """Return the path to the json folder"""
    if not ext.startswith("."):
        ext = f".{ext}"
    translation_language = translation_language and f"_{translation_language}"
    return (Path(st.session_state.downloads_path) / st.session_state.chooser_file).with_suffix(
        ext + translation_language
    )


def transcribe_audio():
    """Transcribe audio"""

    audio_file_path = st.session_state.downloads_path / st.session_state.chooser_file

    if not st.session_state.get("clip_duration"):
        st.session_state["clip_duration"] = AudioFileClip(audio_file_path.as_posix()).duration

    if (
        st.session_state["clip_duration"] > max_clip_duration
        and not first_split_file(audio_file_path).exists()
    ):
        st.error(
            f"Audio file is too long: {st.session_state['clip_duration']:.1f}s. Max duration is 45 minutes. Needs splitting."
        )
        if st.button("Split"):
            with st.spinner("Splitting..."):
                st.session_state["segments"] = detect_silence_splits_with_ffmpeg(audio_file_path)
                if check_segments_length(st.session_state["segments"]):
                    st.error("Some segments are too long.")
                split_audio_with_ffmpeg(audio_file_path, st.session_state["segments"])

    if (
        st.session_state["clip_duration"] <= max_clip_duration
        or first_split_file(audio_file_path).exists()
    ):
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                perform_transcription(audio_file_path)
                st.experimental_rerun()


def perform_transcription(
    audio_file_path: Path,
    force=False,
):
    """Perform transcription"""
    if first_split_file(audio_file_path).exists():
        status = st.empty()
        status.progress(0)
        if not st.session_state.get("segments"):
            st.session_state["segments"] = detect_silence_splits_with_ffmpeg(audio_file_path)
        transcription = ""
        for segment_no, offset in enumerate(st.session_state["segments"]):
            transcription += transcribe_file(audio_file_path, force, segment_no, offset)
            status.progress((segment_no + 1) / len(st.session_state["segments"]))

        status.empty()
    else:
        transcription = transcribe_file(audio_file_path, force)

    # write the transcription file
    with open(transcription_path(st.session_state["transcription_format"]), "w") as f:
        if (
            st.session_state.transcription_format == "json"
            or st.session_state.transcription_format == "verbose_json"
        ):
            f.write(json.dumps(transcription))
        else:
            f.write(transcription)


def transcribe_file(audio_file_path: Path, force=False, split_no: int | None = None, offset=0.0):
    """Transcribe an audio file."""
    transcription_format = st.session_state["transcription_format"]
    output_path = transcription_path(transcription_format)
    if split_no is not None:
        output_path = n_split_file(output_path, split_no)
        audio_file_path = n_split_file(audio_file_path, split_no)

    if output_path.exists() and not force:
        # read file and return
        with open(output_path) as f:
            return f.read()

    with open(audio_file_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            st.session_state["whisper_model"],
            audio_file,
            # this helps to recognize those words in the audio
            prompt=st.session_state.prompt,
            response_format=transcription_format,
            language=st.session_state.language,
        )
        subs = pysrt.from_string(transcription)

    if transcription_format == "srt" and split_no is not None and split_no > 0:
        subs = shift_subtitles(transcription, offset)

    transcription = '\n'.join(str(sub) for sub in subs) + "\n"

    with open(output_path, "w") as f:
        if transcription_format == "json" or transcription_format == "verbose_json":
            f.write(json.dumps(transcription))
        else:
            f.write(transcription)

    return transcription
