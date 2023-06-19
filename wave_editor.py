######################################################################
# FILE: wave_editor.py
# EXERCISE: intro2cs2 ex6 2021
# DESCRIPTION: an editor for .wav files (see full description of all
# functions in description.txt)
#####################################################################


import wave_helper as wh
import math
import os


WELCOME = "Welcome to Wave Editor!\n"
MAIN_MENU = "What to do:\n" \
            "1. Modify a .wav file\n" \
            "2. Compose a melody\n" \
            "3. Exit\n " \
            "Enter the number of the option to proceed: "
MODIFY_CHOICE = "1"
COMPOSE_CHOICE = "2"
EXIT = "3"
EXIT_MESSAGE = "Closing the program... Goodbye!\n"
MAIN_MENU_ERROR = "You entered an invalid option. " \
                  "Please enter one of the option numbers."
FILE_REQUEST = "Enter the name of the file you want to modify: "
FILE_ERROR_MESSAGE = "The file is not found or invalid.\n"
MODIFY_MENU = "These are the modifications you can do:\n" \
              "1. Reverse\n" \
              "2. Audio denial\n" \
              "3. Increase playback speed\n" \
              "4. Decrease playback speed\n" \
              "5. Increase volume\n" \
              "6. Decrease volume\n" \
              "7. Low pass filter\n" \
              "8. Go to the end menu\n" \
              "Please pick a single option:"
MODIFY_MENU_ERROR = "You entered an invalid option." \
                    "Please enter one of the option numbers."
MODIFY_MENU_OPTIONS = ['1', '2', '3', '4', '5', '6', '7', '8']
REVERSED = "The file was successfully reversed.\n"
AUDIO_DENIAL = "The file successfully passed audio denial.\n"
SPEED_UP = "The file was successfully sped up.\n"
SLOW_DOWN = "The file was successfully slowed down.\n"
VOLUME_UP = "The volume was successfully increased.\n"
VOLUME_DOWN = "The volume was successfully decreased.\n"
LOW_PASS_FILTER = "The file successfully passed low pass filter.\n"
SAVE_MESSAGE = "Please enter the file name: "
SAVED_NAME_MESSAGE = "The file is successfully saved under the name: "
SAVE_ERROR = "The was an error while saving a file.\n"
COMPOSING_FILE = "Write the name of .txt file for composing: "
COMPOSING_ERROR = "File is invalid or doesn't exist."
MAX_VALUE = 32767
MIN_VALUE = -32768
VOLUME_CONST = 1.2
SAMPLE_RATE = 2000
FREQ_DICT = {"A": 440, "B": 494, "C": 523, "D": 587, "E": 659, "F": 698, "G": 784, "Q": 0}


def check_validity_mod():
    """
        This function receives input from user and checks the file
        with the help of function from wave_helper.py. If file is not
        valid - user is asked again for new file name. If input file exists
        function opens modify_file menu.
    """
    file = input(FILE_REQUEST)
    if wh.load_wave(file) == -1:
        print(FILE_ERROR_MESSAGE)
        main()
    else:
        rate, data = wh.load_wave(file)
        modify_file(rate, data)


def save_file(rate, data, filename):
    """
     Saves the file with the given values of rate and data
     using save_wave function from wave_helper.py
     :param rate: sample_rate
     :param data: audio_data
     :param filename: name of the file
     """
    if wh.save_wave(rate, data, filename) == -1:
        print(SAVE_ERROR)
    else:
        print(SAVED_NAME_MESSAGE + filename + "!")
    main()


def modify_file(rate, data):
    """
    Receives input from user for the MODIFY_MENU options.
    Each choice leads to new function. If the choice is
    not specified by the function - error message is raised
    and MODIFY_MENU is opened again.
    :param rate: sample_rate
    :param data: audio_data
    """
    modify_menu = input(MODIFY_MENU)
    if modify_menu == "1":
        data = reverse_lst(data)
        print(REVERSED)
        modify_file(rate, data)
    elif modify_menu == "2":
        data = audio_denial(data)
        print(AUDIO_DENIAL)
        modify_file(rate, data)
    elif modify_menu == "3":
        data = speed_up(data)
        print(SPEED_UP)
        modify_file(rate, data)
    elif modify_menu == "4":
        data = slow_down(data)
        print(SLOW_DOWN)
        modify_file(rate, data)
    elif modify_menu == "5":
        data = volume_up(data)
        print(VOLUME_UP)
        modify_file(rate, data)
    elif modify_menu == "6":
        data = volume_down(data)
        print(VOLUME_DOWN)
        modify_file(rate, data)
    elif modify_menu == "7":
        print(LOW_PASS_FILTER)
        data = low_pass_filter(data)
        modify_file(rate, data)
    if modify_menu == "8":
        filename = input(SAVE_MESSAGE)
        save_file(rate, data, filename)
    if modify_menu not in MODIFY_MENU_OPTIONS:
        print(MODIFY_MENU_ERROR)
        modify_file(rate, data)


def reverse_lst(lst):
    """
    Receives list of data and returns a reversed list.
    :param: lst
    :return: reversed list
    """
    reversed_lst = lst[::-1]
    return reversed_lst


def audio_denial(lst):
    """
    Receives list of data and returns list of lists where
    each parameter in inner list is multiplied by -1.
    :param: lst
    :return: audio_denial_lst
    """
    audio_denial_lst = []
    for pair in lst:
        inner_lst = []
        for i in pair:
            i = int(-i)
            if i < MIN_VALUE:
                i = MIN_VALUE
            if i > MAX_VALUE:
                i = MAX_VALUE
            inner_lst.append(i)
        audio_denial_lst.append(inner_lst)
    return audio_denial_lst


def speed_up(lst):
    """
    Receives list of data and returns list of lists, where
    all inner lists are imported from lst only if they were even.
    :param lst: data_list
    :return: speed_up_lst
    """
    speed_up_lst = []
    for i in range(len(lst)):
        if i % 2 == 0:
            speed_up_lst.append(lst[i])
    return speed_up_lst


def slow_down(lst):
    """
    Receives data list of lists, which is modified: between
    each pair of inner lists there is a new inner list that is
    mean of the previous and next one.
    :param: lst
    :return: lst
    """
    for i in range(len(lst) - 1, 0, -1):
        avg1 = int((lst[i][0] + lst[i - 1][0]) / 2)
        avg2 = int((lst[i][1] + lst[i - 1][1]) / 2)
        avg = [avg1, avg2]
        lst.insert(i, avg)
    return lst


def volume_up(lst):
    """
    Receives data list of lists and returns new list
    of list, where each member is multiplied by 1,2.
    :param: lst
    :return: volume_up_lst
    """
    volume_up_lst = []
    for inner_lst in lst:
        inner_mod = []
        for elem in inner_lst:
            elem = int(elem * VOLUME_CONST)
            if elem < MIN_VALUE:
                elem = MIN_VALUE
            if elem > MAX_VALUE:
                elem = MAX_VALUE
            inner_mod.append(elem)
        volume_up_lst.append(inner_mod)
    return volume_up_lst


def volume_down(lst):
    """
    Receives data list of lists and returns new list
    of list, where each member is divided by 1,2.
    :param: lst
    :return: volume_down_lst
    """
    volume_down_lst = []
    for inner_lst in lst:
        inner_mod = []
        for elem in inner_lst:
            elem = int(elem / VOLUME_CONST)
            if elem < MIN_VALUE:
                elem = MIN_VALUE
            if elem > MAX_VALUE:
                elem = MAX_VALUE
            inner_mod.append(elem)
        volume_down_lst.append(inner_mod)
    return volume_down_lst


def low_pass_filter(lst):
    """
    Receives list of data and returns modified list of
    lists, where each inner list is the result of average
    of the list itself and two lists, that are located before and
    after it.
    :param: lst
    :return: low_pass_filter_lst
    """
    low_pass_filter_lst = []
    for i in range(len(lst)):
        if i == 0:
            avg1 = int((lst[i][0] + lst[i + 1][0]) / 2)
            avg2 = int((lst[i][1] + lst[i + 1][1]) / 2)
            avg = [avg1, avg2]
            low_pass_filter_lst.append(avg)
        elif i == len(lst) - 1:
            avg1 = int((lst[i][0] + lst[i - 1][0]) / 2)
            avg2 = int((lst[i][1] + lst[i - 1][1]) / 2)
            avg = [avg1, avg2]
            low_pass_filter_lst.append(avg)
        else:
            avg1 = int((lst[i - 1][0] + lst[i][0] + lst[i + 1][0]) / 3)
            avg2 = int((lst[i - 1][1] + lst[i][1] + lst[i + 1][1]) / 3)
            avg = [avg1, avg2]
            low_pass_filter_lst.append(avg)
    return low_pass_filter_lst


def read_file(filename):
    """
    Receives filename of the text file that is used for
    composing. Opens the file and reads it, adding
    whitespaces in between.
    :param: filename
    :return: lst_of_instr
    """
    with open(filename, "r") as file:
        lst_of_instr = file.read().split()
    return lst_of_instr


def compose_melody():
    """
    Asks user for text file with notes and time intervals checks,
    if file exists. If not - error message is raised and user is asked
    again to write the name. If file exists - function reads it and
    creates new data list that is used to create new audio as a result of
    composing. After that save_edit_menu is called and new .wav file is saved.
    """
    data_lst = []
    filename = input(COMPOSING_FILE)
    while os.path.isfile(filename) is False:
        print(COMPOSING_ERROR)
        filename = input(COMPOSING_FILE)
    lst_of_instr = read_file(filename)
    for i in range(0, len(lst_of_instr), 2):
        freq = FREQ_DICT[lst_of_instr[i]]
        time = int(lst_of_instr[i+1])
        if freq == 0:
            for n in range(time * 125):
                data_lst.append([0, 0])
        else:
            for n in range(time * 125):
                sample = SAMPLE_RATE / freq
                data = int(MAX_VALUE * math.sin(math.pi * 2 * (n / sample)))
                data_lst.append([data, data])
    modify_file(SAMPLE_RATE, data_lst)


def main():
    """
    Main function that activates relevant functions according to
    users' input choice from MAIN_MENU options. Prints MAIN_MENU_ERROR
    if users' input is not acceptable.
    """
    menu_choice = input(MAIN_MENU)
    if menu_choice == MODIFY_CHOICE:
        check_validity_mod()
    elif menu_choice == COMPOSE_CHOICE:
        compose_melody()
    elif menu_choice == EXIT:
        print(EXIT_MESSAGE)
    else:
        print(MAIN_MENU_ERROR)
        main()


if __name__ == "__main__":
    print(WELCOME)
    main()
