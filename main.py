import pickle
from datetime import time
from functools import reduce, partial
import random
import matplotlib as matplotlib
from tkinter import *
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from matplotlib.figure import Figure
import time
import matplotlib.pyplot as plt

def chooseFile():
    file_name = fd.askopenfilename()
    return file_name

def Graph1():
    global col_hash_list, col_text_list
    try:
        k = int(K.get())
        if (k > 128):
            text1.delete(1.0, END)
            text1.insert(1.0, "Максимальное количество бит коллизий хэша: 128")
        if (k < 1):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальное количество бит коллизий хэша: 1")
            k = 1
    except:
        text1.delete(1.0, END)
        text1.insert(1.0, "Введите количество бит k коллизий хэша: от 0 до 128")

    try:
        l = int(L.get())
        if (l < 0):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальная длина строки: 0")
            l = 0
    except:
        text1.delete(1.0, END)
        text1.insert(1.0, "Введите длину строки L в символах")

    k_v = k
    k_list = []
    n_list = []
    for i in range(1,k_v):
        k = i
        k_list.append(i)

        col_hash_list = []
        col_text_list = []
        TextHashGen(l)
        hash_equal = False
        j = 0
        match_hash_index = 0
        while hash_equal == False:
            TextHashGen(l)
            j += 1
            for i in range(0, len(col_hash_list) - 1):
                if (k_bitsOfHash(col_hash_list[i], k) == k_bitsOfHash(col_hash_list[j], k)):
                    hash_equal = True
                    match_hash_index = i
        l3.config(text="")
        n_list.append(len(col_text_list))


    plt.grid()  # включение отображение сетки
    plt.title("Поиск коллизий.\nЗависимость количества итераций от k")
    plt.xlabel("k")
    plt.ylabel("Количество итераций")
    plt.plot(k_list, n_list)
    plt.show()

def Graph2():
    global col_hash_list, col_text_list
    try:
        k = int(K.get())
        if (k > 128):
            text1.delete(1.0, END)
            text1.insert(1.0, "Максимальное количество бит коллизий хэша: 128")
        if (k < 1):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальное количество бит коллизий хэша: 1")
            k = 1
    except:
        text1.delete(1.0, END)
        text1.insert(1.0, "Введите количество бит k коллизий хэша: от 0 до 128")

    if (var.get() == False): # Генерируем хеш введеного сообщения
        String_1 = text1.get(1.0, END)
        String_1_b = text1.get(1.0, END).encode("utf-8")
        tmp, String_1_hesh = HeshCount(String_1_b[0:len(String_1_b)-1])
    if (var.get()): # Генерируем хеш выбранного файла
        file_name = chooseFile()
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                String_1 = file.read()
        except:
            with open(file_name, 'r', encoding="ANSI") as file:
                String_1 = file.read()
        with open(file_name, 'rb') as file:
            fb = file.read()
        tmp, String_1_hesh = HeshCount(fb)

    k_v = k
    k_list = []
    n_list = []
    for i in range(1,k_v):
        k = i
        k_list.append(i)

        col_text_list = []
        col_hash_list = []
        equal = False
        j = 0
        while equal == False:
            gen_len = random.randint(1, 153)
            TextHashGen(gen_len)
            if (k_bitsOfHash(col_hash_list[j], k) == k_bitsOfHash(String_1_hesh, k)):
                equal = True
                l3.config(text="")
            j += 1
        n_list.append(len(col_text_list))


    plt.grid()  # включение отображение сетки
    plt.title("Поиск прообраза заданной строки.\nЗависимость количества итераций от k")
    plt.xlabel("k")
    plt.ylabel("Количество итераций")
    plt.plot(k_list, n_list)
    plt.show()

def F(x,y,z):
    return x & y | ~x & z

def G(x,y,z):
    return x & y | x & z | y & z

def H(x,y,z):
    return x ^ y ^ z

def CircleStep(string,a):
    string_list = list(string)
    for i in range(a):
        first = string_list[0]
        string_list = string_list[1:]
        string_list.append(first)
    return ''.join(string_list)

def FirstRound(a,b,c,d,k,s,Words_list):
    Pre_a_bit = list("{:032b}".format(a + F(b,c,d) + int(Words_list[k],2)))
    while(len(Pre_a_bit) != 32):
        Pre_a_bit.pop(0)
    Pre_a_bit = ''.join(Pre_a_bit)
    return int(CircleStep(Pre_a_bit,s),2)

def SecondRound(a,b,c,d,k,s,Words_list):
    Pre_a_bit = list("{:032b}".format(a + G(b,c,d) + int(Words_list[k],2) + 0x5A827999))
    while (len(Pre_a_bit) != 32):
        Pre_a_bit.pop(0)
    Pre_a_bit = ''.join(Pre_a_bit)
    return int(CircleStep(Pre_a_bit,s),2)

def ThirdRound(a,b,c,d,k,s,Words_list):
    Pre_a_bit = list("{:032b}".format(a + H(b,c,d) + int(Words_list[k],2) + 0x6ED9EBA1))
    while (len(Pre_a_bit) != 32):
        Pre_a_bit.pop(0)
    Pre_a_bit = ''.join(Pre_a_bit)
    return int(CircleStep(Pre_a_bit,s),2)

def HeshCount(Message):
    Message_b_list = []
    for i in range(0, len(Message)):
        Message_b_list.append("{:08b}".format(Message[i]))
    Message_b = ''.join(Message_b_list)
    Message_len = len(Message_b)  # длина исходного сообщения в битах
    Message_b = Message_b + '1'
    Blocs = []

    for i in range(0, len(Message_b), 512):  # деление по блокам по 512 бит
        Blocs.append(Message_b[i:i + 512])
    while (len(Blocs[len(Blocs) - 1]) < 448):
        Blocs[len(Blocs) - 1] = Blocs[len(Blocs) - 1] + '0'
    if (len(Blocs[len(Blocs) - 1]) > 448):
        while (len(Blocs[len(Blocs) - 1]) < 512):
            Blocs[len(Blocs) - 1] = Blocs[len(Blocs) - 1] + '0'
        zeros_list = ['0' for i in range(448)]
        zeros = ''.join(zeros_list)
        Blocs.append(zeros)

    last_bits = "{:064b}".format(Message_len)
    first_part = list(last_bits)[0:32]
    second_part = list(last_bits)[32:64]

    a1 = ''.join(second_part[0:8])
    b1 = ''.join(second_part[8:16])
    c1 = ''.join(second_part[16:24])
    d1 = ''.join(second_part[24:32])
    second_part = d1 + c1 + b1 + a1

    a2 = ''.join(first_part[0:8])
    b2 = ''.join(first_part[8:16])
    c2 = ''.join(first_part[16:24])
    d2 = ''.join(first_part[24:32])
    first_part = d2 + c2 + b2 + a2

    Blocs[len(Blocs) - 1] = Blocs[len(Blocs) - 1] + second_part + first_part

    A = int('0x67452301', 16)
    B = int('0xefcdab89', 16)
    C = int('0x98badcfe', 16)
    D = int('0x10325476', 16)

    for i in Blocs:
        Words = []
        for j in range(0, len(i), 32):
            tmp = list(''.join(list(i)[j:j + 32]))
            a = ''.join(tmp[0:8])
            b = ''.join(tmp[8:16])
            c = ''.join(tmp[16:24])
            d = ''.join(tmp[24:32])
            Words.append(d + c + b + a)

        AA = A
        BB = B
        CC = C
        DD = D

        A = FirstRound(A, B, C, D, 0, 3, Words)
        D = FirstRound(D, A, B, C, 1, 7, Words)
        C = FirstRound(C, D, A, B, 2, 11, Words)
        B = FirstRound(B, C, D, A, 3, 19, Words)
        A = FirstRound(A, B, C, D, 4, 3, Words)
        D = FirstRound(D, A, B, C, 5, 7, Words)
        C = FirstRound(C, D, A, B, 6, 11, Words)
        B = FirstRound(B, C, D, A, 7, 19, Words)
        A = FirstRound(A, B, C, D, 8, 3, Words)
        D = FirstRound(D, A, B, C, 9, 7, Words)
        C = FirstRound(C, D, A, B, 10, 11, Words)
        B = FirstRound(B, C, D, A, 11, 19, Words)
        A = FirstRound(A, B, C, D, 12, 3, Words)
        D = FirstRound(D, A, B, C, 13, 7, Words)
        C = FirstRound(C, D, A, B, 14, 11, Words)
        B = FirstRound(B, C, D, A, 15, 19, Words)

        A = SecondRound(A, B, C, D, 0, 3, Words)
        D = SecondRound(D, A, B, C, 4, 5, Words)
        C = SecondRound(C, D, A, B, 8, 9, Words)
        B = SecondRound(B, C, D, A, 12, 13, Words)
        A = SecondRound(A, B, C, D, 1, 3, Words)
        D = SecondRound(D, A, B, C, 5, 5, Words)
        C = SecondRound(C, D, A, B, 9, 9, Words)
        B = SecondRound(B, C, D, A, 13, 13, Words)
        A = SecondRound(A, B, C, D, 2, 3, Words)
        D = SecondRound(D, A, B, C, 6, 5, Words)
        C = SecondRound(C, D, A, B, 10, 9, Words)
        B = SecondRound(B, C, D, A, 14, 13, Words)
        A = SecondRound(A, B, C, D, 3, 3, Words)
        D = SecondRound(D, A, B, C, 7, 5, Words)
        C = SecondRound(C, D, A, B, 11, 9, Words)
        B = SecondRound(B, C, D, A, 15, 13, Words)

        A = ThirdRound(A, B, C, D, 0, 3, Words)
        D = ThirdRound(D, A, B, C, 8, 9, Words)
        C = ThirdRound(C, D, A, B, 4, 11, Words)
        B = ThirdRound(B, C, D, A, 12, 15, Words)
        A = ThirdRound(A, B, C, D, 2, 3, Words)
        D = ThirdRound(D, A, B, C, 10, 9, Words)
        C = ThirdRound(C, D, A, B, 6, 11, Words)
        B = ThirdRound(B, C, D, A, 14, 15, Words)
        A = ThirdRound(A, B, C, D, 1, 3, Words)
        D = ThirdRound(D, A, B, C, 9, 9, Words)
        C = ThirdRound(C, D, A, B, 5, 11, Words)
        B = ThirdRound(B, C, D, A, 13, 15, Words)
        A = ThirdRound(A, B, C, D, 3, 3, Words)
        D = ThirdRound(D, A, B, C, 11, 9, Words)
        C = ThirdRound(C, D, A, B, 7, 11, Words)
        B = ThirdRound(B, C, D, A, 15, 15, Words)

        A = A + AA
        B = B + BB
        C = C + CC
        D = D + DD

        A_tmp = list("{:032b}".format(A))
        while (len(A_tmp) != 32):
            A_tmp.pop(0)
        A = int(''.join(A_tmp),2)

        B_tmp = list("{:032b}".format(B))
        while (len(B_tmp) != 32):
            B_tmp.pop(0)
        B = int(''.join(B_tmp), 2)

        C_tmp = list("{:032b}".format(C))
        while (len(C_tmp) != 32):
            C_tmp.pop(0)
        C = int(''.join(C_tmp), 2)

        D_tmp = list("{:032b}".format(D))
        while (len(D_tmp) != 32):
            D_tmp.pop(0)
        D = int(''.join(D_tmp), 2)

    A = list("{:032b}".format(A))
    a = ''.join(A[0:8])
    b = ''.join(A[8:16])
    c = ''.join(A[16:24])
    d = ''.join(A[24:32])
    A = int(''.join(d+c+b+a), 2)

    B = list("{:032b}".format(B))
    a = ''.join(B[0:8])
    b = ''.join(B[8:16])
    c = ''.join(B[16:24])
    d = ''.join(B[24:32])
    B = int(''.join(d + c + b + a), 2)

    C = list("{:032b}".format(C))
    a = ''.join(C[0:8])
    b = ''.join(C[8:16])
    c = ''.join(C[16:24])
    d = ''.join(C[24:32])
    C = int(''.join(d + c + b + a), 2)

    D = list("{:032b}".format(D))
    a = ''.join(D[0:8])
    b = ''.join(D[8:16])
    c = ''.join(D[16:24])
    d = ''.join(D[24:32])
    D = int(''.join(d + c + b + a), 2)

    hesh = "{:08x}".format(A) + "{:08x}".format(B) + "{:08x}".format(C) + "{:08x}".format(D)
    l3.config(text=hesh)

    return("{:08b}".format(A) + "{:08b}".format(B) + "{:08b}".format(C) + "{:08b}".format(D), hesh)

def k_bitsOfHash(hesh, k):
    tmp = int(hesh, 16)
    tmp_bin = list(bin(tmp)[2:].zfill(128))
    result = int(''.join(tmp_bin[0:k]))
    return result

def heshGen():
    l6.config(text='')
    if (var.get() == False): # Генерируем хеш введеного сообщения
        Message = text1.get(1.0,END).encode("utf-8")
        HeshCount(Message[0:len(Message)-1])
    if (var.get()): # Генерируем хеш выбранного файла
        file_name = chooseFile()
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                f = file.read()
        except:
            with open(file_name, 'r', encoding="ANSI") as file:
                f = file.read()
        with open(file_name, 'rb') as file:
            fb = file.read()
        HeshCount(fb)
        text1.delete(1.0, END)
        text1.insert(1.0, f)

def TextHashGen(l):
    global col_hash_list, col_text_list
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!{}[];/.,@#$%^&*()_+=-' \
               'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя\n\r\''
    text = []
    if (l == 0):
        text = ''
    else:
        for i in range(0, l):
            text.append(random.choice(list(alphabet)))
        text = ''.join(text)
    tmp, hesh = HeshCount(text.encode("utf-8"))
    col_text_list.append(text)
    col_hash_list.append(hesh)
    return hesh

def CollisionSearch():
    global col_hash_list, col_text_list

    l6.config(text='')
    l7.config(text='')
    try:
        k = int(K.get())
        if(k > 128):
            text1.delete(1.0, END)
            text1.insert(1.0, "Максимальное количество бит коллизий хэша: 128")
        if (k < 1):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальное количество бит коллизий хэша: 1")
            k = 1
    except:
        text1.delete(1.0,END)
        text1.insert(1.0,"Введите количество бит k коллизий хэша: от 0 до 128")

    try:
        l = int(L.get())
        if (l < 0):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальная длина строки: 0")
            k = 0
    except:
        text1.delete(1.0,END)
        text1.insert(1.0,"Введите длину строки L в символах")

    col_hash_list = []
    col_text_list = []
    start = time.time()
    TextHashGen(l)
    hash_equal = False
    j = 0
    match_hash_index = 0
    while hash_equal == False:
        TextHashGen(l)
        j += 1
        for i in range(0, len(col_hash_list) - 1):
            if (k_bitsOfHash(col_hash_list[i], k) == k_bitsOfHash(col_hash_list[j], k)):
                l3.config(text="")
                hash_equal = True
                match_hash_index = i
    end = time.time()
    text1.delete(1.0, END)
    text1.insert(1.0, "Первая случайно сгенерированная строка:\n" + col_text_list[match_hash_index]
                 + "\nХэш первой строки:\n" + col_hash_list[match_hash_index]
                 + "\n\nВторая случайно сгенерированная строка:\n" + col_text_list[j]
                 + "\nХэш второй строки:\n" + col_hash_list[j])
    l6.config(text="N = " + str(len(col_text_list)))
    l7.config(text="t = " + "".join(list(str(end - start))[0:5]))

def ProobrazSearch():
    global col_hash_list, col_text_list

    l6.config(text='')
    l7.config(text='')
    try:
        k = int(K.get())
        if(k > 128):
            text1.delete(1.0, END)
            text1.insert(1.0, "Максимальное количество бит коллизий хэша: 128")
        if (k < 1):
            text1.delete(1.0, END)
            text1.insert(1.0, "Минимальное количество бит коллизий хэша: 1")
            k = 1
    except:
        text1.delete(1.0,END)
        text1.insert(1.0,"Введите количество бит k коллизий хэша: от 0 до 128")

    if (var.get() == False): # Генерируем хеш введеного сообщения
        String_1 = text1.get(1.0, END)
        String_1_b = text1.get(1.0, END).encode("utf-8")
        tmp, String_1_hesh = HeshCount(String_1_b[0:len(String_1_b)-1])
    if (var.get()): # Генерируем хеш выбранного файла
        file_name = chooseFile()
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                String_1 = file.read()
        except:
            with open(file_name, 'r', encoding="ANSI") as file:
                String_1 = file.read()
        with open(file_name, 'rb') as file:
            fb = file.read()
        tmp, String_1_hesh = HeshCount(fb)

    col_text_list = []
    col_hash_list = []
    equal = False
    j = 0
    start = time.time()
    while equal == False:
        gen_len = random.randint(1,153)
        TextHashGen(gen_len)
        if (k_bitsOfHash(col_hash_list[j], k) == k_bitsOfHash(String_1_hesh, k)):
            equal = True
            l3.config(text="")
        j += 1
    end = time.time()

    if(var.get() == False):
        String_1 = "".join(list(String_1)[0:len(String_1)-1])
    text1.delete(1.0, END)
    text1.insert(1.0, "Исходная строка:\n" + String_1
                 + "\nХэш выбранной строки:\n" + String_1_hesh
                 + "\n\nСлучайно сгенерированная строка:\n" + col_text_list[j - 1]
                 + "\nХэш второй строки:\n" + col_hash_list[j - 1])
    l6.config(text="N = "+str(len(col_text_list)))
    l7.config(text="t = " + "".join(list(str(end - start))[0:5]))

if __name__ == "__main__":
    global col_hash_list, col_text_list
    col_hash_list, col_text_list = [], []
    matplotlib.use('TkAgg')
    root = Tk()
    root.title("MD4 Hesh")
    root.geometry("500x450")
    root.resizable(False, False)

    canvas = Canvas(width=500, height=450, bg="#385773") \
        .place(x=-2, y=-2)

    text1 = Text(width=59, height=11, bg="#A9C6D9", fg='#1C1C1C', wrap=WORD)
    text1.place(x=11, y=24)

    l1 = Label(root, justify=RIGHT, text="Введите текст:", bg="#385773", fg='#F2F2F0', font="Noah 10")
    l1.place(x=11, y=2)
    l2 = Label(root, justify=RIGHT, text="Хеш сообщения:", bg="#385773", fg='#F2F2F0', font="Noah 10")
    l2.place(x=11, y=363)
    l3 = Label(root, justify=RIGHT, text="", bg="#385773", fg='#F2F2F0', font="Noah 14", )
    l3.place(x=11, y=383)
    l4 = Label(root, justify=RIGHT, text="k = ", bg="#385773", fg='#F2F2F0', font="Noah 14", )
    l4.place(x=200, y=270)
    l5 = Label(root, justify=RIGHT, text="L = ", bg="#385773", fg='#F2F2F0', font="Noah 14", )
    l5.place(x=200, y=320)
    l6 = Label(root, justify=RIGHT, text="", bg="#385773", fg='#F2F2F0', font="Noah 14", )
    l6.place(x=280, y=320)
    l7 = Label(root, justify=RIGHT, text="", bg="#385773", fg='#F2F2F0', font="Noah 14", )
    l7.place(x=280, y=350)

    K = StringVar()
    L = StringVar()
    entry = Entry(root, width=3, font=24, textvariable=K, bg="#35648C", fg='#F2F2F0') \
        .place(x=230, y=275)
    entry1 = Entry(root, width=3, font=24, textvariable=L, bg="#35648C", fg='#F2F2F0') \
        .place(x=230, y=325)

    button1 = Button(root, width=25, height=2, text="Сгенерировать хэш", bg="#35648C", fg='#F2F2F0',
                     command=heshGen) \
        .place(x=11, y=215)
    button2 = Button(root, width=15, height=2, text="Поиск коллизий", bg="#35648C", fg='#F2F2F0',
                     command=CollisionSearch) \
        .place(x=11, y=265)
    button3 = Button(root, width=15, height=2, text="Поиск прообраза", bg="#35648C", fg='#F2F2F0',
                     command=ProobrazSearch) \
        .place(x=11, y=315)
    button4 = Button(root, width=8, height=2, text="График", bg="#35648C", fg='#F2F2F0',
                     command=Graph1) \
        .place(x=130, y=265)
    button5 = Button(root, width=8, height=2, text="График", bg="#35648C", fg='#F2F2F0',
                     command=Graph2) \
        .place(x=130, y=315)

    var = BooleanVar()
    var.set(0)
    r1 = Radiobutton(root, text='Использовать текст', width=20, height=2,
                     value=0, variable=var, bg="#6387A6").place(x=320, y=215)
    r2 = Radiobutton(root, text='Загрузить файл', width=20, height=2,
                     value=1, variable=var, bg="#6387A6").place(x=320, y=265)

    # hesh1, h1 = HeshCount("RAPTOR".encode())
    # print("Хэш значение строки 'RAPTOR': ", h1)
    # hesh2, h2 = HeshCount("RCPTOR".encode())
    # print("Хэш значение строки 'RCPTOR': ", h2)
    # print("Сложение хэшей по модулю 2:")
    # print(bin(int(hesh2,2) ^ int(hesh1,2)))
    # count = 0
    # for i in list(bin(int(hesh2,2) ^ int(hesh1,2))):
    #     if i == '1':
    #         count += 1
    # print("Количество отличающихся битов: ",count)

    root.mainloop()
