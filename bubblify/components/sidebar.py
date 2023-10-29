"""Sidebar component for the app."""

from bubblify import styles
from bubblify.state import State

import reflex as rx

def sidebar_item(text: str, icon: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        icon: The icon of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.
    """
    # Whether the item is active.
    active = (State.router.page.path == f"/{text.lower()}") | (
        (State.router.page.path == "/") & text == "Home"
    ) | (State.router.page.path == "/add-cluster") & (text == "Add Cluster")


    return rx.link(
        rx.hstack(
            rx.image(
                src=icon,
                padding="0.5em",
            ),
            bg=rx.cond(
                active,
                styles.accent_color,
                "transparent",
            ),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            border_radius="50%",
            box_shadow=styles.box_shadow,
            width="80px",
            height="80px",
            padding="0.9em",
            margin="0.5em",
        ),
        href=url,
    )


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
        ),
        display="flex",
        flex_direction="column",
        position="fixed",
        right="0",
        bottom="0",
        z_index="1",
    )
