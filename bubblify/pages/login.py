"""The settings page."""

from bubblify.templates import template

import reflex as rx
from ..state import State


def get_input_field(icon: str, placeholder: str, _type: str, binding):
    return rx.container(
        rx.hstack(
            rx.icon(
                tag=icon,
                color="black",
                font_size="11px"
            ),
            rx.input(
                on_blur = binding,
                placeholder=placeholder,
                font_size="11px",
                color="black",
                border="none",
                border_bottom="1px solid black",
                width="100%",
                padding="10px",
                type=_type,
            )
            ,
            border_bottom="0.1px solid grey",
            width="300px",
            height="45px"
        )
    )



@template(route="/login", title="Login", image="/settings.svg")
def login() -> rx.Component:
    
    login_container = rx.container(
        rx.cond(State.authenticated_user,
                rx.vstack(
                    rx.text("You are already logged in."),
                    rx.button("Logout", on_click=lambda : State.logout),
                    width="250px",
                    center_content=True,
                ),
                rx.vstack(
            rx.container(height="65px"),
            rx.container(
                rx.text(
                    "Sign In",
                    font_size="30px",
                    color="black",
                    font_weight="bold",
                    letter_spacing="2px",
                ),
                width="250px",
                center_content=True,
            ),
            get_input_field("email", "Email", "email", State.set_current_email),
            rx.container(height="10px"),
            get_input_field("lock", "Password", "password", State.set_current_password),
            rx.container(height="10px"),
            rx.container(
                rx.button(
                    "Sign In",
                    background_color="black",
                    color="white",
                    border="none",
                    width="100%",
                    height="45px",
                    font_size="11px",
                    font_weight="bold",
                    letter_spacing="2px",
                    on_click=State.login(State.current_email, State.current_password)
                ),
                width="300px",
                center_content=True,
            ),  
        )),
        width = "400px",
        height = "75vh",
        box_shadow = "0px 0px 10px 0px rgba(0,0,0,0.75)",
        center_content=True,
    )
    
    _main = rx.container(
        login_container,
        center_content=True,
        justify_content="center",
        max_width="auto",
        height="100vh",
    )
    
    
    return _main