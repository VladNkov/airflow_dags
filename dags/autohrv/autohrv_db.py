from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('AUTOHRV_DB')
if not DATABASE_URL:
    raise ValueError("AUTOHRV_DB is not set in environment variables!")

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class CarsDataTable(Base):
    __tablename__ = 'cars_data_table'

    id = Column(Float, primary_key=True)
    created_stamp = Column(DateTime, default=datetime.utcnow)
    brand = Column(String)
    model = Column(String)
    year = Column(String)
    engine = Column(String)
    volume = Column(String)
    power = Column(String)
    odometer = Column(String)
    transmission = Column(String)
    color = Column(String)
    owner = Column(String)
    vin = Column(String)
    car_id = Column(String)
    drive_type = Column(String)
    price = Column(String)


Base.metadata.create_all(engine)

