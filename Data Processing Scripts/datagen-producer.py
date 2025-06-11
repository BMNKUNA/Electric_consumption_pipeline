# datagen-producer.py
#
import random, time, json
from kafka import KafkaProducer
# Standard kafka producer setup with network address and JSON serializer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# Defines the cities for my randomiser data generator
cities=["Johannesburg", "Tshwane", "Ekurhuleni", "Soweto", "Benoni", "Vereeniging"]
sectors=["Residential", "Commercial", "Industrial"]


# Defined constants for my data generator
MIN_POWER_CONS = 50  # Minimum power consumption in kWh
MAX_POWER_CONS = 2000  # Maximum power consumption in kWh
MIN_VOLTAGE = 220  # Minimum voltage in volts
MID_VOLTAGE = 230  # Medium voltage in volts
MAX_VOLTAGE = 240  # Maximum voltage in volts

# Function to generate the data from global declared variables
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
# Infinite Loops that makes the real time stream run continuosly
while True:
    data =gen_fx()
    producer.send('electric_data_topic', data)
    print(f"Sent: {data}")
    time.sleep(3)