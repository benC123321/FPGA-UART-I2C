import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time

# Global variable to hold the serial connection
ser = None

WRITE_TO_OUTPUT_REGS="69"

data = ''

def ASCII_to_HEX(my_string):
    char_list = [chr(0)]*(len(my_string)+(len(my_string)%2))
    for i in range(len(my_string)):
        if my_string[i] == '0':
            char_list[i] = chr(0)
        elif my_string[i] == '1':
            char_list[i] = chr(1)
        elif my_string[i] == '2':
            char_list[i] = chr(2)
        elif my_string[i] == '3':
            char_list[i] = chr(3)
        elif my_string[i] == '4':
            char_list[i] = chr(4)
        elif my_string[i] == '5':
            char_list[i] = chr(5)
        elif my_string[i] == '6':
            char_list[i] = chr(6)
        elif my_string[i] == '7':
            char_list[i] = chr(7)
        elif my_string[i] == '8':
            char_list[i] = chr(8)
        elif my_string[i] == '9':
            char_list[i] = chr(9)
        elif my_string[i] == 'a':
            char_list[i] = chr(10)
        elif my_string[i] == 'b':
            char_list[i] = chr(11)
        elif my_string[i] == 'c':
            char_list[i] = chr(12)
        elif my_string[i] == 'd':
            char_list[i] = chr(13)
        elif my_string[i] == 'e':
            char_list[i] = chr(14)
        elif my_string[i] == 'f':
            char_list[i] = chr(15)
        else:
            raise ValueError("Invalid input")
    new_string = "".join(char_list)
    return new_string

def HEX_to_ASCII(my_string):
    char_list = ['X']*(len(my_string))
    for i in range(len(my_string)):
        if my_string[i] == chr(0):
            char_list[i] = '0'
        elif my_string[i] == chr(1):
            char_list[i] = '1'
        elif my_string[i] == chr(2):
            char_list[i] = '2'
        elif my_string[i] == chr(3):
            char_list[i] = '3'
        elif my_string[i] == chr(4):
            char_list[i] = '4'
        elif my_string[i] == chr(5):
            char_list[i] = '5'
        elif my_string[i] == chr(6):
            char_list[i] = '6'
        elif my_string[i] == chr(7):
            char_list[i] = '7'
        elif my_string[i] == chr(8):
            char_list[i] = '8'
        elif my_string[i] == chr(9):
            char_list[i] = '9'
        elif my_string[i] == chr(10):
            char_list[i] = 'A'
        elif my_string[i] == chr(11):
            char_list[i] = 'B'
        elif my_string[i] == chr(12):
            char_list[i] = 'C'
        elif my_string[i] == chr(13):
            char_list[i] = 'D'
        elif my_string[i] == chr(14):
            char_list[i] = 'E'
        elif my_string[i] == chr(15):
            char_list[i] = 'F'
        elif my_string[i] == 'Z':
            char_list[i] = ''
            new_string = "".join(char_list)
            return new_string
        else:
            raise ValueError("Invalid input")
    new_string3 = "".join(char_list)
    return new_string3

# Function to open the serial connection
def open_serial_connection():
    global ser
    try:
        # Get selected baud rate from the dropdown
        baud_rate = baud_rate_combo.get()
        
        # Open the serial port with the selected baud rate
        ser = serial.Serial(port=serial_port.get(), baudrate=int(baud_rate), timeout=1)
        if ser.is_open:
            messagebox.showinfo("Success", f"Serial port opened successfully at {baud_rate} baud!")
            # Start a new thread to read data from serial port
            read_thread = threading.Thread(target=read_from_serial, args=(ser,))
            read_thread.daemon = True
            read_thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open serial port: {e}")

# # Function to read data from the serial port
# def read_from_serial(ser):
#     data = ''
#     while True:
#         if ser.in_waiting > 0:
#             # Read the serial data
#             data = data + ser.readline().decode('utf-8')#.strip()
#             if data.find('Z')!=-1:
#                 # Display the data in the text box
#                 data = HEX_to_ASCII(data)
#                 text_box.insert(tk.END, "Received: " + data + '\n')
#                 text_box.yview(tk.END)  # Scroll to the latest data
#                 data = ''
#         time.sleep(0.1)

# Function to read data from the serial port OG
def read_from_serial(ser):
    while True:
        if ser.in_waiting > 0:
            # Read the serial data
            data = HEX_to_ASCII(ser.readline().decode('utf-8'))
            # data = ser.readline().decode('utf-8')#.strip()
            if data:
                # Display the data in the text box
                text_box.insert(tk.END, 'Received: ' + data + '\n')
                text_box.yview(tk.END)  # Scroll to the latest data
        time.sleep(0.1)

# Function to send data to the serial port
def send_data():
    if ser and ser.is_open:
        ##
        ## calculate and format UART message to send 
        ##

        ##
        ## Get Read or Write
        ##

        command_string = command_combo.get()
        if command_string == "Read":
            command_string = "ff"
        else:
            command_string = "00"

        ##
        ## Calculate output voltage message
        ##
        # number = (float(send_entry.get())/3300)*4095
        # number = int(number)
        # number = hex(number)
        # numberString = number[2:]     //address is 0x60 // start write message with 69
        message = ASCII_to_HEX(command_string + send_address_entry.get()+send_entry.get()) + 'Z'  # using ASCII 'Z' to mark end of message to FPGA 
        if message:
            # Send the message through the serial port
            ser.write(message.encode('utf-8'))
            text_box.insert(tk.END, "Sent: " + send_entry.get() + 'mV\n')
            text_box.yview(tk.END)  # Scroll to the latest data
            send_entry.delete(0, tk.END)  # Clear the input field after sending
        else:
            messagebox.showwarning("Input Error", "Please enter a message to send.")
    else:
        messagebox.showerror("Serial Error", "Serial port is not open.")

# Function to close the serial connection
def close_serial_connection():
    global ser
    if ser and ser.is_open:
        ser.close()
        messagebox.showinfo("Closed", "Serial port closed successfully!")
    else:
        messagebox.showerror("Error", "No open serial connection to close.")

# Set up the main window
root = tk.Tk()
root.title("Serial Port Reader and Writer")

# Serial port selection
serial_port_label = tk.Label(root, text="Select Serial Port:")
serial_port_label.pack(pady=5)

# Dropdown for serial ports
available_ports = [f"COM{i}" for i in range(1, 21)]  # Adjust this for your system
serial_port = ttk.Combobox(root, values=available_ports)
serial_port.set(available_ports[0])  # Default to first port
serial_port.pack(pady=5)

# Baud rate selection
baud_rate_label = tk.Label(root, text="Select Baud Rate:")
baud_rate_label.pack(pady=5)

# Dropdown for baud rates
baud_rates = ["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
baud_rate_combo = ttk.Combobox(root, values=baud_rates)
baud_rate_combo.set("9600")  # Default to 9600
baud_rate_combo.pack(pady=5)

# Button to open the serial port
open_button = tk.Button(root, text="Open Serial Port", command=open_serial_connection)
open_button.pack(pady=5)

# Text box to display incoming data
text_box = tk.Text(root, height=15, width=50, wrap=tk.WORD)
text_box.pack(padx=10, pady=10)

# Entry widget to input data to send over UART
send_entry_label = tk.Label(root, text="Output Voltage(maximum 3300 in mV):")
send_entry_label.pack(padx=5)
send_entry = tk.Entry(root, width=40)
send_entry.pack(padx=5)

# Entry widget to input I2C Address
send_address_entry_label = tk.Label(root, text="Address of target in HEX:")
send_address_entry_label.pack(padx=5)
send_address_entry = tk.Entry(root, width=40)
send_address_entry.pack(padx=5)

# Entry widget to input I2C Address
bytes_num_label = tk.Label(root, text="Number of bytes to read in HEX (ignored during write):")
bytes_num_label.pack(padx=5)
bytes_num = tk.Entry(root, width=40)
bytes_num.pack(padx=5)

# Read/Write Selection
command_label = tk.Label(root, text="Select Read/Write:")
command_label.pack(pady=5)

# Dropdown for read/write
commands = ["Read","Write"]
command_combo = ttk.Combobox(root, values=commands)
command_combo.set("Read")  # Default to 9600
command_combo.pack(pady=5)

# Button to send data over the serial port
send_button = tk.Button(root, text="Send", command=send_data)
send_button.pack(pady=5)

# Button to close the serial connection
close_button = tk.Button(root, text="Close Serial Port", command=close_serial_connection)
close_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
