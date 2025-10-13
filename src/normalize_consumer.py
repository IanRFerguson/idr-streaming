import json
import os

from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from utilities.logger import logger
from data.model import PIIModel

#####


consumer = KafkaConsumer(
    "pii_topic",
    bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="pii-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),  # Deserialize JSON data
)


def receive_pii(session: Session):
    for message in consumer:
        pii_id = message.value  # Already deserialized by value_deserializer
        logger.info(f"Received PII ID: {pii_id}")

        data = session.query(PIIModel).filter(PIIModel.id == pii_id).first()
        if data:
            logger.info(
                f"Retrieved PII Data: {data.name}, {data.address}, {data.email}, {data.phone_number}"
            )
        else:
            logger.warning(f"No PII Data found for ID: {pii_id}")


#####

if __name__ == "__main__":
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(bind=engine) as session:
        receive_pii(session=session)
