import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

'''Берем ссылку из сайта, откуда нужно спарсить данные'''
URL = 'https://www.akchabar.kg/ru/exchange-rates/'

'''Эта функция вытаскивает данные с таблицы, c помощью пакета Beautifulsoup (анализа документов HTML и XML). rows ищет все данные, которые лежат под тэгом tr. Открываем пустой лист all_rates, куда appendим найденные текстовые данные, которые лежат под определенным индексом [n].'''
def get_rate():
    page = requests.get(url=URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    table1 = soup.find('table', attrs={'id' : 'rates_table'})

    all_rates = []
    for i in table1.find_all('tbody'):
        rows = i.find_all('tr')

        for row in rows:
            all_rates.append({
                "banks" : row.find('td').text,
                "usd_pokupka" : row.find_all('td')[1].text,
                "usd_prodaja" : row.find_all('td')[2].text,
                "eur_pokupka" : row.find_all('td')[3].text,
                "eur_prodaja" : row.find_all('td')[4].text,
                "rub_pokupka" : row.find_all('td')[5].text,
                "rub_prodaja" : row.find_all('td')[6].text,
                "kzt_pokupka" : row.find_all('td')[7].text,
                "kzt_prodaja" : row.find_all('td')[8].text,
    })

    t_date = datetime.now().strftime('%d_%m_%Y')

    field_names = ["banks",
            'usd_pokupka',
            "usd_prodaja",
            "eur_pokupka",
            "eur_prodaja",
            "rub_pokupka",
            "rub_prodaja",
            "kzt_pokupka",
            "kzt_prodaja"]
    with open(f'table_of_exchange_rates_for_{t_date}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(all_rates)
'''Записываем полученные данные (словарь 'DictWriter') в csv file, c последовательностью ключей с помощью параметра field_names. '''       

def main():
    get_rate()

if __name__ == "__main__":
    main()
