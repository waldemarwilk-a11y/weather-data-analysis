import time
import os
from scraping import get_weather_data, cities
from db import insert_weather_data

# --- DODAJEMY IMPORTY DO WIZUALIZACJI ---
from visualization import (
    fetch_weather_data as fetch_viz_data,
    prepare_data,
    avg_temperature_figure,
    temp_vs_humidity_figure,
    daily_temperature_figure,
    rain_sum_figure,
    wind_vs_temperature_figure,
    humidity_histogram_figure,
    correlation_heatmap_figure,
    temperature_by_hour_figure,
    wind_effect_on_feel_temp_figure,
    wind_direction_figure,
    next_24h_temperature_figure,
    daily_hourly_figure,
    avg_temperature_for_city,
    temp_vs_humidity_for_city,
    next_24h_temperature_for_city,
    daily_hourly_for_city_and_day,
    save_plot
)

def main():
    # 1) SCRAPING + WSTAWIANIE DO BAZY
    city = os.environ.get("CITY", "Warszawa")  # Pobierz wybrane miasto z GUI, domyślnie Warszawa
    print(f"Przetwarzanie danych dla {city.capitalize()}...")

    weather_data = get_weather_data(city)
    if weather_data:
        for record in weather_data:
            insert_weather_data(city, city.capitalize(), record)
            print(f"  – Wstawiono rekord o godzinie {record['time']}")
    else:
        print(f"  – Brak danych dla {city.capitalize()}.")
    time.sleep(2)

    # 2) GENEROWANIE WIZUALIZACJI
    print("\nPobieram z bazy i generuję wykresy…")
    raw = fetch_viz_data()
    df = prepare_data(raw)

    # 2.1) Wykresy ogólnopolskie (dla wszystkich miast)
    print("\nGenerowanie wykresów ogólnopolskich...")
    save_plot(avg_temperature_figure(df), "avg_temperature")
    save_plot(temp_vs_humidity_figure(df), "temp_vs_humidity")
    save_plot(daily_temperature_figure(df), "daily_temperature")
    save_plot(rain_sum_figure(df), "rain_sum")
    save_plot(wind_vs_temperature_figure(df), "wind_vs_temperature")
    save_plot(humidity_histogram_figure(df), "humidity_histogram")
    save_plot(correlation_heatmap_figure(df), "correlation_heatmap")
    save_plot(temperature_by_hour_figure(df), "temperature_by_hour")
    save_plot(wind_effect_on_feel_temp_figure(df), "wind_effect_on_feel_temp")
    save_plot(wind_direction_figure(df), "wind_direction")
    save_plot(next_24h_temperature_figure(df), "next_24h_temperature")
    save_plot(daily_hourly_figure(df), "daily_hourly")
    

    # 2.2) Generowanie wykresów dla wybranego miasta
    print(f"\nGenerowanie wykresów dla {city.capitalize()}...")
    df_city = df[df['miasto'] == city]

    save_plot(avg_temperature_for_city(df_city, city), f"avg_temperature_{city}")
    save_plot(temp_vs_humidity_for_city(df_city, city), f"temp_vs_humidity_{city}")
    save_plot(next_24h_temperature_for_city(df_city, city), f"next_24h_temperature_{city}")
    save_plot(daily_hourly_for_city_and_day(df_city, city, None), f"daily_hourly_{city}_today")
    save_plot(daily_temperature_figure(df_city), f"daily_temperature_{city}.html")
    save_plot(wind_vs_temperature_figure(df_city), f"wind_vs_temperature_{city}.html")
    save_plot(humidity_histogram_figure(df_city), f"humidity_histogram_{city}.html")
    save_plot(correlation_heatmap_figure(df_city), f"correlation_heatmap_{city}.html")
    save_plot(temperature_by_hour_figure(df_city), f"temperature_by_hour_{city}.html")
    save_plot(wind_effect_on_feel_temp_figure(df_city), f"wind_effect_on_feel_temp_{city}.html")
    save_plot(wind_direction_figure(df_city), f"wind_direction_{city}.html")

    print(f"Wykresy dla {city.capitalize()} zapisane w katalogu plots/.")


if __name__ == '__main__':
    main()
