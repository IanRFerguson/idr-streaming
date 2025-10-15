import json
import os

from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from utilities.logger import logger
from data.model import PIIModel, NormalizedPIIModel
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError
from typing import Tuple

#####

# TODO - This feels brittle
COMMON_STRING_NOISE = ["MR.", "MRS.", "MS.", "DR.", "JR.", "SR.", "II", "III", "IV"]


consumer = KafkaConsumer(
    "pii_topic",
    bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="pii-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),  # Deserialize JSON data
)


def clean_name_fields(name: str) -> Tuple[str, str]:
    """
    TODO - Fill this in
    """

    name = name.upper()
    for noise in COMMON_STRING_NOISE:
        name = name.replace(noise, "").strip()

    parts = name.split()

    if len(parts) == 2:
        return parts[0].title(), parts[1].title()
    elif len(parts) > 2:
        return parts[0].title(), " ".join(parts[1:]).title()
    else:
        return name.title(), ""


def clean_phone_number(phone: str) -> Tuple[str, str]:
    """
    TODO - Fill this in
    """

    phone_number, extension = phone.split("x") if "x" in phone else (phone, "")
    phone_number = "".join(filter(str.isdigit, phone_number))

    return phone_number, extension


def clean_email_address(email: str) -> str:
    """
    TODO - Fill this in
    """

    address, host = email.split("@")

    return f"{address.upper()}@{host.lower()}"


def clean_and_write_normalized_data(session: Session, pii_data: PIIModel):
    # Normalize address using scourgify
    try:
        clean_address_data = normalize_address_record(pii_data.address)
    except UnParseableAddressError as e:
        logger.error(f"Error normalizing address: {e}")
        clean_address_data = {}

    # Normalize name fields
    clean_first_name, clean_last_name = clean_name_fields(pii_data.name)

    # TODO
    clean_phone, clean_extension = clean_phone_number(pii_data.phone_number)

    # TODO
    clean_email = clean_email_address(pii_data.email)

    # Create a new instance in the normalized table
    new_record = NormalizedPIIModel(
        first_name=clean_first_name,
        last_name=clean_last_name,
        address_line_1=clean_address_data.get("address_line_1"),
        address_line_2=clean_address_data.get("address_line_2"),
        city=clean_address_data.get("city"),
        state=clean_address_data.get("state"),
        zip_code=clean_address_data.get("postal_code"),
        zip_plus_4=clean_address_data.get("zip_plus_4"),
        phone_number=clean_phone,
        phone_extension=clean_extension,
        email=clean_email,
        created_at=pii_data.created_at,
        source_id=pii_data.id,
    )
    session.add(new_record)
    session.commit()

    logger.info(f"Normalized data written for Normalized PII ID: {new_record.id}")


def receive_pii(session: Session):
    for message in consumer:
        pii_id = message.value  # Already deserialized by value_deserializer
        logger.info(f"Received PII ID: {pii_id}")

        data = session.query(PIIModel).filter(PIIModel.id == pii_id).first()
        if data:
            clean_and_write_normalized_data(session=session, pii_data=data)
        else:
            logger.warning(f"No PII Data found for ID: {pii_id}")


#####

if __name__ == "__main__":
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(bind=engine) as session:
        receive_pii(session=session)
