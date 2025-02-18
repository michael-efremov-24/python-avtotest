import sys
import requests
import time
def Proverka_adresov(String):
    if String[0:8] != "https://":
        print("Некорректные входные данные!")
        return False
    else:
        if String[8:].find(".") == -1:
            print("Некорректные входные данные!")
            return False
        j = 8
        while String[j] != ".":
            if ord(String[j]) == 45 or 48 <= ord(String[j]) <= 57 or 65 <= ord(String[j]) <= 90 or 97 <= ord(String[j]) <= 122:
                j += 1
            else:
                print("Некорректные входные данные!")
                return False
        for t in range(j + 1, len(String)):
            if ord(String[t]) == 45 or 48 <= ord(String[t]) <= 57 or 65 <= ord(String[t]) <= 90 or 97 <= ord(String[t]) <= 122:
                t += 1
            else:
                print("Некорректные входные данные!")
                return False
    return True
def Proverka_probelov(String, list_of_keys):
    for j in list_of_keys:
        if j != -1:
            if (String[j + 2] == " " and String[j + 3] == " ") or String[j + 2] != " ":
                print("Отсутствуют пробелы или есть лишние.")
                return False
    return True
print("Введите текст...")
Input_string = input()
Index_key_H = Input_string.find("-H")
Index_key_C = Input_string.find("-C")
Index_key_F = Input_string.find("-F")
Index_key_O = Input_string.find("-O")
if not Proverka_probelov(Input_string, [Index_key_H, Index_key_F, Index_key_C, Index_key_O]):
    sys.exit()
if Index_key_F != -1 and Index_key_H != -1:
    print("Некорректные данные, содержатся и ключ -F, и ключ -H.")
    sys.exit()
if Index_key_F == -1 and Index_key_H == -1:
    print("Некорректные данные, отсутствуют ключи -F или -H.")
    sys.exit()
if Index_key_H != -1:
    Short_string_H = Input_string[Index_key_H + 3:]
    if Short_string_H.find(" ") != -1:
        Hosts_list_string = Short_string_H[:Short_string_H.find(" ")]
        Hosts_list = Hosts_list_string.split(",")
    else:
        Hosts_list = Short_string_H.split(",")
    for host in Hosts_list:
        if not Proverka_adresov(host): sys.exit()
if Index_key_F != -1:
    Short_string_F = Input_string[Index_key_F + 3:]
    if Short_string_F.find(" ") != -1: File_name = Short_string_F[:Short_string_F.find(" ")]
    else: File_name = Short_string_F
    try:
        File = open(File_name, "r")
    except (FileNotFoundError, OSError):
        print("Файл не найден!")
        sys.exit()
    else:
        Hosts_list = File.readlines()
        Hosts_list = [line.rstrip("\n") for line in Hosts_list]
        File.close()
    for host in Hosts_list:
        if not Proverka_adresov(host): sys.exit()
if Index_key_C == -1: C = 1
else:
    Short_string_C = Input_string[Index_key_C + 3:]
    if Short_string_C.find(" ") != -1:
        C_str = Short_string_C[:Short_string_C.find(" ")]
        if C_str.isdigit(): C = int(C_str)
        else:
            print("Значение ключа -C не является натуральным числом!")
            sys.exit()
    else:
        if Short_string_C.isdigit(): C = int(Short_string_C)
        else:
            print("Значение ключа -C не является натуральным числом!")
            sys.exit()
if Index_key_O == -1:
    for host in Hosts_list:
        print("a. ", host)
        Success = 0
        Failed = 0
        Errors = 0
        Average_time = 0
        Time_max = 0
        Time_min = 0
        for i in range (C):
            time_start = time.perf_counter()
            try:
                response = requests.get(host)
            except Exception:
                print("Ошибка при выполнении запроса!")
                sys.exit()
            time_end = time.perf_counter()
            request_time = time_end - time_start
            if i == 0: Time_min = request_time
            elif request_time < Time_min: Time_min = request_time
            if request_time > Time_max: Time_max = request_time
            Average_time += request_time
            if response.ok: Success += 1
            if response.status_code == 400 or response.status_code == 500: Failed += 1
            if response.status_code == 503: Errors += 1
        print("b. Success = ", Success)
        print("c. Failed = ", Failed)
        print("d. Errors = ", Errors)
        print("e. Min = ", Time_min)
        print("f. Max = ", Time_max)
        print("g. Avg = ", Average_time/C)
        print("\n")
else:
    Short_string_O = Input_string[Index_key_O + 3:]
    if Short_string_O.find(" ") != -1:
        Output_file_name = Short_string_O[:Short_string_O.find(" ")]
    else: Output_file_name = Short_string_O
    Output_file = open(Output_file_name, "w")
    for host in Hosts_list:
        Output_file.write("a. ")
        Output_file.write(host)
        Output_file.write("\n")
        Success = 0
        Failed = 0
        Errors = 0
        Average_time = 0
        Time_max = 0
        Time_min = 0
        for i in range(C):
            time_start = time.perf_counter()
            try:
                response = requests.get(host)
            except Exception:
                Output_file.write("Ошибка при выполнении запроса!")
                sys.exit()
            time_end = time.perf_counter()
            request_time = time_end - time_start
            if i == 0:
                Time_min = request_time
            elif request_time < Time_min:
                Time_min = request_time
            if request_time > Time_max: Time_max = request_time
            Average_time += request_time
            if response.ok: Success += 1
            if response.status_code == 400 or response.status_code == 500: Failed += 1
            if response.status_code == 503: Errors += 1
        Output_file.write("b. Success = ")
        Output_file.write(str(Success))
        Output_file.write("\n")
        Output_file.write("c. Failed = ")
        Output_file.write(str(Failed))
        Output_file.write("\n")
        Output_file.write("d. Errors = ")
        Output_file.write(str(Errors))
        Output_file.write("\n")
        Output_file.write("e. Min = ")
        Output_file.write(str(Time_min))
        Output_file.write("\n")
        Output_file.write("f. Max = ")
        Output_file.write(str(Time_max))
        Output_file.write("\n")
        Output_file.write("g. Avg = ")
        Output_file.write(str(Average_time/C))
        Output_file.write("\n\n")
    Output_file.close()









