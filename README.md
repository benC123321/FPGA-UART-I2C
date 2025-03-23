There are two ways to use the scripts in this repo:
1. GUI to read/write I2C target data. This is done by running eeprom_gui.py
2. Write the data from a CSV file to the I2C target. This is done by running **python writeDataFile.py path_to_your_file.csv**
    CSV file is expected to have exactly one byte per row

These scripts are meant to be used along with the Basys 3 project shown in this repo:
