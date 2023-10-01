from pathlib import Path

import streamlit as st

from sub_dude.webui.config import project_sidebar, downloads_path


def project():
    """Project"""
    project_sidebar()

    st.title("Enter project name")

    project_name = st.text_input(
        "Enter Project Name",
        # st.session_state.get("project_name", ""),
    )
    if not project_name:
        subdirs = [
            (str(subdir), subdir.name)
            for subdir in Path(st.session_state.data_folder).iterdir()
            if subdir.is_dir()
        ]
        subdirs.insert(0, ("", "Select a subdirectory"))
        selected_subdir = st.selectbox(
            "Or select project",
            options=subdirs,
            format_func=lambda x: x[1],
        )

        if selected_subdir[0]:
            project_name = selected_subdir[1]

    if project_name:
        st.session_state.project_name = project_name
        st.session_state.downloads_path = downloads_path().resolve()
        if st.session_state.downloads_path.exists():
            # navigation_buttons(forward="chooser", forward_label="Open")
            if st.button("Open"):
                st.session_state["STATE"] = "chooser"
                st.experimental_rerun()
        else:
            # navigation_buttons(forward="chooser", forward_label="Create")
            if st.button("Create"):
                st.session_state["STATE"] = "chooser"
                st.session_state.downloads_path.mkdir(parents=True, exist_ok=True)
                st.experimental_rerun()
