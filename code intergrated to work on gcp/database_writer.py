#
import sqlite3
import time, json
from kafka import KafkaConsumer

# Connectors
conn = sqlite3.connect('GP_electric_cons.db')
cursor = conn.cursor()

# standard table creation incase it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS GP_electric_cons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    city TEXT,
    sector TEXT,
    power_cons_in_kwh REAL,
    voltage INTEGER
)
''')
conn.commit()

# Kafka Receiver 
Receiver = KafkaConsumer(
    'processed_electric_data_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Storing streamed messages to database...")

# Store incoming messages into SQLite
for message in Receiver:
    data = message.value
    cursor.execute('''
        INSERT INTO GP_electric_cons (timestamp, city, sector, power_cons_in_kwh, voltage)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['timestamp'],
        data['city'],
        data['sector'],
        data['power_cons_in_kwh'],
        data['voltage']
    ))
    conn.commit()
    print(f"Stored in DB: {data}")