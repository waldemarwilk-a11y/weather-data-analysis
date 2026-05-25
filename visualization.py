# visualization.py

import os
from datetime import datetime, timedelta, date

import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import DB_CONFIG

# Wymagane: pip install plotly pandas mysql-connector-python



__all__ = [
    'fetch_weather_data', 'prepare_data',
    'avg_temperature_figure', 'temp_vs_humidity_figure',
    'daily_temperature_figure', 'rain_sum_figure',
    'wind_vs_temperature_figure', 'humidity_histogram_figure',
    'correlation_heatmap_figure', 'temperature_by_hour_figure',
    'wind_effect_on_feel_temp_figure', 'wind_direction_figure',
    'next_24h_temperature_figure', 'daily_hourly_figure',
    'avg_temperature_for_city', 'temp_vs_humidity_for_city',
    'wind_effect_on_feel_temp_for_city', 'next_24h_temperature_for_city',
    'daily_hourly_for_city_and_day', 'save_plot', 'avg_humidity_figure'
]

def get_connection():
    """
    Ustanawia połączenie z bazą MySQL na podstawie parametrów z db_config.py.
    Zwraca obiekt połączenia lub None w razie błędu.
    """
    try:
        return mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset=DB_CONFIG['charset']
        )
    except mysql.connector.Error as err:
        print("Błąd połączenia z bazą:", err)
        return None

def fetch_weather_data():
    """
    Pobiera wszystkie rekordy z tabeli dane_pogodowe wraz z nazwą miasta (join z tabelą miasta).
    Zwraca DataFrame pandas.
    """
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    query = """
        SELECT dp.*, m.nazwa AS miasto
        FROM dane_pogodowe dp
        JOIN miasta m ON dp.miasto_id = m.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def prepare_data(df):
    """
    Czyści i przygotowuje surowy DataFrame:
      - konwersja kolumn tekstowych na liczby,
      - ujednolicenie wartości opadów ("-" -> 0),
      - parsowanie daty/godziny do datetime,
      - wyodrębnienie dnia, godziny i stopni kierunku wiatru.
    Zwraca wzbogacony DataFrame.
    """
    df = df.copy()
    df['temperatura'] = pd.to_numeric(df['temperatura'], errors='coerce').fillna(0)
    df['wilgotnosc']  = pd.to_numeric(df['wilgotnosc'], errors='coerce').fillna(0)

    df['opady'] = df['opady'].replace('-', '0').replace(',', '.', regex=True)
    df['opady'] = pd.to_numeric(df['opady'], errors='coerce').fillna(0)

    df['wiatr_num'] = (df['wiatr']
        .str.extract(r"([\d.,]+)")
        .replace(',', '.', regex=True)
        .astype(float)
        .fillna(0)
    )

    df['godzina_dt'] = pd.to_datetime(df['godzina'], errors='coerce')
    df['data']       = df['godzina_dt'].dt.date
    df['godzina']    = df['godzina_dt'].dt.hour

    df['kierunek_stopnie'] = df['kierunek'].str.extract(r'^(\d+)').astype(float)
    return df

def avg_temperature_figure(df):
    """
    Tworzy słupkowy wykres średniej temperatury dla każdego miasta.
    """
    data = df.groupby('miasto', as_index=False)['temperatura'].mean()
    fig = px.bar(
        data, x='miasto', y='temperatura',
        color_discrete_sequence=['#1f77b4'],
        title='Średnia temperatura w miastach',
        labels={'temperatura': 'Temperatura [°C]', 'miasto': 'Miasto'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def temp_vs_humidity_figure(df):
    """
    Wykres rozrzutu: temperatura vs wilgotność.
    Opady jako kolor, prędkość wiatru jako wielkość punktu.
    """
    fig = px.scatter(
        df, x='temperatura', y='wilgotnosc',
        color='opady', size='wiatr_num', hover_data=['miasto', 'godzina'],
        title='Temperatura vs Wilgotność (opady jako kolor, wiatr jako wielkość)',
        labels={'temperatura': '°C', 'wilgotnosc': '%', 'opady': 'Opady [mm]', 'wiatr_num': 'Wiatr [m/s]'},
        color_continuous_scale='Blues'
    )
    return fig

def daily_temperature_figure(df):
    """
    Linia pokazująca średnią temperaturę dla każdego dnia (bez godzin).
    """
    df['godzina_dt'] = pd.to_datetime(df['godzina_dt'], errors='coerce')
    daily = df.dropna(subset=['godzina_dt']).copy()
    daily['data_bez_godziny'] = daily['godzina_dt'].dt.floor('d')
    summary = (daily.groupby('data_bez_godziny', as_index=False)['temperatura']
               .mean().sort_values('data_bez_godziny'))
    fig = px.line(
        summary, x='data_bez_godziny', y='temperatura', markers=True,
        title='Średnia dzienna temperatura',
        labels={'data_bez_godziny': 'Data', 'temperatura': 'Temperatura [°C]'}
    )
    fig.update_xaxes(dtick="D", tickformat="%Y-%m-%d")
    return fig

def rain_sum_figure(df):
    """
    Słupki pokazujące sumę opadów w każdym mieście.
    Zerowe opady wyświetlane na szaro, pozostałe na kolorowo.
    """
    data = df.groupby('miasto', as_index=False)['opady'].sum()
    data['zero'] = data['opady'] == 0
    colors = data['zero'].map({True: 'lightgrey', False: 'teal'})
    fig = go.Figure(go.Bar(
        x=data['miasto'], y=data['opady'],
        marker_color=colors,
        text=data['opady'], textposition='outside'
    ))
    fig.update_layout(
        title='Suma opadów w miastach',
        xaxis_title='Miasto', yaxis_title='Opady [mm]',
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, data['opady'].max() + 1])
    )
    return fig

def wind_vs_temperature_figure(df):
    """
    Scatter: prędkość wiatru vs temperatura.
    Kolor to wartość temperatury.
    """
    fig = px.scatter(
        df, x='wiatr_num', y='temperatura',
        color='temperatura', hover_data=['miasto', 'godzina'],
        title='Prędkość wiatru vs Temperatura',
        labels={'wiatr_num': 'Prędkość wiatru [m/s]', 'temperatura': 'Temperatura [°C]'},
        color_continuous_scale='Portland'
    )
    return fig

def humidity_histogram_figure(df):
    """
    Histogram rozkładu wilgotności (%).
    """
    fig = px.histogram(
        df, x='wilgotnosc', nbins=20,
        title='Rozkład wilgotności',
        labels={'wilgotnosc': 'Wilgotność [%]'}
    )
    return fig

def correlation_heatmap_figure(df):
    """
    Heatmapa macierzy korelacji między: temperatura, wilgotność, wiatr, opady.
    """
    corr = df[['temperatura', 'wilgotnosc', 'wiatr_num', 'opady']].corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index, colorscale='Blues'
    ))
    fig.update_layout(title='Macierz korelacji parametrów pogodowych')
    return fig

def temperature_by_hour_figure(df):
    """
    Linia średniej temperatury co godzinę (dla całego zbioru).
    """
    hourly = df.dropna(subset=['godzina_dt']).copy().sort_values('godzina_dt')
    hourly_avg = hourly.groupby('godzina_dt', as_index=False)['temperatura'].mean()
    fig = px.line(
        hourly_avg, x='godzina_dt', y='temperatura', markers=True,
        title='Średnia temperatura w czasie (co godzinę)',
        labels={'godzina_dt': 'Godzina', 'temperatura': 'Temperatura [°C]'}
    )
    return fig

def wind_effect_on_feel_temp_figure(df):
    """
    Scatter: rzeczywista vs odczuwalna temperatura.
    Kolor i rozmiar punktu = prędkość wiatru.
    """
    fig = px.scatter(
        df, x='temperatura', y='odczuwalna',
        color='wiatr_num', size='wiatr_num', hover_data=['miasto', 'godzina'],
        title='Temperatura vs Temperatura odczuwalna (wiatr jako kolor/rozmiar)',
        labels={'temperatura': 'Temperatura [°C]', 'odczuwalna': 'Temperatura odczuwalna [°C]', 'wiatr_num': 'Wiatr [m/s]'},
        color_continuous_scale='Blues'
    )
    return fig

def wind_direction_figure(df):
    """
    Barpolar: średnia prędkość wiatru wg kierunku (kolor = średnia temp.).
    Na osi kątowej dodatkowo opisujemy główne kierunki N, E, S, W.
    """
    df['kierunek_simple'] = (
        df['kierunek']
        .str.extract(r'\d+°\s+([A-Z]+)')[0]
        .map({
            'N': 'Północ', 'NE': 'Płn.-Wsch.', 'E': 'Wschód',
            'SE': 'Płd.-Wsch.', 'S': 'Południe', 'SW': 'Płd.-Zach.',
            'W': 'Zachód', 'NW': 'Płn.-Zach.'
        })
        .fillna('Inny')
    )
    grouped = df.groupby('kierunek_simple', as_index=False).agg({
        'wiatr_num': 'mean', 'temperatura': 'mean'
    })
    angles = {
        'Północ': 0, 'Płn.-Wsch.': 45, 'Wschód': 90, 'Płd.-Wsch.': 135,
        'Południe': 180, 'Płd.-Zach.': 225, 'Zachód': 270, 'Płn.-Zach.': 315, 'Inny': 360
    }
    grouped['theta'] = grouped['kierunek_simple'].map(angles)

    fig = go.Figure(go.Barpolar(
        r=grouped['wiatr_num'],
        theta=grouped['theta'],
        marker=dict(
            color=grouped['temperatura'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Śr. temperatura [°C]')
        ),
        name='Prędkość wiatru'
    ))
    fig.update_layout(
        title='Średnia prędkość wiatru wg kierunku (kolor=średnia temp.)',
        polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(
                direction='clockwise',
                rotation=90,
                tickmode='array',
                tickvals=[0, 90, 180, 270],
                ticktext=['N', 'E', 'S', 'W']
            )
        )
    )
    return fig

def next_24h_temperature_figure(df, start_time=None):
    """
    Linia temperatury w kolejnych 24h od momentu start_time (domyślnie teraz),
    resamplowane co godzinę.
    """
    now = start_time or datetime.now()
    end = now + timedelta(hours=24)
    subset = df[(df['godzina_dt'] >= now) & (df['godzina_dt'] <= end)].copy()
    if subset.empty:
        print("Brak danych dla następnych 24h.")
        return go.Figure()
    subset = subset.set_index('godzina_dt').sort_index()
    avg = subset['temperatura'].resample('1h').mean().reset_index()
    fig = px.line(
        avg, x='godzina_dt', y='temperatura', markers=True,
        title='Temperatura w następnych 24 godzinach',
        labels={'godzina_dt': 'Czas', 'temperatura': 'Temperatura [°C]'}
    )
    return fig

def daily_hourly_figure(df, day=None):
    """
    Linia średniej godzinowej temperatury dla wybranego dnia (uśredniona po wszystkich miastach).
    `day` może być date lub string "YYYY-MM-DD".
    """
    day = day or date.today()
    if isinstance(day, str):
        day = datetime.strptime(day, "%Y-%m-%d").date()
    subset = df[df['data'] == day].copy()
    if subset.empty:
        print(f"Brak danych dla dnia {day}.")
        return go.Figure()
    hourly_avg = subset.groupby('godzina', as_index=False)['temperatura'].mean()
    fig = px.line(
        hourly_avg, x='godzina', y='temperatura', markers=True,
        title=f'Średnia temperatura godzinowa: {day}',
        labels={'godzina': 'Godzina', 'temperatura': 'Temperatura [°C]'}
    )
    fig.update_xaxes(dtick=1)
    return fig

def avg_humidity_figure(df):
    """
    Tworzy słupkowy wykres średniej wilgotności (%) dla każdego miasta.
    """
    data = df.groupby('miasto', as_index=False)['wilgotnosc'].mean()
    fig = px.bar(
        data,
        x='miasto',
        y='wilgotnosc',
        color_discrete_sequence=['#636EFA'],  # kontrastowy niebieski
        title='Średnia wilgotność w miastach',
        labels={'wilgotnosc': 'Wilgotność [%]', 'miasto': 'Miasto'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# === wrappery do użycia w GUI ===

def avg_temperature_for_city(df, city):
    """Wrapper: średnia temperatura dla jednego miasta."""
    return avg_temperature_figure(df[df['miasto'] == city])

def temp_vs_humidity_for_city(df, city):
    """Wrapper: temp vs wilgotność dla jednego miasta."""
    return temp_vs_humidity_figure(df[df['miasto'] == city])

def wind_effect_on_feel_temp_for_city(df, city):
    """Wrapper: temp vs odczuwalna dla jednego miasta."""
    return wind_effect_on_feel_temp_figure(df[df['miasto'] == city])

def next_24h_temperature_for_city(df, city, start_time=None):
    """Wrapper: następne 24h temp dla jednego miasta."""
    return next_24h_temperature_figure(df[df['miasto'] == city], start_time)

def daily_hourly_for_city_and_day(df, city, day=None):
    """Wrapper: profil godzinowy dla jednego miasta i dnia."""
    return daily_hourly_figure(df[df['miasto'] == city], day)


def save_plot(fig, name, folder="plots"):
    """
    Zapisuje podany plotly Figure jako plik HTML w katalogu `plots/`.
    """
    os.makedirs(folder, exist_ok=True)
    fig.write_html(os.path.join(folder, f"{name}.html"))

if __name__ == '__main__':
    # 1) Pobranie zmiennej CITY (ustawianej przez GUI lub main.py)
    city = os.environ.get("CITY", None)

    # 2) Pobranie i przygotowanie danych
    raw = fetch_weather_data()
    df  = prepare_data(raw)

    # 3) WYKRESY OGÓLNOPOLSKIE (dla wszystkich miast)
    save_plot(avg_temperature_figure(df),"avg_temperature")
    save_plot(temp_vs_humidity_figure(df),"temp_vs_humidity")
    save_plot(daily_temperature_figure(df),"daily_temperature")
    save_plot(rain_sum_figure(df),"rain_sum")
    save_plot(wind_vs_temperature_figure(df),"wind_vs_temperature")
    save_plot(humidity_histogram_figure(df),"humidity_histogram")
    save_plot(correlation_heatmap_figure(df),"correlation_heatmap")
    save_plot(temperature_by_hour_figure(df),"temperature_by_hour")
    save_plot(wind_effect_on_feel_temp_figure(df),"wind_effect_on_feel_temp")
    save_plot(wind_direction_figure(df),"wind_direction")
    save_plot(next_24h_temperature_figure(df),"next_24h_temperature")
    save_plot(daily_hourly_figure(df),"daily_hourly")
    save_plot(avg_humidity_figure(df), "avg_humidity") #DODANA FUNKCJA DLA WILGOTNOSCI


    # 4) WYKRESY DLA WYBRANEGO MIASTA
# 4) WYKRESY DLA WYBRANEGO MIASTA
    if city:
        df_city = df[df['miasto'] == city]
        save_plot(avg_temperature_for_city(df_city, city),f"avg_temperature_{city}")
        save_plot(temp_vs_humidity_for_city(df_city, city),f"temp_vs_humidity_{city}")
        save_plot(next_24h_temperature_for_city(df_city, city),f"next_24h_temperature_{city}")
        save_plot(daily_hourly_for_city_and_day(df_city, city, date.today()),f"daily_hourly_{city}_today")
        save_plot(daily_temperature_figure(df_city), f"daily_temperature_{city}.html")
        save_plot(wind_vs_temperature_figure(df_city), f"wind_vs_temperature_{city}.html")
        save_plot(humidity_histogram_figure(df_city), f"humidity_histogram_{city}.html")
        save_plot(correlation_heatmap_figure(df_city), f"correlation_heatmap_{city}.html")
        save_plot(temperature_by_hour_figure(df_city), f"temperature_by_hour_{city}.html")
        save_plot(wind_effect_on_feel_temp_figure(df_city), f"wind_effect_on_feel_temp_{city}.html")
        save_plot(wind_direction_figure(df_city), f"wind_direction_{city}.html")
        

    print("Wykresy zapisano.")





