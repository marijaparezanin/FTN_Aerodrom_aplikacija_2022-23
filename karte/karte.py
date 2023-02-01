from common import konstante
from functools import reduce
from datetime import datetime
import csv

"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1
"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs
): #-> (dict, dict):
    global sledeci_broj_karte
    prodavac = kwargs['prodavac']
    if prodavac['uloga'] != konstante.ULOGA_PRODAVAC:
        raise Exception("Samo prodavac moze prodati kartu")
    if kupac['uloga'] != konstante.ULOGA_KORISNIK:
        raise Exception('Kupac mora biti korisnik')
    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("Nepostojeci let")
    
    karta = {}
    karta['broj_karte'] = sledeci_broj_karte
    karta['putnici'] = putnici
    karta['sifra_konkretnog_leta'] = sifra_konkretnog_leta
    karta['status'] = konstante.STATUS_NEREALIZOVANA_KARTA
    karta['obrisana'] = False
    karta['datum_prodaje'] = kwargs['datum_prodaje']
    karta['prodavac'] = prodavac
    karta['kupac'] = kupac
    #karta['sifra_sedista'] = 

    sve_karte[sledeci_broj_karte] = karta
    sledeci_broj_karte += 1
    return karta, sve_karte

def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):
    nerealizovane_karte = []
    for kolona in sve_karte:
        if kolona["status"] == konstante.STATUS_NEREALIZOVANA_KARTA:
            for putnik in kolona["putnici"]:
                if putnik == korisnik:
                    nerealizovane_karte.append(kolona)
    return nerealizovane_karte

"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska:
    datetime=None,
    sediste=None
) -> dict:
    try:
        if nova_sifra_konkretnog_leta is not None:
            nova_sifra_konkretnog_leta = int(nova_sifra_konkretnog_leta)
    except:
        raise Exception("Pogresna sifra konketnog leta.\n")
    
    tacno = False
    for i in sve_karte.values():
        if i['broj_karte'] == broj_karte:
            tacno = True
    if not tacno:
        raise Exception('Nepostojeci broj leta.\n')
    tacno = False
    for i in svi_konkretni_letovi.values():
        if nova_sifra_konkretnog_leta is not None and nov_datum_polaska is not None:
            if str(svi_konkretni_letovi[nova_sifra_konkretnog_leta]['datum_i_vreme_polaska']) == str(nov_datum_polaska):
                tacno = True
        else:
            tacno = True
    if not tacno:
        raise Exception("Unjeti datum polaska ne odgovara odabranom konkretnom letu.\n")
    
    for i in svi_konkretni_letovi.values():
        if i['sifra'] == nova_sifra_konkretnog_leta or nova_sifra_konkretnog_leta is None:
            tacno = True
    if not tacno:
        raise Exception('Nepostojeca sifra leta')
    sve_karte[broj_karte]['sifra_konkretnog_leta'] = nova_sifra_konkretnog_leta
    return sve_karte
    
"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik["uloga"] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
        return sve_karte
    elif korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]["obrisana"] = True
        return sve_karte
    elif korisnik["uloga"] == konstante.ULOGA_KORISNIK:
        raise Exception("Korisnik ne moze da izbrise kartu!")
    else:
        raise Exception("Pogresan unos!")

"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: str="",
                             korisnicko_ime_putnika: str="")->list:
    lista = []
    
    for karta in sve_karte.values():
        if korisnicko_ime_putnika == karta['kupac']['korisnicko_ime'] or korisnicko_ime_putnika == '':
            if (svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska'] == datum_polaska or datum_polaska == '') and (str(svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_dolaska']) == datum_dolaska or datum_dolaska == ''):
                if (svi_letovi[svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta']]['sifra_polazisnog_aerodroma'] == polaziste or polaziste == '') and (svi_letovi[svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['broj_leta']]['sifra_odredisnog_aerodorma'] == odrediste or odrediste == ''):
                    lista.append(karta)
    return lista
    '''for k_let in svi_konkretni_letovi.values():
    if k_let['sifra'] > 
    if k_let['sifra'] == karta['sifra_konkretnog_leta']:'''
    
"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    karte_lista = []    #moram dictionary prebaciti u listu
    for karta in sve_karte:
        pomoc = sve_karte[karta]
        karte_lista.append(pomoc)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, karte_lista[0])
    writer.writeheader()
    writer.writerows(karte_lista)
    file.close()
"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    global sledeci_broj_karte
    sve_karte = {}
    file = open(putanja)
    reader = csv.DictReader(file)
    for karta in reader: #korisnik je linija
        if karta['obrisana']  == 'False':
            karta['obrisana'] = False
        if karta['obrisana']  == 'True':
            karta['obrisana'] = True
        karta['putnici'] = eval(karta['putnici'])
        karta['prodavac'] = eval(karta['prodavac'])
        karta['kupac'] = eval(karta['kupac'])
        #karta['datum_prodaje'] = datetime.strptime(karta['datum_prodaje'], '%d.%m.%Y.')    #ovo dvoje mora biti pod komentarom da bi radio karte fajl
        #karta['sediste'] = int(karta['sediste'])
        karta['sifra_konkretnog_leta'] = int(karta['sifra_konkretnog_leta']) 
        karta['broj_karte'] = int(karta['broj_karte']) 
        broj = karta['broj_karte'] 
        sledeci_broj_karte = broj
        sve_karte[broj] = karta    
    file.close()
    sledeci_broj_karte +=1
    return sve_karte