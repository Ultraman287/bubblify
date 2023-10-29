"""Bubble component for the app."""

from bubblify import styles
from bubblify.state import State

import reflex as rx

def sidebar() -> rx.Component:
    """The sidebar.

    Returns:
        The sidebar component.
    """
    # Get all the decorated pages and add them to the sidebar.
    from reflex.page import get_decorated_pages

    return rx.box(
        rx.vstack(
            rx.vstack(
                *[
                    sidebar_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        icon=page.get("image", "/github.svg"),
                        url=page["route"],
                    )
                    for page in get_decorated_pages()
                ],
                width="100%",
                overflow_y="auto",
                align_items="flex-start",
                padding="1em",

            ),
            rx.spacer(),
        ),
        display="flex",
        flex_direction="column",
        position="fixed",
        right="0",
        bottom="0",
    )
