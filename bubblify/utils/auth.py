import psycopg2
import json
from datetime import date
import psycopg
from psycopg.errors import SerializationFailure, Error
from psycopg.rows import namedtuple_row
import os
import hashlib
# from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.

import psycopg2
from psycopg2.extras import execute_values


conn = psycopg2.connect(os.environ['DATABASE_URL'])


class Auth:
    
    def get_user(email):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
            
            user = cur.fetchone()
            
            if user:
                return True
            else:
                return False
    
    def authenticate_user(email, password):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s AND password = %s;", (email, 
                                                                                    hashlib.sha256(password.encode()).hexdigest()
                                                                                    ))
            
            user = cur.fetchone()
            
            if user:
                return True
            else:
                return False
    
    def create_new_user(email, password):
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (email, password) VALUES (%s, %s);", (email, 
                                                                                 hashlib.sha256(password.encode()).hexdigest()
                                                                                 ))
            conn.commit()
            
            return True