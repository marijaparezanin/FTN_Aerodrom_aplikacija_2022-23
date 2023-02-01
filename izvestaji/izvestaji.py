from datetime import datetime, date
"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    lista_prodanih = []
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            lista_prodanih.append(sve_karte[karta])
    if len(lista_prodanih) == 0:
        raise Exception("\nNema karata sa tim danom prodaje.")
    return lista_prodanih

"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    lista_prodanih = []
    for k_let in svi_konkretni_letovi:
        if str(svi_konkretni_letovi[k_let]["datum_i_vreme_polaska"].date()) == str(dan):  #iz date and time izvucem samo date
            for karta in sve_karte:
                if sve_karte[karta]['sifra_konkretnog_leta'] == svi_konkretni_letovi[k_let]['sifra']:
                    lista_prodanih.append(sve_karte[karta])
    return lista_prodanih

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    lista_prodanih = []
    for karta in sve_karte:
        if str(sve_karte[karta]["datum_prodaje"]) == str(dan):
            if str(sve_karte[karta]['prodavac']) == prodavac:
                lista_prodanih.append(sve_karte[karta])
    return lista_prodanih

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    broj = 0
    suma = 0
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            broj += 1
            for k_let in svi_konkretni_letovi:  #ako je dobar datum, prvo nadjem sifru u konkretnim pa br leta u svim da bih dosla do cijene
                if svi_konkretni_letovi[k_let]['sifra'] == sve_karte[karta]['sifra_konkretnog_leta']:
                    for let in svi_letovi:
                        if svi_letovi[let]['broj_leta'] == svi_konkretni_letovi[k_let]['broj_leta']:
                            suma += svi_letovi[let]['cena']
    '''if broj == 0:
        raise Exception("Nijedna karta nije prodana na ovaj dan")'''
    return broj, suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:
    broj = 0
    suma = 0
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            broj += 1
            for k_let in svi_konkretni_letovi:  #ako je dobar datum, prvo nadjem sifru u konkretnim pa br leta u svim da bih dosla do cijene
                #suma += svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
                if svi_konkretni_letovi[k_let]['sifra'] == sve_karte[karta]['sifra_konkretnog_leta']:
                    for let in svi_letovi:
                        if svi_letovi[let]['broj_leta'] == svi_konkretni_letovi[k_let]['broj_leta']:
                            suma += svi_letovi[let]['cena']
    return broj, suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date,
    prodavac: str
) -> tuple:
    broj = 0
    suma = 0
    for karta in sve_karte:
        if sve_karte[karta]['prodavac'] == prodavac:
            if sve_karte[karta]['datum_prodaje'] == dan:
                broj += 1
                for k_let in konkretni_letovi:  #ako je dobar datum, prvo nadjem sifru u konkretnim pa br leta u svim da bih dosla do cijene
                    if konkretni_letovi[k_let]['sifra'] == sve_karte[karta]['sifra_konkretnog_leta']:
                        for let in svi_letovi:
                            if svi_letovi[let]['broj_leta'] == konkretni_letovi[k_let]['broj_leta']:
                                suma += svi_letovi[let]['cena'] 
    return broj, suma


"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    prodane = {}
    lista = []
    for karta in sve_karte:
        vec_je_unjet = False
        id = sve_karte[karta]['prodavac']
        i = 0
        '''for i in prodane:
            if id[] == prodane[i]:
                vec_je_unjet = True '''
        while not vec_je_unjet:
            brojac = 0
            for kart in sve_karte:
                if sve_karte[kart]['prodavac'] == id:
                    brojac += 1     #brojim koliko puta se pojavio prodavac
            for k_let in svi_konkretni_letovi:
                if svi_konkretni_letovi[k_let]['sifra'] == sve_karte[karta]['sifra_konkretnog_leta']:
                    for let in svi_letovi:
                        if svi_letovi[let]['broj_leta'] == svi_konkretni_letovi[k_let]['broj_leta']:
                            cijena = svi_letovi[let]['cena'] 
            cijena = cijena * brojac    #ukupna cjena
            lista.append(brojac)
            lista.append(cijena)
            lista.append(id)
            prodane[id] = lista
            i +=1
            lista = []
            break
    return prodane
    '''prodane = {}         #verzija iz komentara
    for karta in sve_karte:
        id = (sve_karte[karta]['datum_prodaje'])
        brojac = 0
        for kart in sve_karte:
            if sve_karte[kart]['datum_prodaje'] == id:
                brojac += 1
        prodane[id] = brojac
    return prodane'''

