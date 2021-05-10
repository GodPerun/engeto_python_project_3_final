## Script pro parsovani vysledku voleb z roku 2017:

### zdroj:
https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

### Instalace:
vytvorte si virtualni prostredi s pomoci requirements.txt

### Spousteni:
Script potrebuje 2 vstupni argumenty, z uzemni urovne na vyse zminenem webu vyberte Obec (link v tabulce s "X"). Otevre se Vam nova
stranka, zkopirujte URL a vlozte do argumentu scriptu.<br>
Druhy argument je nazev csv soubory, do ktereho se ulozi vysledky.<br>
<br>
### Priklad pouziti:
python3 volby.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4203" "volby.csv"
