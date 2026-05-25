
# db.py
import mysql.connector
from db_config import DB_CONFIG
from datetime import datetime, timedelta
import re

print("DB_CONFIG:", DB_CONFIG)

CONDITIONS_TRANSLATIONS = {
    "Clear.": "Czyste niebo", "Partly cloudy.": "Częściowe zachmurzenie", "Cloudy.": "Pochmurno", 
    "Overcast.": "Zachmurzenie całkowite", "Light rain.": "Lekki deszcz", "Rain.": "Deszcz", 
    "Heavy rain.": "Ulewa", "Thunderstorm.": "Burza", "Snow.": "Śnieg", "Fog.": "Mgła", 
    "Mist.": "Zamglenie", "Haze.": "Mglisto", "Drizzle.": "Mżawka", "Showers.": "Przelotne opady", 
    "Sunny.": "Słonecznie", "Sleet.": "Deszcz ze śniegiem", "Scattered clouds.": "Rozproszone chmury", 
    "Few clouds.": "Niewielkie zachmurzenie", "Broken clouds.": "Zachmurzenie częściowe", 
    "Shower rain.": "Deszcz przelotny", "Heavy shower rain.": "Ulewny deszcz", "Light snow.": "Lekki śnieg", 
    "Heavy snow.": "Silny śnieg", "Freezing rain.": "Deszcz lodowy", "Thunderstorm with light rain.": "Burza z lekkim deszczem", 
    "Thunderstorm with heavy rain.": "Burza z ulewnym deszczem", "Thunderstorm with snow.": "Burza ze śniegiem", 
    "Thunderstorm with hail.": "Burza z gradem", "Hail.": "Grad", "Dust.": "Pył", "Sand.": "Piasek", 
    "Ash.": "Popiół", "Squall.": "Sztorm", "Tornado.": "Tornado", "Mostly cloudy.": "Głównie pochmurno", 
    "Mostly sunny.": "Głównie słonecznie", "Mostly clear.": "Głównie czyste niebo"
}



# Mapowanie pełnych kierunków z odpowiednim tłumaczeniem (w kontekście stopni)
WIND_DIRECTION_TRANSLATIONS = {
    "170": "170° S do N", "160": "160° S-SE do N-NW", "180": "180° S do N-NW", "190": "190° SSE do N-NW", "200": "200° SSW do N-NE", "210": "210° S-SE do N-NW", 
    "220": "220° S do N", "230": "230° SSW do N-NE", "240": "240° SW do N-NE", "250": "250° WSW do N-NE", "260": "260° W do N-NE", "270": "270° W do N", 
    "280": "280° W-NW do N-NE", "290": "290° NW do N-NE", "300": "300° NW do N", "310": "310° NW do N-NW", "320": "320° N-NW do N", "330": "330° N-NW do N-NE", 
    "340": "340° N do N-NE", "350": "350° N do N-NE", "150": "150° SSE do N-NW", "140": "140° SE do NW", "130": "130° SE do NW", "120": "120° SE do NW", 
    "110": "110° SE do NW"
}

CITY_TO_REGION = {
    "warsaw": "mazowieckie",
    "krakow": "małopolskie",
    "lodz": "łódzkie",
    "wroclaw": "dolnośląskie",
    "poznan": "wielkopolskie",
    "gdansk": "pomorskie",
    "szczecin": "zachodniopomorskie",
    "bydgoszcz": "kujawsko-pomorskie",
    "lublin": "lubelskie",
    "bialystok": "podlaskie",
    "katowice": "śląskie",
    "kielce": "świętokrzyskie",
    "rzeszow": "podkarpackie",
    "olsztyn": "warmińsko-mazurskie",
    "opole": "opolskie",
    "gorzow-wielkopolski": "lubuskie",
    "zielona-gora": "lubuskie"
}

def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        charset=DB_CONFIG['charset']
    )

def clean_wind_direction(raw_direction):
    """
    Czyści frazę "Wind blowing from" i przypisuje kierunek na podstawie stopni.
    """
    if not raw_direction:
        return None

    # Usuwamy frazę "Wind blowing from" i ekstrahujemy stopnie
    cleaned = raw_direction.replace("Wind blowing from ", "").strip()

    try:
        # Wydobywanie stopni z tekstu (zakładając, że stopnie są na początku)
        degree = int(cleaned.split()[0].replace("°", ""))
        
        # Dopasowujemy stopnie do właściwego tłumaczenia
        degree_str = str(degree)
        if degree_str in WIND_DIRECTION_TRANSLATIONS:
            return WIND_DIRECTION_TRANSLATIONS[degree_str]
        
    except ValueError:
        pass

    return cleaned  # Jeśli nie udało się wyodrębnić stopni, zwróć oryginalny tekst

# Przykład:
raw_direction = "Wind blowing from 170° South to North"
cleaned_direction = clean_wind_direction(raw_direction)
print(cleaned_direction)  # Zwróci: 170° S do N

def translate_conditions(condition):
    """
    Tłumaczy warunki pogodowe na język polski.
    """
    if not condition:
        return None
    return CONDITIONS_TRANSLATIONS.get(condition.strip(), condition)

def parse_wind(wind_str):
    """Funkcja do parsowania prędkości wiatru i kierunku"""
    if not wind_str:
        print("Wind string is empty or None")
        return None, None
    
    print(f"Parsing wind data: {wind_str}")  # Logowanie wejściowego ciągu
    
    # Regex do wyciągania prędkości i kierunku
    match = re.search(r"([\d.,]+)\s*m/s\s*z\s+([A-Z]+)", wind_str)
    
    if match:
        try:
            speed = float(match.group(1).replace(',', '.'))
        except ValueError:
            speed = None
        direction = match.group(2)
        # Logowanie wartości wiatru przed zwróceniem
        print(f"Parsed wind speed: {speed}, direction: {direction}")
        return speed, direction
    else:
        print(f"No match found for wind: {wind_str}")
        return None, None


def parse_record_time(time_str):
    """
    Zwraca obiekt datetime, który dokładnie odwzorowuje datę i godzinę prognozy:
    - Każda godzina wcześniejsza niż teraz -> przypisana do jutra.
    - Każda godzina równa lub późniejsza niż teraz -> przypisana do dzisiaj.
    """
    time_str = time_str.strip()
    match = re.match(r"(\d{2}):(\d{2})", time_str)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2))
    
    now = datetime.now()
    candidate_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if candidate_dt < now:
        candidate_dt += timedelta(days=1)

    return candidate_dt


def insert_weather_data(city_url_name, city_display_name, record):
    conn = get_connection()
    cursor = conn.cursor()

    # Sprawdzenie, czy miasto istnieje
    cursor.execute("SELECT id FROM miasta WHERE LOWER(nazwa) = %s", (city_url_name.lower(),))
    result = cursor.fetchone()
    if result:
        miasto_id = result[0]
        # Aktualizuj województwo, jeśli jest puste
        region = CITY_TO_REGION.get(city_url_name.lower())
        if region:
            cursor.execute("SELECT wojewodztwo FROM miasta WHERE id = %s", (miasto_id,))
            woj = cursor.fetchone()
            if woj and not woj[0]:
                cursor.execute("UPDATE miasta SET wojewodztwo = %s WHERE id = %s", (region, miasto_id))
                conn.commit()
    else:
        region = CITY_TO_REGION.get(city_url_name.lower())
        cursor.execute("INSERT INTO miasta (nazwa, wojewodztwo) VALUES (%s, %s)", (city_display_name, region))
        conn.commit()
        miasto_id = cursor.lastrowid

    # Parsujemy pełny datetime z pola 'time'
    godzina = parse_record_time(record['time'])
    if not godzina:
        print(f"Błąd: nie udało się sparsować czasu dla rekordu: {record['time']}")
    
    try:
        temp_val = float(record['temperature'].split()[0])
    except Exception:
        temp_val = None

    try:
        feels_like_val = float(record['feels_like'].split()[0])
    except Exception:
        feels_like_val = None

    try:
        humidity_val = int(record['humidity'].replace('%', '').strip())
    except Exception:
        humidity_val = None

    # Odczytujemy prędkość wiatru i kierunek wiatru z osobnych kluczy
    wind_speed = record.get('wind_speed', None)
    wind_dir = record.get('wind_direction', None)

    # Tłumaczymy warunki i kierunek wiatru
    translated_conditions = translate_conditions(record.get('conditions'))
    translated_wind_dir = clean_wind_direction(wind_dir)

    # Logowanie wartości wiatru przed zapisaniem do bazy
    print(f"Translated Wind speed: {wind_speed}, Wind direction: {translated_wind_dir}")

    # Sprawdzenie, czy rekord dla danego miasta i godziny już istnieje
    cursor.execute("""
        SELECT id FROM dane_pogodowe 
        WHERE miasto_id = %s AND godzina = %s
    """, (miasto_id, godzina))

    if cursor.fetchone():
        # Jeśli rekord już istnieje, aktualizujemy go
        print(f"Rekord już istnieje dla miasta {city_display_name} o godzinie {godzina}. Aktualizowanie.")
        
        update_sql = """
            UPDATE dane_pogodowe 
            SET temperatura = %s, odczuwalna = %s, warunki = %s, wiatr = %s, kierunek = %s, wilgotnosc = %s, opady = %s
            WHERE miasto_id = %s AND godzina = %s
        """
        update_values = (
            temp_val, feels_like_val, translated_conditions, wind_speed, translated_wind_dir,
            humidity_val, record.get('precipitation'), miasto_id, godzina
        )
        cursor.execute(update_sql, update_values)
        conn.commit()

    else:
        # Jeśli rekord nie istnieje, wstawiamy nowy
        insert_sql = """
            INSERT INTO dane_pogodowe 
            (miasto_id, godzina, temperatura, odczuwalna, warunki, wiatr, kierunek, wilgotnosc, opady)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_values = (
            miasto_id, godzina, temp_val, feels_like_val, translated_conditions,
            wind_speed, translated_wind_dir, humidity_val, record.get('precipitation')
        )
        cursor.execute(insert_sql, insert_values)
        conn.commit()

    cursor.close()
    conn.close()