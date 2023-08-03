import os
from pathlib import Path
import openai

import streamlit as st

from sub_dude.secrets import read_secret


def _downloads_path() -> Path:
    """Return the path to the downloads folder"""
    return Path(st.session_state.data_folder) / 'downloads'


def _transcriptions_path() -> Path:
    """Return the path to the transcriptions folder"""
    return Path(st.session_state.data_folder) / 'transcriptions'


def chooser_sidebar():
    """Configuration sidebar"""
    st.sidebar.title("🤖Sub Dude Config")

    if st.sidebar.text_input(
        "Data folder",
        st.session_state.get("data_folder", "./data"),
        key="data_folder",
    ):
        os.makedirs(_downloads_path(), exist_ok=True)
        os.makedirs(_transcriptions_path(), exist_ok=True)

    st.session_state.downloads_path = _downloads_path().resolve()
    st.session_state.transcriptions_path = _transcriptions_path().resolve()


def model_choose(*, model_prefix, default_model, session_name):
    """Select a model"""
    openai_models = openai.Model.list().data
    whisper_models = [model["id"] for model in openai_models if model["id"].startswith(model_prefix)]

    st.session_state[session_name] = st.sidebar.selectbox(
        "Model",
        whisper_models,
        index=whisper_models.index(st.session_state.get(session_name, default_model)),
    )


def transcribe_sidebar():
    """Transcribe configuration sidebar"""
    st.sidebar.title("🤖Options")

    openai.api_key = st.sidebar.text_input(
        "OpenAI API key",
        getattr(openai, "api_key") or read_secret("openai_api_key.txt"),
        type="password",
    )
    model_choose(model_prefix="whisper-", default_model="whisper-1", session_name="whisper_model")
    openai.organization = st.sidebar.text_input("OpenAI organization", openai.organization or "")


def manipulate_sidebar():
    """Transcribe configuration sidebar"""
    st.sidebar.title("🤖Options")

    openai.api_key = st.sidebar.text_input(
        "OpenAI API key",
        getattr(openai, "api_key") or read_secret("openai_api_key.txt"),
        type="password",
    )
    model_choose(model_prefix="gpt-", default_model="gpt-3.5-turbo", session_name="gpt_model")
    openai.organization = st.sidebar.text_input("OpenAI organization", openai.organization or "")
