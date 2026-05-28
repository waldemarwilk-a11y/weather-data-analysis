# Weather Data Analysis System

## Overview

Weather Data Analysis System is an end-to-end data pipeline application that collects, processes, stores, analyzes, and visualizes weather data for major cities in Poland.

The system integrates:
- web scraping
- MySQL database
- data processing with Pandas
- interactive visualization with Plotly
- desktop GUI built with Tkinter

It demonstrates a full ETL workflow from raw data acquisition to analytical dashboards.

---

## System Architecture

Web Scraping → Data Cleaning → MySQL Storage → Data Processing (Pandas) → Visualization (Plotly) → HTML Reports → Desktop GUI (Tkinter)

---

## Features

### Data Collection
- Hourly weather data scraping from timeanddate.com
- Multiple Polish cities support
- Extracted parameters:
  - temperature
  - perceived temperature
  - weather conditions
  - wind speed and direction
  - humidity
  - precipitation

---

### Data Processing
- Cleaning and normalization of scraped data
- Translation of weather conditions into Polish
- Wind direction parsing and normalization
- Time string conversion to datetime
- Missing value handling

---

### Database (MySQL)
- Tables:
  - miasta (cities)
  - dane_pogodowe (weather records)
- Insert/update logic preventing duplicates
- Mapping cities to Polish voivodeships

---

### Data Analysis (Pandas)
- Average temperature per city
- Humidity distribution
- Precipitation totals
- Correlation between variables
- Hourly and daily trends

---

### Visualization (Plotly)
All charts are exported as interactive HTML files.

Includes:
- temperature trends over time
- temperature vs humidity
- wind vs temperature
- precipitation analysis
- correlation heatmaps
- 24-hour forecast
- wind direction analysis

---

### Desktop GUI (Tkinter)
- City selection dropdown
- One-click data scraping
- One-click visualization generation
- Automatic opening of results in browser

---

## Project Structure

```text
weather-data-analysis/
├── main.py                 # ETL pipeline (scraping + DB + visualization)
├── scraping.py             # web scraping logic
├── db.py                   # database connection + insert/update logic
├── db_config.py           # MySQL configuration
├── visualization.py       # data analysis + Plotly charts
├── gui.py                 # Tkinter GUI
├── requirements.txt
├── weather_db_dump.sql    # database schema
└── plots/                 # generated HTML visualizations
```

## Database Schema

### Table: miasta
- id (PK)
- nazwa
- wojewodztwo

### Table: dane_pogodowe
- id (PK)
- miasto_id (FK)
- godzina (datetime)
- temperatura
- odczuwalna
- warunki
- wiatr
- kierunek
- wilgotnosc
- opady

---

## Installation

### Clone repository

git clone https://github.com/waldemarwilk-a11y/weather-data-analysis
cd weather-data-analysis

### Install dependencies

pip install -r requirements.txt

### Database setup

Import weather_db_dump.sql into MySQL and update credentials in db_config.py.

---

## Usage

### Run GUI

python gui.py

### Run pipeline manually

python main.py

---

## Screenshots

### GUI

<img width="396" height="375" alt="Zrzut ekranu 2026-05-28 214957" src="https://github.com/user-attachments/assets/4caf4f6f-845e-4dd0-b31a-884952797d34" />

### Example visualization

<img width="804" height="883" alt="Zrzut ekranu 2026-05-28 215522" src="https://github.com/user-attachments/assets/c368ff8b-9239-45ac-8e65-e3134b9e2ca1" />

---

## Key Insights

- comparison of weather across Polish cities
- temperature and humidity relationships
- wind influence on perceived temperature
- 24-hour weather trend analysis
- regional climate differences

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- MySQL
- Pandas
- Plotly
- Tkinter

---

## Project Summary

This project demonstrates end-to-end data engineering skills:

- ETL pipeline design
- web scraping and data ingestion
- relational database usage
- data cleaning and transformation
- exploratory data analysis
- interactive visualization
- desktop application development

Suitable for data engineering / backend portfolio.
