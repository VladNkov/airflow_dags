import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_page_url(base_url, pages):
    list_car_url = []
    for count in range(1, pages + 1):
        print(f"Scrapping page {count} from {pages}")
        url = f"{base_url}&page={count}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="col c6 tablet-c12 mob-c24")

        for i in data:
            car_url = urljoin(base_url, i.find("a").get("href"))
            list_car_url.append(car_url)
    return list_car_url


def parse_car_data(car_url):
    print(f"Scraping data from {car_url}")
    response = requests.get(car_url)
    soup = BeautifulSoup(response.text, "lxml")
    data_container = soup.find("main", id="pageContainer")
    if not data_container:
        return None

    all_li = data_container.find_all("li")
    car_data = {}

    for li in all_li:
        description = li.find("span", class_="description")
        value = li.find("span", class_="value").text.strip() if li.find("span", class_="value") else None

        if description and "Marka vozila" in description.text:
            car_data['brand'] = value
        elif description and "Model" in description.text:
            car_data['model'] = value
        elif description and "Godina proizvodnje" in description.text:
            car_data['year'] = value.strip('.')
        elif description and "Vrsta motora" in description.text:
            car_data['engine'] = value
        elif description and "Motor" in description.text:
            car_data['volume'] = value
        elif description and "Snaga motora" in description.text:
            car_data['power'] = value
        elif description and "Kilometraža" in description.text:
            car_data['odometer'] = value
        elif description and "Vrsta mjenjača" in description.text:
            car_data['transmission'] = value
        elif description and "Boja" in description.text:
            car_data['color'] = value
        elif description and "Vlasnik" in description.text:
            car_data['owner'] = value
        elif description and "Broj šasije" in description.text:
            car_data['vin'] = value
        elif description and "Šifra vozila" in description.text:
            car_data['car_id'] = value
        elif description and "Vrsta pogona" in description.text:
            car_data['drive_type'] = value

    price_tag = data_container.find('span', class_="full-price")
    car_data['price'] = price_tag.text.strip() if price_tag else None

    img_url_tag = data_container.find('a', href=True, class_='colorbox')
    img_url = None
    if img_url_tag:
        img_url = img_url_tag['href']
        if not img_url.startswith("http"):
            img_url = urljoin(car_url, img_url)
    car_data['image_url'] = img_url

    return car_data


def scrape_cars(base_url, pages):
    car_urls = get_page_url(base_url, pages)
    all_cars = []
    for car_url in car_urls:
        car_details = parse_car_data(car_url)
        if car_details:
            all_cars.append(car_details)

    return all_cars



