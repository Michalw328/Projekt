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

class Client:
    def __init__(self, name, city, line):
        self.name = name
        self.city = city
        self.line = line
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Klient: {self.name}, linia {self.line}")

buses = []
drivers = []
clients = []

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

def add_client():
    line = entry_client_line.get()
    name = entry_client_name.get()
    city = entry_client_city.get()
    client = Client(name, city, line)
    clients.append(client)
    listbox_clients.insert(END, f"Linia {line} | {name} | {city}")
    entry_client_line.delete(0, END)
    entry_client_name.delete(0, END)
    entry_client_city.delete(0, END)

def edit_client():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        entry_client_line.delete(0, END)
        entry_client_line.insert(0, clients[idx].line)
        entry_client_name.delete(0, END)
        entry_client_name.insert(0, clients[idx].name)
        entry_client_city.delete(0, END)
        entry_client_city.insert(0, clients[idx].city)
        button_add_client.config(text="Zapisz klienta", command=lambda: update_client(idx))

def update_client(idx):
    clients[idx].marker.delete()
    clients[idx].line = entry_client_line.get()
    clients[idx].name = entry_client_name.get()
    clients[idx].city = entry_client_city.get()
    clients[idx].coordinates = get_coordinates(clients[idx].city)
    clients[idx].marker = map_widget.set_marker(clients[idx].coordinates[0], clients[idx].coordinates[1], text=f"Klient: {clients[idx].name}, linia {clients[idx].line}")
    listbox_clients.delete(idx)
    listbox_clients.insert(idx, f"Linia {clients[idx].line} | {clients[idx].name} | {clients[idx].city}")
    button_add_client.config(text="Dodaj klienta", command=add_client)
    entry_client_line.delete(0, END)
    entry_client_name.delete(0, END)
    entry_client_city.delete(0, END)

def delete_client():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        clients[idx].marker.delete()
        clients.pop(idx)
        listbox_clients.delete(idx)

def delete_data():
    idx = listbox_data.index(ACTIVE)
    if idx < len(buses):
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
    if idx < len(buses):
        bus = buses[idx]
        map_widget.set_position(bus.coordinates[0], bus.coordinates[1])
        map_widget.set_zoom(14)

def show_client_on_map():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        client = clients[idx]
        map_widget.set_position(client.coordinates[0], client.coordinates[1])
        map_widget.set_zoom(14)

# ======= GUI Setup =======
root = Tk()
root.title("Zarządzanie autobusami i kierowcami")
root.geometry("1024x768")

# ======= Formularz Lewy =======
left_frame = Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N)

Label(left_frame, text="Linia autobusu:").grid(row=0, column=0, sticky=W)
entry_line = Entry(left_frame, width=40)
entry_line.grid(row=0, column=1, padx=10, pady=2)

Label(left_frame, text="Miasto:").grid(row=1, column=0, sticky=W)
entry_bus_city = Entry(left_frame, width=40)
entry_bus_city.grid(row=1, column=1, padx=10, pady=2)

Label(left_frame, text="Imię i nazwisko kierowcy:").grid(row=2, column=0, sticky=W)
entry_driver_name = Entry(left_frame, width=40)
entry_driver_name.grid(row=2, column=1, padx=10, pady=2)

Label(left_frame, text="Miasto kierowcy:").grid(row=3, column=0, sticky=W)
entry_driver_city = Entry(left_frame, width=40)
entry_driver_city.grid(row=3, column=1, padx=10, pady=2)

Button(left_frame, text="Dodaj", command=add_data).grid(row=4, column=1, pady=5, sticky=E)

# ======= Lista =======
listbox_data = Listbox(left_frame, width=80)
listbox_data.grid(row=5, column=0, columnspan=2, pady=10)

Button(left_frame, text="Pokaż na mapie", command=show_on_map).grid(row=6, column=0)
Button(left_frame, text="Usuń", command=delete_data).grid(row=6, column=1, sticky=E)

# ======= Formularz Prawy =======
right_frame = Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N)

Label(right_frame, text="Linia autobusowa:").grid(row=0, column=0, sticky=W)
entry_client_line = Entry(right_frame, width=30)
entry_client_line.grid(row=0, column=1, padx=5, pady=2)

Label(right_frame, text="Klienci:").grid(row=1, column=0, sticky=W)
entry_client_name = Entry(right_frame, width=30)
entry_client_name.grid(row=1, column=1, padx=5, pady=2)

Label(right_frame, text="Miasto klienta:").grid(row=2, column=0, sticky=W)
entry_client_city = Entry(right_frame, width=30)
entry_client_city.grid(row=2, column=1, padx=5, pady=2)

button_add_client = Button(right_frame, text="Dodaj klienta", command=add_client)
button_add_client.grid(row=3, column=1, pady=5, sticky=E)

listbox_clients = Listbox(right_frame, width=60)
listbox_clients.grid(row=4, column=0, columnspan=2, pady=10)

Button(right_frame, text="Pokaż klienta na mapie", command=show_client_on_map).grid(row=5, column=1, sticky=E)
Button(right_frame, text="Edytuj klienta", command=edit_client).grid(row=6, column=0, sticky=W)
Button(right_frame, text="Usuń klienta", command=delete_client).grid(row=6, column=1, sticky=E)

# ======= Mapa =======
map_widget = tkintermapview.TkinterMapView(root, width=1000, height=400)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)
map_widget.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()