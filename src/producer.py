from collections import defaultdict
from typing import Dict, Any
import traceback
import time
import logging

from kafka.errors import KafkaConfigurationError
from prometheus_client import Gauge, Counter

from kafka import KafkaProducer

from data import serialize_booking as serialize, random_booking

logger = logging.getLogger(__name__)

def run_producer(kafka_config: Dict[str, Any], topic: str):
    producer = KafkaProducer(value_serializer=serialize, **kafka_config)
    metrics: Dict[str, float] = {}

    Gauge(
        'kafka_producer_batch_size_avg',
        'Average batch size of messages produced'
    ).set_function(lambda: metrics.get('batch-size-avg', 0))
    Gauge(
        'kafka_producer_batch_size_max',
        'Maximum batch size of messages produced'
    ).set_function(lambda: metrics.get('batch-size-max', 0))
    Gauge(
        'kafka_producer_compression_rate_avg',
        'Average compression rate of messages produced'
    ).set_function(lambda: metrics.get('compression-rate-avg', 0))
    Gauge(
        'kafka_producer_records_per_request_avg',
        'Average number of records per request sent to Kafka'
    ).set_function(lambda: metrics.get('records-per-request-avg', 0))
    Gauge(
        'kafka_producer_record_send_rate',
        'The average number of records sent per second. Global request metric'
    ).set_function(lambda: metrics.get('record-send-rate', 0))

    try:
        t = time.time()
        while True:
            booking = random_booking()
            producer.send(topic, value=booking)
            logger.info(f"New booking: {booking.checkin_date} to {booking.checkout_date} at {booking.hotel.name}")
            time.sleep(0.020)
            # Expose metrics every second
            if time.time() - t > 1:
                t = time.time()
                producer_metrics = producer.metrics().get("producer-metrics", {})
                for metric_name, metric_value in producer_metrics.items():
                    metrics[metric_name] = producer_metrics.get(metric_name)
    except KeyboardInterrupt:
        logger.info("Producer stopped by user.")
    except Exception as e:
        logger.error(f"Error producing message", exc_info=e)
    finally:
        producer.close()
        print("Producer closed.")
