from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# ======= Pobieranie współrzędnych =======
def get_coordinates(location):
    try:
        url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [lat, lon]
    except:
        return [52.23, 21.01]  # Domyślna lokalizacja: Warszawa

# ======= Klasy =======
class Bus:
    def __init__(self, line, city):
        self.line = line
        self.city = city
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Autobus {self.line}")

class Driver:
    def __init__(self, name, city, line):
        self.name = name
        self.city = city
        self.line = line
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} - linia {self.line}")

buses = []
drivers = []

# ======= Funkcje =======
def add_data():
    line = entry_line.get()
    bus_city = entry_bus_city.get()
    driver_name = entry_driver_name.get()
    driver_city = entry_driver_city.get()

    bus = Bus(line, bus_city)
    driver = Driver(driver_name, driver_city, line)

    buses.append(bus)
    drivers.append(driver)

    listbox_data.insert(END, f"Linia {line} | {bus_city} | {driver_name} | {driver_city}")
    clear_form()

def delete_data():
    idx = listbox_data.index(ACTIVE)
    buses[idx].marker.delete()
    drivers[idx].marker.delete()
    buses.pop(idx)
    drivers.pop(idx)
    listbox_data.delete(idx)

def clear_form():
    entry_line.delete(0, END)
    entry_bus_city.delete(0, END)
    entry_driver_name.delete(0, END)
    entry_driver_city.delete(0, END)

def show_on_map():
    idx = listbox_data.index(ACTIVE)
    bus = buses[idx]
    map_widget.set_position(bus.coordinates[0], bus.coordinates[1])
    map_widget.set_zoom(14)

# ======= GUI Setup =======
root = Tk()
root.title("Zarządzanie autobusami i kierowcami")
root.geometry("1024x768")

# ======= Formularz =======
Label(root, text="Linia autobusu:").grid(row=0, column=0, sticky=W)
entry_line = Entry(root, width=40)
entry_line.grid(row=0, column=1, padx=10, pady=2)

Label(root, text="Miasto:").grid(row=1, column=0, sticky=W)
entry_bus_city = Entry(root, width=40)
entry_bus_city.grid(row=1, column=1, padx=10, pady=2)

Label(root, text="Imię i nazwisko kierowcy:").grid(row=2, column=0, sticky=W)
entry_driver_name = Entry(root, width=40)
entry_driver_name.grid(row=2, column=1, padx=10, pady=2)

Label(root, text="Miasto kierowcy:").grid(row=3, column=0, sticky=W)
entry_driver_city = Entry(root, width=40)
entry_driver_city.grid(row=3, column=1, padx=10, pady=2)

Button(root, text="Dodaj", command=add_data).grid(row=4, column=1, pady=5, sticky=E)

# ======= Lista =======
listbox_data = Listbox(root, width=100)
listbox_data.grid(row=5, column=0, columnspan=2, pady=10)

Button(root, text="Pokaż na mapie", command=show_on_map).grid(row=6, column=0)
Button(root, text="Usuń", command=delete_data).grid(row=6, column=1, sticky=E)

# ======= Mapa =======
map_widget = tkintermapview.TkinterMapView(root, width=1000, height=400)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)
map_widget.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()