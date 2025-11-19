import requests
from bs4 import BeautifulSoup


products = {'sheet_1mm_1000_2000': {'url': 'https://stroyryad.com.ua/cat/lyst-chornyi', 'id': 2821},
            'sheet_2mm_1000_2000': {'url': 'https://stroyryad.com.ua/cat/lyst-chornyi', 'id': 2823},
            'sheet_2mm_1250_2500': {'url': 'https://stroyryad.com.ua/cat/lyst-chornyi','id': 2829},
            'sheet_8mm_m2': {'url': 'https://stroyryad.com.ua/cat/lyst-chornyi', 'id': 7784},
            'sheet_10mm_m2': {'url': 'https://stroyryad.com.ua/cat/lyst-chornyi', 'id': 7791},
            'sheet_corrug_3mm_1000_4000': {'url': 'https://stroyryad.com.ua/cat/lyst-ryflenyi', 'id': 10515},
            'sheet_perf_2mm_1000_2000': {'url': 'https://stroyryad.com.ua/cat/lyst-perforovanyi', 'id': 7165},
            'sheet_expand_3mm_1000_2000': {'url': 'https://stroyryad.com.ua/cat/lyst-prosichno-vytiazhnyi', 'id': 6650},
            'pipe_20_20_2': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 2897},
            'pipe_30_30_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 3469},
            'pipe_40_20_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 13525},
            'pipe_40_40_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 16080},
            'pipe_50_30_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 3406},
            'pipe_50_50_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 3029},
            'pipe_100_50_3': {'url': 'https://stroyryad.com.ua/cat/truby-profilni', 'id': 3027},
            'corner_20_20_3': {'url': 'https://stroyryad.com.ua/cat/kutyk-katanyi', 'id': 2975},
            'corner_30_30_3': {'url': 'https://stroyryad.com.ua/cat/kutyk-katanyi', 'id': 7458},
            'corner_50_50_3': {'url': 'https://stroyryad.com.ua/cat/kutyk-katanyi', 'id': 6216},
            'armature_8mm': {'url': 'https://stroyryad.com.ua/cat/armatura', 'id': 2857},
            'stripe_20_4': {'url': 'https://stroyryad.com.ua/cat/smuha', 'id': 12764},
            'rod_m10': {'url': 'https://stroyryad.com.ua/cat/shpylky', 'id': 3418},
            'screw_m10': {'url': 'https://stroyryad.com.ua/cat/haiky', 'id': 3423},
            'navis_16': {'url': 'https://stroyryad.com.ua/cat/navisy', 'id': 3132}
            }


def get_prices_and_name(url, pid):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    a_tag = soup.find('a', href=f"/cat/{url.split('/')[-1]}/product/{pid}")
    tr = a_tag.find_parent('tr')
    tds = tr.find_all('td')
    price = (tds[2].get_text(strip=True))
    price = price.replace('грн.', '').replace('\xa0', '').strip()
    price = float(price.replace(',', '.'))
    name = a_tag.get_text(strip=True).replace('Купити', '')
    return {"name": name, "price": price}


def get_all_prices():
    all_prices = {}
    for key, info in products.items():
        try:
            result = get_prices_and_name(info['url'], info['id'])
            all_prices[key] = result
        except Exception as e:
            all_prices[key] = {'name': 'error', 'price': 0}
            print(f'Ошибка для {key}: {e}')
    return all_prices




