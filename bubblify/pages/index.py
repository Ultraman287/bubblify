"""The home page of the app."""

from bubblify import styles
from bubblify.templates import template
from bubblify.state import State

import reflex as rx

def get_clusters():
    """Get the clusters from the database.

    Returns:
        The clusters.
    """
    clusters = {"Work": [{"message": "Email 1"}, {"message": "Email 2"}], "School": [{"message": "Email 3"}, {"message": "Email 4"}]
    }
    State.set_clusters(clusters)

@template(route="/", title="Home", image="/home.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        rx.heading("Home", font_size="3em"),
        rx.text("Welcome to Reflex!"),
        rx.text(
            "You can edit this page in ",
            rx.code("{your_app}/pages/index.py"),
        ),
    )