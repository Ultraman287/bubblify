"""Base state for the app."""

import reflex as rx
from collections import Counter

import random

from bubblify import styles

class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """
    dummy_data = [
        {
            "sender": "GitGuardian <security@getgitguardian.com>",
            "snippet": "GitGuardian has detected the following Google OAuth2 Keys exposed within your GitHub account. Details - Secret type: Google OAuth2 Keys - Repository: Joshtray/bubblify - Pushed date: October 29th 2023,",
            "subject": "[Joshtray/bubblify] Google OAuth2 Keys exposed on GitHub",
            "date_received": "2023-10-28",
            "unread": False,
            "category_name": "INBOX"
        },
        {
            "sender": "John Doe <john.doe@example.com>",
            "snippet": "Hello, just checking in on our project progress. How's it going?",
            "subject": "Project Progress",
            "date_received": "2023-10-27",
            "unread": True,
            "category_name": "INBOX"
        },
        {
            "sender": "Alice Smith <alice.smith@example.com>",
            "snippet": "Meeting reminder for next week. Don't forget to prepare the presentation.",
            "subject": "Meeting Reminder",
            "date_received": "2023-10-26",
            "unread": False,
            "category_name": "INBOX"
        },
        {
            "sender": "Support Team <support@example.com>",
            "snippet": "Your support ticket #12345 has been resolved. If you have any more questions, feel free to ask.",
            "subject": "Support Ticket Resolution",
            "date_received": "2023-10-25",
            "unread": False,
            "category_name": "INBOX"
        },
        {
            "sender": "Jane Williams <jane.williams@example.com>",
            "snippet": "Weekly report attached. Please review and provide feedback.",
            "subject": "Weekly Report",
            "date_received": "2023-10-24",
            "unread": True,
            "category_name": "INBOX"
        },
        {
            "sender": "Free Offers <offers@example.com>",
            "snippet": "Congratulations! You've won a free cruise vacation. Click here to claim your prize!",
            "subject": "Free Cruise Offer",
            "date_received": "2023-10-27",
            "unread": False,
            "category_name": "Spam"
        },
        {
            "sender": "Growth Hacks <hacks@example.com>",
            "snippet": "Get rich quick with our amazing investment opportunity. Don't miss out!",
            "subject": "Investment Opportunity",
            "date_received": "2023-10-26",
            "unread": False,
            "category_name": "Spam"
        },
        {
            "sender": "Unsolicited Newsletter <newsletter@example.com>",
            "snippet": "You're receiving this email because you subscribed to our newsletter. To unsubscribe, click here.",
            "subject": "Weekly Newsletter",
            "date_received": "2023-10-25",
            "unread": False,
            "category_name": "Spam"
        },
        {
            "sender": "Amazon Deals <deals@amazon.com>",
            "snippet": "Check out our latest deals and discounts on electronics, clothing, and more!",
            "subject": "Amazon Promotions",
            "date_received": "2023-10-28",
            "unread": False,
            "category_name": "Promotions"
        },
        {
            "sender": "Tech Store <info@techstore.com>",
            "snippet": "Exclusive offer for tech enthusiasts: 20% off on all gadgets this week only!",
            "subject": "Tech Store Promotion",
            "date_received": "2023-10-27",
            "unread": False,
            "category_name": "Promotions"
        },
        {
            "sender": "Fashion Outlet <sales@fashionoutlet.com>",
            "snippet": "New arrivals and special discounts on fashion items. Shop now!",
            "subject": "Fashion Outlet Sale",
            "date_received": "2023-10-26",
            "unread": False,
            "category_name": "Promotions"
        },
        {
            "sender": "Travel Discounts <info@traveldiscounts.com>",
            "snippet": "Plan your next vacation with our exclusive travel deals and discounts!",
            "subject": "Travel Discounts",
            "date_received": "2023-10-25",
            "unread": False,
            "category_name": "Promotions"
        },
        {
            "sender": "Food Delivery <offers@fooddelivery.com>",
            "snippet": "Get 10% off on your next food delivery order. Use code: DELICIOUS10",
            "subject": "Food Delivery Discount",
            "date_received": "2023-10-24",
            "unread": False,
            "category_name": "Promotions"
        }
    ]

    clusters: list[tuple[str, int, list, float, float, float]] = []
    index_index: int = 0
    name_index: int = 1
    size_index: int = 2
    messages_index: int = 3
    diameter_index: int = 4
    positionx_index: int = 5
    positiony_index: int = 6
    color_index: int = 7
    z_index_index: int = 8

    colors: list[str] = ["#d27cbf", "#d2bf7c", "#7cb3d2", "#7cd2be", "#d27c7c", "#7cd2b3", "#d27cbf", "#7cbfd2"]

    prev_index: int = 0
    prev_diameter: float = 0
    prev_pos_x: float = 0
    prev_pos_y: float = 0
    in_focus: bool = False

    def get_clusters(self):
        """Get the clusters from the database.

        Returns:
            The clusters.
        """

        clusters = {}
        for message in self.dummy_data:
            if message["category_name"] not in clusters:
                clusters[message["category_name"]] = []
            clusters[message["category_name"]].append(message)

        diameters = self.get_diameters(clusters)
        positions = self.get_positions(clusters, diameters)
        colors = self.get_colors(clusters)
        self.clusters = [(i, name, len(clusters[name]), clusters[name], diameters[i], positions[i][0], positions[i][1], colors[i], 1) for i, name in enumerate(clusters)]
    
    def get_diameters(self, clusters):
        """Get the diameters of the clusters.

        Returns:
            The diameters.
        """
        n = len(clusters)
        min_size = styles.min_bubble_size
        max_size = 1200 / n
        mean = sum([len(clusters[cluster]) for cluster in clusters]) / len(clusters)
        deviations = [(len(clusters[cluster]) - mean)/mean for cluster in clusters]
        diff = (max_size - min_size)/2
        avg_diam = (max_size + min_size)/2
        return [((dev * diff) + avg_diam) for dev in deviations]
    
    def get_positions(self, clusters, diameters):
        """Get the positions of the clusters.

        Returns:
            The positions.
        """
        positions = []
        n = len(clusters)
        x_ranges = [(-600 + i*(1200/n), -600 + (i+1)*(1200/n)) for i in range(n)]

        for i in range(n):
            diameter = diameters[i]

            x_range_ind = random.choice(range(len(x_ranges)))

            x = random.uniform(x_ranges[x_range_ind][0], x_ranges[x_range_ind][1] - diameter)

            x_ranges.pop(x_range_ind)

            y = random.uniform(-(800 - diameter)/2, (800 - diameter)/2)
            
            positions.append((x, y - (diameter/2)))
        return positions
    
    def get_colors(self, clusters):
        """Get the colors of the clusters.

        Returns:
            The colors.
        """
        return random.sample(self.colors, k=len(clusters))
    
    def mouse_enter(self, cluster):
        """Mouse enter the bubble.

        Returns:
            The new bubble size.
        """
        new_cluster = list(cluster)
        new_cluster[self.diameter_index] = cluster[self.diameter_index] * 1.1

        self.clusters[cluster[self.index_index]] = tuple(new_cluster)
    
    def mouse_leave(self, cluster):
        """Mouse leave the bubble.

        Returns:
            The new bubble size.
        """
        new_cluster = list(cluster)
        new_cluster[self.diameter_index] = cluster[self.diameter_index] / 1.1

        self.clusters[cluster[self.index_index]] = tuple(new_cluster)
    
    def bubble_click(self, cluster):
        """Click the bubble.

        Returns:
            The new bubble size.
        """
        self.in_focus = True
        self.prev_index = cluster[self.index_index]
        self.prev_diameter = cluster[self.diameter_index]
        self.prev_pos_x = cluster[self.positionx_index]
        self.prev_pos_y = cluster[self.positiony_index]

        new_cluster = list(cluster)
        new_cluster[self.diameter_index] = cluster[self.diameter_index] * 2 
        new_cluster[self.positionx_index] = -(new_cluster[self.diameter_index] / 2)
        new_cluster[self.positiony_index] = -(new_cluster[self.diameter_index] / 2)
        new_cluster[self.z_index_index] = 3

        self.clusters[cluster[self.index_index]] = tuple(new_cluster)

    def bubble_close(self):
        """Close the bubble.

        Returns:
            The new bubble size.
        """
        if not self.in_focus:
            return
        
        self.in_focus = False
        cluster = self.clusters[self.prev_index]
        new_cluster = list(cluster)
        new_cluster[self.diameter_index] = self.prev_diameter
        new_cluster[self.positionx_index] = self.prev_pos_x
        new_cluster[self.positiony_index] = self.prev_pos_y
        new_cluster[self.z_index_index] = 1

        self.clusters[cluster[self.index_index]] = tuple(new_cluster)