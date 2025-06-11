import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import psycopg2
import time


DB_HOST = "34.72.143.59"
DB_PORT = "5432"
DB_NAME = "gpelectriccons"
DB_USER = "postgres"
DB_PASSWORD = "Sb@879454"


Receiver = None
MAX_RETRIES = 30
RETRY_DELAY_SECONDS = 5

print("Attempting to connect to Kafka broker...")
for i in range(MAX_RETRIES):
    try:
        Receiver = KafkaConsumer(
            'processed_electric_data_topic',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            client_id='google-cloud-writer'
        )
        print("Successfully connected to Kafka!")
        break
    except NoBrokersAvailable:
        print(f"Kafka broker not available, retrying in {RETRY_DELAY_SECONDS}s... (Attempt {i+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY_SECONDS)
    except Exception as e:
        print(f"An unexpected error occurred during Kafka connection: {e}")
        time.sleep(RETRY_DELAY_SECONDS)

if Receiver is None:
    print("Failed to connect to Kafka after multiple retries. Exiting.")
    exit(1)


print("Attempting to connect to Cloud SQL database...")

conn = None
cursor = None
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Successfully connected to Cloud SQL database!")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gp_electric_cons (
        id SERIAL PRIMARY KEY,
        timestamp REAL,
        city TEXT,
        sector TEXT,
        power_cons_in_kwh REAL,
        voltage INTEGER
    )
    ''')
    conn.commit()
    print("Table 'gp_electric_cons' checked/created in Cloud SQL.")

    print("Storing streamed messages to Cloud SQL database...")

    for message in Receiver:
        data = message.value
        cursor.execute('''
            INSERT INTO gp_electric_cons (timestamp, city, sector, power_cons_in_kwh, voltage)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data['timestamp'],
            data['city'],
            data['sector'],
            data['power_cons_in_kwh'],
            data['voltage']
        ))
        conn.commit()
        print(f"Stored in Cloud SQL: {data}")

except psycopg2.Error as e:
    print(f"Database connection or operation error: {e}")
    if conn:
        conn.rollback()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
