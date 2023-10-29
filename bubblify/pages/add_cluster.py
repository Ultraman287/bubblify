"""The settings page."""

from bubblify.templates import template

import reflex as rx
from ..state import State




@template(route="/add-cluster", title="Add Cluster", image="/add_cluster.svg")
def add_cluster() -> rx.Component:
    """The add cluster page.

    Returns:
        The UI for the add cluster page.
    """
    return rx.ordered_list(

            rx.foreach(State.cluster_names, lambda item : 
                
                rx.list_item(
                    rx.vstack(
                    rx.text(item),
                    rx.button(rx.text("Delete"), on_click=lambda : State.delete_cluster(item)),
                    )
                )
            ),
            rx.list_item(
                rx.vstack(
                rx.input(on_blur=lambda val : State.set_new_cluster_name(val)),
                rx.button(rx.text("Add Cluster"), on_click=lambda : State.add_cluster(State.new_cluster_name))
                )
            ),
            width="400px",
            justify_content="center",
            align_items="center",

    )