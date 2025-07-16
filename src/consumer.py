import logging
import time
from typing import Dict, Any

from kafka import KafkaConsumer, TopicPartition
from prometheus_client import Gauge

from data import deserialize_booking

logger = logging.getLogger(__name__)

def run_consumer(kafka_config: Dict[str, Any], topic: str):
    """
    Run a Kafka consumer that consumes bookings from the specified topic.

    Args:
        kafka_config: Configuration for the Kafka consumer.
        topic: The Kafka topic to consume from.
    """
    consumer = KafkaConsumer(
        topic,
        value_deserializer=deserialize_booking,
        **kafka_config
    )

    metrics: Dict[str, float] = {}

    Gauge(
        "kafka_consumer_records_lag_max",
        "Maximum lag in terms of number of records for any partition"
    ).set_function(lambda: metrics.get("records-lag-max", 0))

    Gauge(
        "kafka_consumer_records_consumed_rate",
        "Average number of records consumed per second"
    ).set_function(lambda: metrics.get("records-consumed-rate", 0))

    Gauge(
        "kafka_consumer_records_per_request_avg",
        "Average number of records per request consumed from Kafka"
    ).set_function(lambda: metrics.get("records-per-request-avg", 0))

    Gauge(
        "kafka_consumer_fetch_size_avg",
        "The average number of bytes fetched per request."
    ).set_function(lambda: metrics.get("fetch-size-avg", 0))

    try:
        t = time.time()
        while True:
            batches = consumer.poll(timeout_ms=1000)
            messages = []
            for tp, messages_batch in batches.items():
                messages.extend(messages_batch)
            for message in messages:
                booking = message.value

                # Log booking summary
                logger.info(
                    f"Consumed booking: {booking.confirmation_number} - "
                    f"{booking.checkin_date} to {booking.checkout_date} at {booking.hotel.name} - "
                    f"{len(booking.guests)} guests - {booking.payment.amount} {booking.payment.currency}"
                )

            # Update consumer metrics every second
            if time.time() - t > 1:
                t = time.time()
                consumer_metrics = consumer.metrics().get("consumer-fetch-manager-metrics", {})
                for metric_name, metric_value in consumer_metrics.items():
                    metrics[metric_name] = consumer_metrics.get(metric_name)

    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error("Error consuming message", exc_info=e)
    finally:
        consumer.close()
        logger.info("Consumer closed")
