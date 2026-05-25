import requests
from bs4 import BeautifulSoup
import time

cities = [
    'warsaw', 'krakow', 'lodz', 'wroclaw', 'poznan', 'gdansk',
    'szczecin', 'bydgoszcz', 'lublin', 'katowice', 'gorzow-wielkopolski',
    'zielona-gora', 'opole', 'rzeszow', 'kielce'
]

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/90.0.4430.93 Safari/537.36')
}

def get_weather_data(city):
    url = f"https://www.timeanddate.com/weather/poland/{city}/hourly"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Błąd podczas pobierania danych dla {city}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'zebra'})
    if not table:
        print(f"Nie znaleziono tabeli dla {city}.")
        return None

    rows = table.find_all('tr')
    data_list = []
    for row in rows[1:]:  # pomijamy nagłówek
        th = row.find('th')
        if not th:
            continue
        # Pobieramy tylko pierwszy węzeł tekstowy z <th>
        hour_text = th.get_text(strip=True)
        # Jeśli tekst nie zawiera ":", lub pierwsza część nie jest cyfrą, pomijamy ten wiersz
        if ":" not in hour_text or not hour_text.split(":")[0].isdigit():
            continue
        # Jeśli godzina to "24:00" zamieniamy ją na "00:00"
        if hour_text == "24:00":
            hour_text = "00:00"
        elif int(hour_text.split(":")[0]) > 23:
            # Jeśli liczba jest większa niż 23 (np. 25:00, 26:00 itd.), to pomijamy wiersz
            continue

        tds = row.find_all('td')
        if len(tds) < 9:
            continue

        temperature = tds[1].get_text(strip=True).replace("\xa0", " ")
        feels_like = tds[3].get_text(strip=True).replace("\xa0", " ")
        conditions = tds[2].get_text(strip=True)
        wind_speed = tds[4].get_text(strip=True).replace("\xa0", " ")
        wind_direction_span = tds[5].find('span')
        wind_direction = wind_direction_span['title'].strip() if wind_direction_span and wind_direction_span.has_attr('title') else ""
        humidity = tds[6].get_text(strip=True).replace("\xa0", " ")
        precipitation = tds[8].get_text(strip=True).replace("\xa0", " ")

        data_list.append({
            'time': hour_text,
            'temperature': temperature,
            'feels_like': feels_like,
            'conditions': conditions,
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'humidity': humidity,
            'precipitation': precipitation
        })
    return data_list

if __name__ == '__main__':
    test_city = 'krakow'
    data = get_weather_data(test_city)
    if data:
        for entry in data:
            print(entry)
    else:
        print("Brak danych.")