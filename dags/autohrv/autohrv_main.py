import os
from dotenv import load_dotenv
from autohrv.autohrv_scrapper import scrape_cars
from autohrv.autohrv_saver import save_json_file, make_dir, save_car_data_db, create_session, save_images_cars
load_dotenv()
# DATABASE_URL = os.getenv('AUTOHRV_DB')


def main():
    BASE_URL = 'https://rabljena.autohrvatska.hr/rezultati-pretrage.aspx?uid=axyybqDY116'
    NUM_PAGES = 30
    data_dir = 'data'

    os.makedirs(data_dir, exist_ok=True)

    session = create_session()
    cars = scrape_cars(BASE_URL, NUM_PAGES)
    img_dir, jsons_dir = make_dir(data_dir)

    saved_cars = []
    for car in cars:
        car_vin = car.get('vin')
        if car_vin:
            car['img_path'] = os.path.join(img_dir, f'{car_vin}.jpg')
        else:
            car['img_path'] = None

        save_car_data_db(session, car)
        # saved_cars.append(car)

    save_json_file(cars, jsons_dir)
    save_images_cars(cars, img_dir)
    print("AUTOHRV DONE")


if __name__ == "__main__":
    main()
