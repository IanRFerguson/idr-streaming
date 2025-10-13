import json
import os
from time import sleep

from faker import Faker
from kafka import KafkaProducer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from utilities.logger import logger
from data.model import PIIModel

#####

producer = KafkaProducer(
    bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),  # Serialize data to JSON
)


def send_pii(session: Session):
    while True:
        fake = Faker()
        pii_data = {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
        }
        new_pii = PIIModel(**pii_data)
        session.add(new_pii)
        session.commit()

        producer.send("pii_topic", new_pii.id)
        logger.info(f"Sent PII Data: {pii_data['name']}")
        sleep(2)  # Send data every 2 seconds


#####

if __name__ == "__main__":
    engine = create_engine(os.environ["DATABASE_URL"], echo=True)
    with Session(bind=engine) as session:
        send_pii(session=session)
