import tkinter as tk
from tkinter import messagebox
import math


class Flight:
    def __init__(self, source, destination, duration):
        self.source = source
        self.destination = destination
        self.duration = duration

class FlightNetwork:
    def __init__(self):
        self.flights = []
        self.airports = set()

    def add_flight(self, source, destination, duration):
        self.flights.append(Flight(source, destination, duration))
        self.airports.add(source)
        self.airports.add(destination)

    def bellman_ford(self, source):
        distances = {airport: float('inf') for airport in self.airports}
        distances[source] = 0

        for _ in range(len(self.airports) - 1):
            for flight in self.flights:
                if distances[flight.source] != float('inf') and distances[flight.source] + flight.duration < distances[flight.destination]:
                    distances[flight.destination] = distances[flight.source] + flight.duration

        # Check for negative cycles
        for flight in self.flights:
            if distances[flight.source] != float('inf') and distances[flight.source] + flight.duration < distances[flight.destination]:
                raise ValueError("Negative cycle detected")

        return distances


    def get_shortest_path(self, source, destination):
        distances = self.bellman_ford(source)

        path = []
        current = destination

        while current != source:
            path.append(current)
            found_prev = False
            for flight in self.flights:
                if flight.destination == current and distances[flight.source] + flight.duration == distances[current]:
                    current = flight.source
                    found_prev = True
                    break
            if not found_prev:
                return []  # No path found

        path.append(source)
        path.reverse()

        return path



class FlightDetailsGUI:
    def __init__(self):
        self.network = FlightNetwork()

        self.root = tk.Tk()
        self.root.title("Flight Details")

        self.canvas_width = 600
        self.canvas_height = 400

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label_source = tk.Label(self.frame, text="Source Airport:")
        self.label_source.grid(row=0, column=0)

        self.entry_source = tk.Entry(self.frame)
        self.entry_source.grid(row=0, column=1)

        self.label_destination = tk.Label(self.frame, text="Destination Airport:")
        self.label_destination.grid(row=1, column=0)

        self.entry_destination = tk.Entry(self.frame)
        self.entry_destination.grid(row=1, column=1)

        self.label_duration = tk.Label(self.frame, text="Flight Duration:")
        self.label_duration.grid(row=2, column=0)

        self.entry_duration = tk.Entry(self.frame)
        self.entry_duration.grid(row=2, column=1)

        self.button_add = tk.Button(self.root, text="Add Flight", command=self.add_flight)
        self.button_add.pack()

        self.button_display = tk.Button(self.root, text="Display Flights", command=self.display_flights)
        self.button_display.pack()

        self.button_shortest_path = tk.Button(self.root, text="Calculate Shortest Path", command=self.calculate_shortest_path)
        self.button_shortest_path.pack()

    def add_flight(self):
        source = self.entry_source.get()
        destination = self.entry_destination.get()
        duration = self.entry_duration.get()

        if source and destination and duration:
            self.network.add_flight(source, destination, int(duration))
            messagebox.showinfo("Flight Added", "Flight details added successfully.")
            self.display_graph()
        else:
            messagebox.showwarning("Missing Information", "Please enter all flight details.")

        self.entry_source.delete(0, tk.END)
        self.entry_destination.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def display_flights(self):
        if self.network.flights:
            message = "Flight Details:\n\n"
            for flight in self.network.flights:
                message += f"Source: {flight.source}\n"
                message += f"Destination: {flight.destination}\n"
                message += f"Duration: {flight.duration}\n"
                message += "\n"
            messagebox.showinfo("Flight Details", message)
        else:
            messagebox.showinfo("No Flights", "No flight details to display.")

    def calculate_shortest_path(self):
        source = self.entry_source.get()
        destination = self.entry_destination.get()

        if source and destination:
            path = self.network.get_shortest_path(source, destination)
            if path:
                messagebox.showinfo("Shortest Path", f"Shortest Path: {' -> '.join(path)}")
            else:
                messagebox.showwarning("No Path Found", "No path found between the specified airports.")
        else:
            messagebox.showwarning("Missing Information", "Please enter source and destination airports.")


    def display_graph(self):
        self.canvas.delete("all")  # Clear the canvas

        num_airports = len(self.network.airports)
        angle_increment = 2 * math.pi / num_airports
        radius = min(self.canvas_width, self.canvas_height) * 0.4
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2

        # Draw airports
        airport_positions = {}
        for i, airport in enumerate(self.network.airports):
            angle = i * angle_increment
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            airport_positions[airport] = (x, y)
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
            self.canvas.create_text(x, y - 20, text=airport)

        # Draw flights
        for flight in self.network.flights:
            source_x, source_y = airport_positions[flight.source]
            dest_x, dest_y = airport_positions[flight.destination]
            self.canvas.create_line(
                source_x, source_y, dest_x, dest_y,
                smooth=True, arrow=tk.LAST, width=2
            )


    def run(self):
        self.root.mainloop()


gui = FlightDetailsGUI()
gui.run()
