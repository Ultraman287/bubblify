from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        results = service.users().messages().list(userId='me', maxResults=20).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        print('Messages:')
        values = []
        id = 0

        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            snpt = message['snippet'][:255] # TODO: make this a config var
            values.append((id, snpt))
            id += 1

        with conn.cursor() as cur:
            execute_values(cur, "INSERT INTO emails (id, snippet) VALUES %s ON CONFLICT (id) DO NOTHING;", values)
            conn.commit()
            cur.execute("SELECT * FROM emails;")
            print(cur.fetchall())
        

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()