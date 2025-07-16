from typing import Dict, Any
import os, argparse, logging
from prometheus_client import start_http_server

logging.basicConfig(level=logging.INFO)

def load_kafka_config() -> Dict[str, Any]:
    """
    Load Kafka configuration from environment variables.

    The configuration is loaded as follows:

    1. Collect all environment variables that start with 'KAFKA_'.
    2. Remove the 'KAFKA_' prefix and convert the remaining part to lowercase.
    3. Store the resulting key-value pairs in a dictionary.
    4. Return the dictionary containing the Kafka configuration.

    Returns:
        A dictionary containing the Kafka configuration.
    """
    kafka_config = {}
    for key, value in os.environ.items():
        if key.startswith('KAFKA_'):
            new_key = key[6:].lower()
            # If the value is a string that contains only digits, convert it to an integer
            if value.isdigit():
                value = int(value)
            kafka_config[new_key] = value

    return kafka_config

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the Kafka XML Producer/Consumer application.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Kafka XML Producer/Consumer.\n"
                                                 "All Kafka configuration is loaded from environment variables starting with 'KAFKA_', e.g. KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, etc.\n"
                                                 "Note that this application configures its own serializers and deserializers, so no need to configure those.")
    parser.add_argument("mode", choices=["producer", "consumer"], help="Mode of operation: producer or consumer")
    parser.add_argument("--topic", required=True, help="Kafka topic to produce/consume messages")
    parser.add_argument("--metrics-port", type=int, default=8000, help="Port number for metrics endpoint")
    return parser.parse_args()

logger = logging.getLogger(__name__)

def main():
    """
    Main function to run the Kafka XML Producer/Consumer application.

    This function:
    1. Parses command line arguments.
    2. Loads Kafka configuration from environment variables.
    3. Initializes the application based on the mode (producer or consumer).
    """
    args = parse_args()

    # Load Kafka configuration
    kafka_config = load_kafka_config()

    logger.info(f"Kafka configuration: {kafka_config}")

    start_http_server(args.metrics_port)

    if args.mode == "producer":
        logger.info("Starting producer...")
        from producer import run_producer
        run_producer(kafka_config, args.topic)
    elif args.mode == "consumer":
        logger.info("Starting consumer...")
        from consumer import run_consumer
        run_consumer(kafka_config, args.topic)

    logger.info("Finished.")

if __name__ == "__main__":
    main()
