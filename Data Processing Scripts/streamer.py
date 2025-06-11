# real-time-receiver.py
from kafka import KafkaConsumer, KafkaProducer 
#import time
import json


# Kafka setup
Input = KafkaConsumer('electric_data_topic', bootstrap_servers='localhost:9092', 
                         auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
Output = KafkaProducer(bootstrap_servers='localhost:9092', 
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Data Processor active.")

# Electricity consumption constants
MIN_POWER_KWH, MAX_POWER_KWH = 0, 5000  # range for power consumption in kWh
MIN_VOLTAGE, MAX_VOLTAGE = 200, 250  # range for voltage

# script to process incoming data
for message in Input:
    data = message.value
    data_valid = (MIN_POWER_KWH < data["power_cons_in_kwh"] < MAX_POWER_KWH) and (MIN_VOLTAGE <= data["voltage"] <= MAX_VOLTAGE)
    if data_valid:
        print(f"Valid data received: {data}")
        Output.send('processed_electric_data_topic', data)
    else:
        print(f"Invalid data received: {data}")

    