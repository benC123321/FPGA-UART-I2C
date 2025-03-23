import tkinter as tk
from tkinter import messagebox
import eeprom_functions as eeprom

class EEPROM_GUI:
    def __init__(self, root):
        eeprom.open_serial_connection()
        self.root = root
        self.root.title("EEPROM Memory Viewer")

        # Set the window size and allow resizing
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Create a frame to hold the widgets in a grid
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Address label and entry field
        self.address_label = tk.Label(self.frame, text="Address:")
        self.address_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.address_entry = tk.Entry(self.frame)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Number of bytes label and entry field
        self.num_bytes_label = tk.Label(self.frame, text="Number of Bytes:")
        self.num_bytes_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.num_bytes_entry = tk.Entry(self.frame)
        self.num_bytes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Load Memory button
        self.load_button = tk.Button(self.frame, text="Load Memory", command=self.load_memory)
        self.load_button.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        # Create a Listbox for displaying memory
        self.memory_listbox = tk.Listbox(self.frame, height=20, width=50)
        self.memory_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Bind the listbox to allow editing of bytes
        self.memory_listbox.bind('<Double-1>', self.edit_byte)

        # Status label
        self.status_label = tk.Label(self.frame, text="Status: Ready")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Continuous Refresh Checkbox
        self.continuous_refresh_var = tk.BooleanVar()
        self.continuous_refresh_checkbox = tk.Checkbutton(
            self.frame, text="Continuous Refresh", variable=self.continuous_refresh_var, command=self.toggle_continuous_refresh
        )
        self.continuous_refresh_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Configure the row and column weights to make the widgets expand appropriately
        self.frame.grid_rowconfigure(3, weight=1)  # The row containing the Listbox should expand
        self.frame.grid_columnconfigure(1, weight=1)  # The column containing entry fields should expand

        # Variables to control refresh timing
        self.refresh_interval = 500  # Time interval in ms (500ms = 2 times per second)
        self.refreshing = False

    def load_memory(self):
        """Load memory from EEPROM and display it in the listbox"""
        try:
            # Get the address and number of bytes from the user
            address = int(self.address_entry.get(), 16)
            num_bytes = int(self.num_bytes_entry.get())

            # Read data from EEPROM
            # print("HELLO 0")
            memory = eeprom.read(address, num_bytes)
            # print(memory)

            # Clear the listbox and insert new data
            self.memory_listbox.delete(0, tk.END)
            for i, byte in enumerate(memory):
                # Display the address and the byte value in the listbox
                self.memory_listbox.insert(tk.END, f'{address + i:04X}: {byte:02X}')
            
            self.status_label.config(text="Status: Memory Loaded")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def toggle_continuous_refresh(self):
        """Start or stop continuous refresh based on checkbox state"""
        if self.continuous_refresh_var.get():
            # Start continuous refresh
            self.refreshing = True
            self.schedule_refresh()
        else:
            # Stop continuous refresh
            self.refreshing = False

    def schedule_refresh(self):
        """Schedule the next refresh if continuous refresh is enabled"""
        if self.refreshing:
            self.load_memory()  # Refresh the memory
            self.root.after(self.refresh_interval, self.schedule_refresh)  # Schedule next refresh

    def edit_byte(self, event):
        """Edit a byte when double-clicked"""
        # Get the index of the selected byte in the listbox
        index = self.memory_listbox.curselection()
        if index:
            index = index[0]
            current_entry = self.memory_listbox.get(index)

            # Parse the address and current byte value from the listbox entry
            address_str, current_value_str = current_entry.split(": ")
            current_address = int(address_str, 16)
            current_value = int(current_value_str, 16)

            # Open a new window to edit the byte
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Byte")
            edit_label = tk.Label(edit_window, text="Enter new byte (00-FF):")
            edit_label.pack(padx=10, pady=5)

            new_value_entry = tk.Entry(edit_window)
            new_value_entry.insert(0, current_value_str)
            new_value_entry.pack(padx=10, pady=5)

            def save_edit():
                try:
                    new_value = int(new_value_entry.get(), 16)
                    if 0 <= new_value <= 255:
                        # Update the listbox with the new byte value
                        self.memory_listbox.delete(index)
                        self.memory_listbox.insert(index, f'{current_address:04X}: {new_value:02X}')
                        # Call the write function to update the EEPROM
                        eeprom.write(current_address, [new_value])
                        edit_window.destroy()
                        self.status_label.config(text="Status: Write Successful")
                    else:
                        messagebox.showerror("Invalid Value", "Enter a value between 00 and FF.")
                except ValueError:
                    messagebox.showerror("Invalid Value", "Please enter a valid hexadecimal value.")

            save_button = tk.Button(edit_window, text="Save", command=save_edit)
            save_button.pack(padx=10, pady=5)

def main():
    root = tk.Tk()
    app = EEPROM_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
