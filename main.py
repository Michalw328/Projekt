from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

class Bus:
    def __init__(self, line, stop_name, passengers):
        self.line = line
        self.stop_name = stop_name
        self.passengers = passengers
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Linia {line}")

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.stop_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except IndexError:
            return [52.23, 21.01]  # domyślnie Warszawa

buses = []

def add_bus():
    line = entry_line.get()
    stop = entry_stop.get()
    passengers = entry_passengers.get()
    bus = Bus(line, stop, passengers)
    buses.append(bus)
    update_bus_list()
    clear_form()

def update_bus_list():
    listbox_buses.delete(0, END)
    for i, bus in enumerate(buses):
        listbox_buses.insert(i, f"{i+1}. Linia {bus.line}, {bus.stop_name}, {bus.passengers} pasażerów")

def delete_bus():
    idx = listbox_buses.index(ACTIVE)
    buses[idx].marker.delete()
    buses.pop(idx)
    update_bus_list()

def show_bus_details():
    idx = listbox_buses.index(ACTIVE)
    bus = buses[idx]
    label_line_value.config(text=bus.line)
    label_stop_value.config(text=bus.stop_name)
    label_passengers_value.config(text=bus.passengers)
    map_widget.set_position(bus.coordinates[0], bus.coordinates[1])
    map_widget.set_zoom(14)

def edit_bus():
    idx = listbox_buses.index(ACTIVE)
    bus = buses[idx]
    entry_line.insert(0, bus.line)
    entry_stop.insert(0, bus.stop_name)
    entry_passengers.insert(0, bus.passengers)
    button_add.config(text="Zapisz", command=lambda: save_edit(idx))

def save_edit(idx):
    buses[idx].marker.delete()
    buses[idx].line = entry_line.get()
    buses[idx].stop_name = entry_stop.get()
    buses[idx].passengers = entry_passengers.get()
    buses[idx].coordinates = buses[idx].get_coordinates()
    buses[idx].marker = map_widget.set_marker(buses[idx].coordinates[0], buses[idx].coordinates[1], text=f"Linia {buses[idx].line}")
    button_add.config(text="Dodaj", command=add_bus)
    update_bus_list()
    clear_form()

def clear_form():
    entry_line.delete(0, END)
    entry_stop.delete(0, END)
    entry_passengers.delete(0, END)
    entry_line.focus()

# GUI
root = Tk()
root.title("Zarządzanie autobusami")
root.geometry("1024x768")

# Layout
frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0, padx=10)
frame_form.grid(row=0, column=1, padx=10)
frame_details.grid(row=1, column=0, columnspan=2, pady=10)
frame_map.grid(row=2, column=0, columnspan=2)

# Lista autobusów
Label(frame_list, text="Lista autobusów:").pack()
listbox_buses = Listbox(frame_list, width=60)
listbox_buses.pack()
Button(frame_list, text="Pokaż szczegóły", command=show_bus_details).pack(pady=5)
Button(frame_list, text="Edytuj", command=edit_bus).pack()
Button(frame_list, text="Usuń", command=delete_bus).pack()

# Formularz dodawania
Label(frame_form, text="Dodaj autobus:").grid(row=0, column=0, columnspan=2)
Label(frame_form, text="Linia:").grid(row=1, column=0, sticky=W)
entry_line = Entry(frame_form)
entry_line.grid(row=1, column=1)

Label(frame_form, text="Przystanek:").grid(row=2, column=0, sticky=W)
entry_stop = Entry(frame_form)
entry_stop.grid(row=2, column=1)

Label(frame_form, text="Pasażerowie:").grid(row=3, column=0, sticky=W)
entry_passengers = Entry(frame_form)
entry_passengers.grid(row=3, column=1)

button_add = Button(frame_form, text="Dodaj", command=add_bus)
button_add.grid(row=4, column=0, columnspan=2, pady=5)

# Szczegóły autobusu
Label(frame_details, text="Szczegóły autobusu:").grid(row=0, column=0, sticky=W)
Label(frame_details, text="Linia:").grid(row=1, column=0)
label_line_value = Label(frame_details, text="...")
label_line_value.grid(row=1, column=1)

Label(frame_details, text="Przystanek:").grid(row=1, column=2)
label_stop_value = Label(frame_details, text="...")
label_stop_value.grid(row=1, column=3)

Label(frame_details, text="Pasażerowie:").grid(row=1, column=4)
label_passengers_value = Label(frame_details, text="...")
label_passengers_value.grid(row=1, column=5)

# Mapa
map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.23, 21.01)  # Warszawa
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()
