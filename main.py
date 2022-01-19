import datetime
import json
import os
import time
from urllib.request import urlopen
import json

# -----------------------------------------------------------
# (C) 2021 Jarno Heinonen
# email jarska90@gmail.com
# -----------------------------------------------------------

# Functions
def unixtime(txt):
    """
    Convert the time to unixtime.
    Also adding a one hour to the day,
    so we get an end day including the array.
    """

    x = txt.split(".")
    dd = int(x[0]) + 1
    aika = datetime.date(int(x[2]), int(x[1]), int(dd))

    return time.mktime(aika.timetuple())


def kaannos():
    """
    Creates a textfile and get data from json-file and
    convert the unix time to gmt time based on location aka. in Finland gmt+2.\n
    After that writing the convert time and Bitcoin's value to a temporary textfile
    """
    f = open("myfile.txt", "w")
    with open("personal.json") as json_file:
        data = json.load(json_file)

        for x in range(len(data["prices"])):
            aika = data["prices"][x][0] / 1000
            my_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(aika))
            f.write(my_time + ", ")
            f.write(str(data["prices"][x][1]))
            f.write(" \n")
    f.close()


def pvm_tarkistus():
    """
    Open a textfile, which contains convereted times,
    then checking the first value of the day and the rest values will be erased.
    """
    my_file = open("myfile.txt", "r")
    content_list = my_file.readlines()

    ainut_arvo_pv = {x.split()[0]: x for x in content_list[::-1]}
    abc = list(ainut_arvo_pv.values())[::-1]

    f = open("myfile.txt", "w")

    for line in abc:
        # cleaning a data
        f.write(line.replace(" \n", "\n"))

    my_file.close()
    f.close()


def max_arvo(adicci):
    """
    Returns a max value from a dictionary
    """
    suurin_arvo = max(adicci, key=adicci.get)
    print(
        "The date with the highest trading volume and the volume on that day in {0} and the volume is {1} euros. \n".format(
            suurin_arvo, adicci[suurin_arvo]
        )
    )


def pisin_lasku(adicci):
    """
    Checking when it's a longest decreased row and returns that.
    """
    arvot = []
    lasku = 0
    pisin = 0
    for key, value in adicci.items():
        arvot.append(value)

    for x in range(len(arvot) - 1):
        if arvot[x] > arvot[x + 1]:
            lasku += 1
            if pisin < lasku:
                pisin = lasku
        elif arvot[x] < arvot[x + 1]:
            lasku = 0

    print(
        "\nIn bitcoin’s historical data from CoinGecko, the price decreased {0} days in a row  for the input from {1} and to {2}".format(
            pisin, alku, loppu
        )
    )


def timeMachine(adicci):
    """
    Checking a minium and maxium value from data.\n
    If data is lower in the end day of range than the start day,
    will inform a user that.
    """
    alhaisin_arvo = min(adicci, key=adicci.get)
    kallein_arvo = max(adicci, key=adicci.get)

    arvot = []
    teksti = ""
    for value in adicci.items():
        arvot.append(value)
    if arvot[0] > arvot[-1]:
        teksti = " Bitcoin's value is only decreasing, do not buy anymore in the time. However if you really want to buy, "

    print(
        "Timemachine result:{0} the best day to buy Bitcoin is {1}, the price is the lowest of the daterange. \nThe best day to sell Bitcoin is {2}, the price is the highest of the daterange. \n".format(
            teksti, alhaisin_arvo, kallein_arvo
        )
    )

# First let's ask dates from a user
alku = input("Please enter a startday in format dd.mm.yyyy: ")
loppu = input("Please enter a end day in format dd.mm.yyyy: ")

# Convert the asked time to unixtime via function
alkutime = unixtime(alku)
lopputime = unixtime(loppu)

# Sending values to coingecko
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from={0}&to={1}".format(
    alkutime, lopputime
)

res = urlopen(url)

# Writing data from url to jsonfile
dajs = json.loads(res.read())

with open("personal.json", "w") as json_file:
    json.dump(dajs, json_file)


kaannos()

pvm_tarkistus()

# Convert the data to an array
adicci = {}
tekstifile = open("myfile.txt", "r")

for line in tekstifile:
    key, value = line.split(",")

    adicci[key] = value[:-1]


pisin_lasku(adicci)
max_arvo(adicci)
timeMachine(adicci)

tekstifile.close()

# In the end, the script will ask from user
# if wants to remove files or keep them.
ending = input(
    "Press q key to delete textfile and json file and quit. If not, just press enter..."
)
if ending == "q":
    os.remove("myfile.txt")
    os.remove("personal.json")
    exit()
