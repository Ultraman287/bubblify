"""Welcome to Reflex!."""

from bubblify import styles

# Import all the pages.
from bubblify.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
