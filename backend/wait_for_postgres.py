import os
import time
import psycopg2
from psycopg2 import OperationalError


def create_conn():
    conn = None
    while not conn:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        except OperationalError:
            print("PostgreSQL is not ready yet. Waiting 5 seconds...")
            time.sleep(5)
    print("PostgreSQL is ready.")
    conn.close()


if __name__ == "__main__":
    create_conn()
