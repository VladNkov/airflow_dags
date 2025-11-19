import os
from datetime import datetime
import json
import requests
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from autohrv.autohrv_db import CarsDataTable

load_dotenv()
DATABASE_URL = os.getenv('AUTOHRV_DB')


def create_session():
    if not DATABASE_URL:
        raise ValueError("AUTOHRV_DB is not set in environment variables!")
    engine = create_engine(DATABASE_URL, echo=True)
    return sessionmaker(bind=engine)()


def make_dir(data_dir):
    img_dir = os.path.join(data_dir, 'images')
    jsons_dir = os.path.join(data_dir, 'jsons')
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(jsons_dir, exist_ok=True)
    return img_dir, jsons_dir


def save_json_file(cars_data, jsons_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f'cars_data_{timestamp}.json'
    file_path = os.path.join(jsons_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(cars_data, json_file, ensure_ascii=False, indent=4)
    print("JSON saved {file_name}")


def save_image(vin, url, path):
    if os.path.exists(path):
        print(f"Image exists {path}, skipping download.")
        return

    try:
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            with open(path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            print(f"Saved image for VIN {vin}")
        else:
            print(f"Failed to retrieve image from {url}")
    except Exception as e:
        print(f"Error saving image for VIN {vin}: {e}")


def save_images_cars(cars_data, img_dir):
    for car in cars_data:
        vin = car.get('vin')
        url = car.get('image_url')

        if not vin or not url:
            print(f"Skipping image for car: {car.get('model')} (VIN: ('vin'))")
            continue

        img_path = os.path.join(img_dir, f"{vin}.jpg")
        save_image(vin, url, img_path)

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
    print(f"Saved car to DB: {car_data.get('vin')}")



