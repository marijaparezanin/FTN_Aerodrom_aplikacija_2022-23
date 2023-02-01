import ast
from datetime import datetime, timedelta
import csv

sledeca_sifra_konkretnog_leta = 5319    #jer mora biti 4-cifren

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    global sledeca_sifra_konkretnog_leta

    pocetak = let['datum_pocetka_operativnosti']
    kraj = let['datum_kraja_operativnosti']
    while(pocetak < kraj):
        sifra = sledeca_sifra_konkretnog_leta
        dan = pocetak.weekday()
        if dan in let['dani']:
            svi_konkretni_letovi[sifra] = {}
            pomoc =  let['vreme_poletanja'].split(':')
            h1 = int(pomoc[0])
            m1 = int(pomoc[1])
            pomoc =  let['vreme_sletanja'].split(':')
            h2 = int(pomoc[0])
            m2 = int(pomoc[1])
            svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'] = pocetak.replace(hour = h1, minute = m1)
            svi_konkretni_letovi[sifra]['datum_i_vreme_dolaska'] = pocetak.replace(hour = h2, minute = m2)
            svi_konkretni_letovi[sifra]['broj_leta'] = let['broj_leta']
            svi_konkretni_letovi[sifra]['sifra'] = sifra
            sledeca_sifra_konkretnog_leta += 1
        pocetak += timedelta(days = 1)  #da je samo 1 bila bi godina
    return svi_konkretni_letovi

"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    let_lista = []    #moram dictionary prebaciti u listu
    for let in svi_konkretni_letovi:
        red = svi_konkretni_letovi[let]
        let_lista.append(red)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, let_lista[0])
    writer.writeheader()
    writer.writerows(let_lista)
    file.close()


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    svi_konkretni_letovi = {}
    file = open(putanja)
    reader = csv.DictReader(file)
    for let in reader: 
        let['sifra'] = int(let['sifra'])
        let['zauzetost'] = ast.literal_eval(let['zauzetost'])
        let['datum_i_vreme_polaska'] = datetime.strptime(let['datum_i_vreme_polaska'], '%Y-%m-%d %H:%M:%S') #da bi prebacio iz stringa u pravi format
        let['datum_i_vreme_dolaska'] = datetime.strptime(let['datum_i_vreme_dolaska'], '%Y-%m-%d %H:%M:%S')
        sifra = int(let['sifra'])
        svi_konkretni_letovi[sifra] = let
    file.close()
    return svi_konkretni_letovi
