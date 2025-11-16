import os
from datetime import datetime
import json
import requests
import shutil
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from autohrv_db import CarsDataTable

load_dotenv()
Base = declarative_base()
DATABASE_URL = os.getenv('DATABASE_URL')


def create_session():
    c_engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=c_engine)
    return Session()


def make_dir(data_dir):
    img_dir = os.path.join(data_dir, 'images')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    jsons_dir = os.path.join(data_dir, 'jsons')
    if not os.path.exists(jsons_dir):
        os.makedirs(jsons_dir)
    return img_dir, jsons_dir


def save_json_file(cars_data, jsons_dir):
    os.makedirs(jsons_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f'cars_data_{timestamp}.json'
    file_path = os.path.join(jsons_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(cars_data, json_file, ensure_ascii=False, indent=4)
    print("Data has been written to {file_name}")


def save_image(car_vin, car_img_url, img_path):
    if os.path.exists(img_path):
        print(f"Image already exists {img_path}, skipping download.")
        return

    try:
        r = requests.get(car_img_url, stream=True)
        if r.status_code == 200:
            with open(img_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            print(f"Saved image for VIN {car_vin}")
        else:
            print(f"Failed to retrieve image from {car_img_url}")
    except Exception as e:
        print(f"Error saving image for VIN {car_vin}: {e}")


def save_images_cars(cars_data, img_dir):
    for car in cars_data:
        car_vin = car.get('vin')
        image_url = car.get('image_url')

        if car_vin and image_url:
            save_image(car_vin, image_url, img_dir)
        else:
            print(f"Skipping image download for car: {car.get('model')} (VIN: {car.get('vin')})")

    print("Image saving completed.")


def save_car_data_db(session, car_data):
    car_data_table = CarsDataTable(
        brand=car_data.get('brand'),
        model=car_data.get('model'),
        year=car_data.get('year'),
        engine=car_data.get('engine'),
        volume=car_data.get('volume'),
        power=car_data.get('power'),
        odometer=car_data.get('odometer'),
        transmission=car_data.get('transmission'),
        color=car_data.get('color'),
        owner=car_data.get('owner'),
        vin=car_data.get('vin'),
        car_id=car_data.get('car_id'),
        drive_type=car_data.get('drive_type'),
        price=car_data.get('price'))
    session.add(car_data_table)
    session.commit()



