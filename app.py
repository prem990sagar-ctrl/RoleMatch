"""
RoleMatch AI: Resume-Based Career Role Recommender
Entry point utilizing the Model-View-Controller (MVC) architecture.
"""
import streamlit as st
from controllers.app_controller import AppController

# Page Configuration
st.set_page_config(
    page_title="RoleMatch AI - Career Role Recommender",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Application entry point initializing the Controller."""
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    main()
