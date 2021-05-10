#!/usr/bin/python3
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
from bs4 import BeautifulSoup as besu
import pandas as pd
import csv
import sys

# Press the green button in the gutter to run the script.

def get_obce(web_address):

    try:
        tables = pd.read_html(web_address, encoding="UTF-8")
    except:
        ImportError
        print("prvni except")
        return []

    listik = []
    print("Stahuji data z vybraneho webu: ", web_address)
    for i in range(len(tables)):
        cislo_obce = tables[i]
        # print(tables[i]['Obec']['číslo'])
        try:
            listik = listik + cislo_obce['Obec']['číslo'].tolist()
        except:
            KeyError
            print("druhy except")
            return []
    try:
        while True:
            listik.remove('-')
    except:
        ValueError

    return listik


def data_z_obci(obce, webovka):
    print("zacatek funkce data_z_obci")
    vyber = webovka.split('numnuts=')[1]
    kraj = re.split('xkraj=|,\&xnumnuts', webovka)

    ## init dict
    vysledky = [{"kod_obce": "", "nazev_obce": "", "volici_v_seznamu": "", "vydane_obalky": "", "platne_hlasy": "",
                 "kandidujici_strany": ""} for k in range(len(obce))]
    # vysledky[0].update({"kod_obce": obec[2]})
    # print(vysledky[0].get("kod_obce"))
    ## konec init dict

    ###zacatek cyklu
    for i in range(len(obce)):

        # vygenerovani linku pro kazdou obec
        if str(obce[i]) == "-":
            continue
        generovana_webovka = str(
            f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=" + kraj[1] + "&xobec=" + str(
                obce[i]) + "&xvyber=" + vyber)
        print( "|| iterace: ", i, "|| pocet obci: ", len(obce), "|| id obce: ", obce[i], "|| vygenerovany web: ", generovana_webovka)
        tables = pd.read_html(generovana_webovka, encoding="UTF-8")
        pocet_tabulek = len(tables)  # prvni tabulka obecne statistiky; druha a dalsi tabulky obsahuji nazvy po. stran

        ## zjisteni nazvu Obce
        response = requests.get(generovana_webovka)
        proparsovane = besu(response.text, "html.parser")
        h3ka = proparsovane.findAll('h3')
        obec = re.split('\n|: ', str(h3ka[2]))

        ## konec zjisteni nazvu obce

        ### vytahnuti z prvni tabulky u obce  - volici_v_seznamu, vydane_obalky, platne_hlasy
        volici_pre = proparsovane.find(attrs={"class": "cislo", "headers": "sa2"})
        volici = str(volici_pre.text).replace(u'\xa0', u'')

        vydane_obalky_pre = proparsovane.find(attrs={"class": "cislo", "headers": "sa3"})
        vydane_obalky = str(vydane_obalky_pre.text).replace(u'\xa0', u'')

        platne_hlasy_pre = proparsovane.find(attrs={"class": "cislo", "headers": "sa6"})
        platne_hlasy = str(platne_hlasy_pre.text).replace(u'\xa0', u'')

        ## KONEC vytahnuti prvni tabulky

        ## zjisteni vsech stran pro obec
        strana = []
        for j in range(pocet_tabulek):  # zjisteni stran
            if j == 0:  # prvni tabulka nejsou strany
                continue
            strana = strana + (tables[j]['Strana']['název'].tolist())


        ### konec zjisteni vsech stran

        vysledky[i].update({"kod_obce": obce[i], \
                            "nazev_obce": obec[2], \
                            "volici_v_seznamu": volici, \
                            "vydane_obalky": vydane_obalky, \
                            "platne_hlasy": platne_hlasy, \
                            "kandidujici_strany": strana})

        ## konec cyklu
    # print(*vysledky, sep="\n")

    return vysledky


def create_csv(slovnik, csv_name):
    with open(csv_name, 'w', newline='') as csvfile:
        fieldnames = ['kod_obce', 'volici_v_seznamu', 'platne_hlasy', 'nazev_obce', 'vydane_obalky',
                      'kandidujici_strany']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(slovnik)):
            writer.writerow(slovnik[i])

def help():
    print("Script se musi spoustet s dvema argumentama - web a jmeno csv filu")
    print("example: python3 volby.py \"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4203\" \"volby.csv\"")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        help()
        exit(3)
    url1 = str(sys.argv[1])
    nazev_csv = str(sys.argv[2])
    print(sys.argv[1], sys.argv[2])
    #nazev_csv = "volby.csv"
    #url1 = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"
    #url1 = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4203"
    #url1 = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=564591&xvyber=4203"
    url2 = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=529303&xokrsek=6&xvyber=2101"

    seznam_obci = get_obce(url1)
    if not seznam_obci:
        help()
        exit(1)
    vysledky_do_csv = data_z_obci(seznam_obci, url1)
    create_csv(vysledky_do_csv, nazev_csv)

