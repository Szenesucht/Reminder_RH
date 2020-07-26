# coding=utf-8
from flask import Flask, render_template, request
from datetime import datetime
import random
app = Flask(__name__)
dateListe = []
toDoListe = []
categoryListe1 = []
categoryListe2 = []
categoryListe3 = []
category = []
now = datetime
key_tuple = []
isAbgelaufen = []
helpListe = []
toDo = ""
category1 = ""
category2 = ""
category3 = ""
dict = []
legend = []

#Reseten aller Variablen
def reset():
    global dateListe
    global toDoListe
    global categoryListe1
    global key_tuple
    global isAbgelaufen
    global helpListe
    global key_tuple
    global dict
    global categoryListe2
    global categoryListe3
    global category
    global legend
    legend = []
    category = []
    dict = []
    dateListe = []
    toDoListe = []
    categoryListe1 = []
    categoryListe2 = []
    categoryListe3 = []
    isAbgelaufen = []
    helpListe = []
    key_tuple = []

#Auslesen der .txt Datei
def read():
    global dateListe
    global toDoListe
    global categoryListe1
    global categoryListe2
    global categoryListe3
    global now
    global key_tuple
    global isAbgelaufen

    reset()
    with open("save.txt", "r") as file:
        counter = 0
        for line in file:
            if counter % 6 ==0:
                dateListe.append(datetime(int(line[:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19])).strftime("%Y-%m-%d %H:%M:%S"))
            elif counter % 6 == 1:
                toDoListe.append(line)
            elif counter % 6 == 2:
                categoryListe1.append(line)
            elif counter % 6 == 3:
                categoryListe2.append(line)
            elif counter % 6 == 4:
                categoryListe3.append(line)
            elif counter % 6 == 5:
                isAbgelaufen.append(line)
            counter +=1

    for i in range(0,len(dateListe)):
        supp = [dateListe[i], toDoListe[i], categoryListe1[i], categoryListe2[i],categoryListe3[i], isAbgelaufen[i]]
        key_tuple.append(supp)

    key_tuple.sort()

#Abspeichern in der .txt Datei
def write():
    global key_tuple

    with open("save.txt", "w") as file:
        for i in range(0,len(key_tuple)):
            file.write(key_tuple[i][0] + "\n" + key_tuple[i][1] + key_tuple[i][2] + key_tuple[i][3] + key_tuple[i][4] + key_tuple[i][5])

#Überprüfung des Datums
def check():
    global now
    global key_tuple
    global helpListe

    read()
    zeit = now.now()

    with open("save.txt", "r") as file:
        counter = 0
        for line in file:
            if counter % 6 ==0:
                helpListe.append(datetime(int(line[:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19])))
            counter += 1

    for i in range(0,len(helpListe)):
        if helpListe[i] <=zeit:
            key_tuple[i][5] = "abgelaufen"
        else:
            key_tuple[i][5] = "zeit"




@app.route("/")
def test():
    global toDo
    global now
    global key_tuple
    global category1
    global category2
    global category3

    reset()

    date = request.args.get("date", "2020-07-23 12:29:54")
    t = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")

    toDo = request.args.get("toDo", "Nothing to do")
    category1 = request.args.get("category1")
    category2 = request.args.get("category2")
    category3 = request.args.get("category3")

    abgelaufen = "zeit"

    if t != "" and toDo != "" and category1 != "" and t != None and toDo != None and category1 != None:
        with open("save.txt", "a") as file:
            file.write(str(t) + "\n" + toDo + "\n" + category1 + "\n" + category2 + "\n" + category3 + "\n" + abgelaufen + "\n")
    read()
    write()
    check()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template("start.html", date=date, )


#Farben je nach Kategorie erstellen
def checkCategory():

    global dict

    check()

    #Nimm alle Kategorien auf
    with open("save.txt", "r") as file,open("category.txt", "r+")as output:
        counter = 0
        hilf = []
        hilf2 =[]
        for zeile in output:
            hilf.append(zeile.strip().split(" "))

        for i in range(0,len(hilf)):
            hilf2.append(hilf[i][0])

        for line in file:
            if (line != "\n" and counter % 6 == 2 and line.strip() not in hilf2) or (line != "\n" and counter % 6 == 3 and line.strip() not in hilf2) or (line != "\n" and counter % 6 == 4 and line.strip() not in hilf2):
                line = line[:-1]
                line += " " + "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) + "\n"
                output.write(line)
                supp = line.split(" ")
                dict.append(supp)

            counter +=1

@app.route("/output")
def input():

    global key_tuple
    global now
    global dict
    global category
    global legend

    read()
    write()
    check()

    checkCategory()

    lenght = len(key_tuple)

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("category.txt", "r") as file:
        for line in file:
            category.append(line.strip().split(" "))

    lenghtCategory = len(category)
    print(len(category))

    for i in range (0,len(key_tuple)):
        for j in range(0,len(category)):
            if category[j][0].strip() == key_tuple[i][2].strip():
                key_tuple[i][2] = category[j][1]
                continue
            elif category[j][0].strip() == key_tuple[i][3].strip():
                key_tuple[i][3] = category[j][1]
                continue
            elif category[j][0].strip() == key_tuple[i][4].strip():
                key_tuple[i][4] = category[j][1]
                continue
            else:
                continue


    return render_template("output.html", key_tuple=key_tuple, date= date, lenght=lenght, dict=dict, category=category, lenghtCategory=lenghtCategory)