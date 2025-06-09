from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

# ======= Pomocnicza funkcja pobierania współrzędnych =======
def get_coordinates(location):
    try:
        url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [lat, lon]
    except:
        return [52.23, 21.01]  # domyślnie Warszawa

# ======= Klasa kierowcy =======
class Driver:
    def __init__(self, name, city, line):
        self.name = name
        self.city = city
        self.line = line
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} - linia {self.line}")

drivers = []

# ======= Funkcje GUI dla kierowców =======
def add_driver():
    name = entry_driver_name.get()
    city = entry_driver_city.get()
    line = entry_driver_line.get()
    driver = Driver(name, city, line)
    drivers.append(driver)
    update_driver_list()
    clear_driver_form()

def update_driver_list():
    listbox_drivers.delete(0, END)
    for i, d in enumerate(drivers):
        listbox_drivers.insert(i, f"{d.name} | {d.city} | linia {d.line}")

def delete_driver():
    idx = listbox_drivers.index(ACTIVE)
    drivers[idx].marker.delete()
    drivers.pop(idx)
    update_driver_list()

def show_driver_on_map():
    idx = listbox_drivers.index(ACTIVE)
    d = drivers[idx]
    map_widget.set_position(d.coordinates[0], d.coordinates[1])
    map_widget.set_zoom(14)

def edit_driver():
    idx = listbox_drivers.index(ACTIVE)
    d = drivers[idx]
    entry_driver_name.delete(0, END)
    entry_driver_name.insert(0, d.name)
    entry_driver_city.delete(0, END)
    entry_driver_city.insert(0, d.city)
    entry_driver_line.delete(0, END)
    entry_driver_line.insert(0, d.line)
    button_driver_add.config(text="Zapisz", command=lambda: update_driver(idx))

def update_driver(idx):
    drivers[idx].marker.delete()
    drivers[idx].name = entry_driver_name.get()
    drivers[idx].city = entry_driver_city.get()
    drivers[idx].line = entry_driver_line.get()
    drivers[idx].coordinates = get_coordinates(drivers[idx].city)
    drivers[idx].marker = map_widget.set_marker(
        drivers[idx].coordinates[0], drivers[idx].coordinates[1],
        text=f"{drivers[idx].name} - linia {drivers[idx].line}"
    )
    button_driver_add.config(text="Dodaj", command=add_driver)
    update_driver_list()
    clear_driver_form()

def clear_driver_form():
    entry_driver_name.delete(0, END)
    entry_driver_city.delete(0, END)
    entry_driver_line.delete(0, END)
    entry_driver_name.focus()

# ======= GUI Setup =======
root = Tk()
root.title("Zarządzanie autobusami i kierowcami")
root.geometry("1024x768")

notebook = ttk.Notebook(root)
frame_buses = Frame(notebook)
frame_drivers = Frame(notebook)
frame_map = Frame(root)

notebook.add(frame_buses, text="Autobusy")
notebook.add(frame_drivers, text="Kierowcy")
notebook.pack(expand=True, fill="both")
frame_map.pack(fill="both")

# ======= GUI dla kierowców =======
Label(frame_drivers, text="Imię i nazwisko:").grid(row=0, column=0, sticky=W)
entry_driver_name = Entry(frame_drivers)
entry_driver_name.grid(row=0, column=1)

Label(frame_drivers, text="Miasto:").grid(row=1, column=0, sticky=W)
entry_driver_city = Entry(frame_drivers)
entry_driver_city.grid(row=1, column=1)

Label(frame_drivers, text="Linia autobusowa:").grid(row=2, column=0, sticky=W)
entry_driver_line = Entry(frame_drivers)
entry_driver_line.grid(row=2, column=1)

button_driver_add = Button(frame_drivers, text="Dodaj", command=add_driver)
button_driver_add.grid(row=3, column=1, pady=5)

listbox_drivers = Listbox(frame_drivers, width=50)
listbox_drivers.grid(row=4, column=0, columnspan=2)

Button(frame_drivers, text="Pokaż na mapie", command=show_driver_on_map).grid(row=5, column=0)
Button(frame_drivers, text="Edytuj", command=edit_driver).grid(row=5, column=1)
Button(frame_drivers, text="Usuń", command=delete_driver).grid(row=6, column=0, columnspan=2)

# ======= Mapa =======
map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.23, 21.01)  # Warszawa
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()
