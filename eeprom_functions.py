# eeprom_functions.py



import serial
import threading
import time
import ASCII_functions as ASCII

# 
# GLOBALS
# 
targetAddress = 50
readData = ""
readDataReady = 0
numData = 0 

returnArray=[]

# Global variable to hold the serial connection
ser = None

def read(address, num_bytes):
    """
    Read 'num_bytes' from 'address' in EEPROM.

    """
    global readData
    # readDataReady is set to 1 by the read_from_serial function, which is called when UART message is received
    global readDataReady
    # need address copy to iterate as we read more bytes
    addressCopy = address
    # array for storing read data
    global returnArray
    returnArray = []
    # counter for number of bytes to read
    num_bytes_counter = 0
    # for tracking number of times readDataReady has been polled
    poll_counter = 0

    ## Tell read function number of expected bytes
    global numData

    while num_bytes_counter < num_bytes:
        # check number of bytes to read, tell set global for read function
        if(num_bytes-num_bytes_counter)>8:
            myNumBytes = 8
        else:
            myNumBytes = num_bytes-num_bytes_counter
        numData = myNumBytes*2
        # format address as 4 character string
        addrStr = hex(addressCopy)[2:]
        while len(addrStr)<4:
            addrStr = "0"+addrStr
        # print(addrStr)

        # This function will send the UART message indicating how many bytes to read from I2C target
        send_data("Read",addrStr,str(myNumBytes))

        time.sleep(.25)

        num_bytes_counter = num_bytes_counter + 8
        addressCopy = addressCopy + myNumBytes
        # readData = ""
    # print(returnArray)
    time.sleep(.5)
    return returnArray

def write(address, data):
    """
    Write 'data' (a list of bytes) to the EEPROM starting from 'address'.
    """

    # print("ADDRESS")
    # print(address)
    # print("DATA")
    # print(data)

    # format address as 4 character string
    addrStr = hex(address)[2:]
    while len(addrStr)<4:
        addrStr = "0"+addrStr

    # format data as 2 character string
    dataStr = hex(data[0])[2:]
    while len(dataStr)<2:
        dataStr = "0"+dataStr

    send_data("Write",addrStr,dataStr)
    
    # # Simulate writing to EEPROM memory (here it's just a list)
    # eeprom_memory = [0x00] * 1024  # 1024 bytes of EEPROM memory
    # for i, byte in enumerate(data):
    #     eeprom_memory[address + i] = byte
    # # Return success message for now
    return "Write Successful"



# Function to open the serial connection
def open_serial_connection():
    global ser
    try:
        # Get selected baud rate from the dropdown
        baud_rate = "9600"
        # Open the serial port with the selected baud rate
        ser = serial.Serial(port="COM4", baudrate=int(baud_rate), timeout=.01)
        if ser.is_open:
            # messagebox.showinfo("Success", f"Serial port opened successfully at {baud_rate} baud!")
            # Start a new thread to read data from serial port
            read_thread = threading.Thread(target=read_from_serial, args=(ser,))
            read_thread.daemon = True
            read_thread.start()
            print("Opened serial port")
    except Exception as e:
        print("Error", f"Failed to open serial port: {e}")



# Function to read data from the serial port OG
def read_from_serial(ser):
    while True:
        if ser.in_waiting > 0:
            # Read the serial data
            data = ASCII.HEX_to_ASCII(ser.readline().decode('utf-8'))
            # data = ser.readline().decode('utf-8')#.strip()
            if data:
                # assign data to global variable readData, then toggle readDataReady which is polled by read function
                global readData
                global readDataReady
                global returnArray
                readData = readData + data
                # check to see if received expected number of bytes
                if len(readData) == 2:
                    counter = 0
                    while counter < len(readData):
                        returnArray.append(int(readData[counter:counter+2],16))
                        counter = counter + 2
                    readData = ""
        time.sleep(.01)


# Function to send data to the serial port
def send_data(command, dataAddress, sendData):
    if ser and ser.is_open:
        ##
        ## calculate and format UART message to send 
        ##

        ##
        ## Get Read or Write
        ##

        command_string = command
        if command_string == "Read":
            command_string = "ff"
        else:
            command_string = "00"
        if command_string == "ff":
            message = ASCII.ASCII_to_HEX(command_string + str(targetAddress) + dataAddress + "0" + sendData) + 'Z'  # using ASCII 'Z' to mark end of message to FPGA 
        else:
            message = ASCII.ASCII_to_HEX(command_string + str(targetAddress) + dataAddress + sendData) + 'Z'  # using ASCII 'Z' to mark end of message to FPGA
        if message:
            # Send the message through the serial port
            ser.write(message.encode('utf-8'))
        else:
            print("Input Error", "Please enter a message to send.")
    else:
        print("Serial Error", "Serial port is not open.")


# Function to close the serial connection
def close_serial_connection():
    global ser
    if ser and ser.is_open:
        ser.close()
        print("Closed", "Serial port closed successfully!")
    else:
        print("Error", "No open serial connection to close.")
