"""Base state for the app."""

import reflex as rx


class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """

    clusters = {}

    def set_clusters(self, clusters):
        """Set the clusters.

        Args:
            clusters: The clusters.
        """
        self.clusters = clusters
