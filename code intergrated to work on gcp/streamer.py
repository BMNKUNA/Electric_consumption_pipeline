# streamer.py
from kafka import KafkaConsumer, KafkaProducer
import json
import time # Import the time module
from kafka.errors import NoBrokersAvailable # Import this

# Kafka setup
Input = None
Output = None
MAX_RETRIES = 30
RETRY_DELAY_SECONDS = 5

print("Attempting to connect to Kafka broker for streamer...")
for i in range(MAX_RETRIES):
    try:
        Input = KafkaConsumer(
            'electric_data_topic',
            bootstrap_servers='kafka:9092', # Use Docker service name
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            client_id='streamer-consumer' # Optional: client_id
        )
        Output = KafkaProducer(
            bootstrap_servers='kafka:9092', # Use Docker service name
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            client_id='streamer-producer' # Optional: client_id
        )
        print("Successfully connected to Kafka for streamer!")
        break
    except NoBrokersAvailable:
        print(f"Kafka broker not available for streamer, retrying in {RETRY_DELAY_SECONDS}s... (Attempt {i+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY_SECONDS)
    except Exception as e:
        print(f"An unexpected error occurred during streamer Kafka connection: {e}")
        time.sleep(RETRY_DELAY_SECONDS)

if Input is None or Output is None:
    print("Failed to connect to Kafka for streamer after multiple retries. Exiting.")
    exit(1)


print("Data Processor active.")

# Electricity consumption constants
MIN_POWER_KWH, MAX_POWER_KWH = 0, 5000
MIN_VOLTAGE, MAX_VOLTAGE = 200, 250

# script to process incoming data
for message in Input:
    data = message.value
    data_valid = (MIN_POWER_KWH < data["power_cons_in_kwh"] < MAX_POWER_KWH) and (MIN_VOLTAGE <= data["voltage"] <= MAX_VOLTAGE)
    if data_valid:
        print(f"Valid data received: {data}")
        Output.send('processed_electric_data_topic', data)
    else:
        print(f"Invalid data received: {data}")

