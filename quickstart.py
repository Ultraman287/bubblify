from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

import logging
import os
import random
import time
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg
from psycopg.errors import SerializationFailure, Error
from psycopg.rows import namedtuple_row

from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.

import psycopg2
from psycopg2.extras import execute_values

import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
load_dotenv()
conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='verify-full', sslrootcert='system')

# write a function to use the connection to list tables
def list_tables():
    with conn.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        print(cur.fetchall())

def create_categories(conn, labels):
    with conn.cursor() as cur:
        category_ids = []  # Store category IDs

        for label in labels:
            # Check if the category already exists in the database
            cur.execute("SELECT id FROM categories WHERE name = %s;", (label,))
            category_id = cur.fetchone()
            
            if category_id is None:
                # If the category doesn't exist, insert it into the categories table
                cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id;", (label,))
                category_id = cur.fetchone()[0]
            else:
                category_id = category_id[0]
            
            category_ids.append(category_id)  # Append the category ID to the list

        conn.commit()

    return category_ids



def insert_email_info(conn, data):
    with conn.cursor() as cur:
        insert_query = """
        INSERT INTO emails_info (snippet, unread, subject, sender, date_received) 
        VALUES %s 
        ON CONFLICT (id) DO NOTHING
        RETURNING id;
        """
        psycopg2.extras.execute_values(cur, insert_query, data)
        email_info_ids = cur.fetchall()
        conn.commit()
    return email_info_ids


def insert_categorized_email(conn, email_info_id, category_id):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO categorized_emails (email_id, category_id) VALUES (%s, %s);", (email_info_id, category_id))
        conn.commit()




def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    list_tables()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow.redirect_uri = "http://127.0.0.1:8080/"  # Use your predefined URI here
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        print('Messages:')
        
        email_info_data = []

        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            
            
            # Extract the date
            date = message['internalDate']
            date = datetime.datetime.fromtimestamp(int(date) / 1000).strftime('%Y-%m-%d %H:%M:%S')

            # Check if the email is unread
            is_unread = 'UNREAD' in message['labelIds']


            subject = None
            for header in message['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break

            # Extract the sender
            sender = None
            for header in message['payload']['headers']:
                if header['name'] == 'From':
                    sender = header['value']
                    break

            # Extract the snippet
            snpt = message['snippet'][:255]  # TODO: make this a config var

            # Extract all label tags
            label_tags = [label for label in message['labelIds'] if label != 'UNREAD']
            
            email_info_data.append((snpt, is_unread, subject, sender, date))

        # Insert data into the emails_info table using execute_values
        email_info_ids = insert_email_info(conn, email_info_data)

        # Create categories for labels
        category_ids = create_categories(conn, label_tags)


        for idx, email_info_id in enumerate(email_info_ids):
        # Insert data into the categorized_emails table
        # For simplicity, let's assume you associate each email with the first category
            if idx < len(category_ids):
                category_id = category_ids[idx]
            else:
                # If there are more emails than categories, use the last category (or any default behavior)
                category_id = category_ids[-1]

            # Insert data into the categorized_emails table
            insert_categorized_email(conn, email_info_id, category_id)


        

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')





if __name__ == '__main__':
    main()