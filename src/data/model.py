from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PIIModel(Base):
    __tablename__ = "pii_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())


class PIILinkage(Base):
    __tablename__ = "linkage"

    id = Column(Integer, ForeignKey("pii_data.id"), primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("pii_data.id"), index=True)


class NormalizedPIIModel(Base):
    __tablename__ = "normalized_pii_data"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address_line_1 = Column(String, nullable=True)
    address_line_2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    zip_plus_4 = Column(String, nullable=True)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    phone_extension = Column(String)
    created_at = Column(DateTime)
    normalized_at = Column(DateTime, default=func.now(), onupdate=func.now())
    source_id = Column(Integer, ForeignKey("pii_data.id"), index=True)
