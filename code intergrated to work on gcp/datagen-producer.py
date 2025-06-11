import json
import time
import random
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


producer = None
MAX_RETRIES = 30
RETRY_DELAY_SECONDS = 5

print("Attempting to connect to Kafka producer...")
for i in range(MAX_RETRIES):
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Successfully connected to Kafka producer!")
        break
    except NoBrokersAvailable:
        print(f"Kafka broker not available for producer, retrying in {RETRY_DELAY_SECONDS}s... (Attempt {i+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY_SECONDS)
    except Exception as e:
        print(f"An unexpected error occurred during Kafka producer connection: {e}")
        time.sleep(RETRY_DELAY_SECONDS)

if producer is None:
    print("Failed to connect to Kafka producer after multiple retries. Exiting.")
    exit(1)


cities=["Johannesburg", "Tshwane", "Ekurhuleni", "Soweto", "Benoni", "Vereeniging"]
sectors=["Residential", "Commercial", "Industrial"]


MIN_POWER_CONS = 50
MAX_POWER_CONS = 2000
MIN_VOLTAGE = 220
MID_VOLTAGE = 230
MAX_VOLTAGE = 240

def gen_fx():
    city = random.choice(cities)
    sector = random.choice(sectors)
    power_cons_in_kwh = round(random.uniform(MIN_POWER_CONS, MAX_POWER_CONS), 2)
    voltage = random.choice([MIN_VOLTAGE , MID_VOLTAGE, MAX_VOLTAGE])
    timestamp = time.time()
    return {
        "timestamp": timestamp,
        "city": city,
        "sector": sector,
        "power_cons_in_kwh": power_cons_in_kwh,
        "voltage": voltage
    }

while True:
    data =gen_fx()
    producer.send('electric_data_topic', data)
    print(f"Sent: {data}")
    time.sleep(3)
