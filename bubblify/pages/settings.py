"""The settings page."""

from bubblify.templates import template

import reflex as rx

from ..state import State

@template(route="/settings", title="Settings", image="/settings.svg")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    val: str = "Hello"
    
    _main = rx.vstack(
        rx.button("Connect to Gmail", on_click=State.connect_google),
        rx.cond(State.have_emails, rx.text("We've got your emails!"),  rx.text("You don't have emails, lonely fuck!")),
    )
    
    return _main
