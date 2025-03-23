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