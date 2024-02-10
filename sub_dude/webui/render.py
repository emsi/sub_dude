import subprocess
from pathlib import Path

import streamlit as st

from sub_dude.transcribe import transcription_path


def audio_video_paths() -> tuple[Path, Path, Path]:
    """Return the path to the json folder"""
    audio_file = Path(st.session_state.downloads_path) / st.session_state.chooser_file
    if not audio_file.name.startswith("audio_"):
        st.error("Wrong audio file!")

    video_file = audio_file.parent / ("video_" + audio_file.name[6:])
    audio_video_file_name = audio_file.parent / audio_file.name[6:]

    return audio_file, video_file, audio_video_file_name


def run_ffmpeg(video_file_path, audio_file_path, subtitle_path, audio_video_file_path, element):
    command = [
        "ffmpeg",
        "-i", video_file_path,
        "-i", audio_file_path,
        "-i", subtitle_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-c:s", "mov_text",
        "-map", "0",
        "-map", "1",
        "-map", "2",
        audio_video_file_path
    ]

    # Use Popen to initiate the ffmpeg process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )

    # Create an empty markdown widget to display the output
    output_area = st.empty()

    full_output = ""
    # Display each line of ffmpeg's output in real-time
    for line in process.stdout:
        full_output += line
        output_area.markdown(f"""```{full_output}```""")
        print(line)

    # Wait for the process to complete
    process.communicate()

    output_area.empty()


def render(element):
    """Render video with subs"""

    audio_file_path, video_file_path, audio_video_file_path = audio_video_paths()
    subtitle_path = transcription_path(
        st.session_state.transcription_format,
        translation_language=st.session_state.target_language,
    )
    if not video_file_path.exists():
        st.error("No video. Please download it first!")
        return

    if audio_video_file_path.exists():
        element.error("Rendered file already exists!")
        return

    with st.spinner("Merging audio and video..."):
        run_ffmpeg(video_file_path, audio_file_path, subtitle_path, audio_video_file_path, element)

    element.success("Done!")
