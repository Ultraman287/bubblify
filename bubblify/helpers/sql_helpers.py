import psycopg2
import json
from datetime import date
import psycopg
from psycopg.errors import SerializationFailure, Error
from psycopg.rows import namedtuple_row
import os
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.

import psycopg2
from psycopg2.extras import execute_values

load_dotenv()
conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='verify-full', sslrootcert='system')


# Custom JSON encoder to handle date objects
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def execute_sql_query(conn, sql_query):
    with conn.cursor() as cur:
        cur.execute(sql_query)
        return cur.fetchall()

def insert_email_info(conn, data):
    with conn.cursor() as cur:
        insert_query = """
        INSERT INTO emails_info (snippet, unread, sender, date_received) 
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

def create_categories(conn, labels):
    with conn.cursor() as cur:
        category_ids = []

        for label in labels:
            cur.execute("SELECT id FROM categories WHERE name = %s;", (label,))
            category_id = cur.fetchone()

            if category_id is None:
                cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id;", (label,))
                category_id = cur.fetchone()[0]
            else:
                category_id = category_id[0]

            category_ids.append(category_id)

        conn.commit()

    return category_ids

def get_json_from_database():

    # Assuming you have the 'conn' connection object already established
    with conn.cursor() as cur:
        cur.execute("""
        SELECT subject, snippet, sender, date_received, unread, name
        FROM emails_info ei
        JOIN categorized_emails ca ON ei.id = ca.email_id
        JOIN categories c ON ca.category_id = c.id;
        """)

        result = cur.fetchall()

        # Convert the query result to a list of dictionaries
        rows_as_dict = [dict(subject=row[0], snippet=row[1], sender=row[2], date_received=row[3], unread=row[4], category_name=row[5]) for row in result]

        # Convert the list of dictionaries to JSON format using the custom encoder
        json_result = json.dumps(rows_as_dict, indent=4, cls=DateEncoder)

        # Print or use the JSON data as needed
        print(json_result)
        return json_result
