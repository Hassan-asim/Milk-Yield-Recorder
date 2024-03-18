import tkinter as tk
from tkinter import messagebox
import re

# Initialize the main application window
root = tk.Tk()
root.title("Milk Yield Recorder")

# Define global data structures
cows = {}  # Dictionary to store cow ID and its yields
daily_milk = []  # List to store daily milk yield
herd_size = 0  # Variable to store the size of the herd

# Function to validate cow ID
def validate_cow_id(cow_id):
    return re.match(r'^\d{3}$', cow_id) is not None

# Function to set the herd size
def set_herd_size():
    global herd_size
    try:
        herd_size = int(herd_size_entry.get())
        if herd_size <= 0:
            raise ValueError("Herd size must be a positive integer.")
        herd_size_window.destroy()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        herd_size_entry.delete(0, tk.END)

# Function to record the yield
def record_yield():
    if len(cows) >= herd_size:
        messagebox.showerror("Error", "All cows in the herd have been recorded.")
        return
    cow_id = cow_id_entry.get()
    try:
        yield_amount = float(yield_entry.get())
        if not validate_cow_id(cow_id):
            raise ValueError("Invalid Cow ID. It must be a 3-digit number.")
        if cow_id not in cows:
            cows[cow_id] = []
        cows[cow_id].append(yield_amount)
        daily_milk.append(yield_amount)
        messagebox.showinfo("Success", f"Yield for cow {cow_id} recorded successfully.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    finally:
        cow_id_entry.delete(0, tk.END)
        yield_entry.delete(0, tk.END)

# Function to calculate statistics
def calculate_statistics():
    if not daily_milk:
        messagebox.showerror("Error", "No milk yield data recorded.")
        return
    total_milk = sum(daily_milk)
    average_yield = total_milk / herd_size
    messagebox.showinfo("Statistics", f"Total weekly volume: {round(total_milk)} litres\nAverage yield per cow: {round(average_yield)} litres")

# Function to identify the most and least productive cows
def identify_cows():
    if not cows:
        messagebox.showerror("Error", "No cows have been recorded.")
        return
    most_milk = max(cows, key=lambda k: sum(cows[k]))
    least_milk = [cow for cow, yields in cows.items() if len([y for y in yields if y < 12]) >= 4]
    messagebox.showinfo("Identification", f"Cow with most milk: {most_milk}\nCows with less than 12 litres on 4+ days: {', '.join(least_milk) if least_milk else 'None'}")

# Create UI elements for the main application
cow_id_label = tk.Label(root, text="Cow ID (3 digits):")
cow_id_label.grid(row=0, column=0)
cow_id_entry = tk.Entry(root)
cow_id_entry.grid(row=0, column=1)

yield_label = tk.Label(root, text="Yield (litres):")
yield_label.grid(row=1, column=0)
yield_entry = tk.Entry(root)
yield_entry.grid(row=1, column=1)

record_button = tk.Button(root, text="Record Yield", command=record_yield)
record_button.grid(row=2, column=0, columnspan=2)

calculate_button = tk.Button(root, text="Calculate Statistics", command=calculate_statistics)
calculate_button.grid(row=3, column=0, columnspan=2)

identify_button = tk.Button(root, text="Identify Cows", command=identify_cows)
identify_button.grid(row=4, column=0, columnspan=2)

# Create a new window to set the herd size
herd_size_window = tk.Toplevel(root)
herd_size_window.title("Set Herd Size")

herd_size_label = tk.Label(herd_size_window, text="Enter the size of the herd:")
herd_size_label.pack()

herd_size_entry = tk.Entry(herd_size_window)
herd_size_entry.pack()

herd_size_button = tk.Button(herd_size_window, text="Set", command=set_herd_size)
herd_size_button.pack()

# Run the application
root.mainloop()
