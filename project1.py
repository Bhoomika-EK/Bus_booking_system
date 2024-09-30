import tkinter as tk
from tkinter import messagebox

class BusReservationSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Bus Reservation System")
        self.master.geometry("600x500")
        self.master.configure(bg="#e0f7fa")

        self.buses = {
            "Bus A": {i: None for i in range(1, 11)},
            "Bus B": {i: None for i in range(1, 11)},
            "Bus C": {i: None for i in range(1, 11)},
        }

        self.create_widgets()

    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.master, bg="#00796b")
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(title_frame, text="Bus Reservation System", font=("Arial", 16, "bold"), bg="#00796b", fg="white")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(self.master, bg="#e0f7fa")
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Select Bus:", font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, padx=10)
        
        self.bus_var = tk.StringVar(value=list(self.buses.keys())[0])
        self.bus_menu = tk.OptionMenu(input_frame, self.bus_var, *self.buses.keys(), command=self.update_seat_display)
        self.bus_menu.config(font=("Arial", 12))
        self.bus_menu.grid(row=0, column=1, padx=10)

        tk.Label(input_frame, text="Select Seat:", font=("Arial", 12), bg="#e0f7fa").grid(row=1, column=0, padx=10)
        
        self.seat_var = tk.StringVar()
        self.seat_menu = tk.OptionMenu(input_frame, self.seat_var, "")
        self.seat_menu.config(font=("Arial", 12))
        self.seat_menu.grid(row=1, column=1, padx=10)

        tk.Label(input_frame, text="Name:", font=("Arial", 12), bg="#e0f7fa").grid(row=2, column=0, padx=10)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.name_entry.grid(row=2, column=1, padx=10)

        # Buttons
        button_frame = tk.Frame(self.master, bg="#e0f7fa")
        button_frame.pack(pady=20)

        book_button = tk.Button(button_frame, text="Book Ticket", command=self.book_ticket, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        book_button.grid(row=0, column=0, padx=10)
        book_button.bind("<Enter>", lambda e: book_button.config(bg="#45a049"))
        book_button.bind("<Leave>", lambda e: book_button.config(bg="#4CAF50"))

        view_button = tk.Button(button_frame, text="View Reservations", command=self.view_reservations, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        view_button.grid(row=0, column=1, padx=10)
        view_button.bind("<Enter>", lambda e: view_button.config(bg="#1e88e5"))
        view_button.bind("<Leave>", lambda e: view_button.config(bg="#2196F3"))

        # Seat Display Frame
        self.seat_frame = tk.Frame(self.master, bg="#e0f7fa")
        self.seat_frame.pack(pady=20)

        # Combined Seats Box
        self.seat_box = tk.LabelFrame(self.seat_frame, text="Seats Availability", font=("Arial", 12), bg="#b2dfdb", fg="black")
        self.seat_box.pack(padx=10, pady=10)

        self.seat_label = tk.Label(self.seat_box, text="", font=("Arial", 12), bg="#b2dfdb")
        self.seat_label.pack(padx=10, pady=10)

        self.update_seat_display()

    def update_seat_display(self, *args):
        bus_name = self.bus_var.get()
        seat_status = [f"Seat {seat}: {'Reserved by ' + name if name else 'Available'}" for seat, name in self.buses[bus_name].items()]
        
        self.seat_var.set("")
        
        menu = self.seat_menu["menu"]
        menu.delete(0, "end")
        
        available_seats = [str(seat) for seat, name in self.buses[bus_name].items() if name is None]
        
        for seat in available_seats:
            menu.add_command(label=seat, command=lambda value=seat: self.seat_var.set(value))

        self.seat_label.config(text="\n".join(seat_status))

    def book_ticket(self):
        bus_name = self.bus_var.get()
        seat_number = self.seat_var.get()
        name = self.name_entry.get()

        if bus_name and seat_number and name:
            if self.buses[bus_name][int(seat_number)] is None:
                self.buses[bus_name][int(seat_number)] = name
                messagebox.showinfo("Success", f"Ticket booked for {name} on {bus_name}, Seat {seat_number}!")
                self.name_entry.delete(0, tk.END)  # Clear the name entry
                self.update_seat_display()
            else:
                messagebox.showerror("Error", "Seat already reserved. Please select another seat.")
        else:
            messagebox.showerror("Error", "Please select a bus, seat, and enter your name.")

    def view_reservations(self):
        reservations = ""
        for bus, seats in self.buses.items():
            reserved = [f"Seat {seat}: {name}" for seat, name in seats.items() if name is not None]
            reservations += f"{bus}: {', '.join(reserved) if reserved else 'No reservations'}\n"
        
        if not reservations.strip():
            reservations = "No reservations made yet."
        
        messagebox.showinfo("Reservations", reservations)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusReservationSystem(root)
    root.mainloop()
