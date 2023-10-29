"""Bubble component for the app."""

from bubblify import styles
from bubblify.state import State

import reflex as rx
import random

def bubble(cluster) -> rx.Component:
    """The bubble.

    Returns:
        The bubble component.
    """
    colors = ["#D27CBF", "#D2BF7C", "#7cb3d2", "#7cd2be", "#d27c7c", "#7cd2b3", "#d27cbf", "#7cbfd2"]

    return rx.circle(
        rx.text(cluster[State.size_index]),
        rx.text(cluster[State.name_index]),
        rx.text(cluster[State.positionx_index]),
        rx.text(cluster[State.positiony_index]),
        display="flex",
        flex_direction="column",
        width=cluster[State.diameter_index] + "px",
        height=cluster[State.diameter_index] + "px",
        position="absolute",
        top="calc(50% + " + cluster[State.positiony_index] + "px)",
        left="calc(50% + " + cluster[State.positionx_index] + "px)",
        background_color=cluster[State.color_index],
        transition="all 0.5s ease",
        on_mouse_enter=State.mouse_enter(cluster),
        on_mouse_leave=State.mouse_leave(cluster),
    )
