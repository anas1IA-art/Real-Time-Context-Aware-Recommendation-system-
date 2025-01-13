import json
import logging
import time
# import uuid
from uuid import UUID
from kafka import KafkaProducer
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from data_collection.data_collection_api import DynamicDataCollectionAPI  # Import your class

# Define the DataStreamer class
class DataStreamer:
    def __init__(self, kafka_servers, topic_name, timeout=60):
        self.kafka_servers = kafka_servers
        self.topic_name = topic_name
        self.timeout = timeout
        self.producer = KafkaProducer(bootstrap_servers=kafka_servers, max_block_ms=5000)
        self.data_collector = DynamicDataCollectionAPI()  # Instance of your dynamic data collection class
        logging.basicConfig(level=logging.INFO)

    def convert_uuids_in_dict(self, data):
        """Convert UUIDs to strings before sending to Kafka."""
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data

    def fetch_and_format_data(self):
        """Fetch and format data from the API."""
        res = self.data_collector.fetch_data()  # Fetch data using your method
        formatted_data = self.data_collector.process_data(res)  # Process data using your method
        return formatted_data

    def stream_data(self):
        """Stream data to Kafka."""
        curr_time = time.time()

        while True:
            if time.time() > curr_time + self.timeout:  # Timeout after defined period
                break
            try:
                # Fetch and format data
                res = self.fetch_and_format_data()

                # Convert UUIDs to strings if needed
                res = self.convert_uuids_in_dict(res)

                # Send the data to Kafka
                self.producer.send(self.topic_name, json.dumps(res).encode('utf-8'))
                logging.info(f"Data sent to Kafka: {res}")

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue


# Define Airflow DAG
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

with DAG('user_automation',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:

    # Instantiate the DataStreamer class
    data_streamer = DataStreamer(kafka_servers=['broker:29092'], topic_name='users_created')

    # Create Airflow task to stream data
    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=data_streamer.stream_data
    )
