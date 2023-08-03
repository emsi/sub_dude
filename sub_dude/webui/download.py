import subprocess
from enum import Enum
from pathlib import Path

import streamlit as st
from pytube import YouTube


class DownloadType(Enum):
    """Type of download"""
    AUDIO = "audio"
    VIDEO = "video"
    BOTH = "both"


def download(yt_url: str, download_type: DownloadType = DownloadType.AUDIO):
    """Download a video from YouTube and return the file name"""
    if not isinstance(download_type, DownloadType):
        raise ValueError("download_type must be an instance of DownloadType Enum")

    def progress_function(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        progress = int(bytes_downloaded / total_size * 100)
        bar.progress(progress)

    status = st.empty()
    status.markdown("Downloading...")

    yt = YouTube(yt_url)
    yt.register_on_progress_callback(progress_function)

    # Download video and audio streams separately
    video_stream = yt.streams.get_highest_resolution()
    # audio_stream = yt.streams.get_audio_only()
    # DOwnload the lower quality as it transcribes well but is smaller
    audio_stream = yt.streams.filter(only_audio=True).first()

    if download_type == DownloadType.AUDIO or download_type == DownloadType.BOTH:
        status.markdown("Downloading audio...")
        bar = status.progress(0)
        audio_file_path = audio_stream.download(
            output_path=st.session_state.downloads_path,
            filename_prefix="audio_",
            skip_existing=False,
        )
    if download_type == DownloadType.VIDEO or download_type == DownloadType.BOTH:
        status.markdown("Downloading video...")
        bar = status.progress(0)
        video_file_path = video_stream.download(
            output_path=st.session_state.downloads_path,
            filename_prefix="video_",
            skip_existing=False,
        )
    status.empty()

    # if download_type == DownloadType.BOTH:
    #     audio_vide_file_path = video_stream.get_file_path(output_path=st.session_state.downloads_path)
    #     command = (
    #         f"ffmpeg -i '{video_file_path}' -i '{audio_file_path}' -c:v copy -c:a aac '{audio_vide_file_path}'"
    #     )
    #     with st.spinner("Merging audio and video..."):
    #         subprocess.run(command, shell=True)
    #     return Path(audio_vide_file_path).name

    if download_type == DownloadType.AUDIO:
        return Path(audio_file_path).name
    elif download_type == DownloadType.VIDEO:
        return Path(video_file_path).name