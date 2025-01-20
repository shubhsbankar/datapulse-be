from psycopg2 import sql
import os
from dotenv import load_dotenv
from psycopg2 import extras, pool
import dns.resolver
from fastapi import FastAPI, HTTPException
from contextlib import contextmanager

from sqlalchemy import create_engine

# Set DNS resolver to use Google's public DNS
resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8", "8.8.4.4"]

load_dotenv()

# Load PostgreSQL credentials from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
print("DB_PASSWORD",DB_PASSWORD)
print("DB_HOST",DB_HOST)
print("DB_NAME",DB_NAME)
print("DB_PORT",DB_PORT)
print("DB_USER",DB_USER)

# Create a connection pool instead of a single connection
try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    print("PostgreSQL connection pool created!")
except Exception as e:
    print("Failed to create connection pool:", str(e))
    connection_pool = None


@contextmanager
def get_db():
    """
    Context manager for database connections.
    Automatically returns connection to pool when done.
    """
    conn = connection_pool.getconn()
    try:
        cursor = conn.cursor()
        yield conn, cursor
    finally:
        cursor.close()
        connection_pool.putconn(conn)


# get sqlalchemy connection
def get_sqlalchemy_conn():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine.connect()