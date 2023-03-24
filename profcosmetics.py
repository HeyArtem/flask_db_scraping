import requests
import os
from bs4 import BeautifulSoup
import json
import csv
import random
import time


"""
Собираю данные с интернет магазина косметики
Выбрал раздел Шампуни
"""

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "accept": "*/*",
    "cookie": "__ddg1_=GKVqPfSAcT8zrdRjf8EQ; GEODATA_REGION=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; GEODATA_CITY=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; PHPSESSID=qokaRD7oQN4gYq0sRJYj1JYLmWeMQW1i; PROF_X_GUEST_ID=91506401; PROF_X_LAST_ADV=11_Y; PROF_X_SALE_UID=551451924; PROF_X_BANNERS=1_3275_1_02032023%2C1_3804_1_02032023%2C1_3803_1_02032023%2C1_3801_1_02032023%2C1_3775_1_02032023%2C1_3630_1_02032023%2C1_3799_1_02032023%2C1_3786_1_02032023; flocktory-uuid=f31b0d2c-1a75-4377-aca4-21e90c1fa2de-6; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A28%2C%22EXPIRE%22%3A1677185940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_uid=1677177022161176317; _ym_d=1677177022; _gid=GA1.2.869134525.1677177022; tmr_lvid=ec7bbb540d71a5fc70ddee1a48d4823a; tmr_lvidTS=1677177022020; blueID=0690a88d-d1ae-4183-a91b-b112ba727346; _ym_isad=1; _gat=1; _ym_visorc=b; _gat_gtag_UA_23018795_4=1; supportOnlineTalkID=9cNUpWtOJohQ3Grs7RSePZN0yZLhJTaQ; PROF_X_LAST_VISIT=23.02.2023%2021%3A30%3A38; tmr_detect=1%7C1677177043372; _ga=GA1.2.694140532.1677177022; _ga_94CRPPMX77=GS1.1.1677177022.1.1.1677177071.0.0.0"
}

url = "https://www.proficosmetics.ru/catalog/dlya-volos/shampuni/"


def get_data():

    print("\n[INFO] Data collection started!")

    # Запрос к странице
    response = requests.get(url=url, headers=headers)

    # Проверяю и вслучае отсутствия создаю директорию "data"
    if not os.path.exists("data"):
        os.mkdir("data")

    # Сохраняю страницу, проверка отдает ли сайт
    with open("data/index.html", "w") as file:
        file.write(response.text)

    # Читаю сохраненную страницу
    with open(file="data/index.html") as file:
        src = file.read()

    # Создаю обьект BeautifulSoup
    soup = BeautifulSoup(src, "lxml")

    # Переменные для записи в json & csv
    all_data_json = []
    all_data_csv = []

    # Пагинация. Нахожу последнюю страницу
    last_page = int(soup.find("div", class_="pager").find_all("a")[-2].text)

    print(f"\n[INFO] Found {last_page} pages.")    

    # # Генерирую ссылки на каждую страницу
    # for page in range(1, last_page + 1):
    
    # test
    for page in range(1, 3): 

        url_page = f"https://www.proficosmetics.ru/catalog/dlya-volos/shampuni/p{page}/"
        
        # # print(url_page)
        # print(f"\n[INFO] Page {page} started.")

        # Запрос к странице
        response = requests.get(url=url_page, headers=headers)

        # Создаю объект BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # Нахожу блок с карточками
        all_cards = soup.find("div", class_="catalogprice").find_all("div", class_="tumb")   

        # Прохожу циклом по карточкам
        for card in all_cards:

            # Получаю наименование товара
            try:                
                card_name = card.find("span", itemprop="name").text.strip().replace("\n", "").replace("\t", "")
            except Exception as ex:
                print(ex)
                card_name = "No data"

            # Описание товара
            try:
                card_description = card.find("p", class_="product_text").text.strip().replace("\t", "").replace("\n", " ")
            except Exception as ex:
                print(ex)
                card_description = "No data"

            # Прайс
            try:                  
                card_dirty_price = card.find("meta", itemprop="price").get("content").strip().split()
                card_price = int("".join(card_dirty_price))
            except Exception as ex:
                print(ex)
                card_price = "No data"

            # Ссылка на карточку
            try:
                link_to_card = f'https://www.proficosmetics.ru{card.find("div", class_="photo").find("a").get("href")}'
            except Exception as ex:
                print(ex)
                link_to_card = "No data"

            # print(f"\n card_name: {card_name}\n card_description: {card_description}\n card_price: {card_price}\n link_to_card: {link_to_card}\n")

            # Собранные данные сохраняю в переменную для json
            all_data_json.append(
                {
                "card_name": card_name,
                "card_description": card_description,
                "card_price": card_price,
                "link_to_card": link_to_card
                }
            )

            # Собранные данные сохраняю в переменную для csv
            all_data_csv.append(
                [
                card_name,
                card_description,
                card_price,
                link_to_card
                ]
            )

        print(f"\n[INFO] Page {page} completed.")

        # Пауза между запросами к станицам
        time.sleep(random.randrange(2, 4))


    # Сохраняю json file
    with open("data/all_data.json", "w") as file:
        json.dump(all_data_json, file, indent=4, ensure_ascii=False)

    # Сохраняю csv file
    with open("data/all_data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
            "card_name",
            "card_description",
            "card_price",
            "link_to_card"
            )
        )
        writer.writerows(all_data_csv)

    print("\n[INFO] Data collection and recording completed!")
    
    return "Hello Python!"
    



def main():
    get_data()


if __name__ == "__main__":
    main()
