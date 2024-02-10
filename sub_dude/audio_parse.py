import subprocess
from pathlib import Path
from typing import List

import streamlit as st

max_clip_duration = 60 * 45


def detect_silence_splits_with_ffmpeg(
    audio_file_path: Path, min_silence_len_sec=3, silence_threshold="-30dB"
):
    """Detect silence in an audio file using ffmpeg.

    :param audio_file_path: The path to the audio file.
    :param min_silence_len_sec: The minimum length of silence to detect.
    :param silence_threshold: The silence threshold.
    :return: A list of tuples, each containing the start and end time of a silence.
    """
    command = [
        "ffmpeg",
        "-i",
        audio_file_path,
        "-af",
        f"silencedetect=noise={silence_threshold}:duration={min_silence_len_sec}",
        "-f",
        "null",
        "-",
    ]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )
    # Use communicate() to capture output
    stdout_output, stderr_output = process.communicate()

    # Check for errors
    if stderr_output:
        st.error("Ffmpeg ERROR:", stderr_output)
        return []

    return [0.0] + [
        float(line.split("silence_start: ")[1]) + min_silence_len_sec / 2
        for line in stdout_output.split("\n")
        if "silence_start" in line
    ]


def split_file_format(audio_file_path: Path):
    """Return the path used to construct the split file name."""
    return audio_file_path.parent / (".splits_" + audio_file_path.name)


def n_split_file(audio_file_path: Path, split_no: int):
    """Return the nth split file name."""
    return split_file_format(audio_file_path).with_suffix(
        f".{split_no:03d}" + audio_file_path.suffix
    )


def first_split_file(audio_file_path: Path):
    """Return the first split file name."""
    return n_split_file(audio_file_path, 0)


def split_audio_with_ffmpeg(audio_file_path: Path, segments: List):
    """Split an audio file using ffmpeg.

    :param audio_file_path: The path to the audio file.
    :param segments: A list of tuples, each containing the split points.
    :return: A list of paths to the split audio files.
    """
    command = [
        "ffmpeg",
        "-i",
        audio_file_path,
        "-f",
        "segment",
        "-segment_times",
        ",".join(str(s) for s in segments),
        "-c",
        "copy",
        split_file_format(audio_file_path).with_suffix(".%03d" + audio_file_path.suffix),
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )

    # Use communicate() to capture output
    stdout_output, stderr_output = process.communicate()

    # Check for errors
    if stderr_output:
        st.error("Ffmpeg ERROR:", stderr_output)
        return []


def check_segments_length(segments):
    """Check if the segments are of a valid length."""

    # segments are just truncation points, compute the length of each segment
    segment_lengths = [segments[i+1] - segments[i] for i in range(len(segments) - 1)]

    # check if all segments are no more than max_clip_duration
    if any(length > max_clip_duration for length in segment_lengths):
        return False

    return True
