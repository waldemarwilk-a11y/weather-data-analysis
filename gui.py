import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import webbrowser

CITIES = ["Warsaw", "Krakow", "Wroclaw", "Poznan", "Gdansk", "Bydgoszcz", "Katowice", "Kielce", "Lublin", "Gorzow-wielkopolski", "Lodz", "Opole", "Szczecin", "Zielona-gora", "Rzeszow"]

def run_main(city):
    try:
        os.environ["CITY"] = city  # Zapisujemy miasto jako zmienną środowiskową
        subprocess.run(["python", "main.py"], check=True)
        messagebox.showinfo("Sukces", f"Dane dla miasta {city} zostały pobrane i zapisane.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Coś poszło nie tak: {e}")

def run_visualization(city):
    try:
        os.environ["CITY"] = city
        subprocess.run(["python", "visualization.py"], check=True)
        messagebox.showinfo("Wykresy", "Wykresy wygenerowane pomyślnie.")
        open_plots_in_browser(city)
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wygenerować wykresów: {e}")

def run_national_visualization():
    try:
        if "CITY" in os.environ:
            del os.environ["CITY"]  # Usuwamy CITY, żeby visualization.py działał ogólnie
        subprocess.run(["python", "visualization.py"], check=True)
        messagebox.showinfo("Wykresy", "Wykresy ogólnopolskie wygenerowane pomyślnie.")
        open_all_national_plots()
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wygenerować ogólnych wykresów: {e}")

def open_all_national_plots():
    plots_dir = "plots"
    html_files = [
        f for f in os.listdir(plots_dir)
        if f.endswith(".html") and all(city.lower() not in f.lower() for city in CITIES)
    ]

    if not html_files:
        messagebox.showinfo("Brak wykresów", "Nie znaleziono żadnych ogólnych wykresów w folderze 'plots/'.")
        return

    index_path = os.path.join(plots_dir, "index_all.html")
    with open(index_path, "w", encoding="utf-8") as idx:
        idx.write("""<!DOCTYPE html>
<html lang="pl">
<head><meta charset="utf-8"><title>Wykresy Ogólnopolskie</title>
<style>iframe{width:100%;height:500px;border:1px solid #ccc;margin-bottom:20px;}</style>
</head><body>
<h1>Wszystkie ogólnopolskie wykresy</h1>
""")
        for fname in html_files:
            idx.write(f'<h2>{fname}</h2>\n')
            idx.write(f'<iframe src="{fname}"></iframe>\n')
        idx.write("</body></html>")

    webbrowser.open(f"file:///{os.path.abspath(index_path)}")

def open_plots_in_browser(city):
    plots_dir = "plots"
    html_files = [f for f in os.listdir(plots_dir) if f.endswith(".html") and city in f]

    if not html_files:
        messagebox.showinfo("Brak wykresów", f"Nie znaleziono żadnych wykresów HTML dla miasta '{city}' w folderze 'plots/'.")
        return

    index_path = os.path.join(plots_dir, f"index_{city}.html")
    with open(index_path, "w", encoding="utf-8") as idx:
        idx.write(f"""<!DOCTYPE html>
<html lang="pl">
<head><meta charset="utf-8"><title>Wykresy dla {city}</title>
<style>iframe{{width:100%;height:500px;border:1px solid #ccc;margin-bottom:20px;}}</style>
</head><body>
<h1>Wszystkie wykresy dla {city.capitalize()}</h1>
""")
        for fname in html_files:
            idx.write(f'<h2>{fname}</h2>\n')
            idx.write(f'<iframe src="{fname}"></iframe>\n')
        idx.write("</body></html>")

    webbrowser.open(f"file:///{os.path.abspath(index_path)}")

def create_gui():
    root = tk.Tk()
    root.title("PogodaProjekt GUI")
    root.geometry("400x350")

    ttk.Label(root, text="Wybierz miasto:", font=("Segoe UI", 12)).pack(pady=10)
    city_var = tk.StringVar(value=CITIES[0])
    city_combobox = ttk.Combobox(root, textvariable=city_var, values=CITIES, state="readonly")
    city_combobox.pack(pady=5)

    ttk.Button(root, text="Pobierz dane pogodowe", command=lambda: run_main(city_var.get())).pack(pady=10)
    ttk.Button(root, text="Generuj i pokaż wykresy", command=lambda: run_visualization(city_var.get())).pack(pady=10)
    ttk.Button(root, text="Wykresy ogólnopolskie", command=run_national_visualization).pack(pady=10)  # <-- Nowy przycisk

    root.mainloop()

if __name__ == "__main__":
    create_gui()
