"""Base state for the app."""

import os

import reflex as rx

from collections import Counter

import random

from bubblify import styles

from .utils.auth import Auth

from bubblify.helpers.sql_helpers import get_json_from_database, create_categories, insert_email_info, execute_sql_query, conn, insert_categorized_email, create_emails_info_table
from quickstart import main

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

    colors: list[str] = ["#d27cbf", "#d2bf7c", "#7cb3d2", "#7cd2be", "#d27c7c", "#7cd2b3", "#d27cbf", "#7cbfd2"]
    cluster_names : list[str] = ["Work", "School"]
    new_cluster_name : str = ""
    current_email: str = ""
    current_password: str = ""
    authenticated_user: bool = False
    have_emails: bool = False
    email_data: list[dict] = []
    

    def get_clusters(self):
        """Get the clusters from the database.

        Returns:
            The clusters.
        """

        # clusters = {"Work": [{"message": "Email 1", "unread": True}, {"message": "Email 2"}, {"message": "Email 3"}], "School": [{"message": "Email 3"}, {"message": "Email 4"}]
        # }
        clusters = {}
        for message in self.dummy_data:
            if message["category_name"] not in clusters:
                clusters[message["category_name"]] = []
            clusters[message["category_name"]].append(message)

        diameters = self.get_diameters(clusters)
        positions = self.get_positions(clusters, diameters)
        colors = self.get_colors(clusters)
        self.clusters = [(i, name, len(clusters[name]), clusters[name], diameters[i], positions[i][0], positions[i][1], colors[i]) for i, name in enumerate(clusters)]
        print(self.clusters)
    
    def get_diameters(self, clusters):
        """Get the diameters of the clusters.

        Returns:
            The diameters.
        """
        n = len(clusters)
        min_size = styles.min_bubble_size
        max_size = max(1200 / n, 600 - ((n - 1) * min_size))
        print(min_size, max_size)
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
        x_ranges = [(-600, 600)]

        for i in range(len(clusters)):
            diameter = diameters[i]

            prev_length = len(x_ranges)
            discard = []
            for j in range(prev_length):
                if (x_ranges[j][1] - x_ranges[j][0]) > diameter:
                    x_ranges.append((x_ranges[j][0], x_ranges[j][1] - diameter))
                else:
                    discard.append(x_ranges[j])

            for _ in range(prev_length):
                x_ranges.pop(0)

            print("A", x_ranges)
            x_range_ind = random.choices(range(len(x_ranges)), weights=[(x_ranges[j][1] - x_ranges[j][0]) for j in range(len(x_ranges))])[0]

            print("B", diameter, x_range_ind)

            x = random.uniform(x_ranges[x_range_ind][0], x_ranges[x_range_ind][1])

            x_ranges.append((x_ranges[x_range_ind][0], x - diameter))
            x_ranges.append((x + diameter, x_ranges[x_range_ind][1]))
    
            x_ranges.pop(x_range_ind)

            prev_length = len(x_ranges)
            for j in range(prev_length):
                x_ranges.append((x_ranges[j][0], x_ranges[j][1] + diameter))

            for _ in range(prev_length):
                x_ranges.pop(0)

            for x_range in discard:
                x_ranges.append(x_range)

            y = random.uniform(-(800 - diameter)/2, (800 - diameter)/2)
            
            print("C", x, x + diameter)
            print("D", x_ranges)
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
        self.clusters = cluster
    

    
    def add_cluster(self, cluster_name):
        """
        Args:
            cluster_name: The name of the cluster to add.
        """
        if cluster_name not in self.clusters:    
            self.clusters[cluster_name] = []
            self.cluster_names.append(cluster_name)
    
    def delete_cluster(self, cluster_name):
        """
        Args:
            cluster_name: The name of the cluster to delete.
        """
        for i in range(len(self.clusters)):
            if self.clusters[i][1] == cluster_name:
                self.clusters.pop(i)
                self.cluster_names.pop(i)
                break
        
    
    def set_new_cluster_name(self, new_cluster_name):
        """
        Args:
            new_cluster_name: The new cluster name.
        """
        self.new_cluster_name = new_cluster_name
    
    def login(self, email, password):
        """
        Args:
            email: The email.
            password: The password.
        """

        if Auth.get_user(email):
            if Auth.authenticate_user(email, password):
                self.authenticated_user = True
            else:
                rx.alert("Incorrect password")
        else:
            print('user does not exist')
            if email != "" and password != "":
                Auth.create_new_user(email, password)
                self.authenticated_user = True
                print('This happened')
                rx.redirect("/", True)
    
    def logout(self):
        self.authenticated_user = False

    def connect_google(self):
        if os.path.exists('token.json'):
            os.remove('token.json')
        create_emails_info_table()
        main()
        self.email_data = get_json_from_database()
        self.have_emails = True
