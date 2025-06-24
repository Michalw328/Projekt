from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

# ======= Pobieranie współrzędnych =======
# Funkcja pobiera współrzędne geograficzne danego miasta z Wikipedii
# Jeśli nie uda się pobrać danych, zwraca domyślną lokalizację (Warszawa)
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
# Klasa reprezentująca autobus
class Bus:
    def __init__(self, line, city):
        self.line = line
        self.city = city
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Autobus {self.line}")

# Klasa reprezentująca kierowcę
class Driver:
    def __init__(self, name, city, line):
        self.name = name
        self.city = city
        self.line = line
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} - linia {self.line}")

# Klasa reprezentująca klienta
class Client:
    def __init__(self, name, city, line):
        self.name = name
        self.city = city
        self.line = line
        self.coordinates = get_coordinates(city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Klient: {self.name}, linia {self.line}")

# Listy do przechowywania danych
buses = []
drivers = []
clients = []
client_line_options = []

# ======= Funkcje =======
# Dodaje autobus i kierowcę do odpowiednich list i wyświetla w listboxie
# Dodaje też linię do listy linii klientów, jeśli jeszcze jej nie ma
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

    if line not in client_line_options:
        client_line_options.append(line)
        combo_client_line['values'] = client_line_options

    clear_form()

# Przygotowuje dane do edycji w formularzu
def edit_data():
    idx = listbox_data.index(ACTIVE)
    if idx < len(buses):
        entry_line.delete(0, END)
        entry_line.insert(0, buses[idx].line)
        entry_bus_city.delete(0, END)
        entry_bus_city.insert(0, buses[idx].city)
        entry_driver_name.delete(0, END)
        entry_driver_name.insert(0, drivers[idx].name)
        entry_driver_city.delete(0, END)
        entry_driver_city.insert(0, drivers[idx].city)
        button_add_data.config(text="Zapisz", command=lambda: update_data(idx))

# Zapisuje zmiany edytowanego wpisu
def update_data(idx):
    buses[idx].marker.delete()
    drivers[idx].marker.delete()

    line = entry_line.get()
    city = entry_bus_city.get()
    name = entry_driver_name.get()
    dcity = entry_driver_city.get()

    buses[idx] = Bus(line, city)
    drivers[idx] = Driver(name, dcity, line)

    listbox_data.delete(idx)
    listbox_data.insert(idx, f"Linia {line} | {city} | {name} | {dcity}")

    button_add_data.config(text="Dodaj", command=add_data)
    clear_form()

# Dodaje klienta i wyświetla go w listboxie
def add_client():
    line = combo_client_line.get()
    name = entry_client_name.get()
    city = entry_client_city.get()
    client = Client(name, city, line)
    clients.append(client)
    listbox_clients.insert(END, f"Linia {line} | {name} | {city}")
    combo_client_line.set("")
    entry_client_name.delete(0, END)
    entry_client_city.delete(0, END)

# Przygotowuje dane klienta do edycji
def edit_client():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        combo_client_line.set(clients[idx].line)
        entry_client_name.delete(0, END)
        entry_client_name.insert(0, clients[idx].name)
        entry_client_city.delete(0, END)
        entry_client_city.insert(0, clients[idx].city)
        button_add_client.config(text="Zapisz klienta", command=lambda: update_client(idx))

# Zapisuje zmienione dane klienta i aktualizuje marker na mapie
def update_client(idx):
    clients[idx].marker.delete()
    clients[idx].line = combo_client_line.get()
    clients[idx].name = entry_client_name.get()
    clients[idx].city = entry_client_city.get()
    clients[idx].coordinates = get_coordinates(clients[idx].city)
    clients[idx].marker = map_widget.set_marker(clients[idx].coordinates[0], clients[idx].coordinates[1], text=f"Klient: {clients[idx].name}, linia {clients[idx].line}")
    listbox_clients.delete(idx)
    listbox_clients.insert(idx, f"Linia {clients[idx].line} | {clients[idx].name} | {clients[idx].city}")
    button_add_client.config(text="Dodaj klienta", command=add_client)
    combo_client_line.set("")
    entry_client_name.delete(0, END)
    entry_client_city.delete(0, END)

# Usuwa klienta z listy i z mapy
def delete_client():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        clients[idx].marker.delete()
        clients.pop(idx)
        listbox_clients.delete(idx)

# Usuwa dane autobusu i kierowcy
def delete_data():
    idx = listbox_data.index(ACTIVE)
    if idx < len(buses):
        buses[idx].marker.delete()
        drivers[idx].marker.delete()
        buses.pop(idx)
        drivers.pop(idx)
    listbox_data.delete(idx)

# Czyści pola formularza kierowcy
def clear_form():
    entry_line.delete(0, END)
    entry_bus_city.delete(0, END)
    entry_driver_name.delete(0, END)
    entry_driver_city.delete(0, END)

# Ustawia mapę na lokalizację autobusu
def show_on_map():
    idx = listbox_data.index(ACTIVE)
    if idx < len(buses):
        bus = buses[idx]
        map_widget.set_position(bus.coordinates[0], bus.coordinates[1])
        map_widget.set_zoom(14)

# Ustawia mapę na lokalizację klienta
def show_client_on_map():
    idx = listbox_clients.index(ACTIVE)
    if 0 <= idx < len(clients):
        client = clients[idx]
        map_widget.set_position(client.coordinates[0], client.coordinates[1])
        map_widget.set_zoom(14)

# ======= GUI Setup =======
# Inicjalizacja głównego okna aplikacji
root = Tk()
root.title(" zarządzania zakładem komunikacji")
root.geometry("1100x800")

# ======= Formularz Lewy =======
# Formularz dodawania autobusu i kierowcy
left_frame = Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N)

Label(left_frame, text="Linia autobusowa:").grid(row=0, column=0, sticky=W)
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

button_add_data = Button(left_frame, text="Dodaj", command=add_data)
button_add_data.grid(row=4, column=1, pady=5, sticky=E)

listbox_data = Listbox(left_frame, width=75, height=15)
listbox_data.grid(row=5, column=0, columnspan=2, pady=10)

btn_frame_left = Frame(left_frame)
btn_frame_left.grid(row=6, column=0, columnspan=2, pady=5)
Button(btn_frame_left, text="Pokaż na mapie", command=show_on_map).grid(row=0, column=0, padx=5)
Button(btn_frame_left, text="Edytuj", command=edit_data).grid(row=0, column=1, padx=5)
Button(btn_frame_left, text="Usuń", command=delete_data).grid(row=0, column=2, padx=5)

# ======= Formularz Prawy =======
# Formularz dodawania klienta
right_frame = Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N)

Label(right_frame, text="Linia autobusowa:").grid(row=0, column=0, sticky=W)
combo_client_line = ttk.Combobox(right_frame, width=27, textvariable=StringVar())
combo_client_line.grid(row=0, column=1, padx=5, pady=2)

Label(right_frame, text="Imię i nazwisko klienta:").grid(row=1, column=0, sticky=W)
entry_client_name = Entry(right_frame, width=30)
entry_client_name.grid(row=1, column=1, padx=5, pady=2)

Label(right_frame, text="Miasto klienta:").grid(row=2, column=0, sticky=W)
entry_client_city = Entry(right_frame, width=30)
entry_client_city.grid(row=2, column=1, padx=5, pady=2)

button_add_client = Button(right_frame, text="Dodaj klienta", command=add_client)
button_add_client.grid(row=3, column=1, pady=5, sticky=E)

Label(right_frame, text="").grid(row=4, column=0)  # pusty wiersz dla wyrównania
listbox_clients = Listbox(right_frame, width=60, height=15)
listbox_clients.grid(row=5, column=0, columnspan=2, pady=10)

btn_frame_right = Frame(right_frame)
btn_frame_right.grid(row=6, column=0, columnspan=2, pady=5)
Button(btn_frame_right, text="Pokaż klienta na mapie", command=show_client_on_map).grid(row=0, column=0, padx=5)
Button(btn_frame_right, text="Edytuj klienta", command=edit_client).grid(row=0, column=1, padx=5)
Button(btn_frame_right, text="Usuń klienta", command=delete_client).grid(row=0, column=2, padx=5)

# ======= Mapa =======
# Tworzenie i wyświetlenie widżetu mapy z domyślną pozycją i przybliżeniem
map_widget = tkintermapview.TkinterMapView(root, width=1000, height=400)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)
map_widget.grid(row=6, column=0, columnspan=2, pady=10)

# Uruchomienie głównej pętli aplikacji
root.mainloop()