"""The add cluster page."""

from bubblify.templates import template

import reflex as rx


@template(route="/add-cluster", title="Add Cluster", image="/add_cluster.svg")
def add_cluster() -> rx.Component:
    """The add cluster page.

    Returns:
        The UI for the add cluster page.
    """
    return rx.vstack(
        rx.heading("Add Cluster", font_size="3em"),
        rx.text("Welcome to Reflex!"),
        rx.text(
            "You can edit this page in ",
            rx.code("{your_app}/pages/add_cluster.py"),
        ),
    )
