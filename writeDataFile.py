import csv
import eeprom_functions as eeprom
import time
import argparse 

def parse_csv_and_send(file_path: str):
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        # Skip header if there is one, uncomment the next line if needed
        # next(csv_reader)

        # Loop through the rows in the CSV and call send_data for each set of 8 rows
        rowCounter = 0
        combinedRows = ""
        address = 0  # keep track of data address
        for row in csv_reader:
            # Join the row as a string (comma-separated values)
            row_string = ','.join(row)
            while len(row_string)<2:
                row_string = "0"+row_string
            combinedRows = combinedRows + row_string
            rowCounter = rowCounter + 1 

            # Write data in 8-byte chunks
            if rowCounter == 8:
                addrStr = hex(address)[2:]
                while len(addrStr)<4:
                    addrStr = "0"+addrStr
                # Call the send_data function with the row string
                # print(combinedRows)
                eeprom.send_data("Write",addrStr,combinedRows.lower())
                # print(address)
                address = address + 8
                combinedRows = ""
                rowCounter = 0
                time.sleep(.1)

# Example usage
eeprom.open_serial_connection()
time.sleep(.5)
parser = argparse.ArgumentParser(description="Parse a CSV file and send each row to send_data function.")
parser.add_argument("csv_file", help="The path to the CSV file to be processed")

args = parser.parse_args()

# Call the function with the file path argument
parse_csv_and_send(args.csv_file)
# file_path = 'testWriteData.csv'  # Replace with your CSV file path
# parse_csv_and_send(file_path)
#eeprom.close_serial_connection()
