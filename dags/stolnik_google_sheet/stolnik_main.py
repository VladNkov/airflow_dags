import sys
from stolnik_google_sheet.scrapper_stolnik import get_all_prices
from stolnik_google_sheet.write_to_gsheet import update_google_sheet


def main():
    print("Старт парсинга и загрузки цен в Google Sheets")

    try:
        all_prices = get_all_prices()
        print(f"Собрано {len(all_prices)} цен с сайта")
        print("Загружаем данные в Google Sheets...")
        update_google_sheet()
        print("Данные успешно загружены")

    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()