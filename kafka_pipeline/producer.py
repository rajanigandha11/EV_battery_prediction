import json
import time
import pandas as pd
from kafka import KafkaProducer

TOPIC_NAME = "ev-battery-telemetry"
KAFKA_SERVER = "localhost:9092"

def publish_telemetry(csv_path):
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    df = pd.read_csv(csv_path)
    print(f"Streaming {len(df)} records to topic '{TOPIC_NAME}'...")

    for idx, row in df.iterrows():
        payload = row.to_dict()
        producer.send(TOPIC_NAME, value=payload)
        if idx % 500 == 0:
            print(f"Produced record {idx} for Vehicle: {payload.get('Vehicle_ID')}")
        time.sleep(0.005)

    producer.flush()
    producer.close()
    print("Kafka streaming complete.")

if __name__ == "__main__":
    publish_telemetry("data/ev_battery_degradation.csv")