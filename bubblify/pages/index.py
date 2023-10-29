"""The home page of the app."""

from bubblify import styles
from bubblify.templates import template
from bubblify.state import State
from bubblify.components.bubble import bubble

import reflex as rx

@template(route="/", title="Home", image="/home.svg", on_load=State.get_clusters)
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    
    return rx.vstack(
        rx.foreach(State.clusters, bubble),
        width="100%",
        height="100%",
        position="relative",
    )