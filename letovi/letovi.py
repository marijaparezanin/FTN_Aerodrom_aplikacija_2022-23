from datetime import datetime, timedelta, date, time
import csv
from common import konstante as konst

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizoivanih_letova(svi_letovi: dict):
    danas = datetime.now()
    lista = []
    for let in svi_letovi:
        if svi_letovi[let]["datum_pocetka_operativnosti"] > danas:
            lista.append(svi_letovi[let])
    return lista
"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    lista = []
    kolona = ['sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_sletanja', 'vreme_poletanja', 'prevoznik']
    parametri = [polaziste, odrediste, vreme_sletanja, vreme_poletanja, prevoznik]
    lose = False
    for let in svi_letovi:
        for i in range(5):
            if svi_letovi[let][kolona[i]] != parametri[i] and parametri[i] != '':
                lose = True     #tj parametar postoji ali nije ispunjen
                    
        for k_let in konkretni_letovi:  #kad sam nasla pravi let u svi letovima, trazim ga u konkretnim 
            if konkretni_letovi[k_let]["broj_leta"] == svi_letovi[let]['broj_leta']:
                if datum_polaska is not None:
                    if konkretni_letovi[k_let]["datum_i_vreme_polaska"] != datum_polaska:
                        lose = True
                if datum_dolaska is not None:
                    if konkretni_letovi[k_let]["datum_i_vreme_dolaska"] != datum_dolaska:
                        lose = True
        
        if not lose:
            for k_let in konkretni_letovi:  #kad sam nasla pravi let u svi letovima, trazim ga u konkretnim 
                if konkretni_letovi[k_let]["broj_leta"] == svi_letovi[let]['broj_leta']:    #zajednicka kolona konkretnih i svih je broj leta
                    lista.append(konkretni_letovi[k_let])
        lose = False
    return lista

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):
    if datum_kraja_operativnosti < datum_pocetka_operativnosti:
        raise Exception("Pocetak posle kraja")
    if len(dani) == 0:
        raise Exception("Nisu unjeti dani")
    if len(broj_leta) != 4:
        raise Exception("Pogresan broj leta")
    if broj_leta is None:
        raise Exception("Prazno, ne moze")
    if cena <= 0:
        raise Exception("Nevalidna cijena")
    if dani is None:
        raise Exception("Provera za nevalidnu vrednost: losi dani")
    if len(model) != 4:
        raise Exception("Nevalidan model")
    if len(vreme_poletanja) != 5:   #mora biti formata xx:xx
        raise Exception("Pogresno vrijeme polaska")
    if len(vreme_sletanja) != 5:   
        raise Exception("Pogresno sletanja")
    if sletanje_sutra != True and sletanje_sutra != False:
        raise Exception("Pogresno sletanje sutra")
    svi_letovi[broj_leta] = {}
    svi_letovi[broj_leta]['broj_leta'] = broj_leta
    svi_letovi[broj_leta]['sifra_polazisnog_aerodroma'] = sifra_polazisnog_aerodroma
    svi_letovi[broj_leta]['sifra_odredisnog_aerodorma'] = sifra_odredisnog_aerodorma  
    svi_letovi[broj_leta]['vreme_poletanja'] = vreme_poletanja
    svi_letovi[broj_leta]['vreme_sletanja'] = vreme_sletanja
    svi_letovi[broj_leta]['sletanje_sutra'] = sletanje_sutra 
    svi_letovi[broj_leta]['prevoznik'] = prevoznik
    svi_letovi[broj_leta]['dani'] = dani
    svi_letovi[broj_leta]['model'] = model
    svi_letovi[broj_leta]['cena'] = cena
    svi_letovi[broj_leta]["datum_pocetka_operativnosti"] = datum_pocetka_operativnosti
    svi_letovi[broj_leta]["datum_kraja_operativnosti"] = datum_kraja_operativnosti
    return svi_letovi
"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(
    svi_letovi : dict,
    broj_leta: str,
    sifra_polazisnog_aerodroma: str,
    sifra_odredisnog_aerodorma: str,
    vreme_poletanja: str,
    vreme_sletanja: str,
    sletanje_sutra: bool,
    prevoznik: str,
    dani: list,
    model: dict,
    cena: float,
    datum_pocetka_operativnosti: datetime,
    datum_kraja_operativnosti: datetime
) -> dict:

    if type(sletanje_sutra) != bool:
        raise Exception("Sletanje nije validnog tipa")

    if prevoznik == '':
        raise Exception("Prevoznik nije unjet")
    
    if dani == [] or type(dani) != list:
        raise Exception("Prazni dani")

    if datum_pocetka_operativnosti.date() > datum_kraja_operativnosti.date():
        raise Exception('Pogresani datumi operativnosti')

    if len(dani) == 0:
        raise Exception("ne")
    if cena <= 0:
        raise Exception("Cijena nije validna (<=0)")
    
    if len(sifra_odredisnog_aerodorma) != 3:
        raise Exception("Sifra odredista nije validna")
    
    if len(sifra_polazisnog_aerodroma) != 3:
        raise Exception("Sifra polazista nije validna")

    if prevoznik is None or dani is None or model is None:
        raise Exception("Prevoznik/model/dan nije validan")

    if vreme_poletanja.count(':') != 1 or vreme_sletanja.count(':') != 1:
        raise Exception("Vrijeme nije dobro")
    
    for let in svi_letovi:
        '''svi_letovi[let]['broj_leta'] = broj_leta''' #ovo je key
        if svi_letovi[let]['broj_leta'] == broj_leta:
            svi_letovi[let]['sifra_polazisnog_aerodroma'] = sifra_polazisnog_aerodroma
            svi_letovi[let]['sifra_odredisnog_aerodorma'] = sifra_odredisnog_aerodorma  
            svi_letovi[let]['vreme_poletanja'] = vreme_poletanja
            svi_letovi[let]['vreme_sletanja'] = vreme_sletanja
            svi_letovi[let]['sletanje_sutra'] = sletanje_sutra 
            svi_letovi[let]['datum_kraja_operativnosti'] = datum_kraja_operativnosti 
            svi_letovi[let]['datum_pocetka_operativnosti'] = datum_pocetka_operativnosti 
            svi_letovi[let]['prevoznik'] = prevoznik
            svi_letovi[let]['dani'] = dani
            svi_letovi[let]['model'] = model
            svi_letovi[let]['cena'] = cena
            return svi_letovi
    raise Exception("Broj leta nije validan")   #tj. nije u svim letovima
"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    let_lista = []    #moram dictionary prebaciti u listu
    for let in svi_letovi:
        red = svi_letovi[let]
        let_lista.append(red)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, let_lista[0])
    writer.writeheader()
    writer.writerows(let_lista)
    file.close()

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    svi_letovi = {}
    file = open(putanja)
    reader = csv.DictReader(file)
    for let in reader: 
        if let['sletanje_sutra']  == 'False':
            let['sletanje_sutra'] = False
        if let['sletanje_sutra']  == 'True':
            let['sletanje_sutra'] = True
        let['cena'] = float(let['cena'])
        let['dani'] = eval(let['dani'])
        let['model'] = eval(let['model'])
        let['datum_pocetka_operativnosti'] = datetime.strptime(let['datum_pocetka_operativnosti'], '%Y-%m-%d %H:%M:%S')
        let['datum_kraja_operativnosti'] = datetime.strptime(let['datum_kraja_operativnosti'], '%Y-%m-%d %H:%M:%S')
        broj_leta = let['broj_leta'] 
        svi_letovi[broj_leta] = let   
    file.close()
    return svi_letovi

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    matrica  = []
    broj_redova = svi_letovi[konkretni_let['broj_leta']]['model']['broj_redova']
    pozicije_sedenja = svi_letovi[konkretni_let['broj_leta']]['model']['pozicije_sedista']
    lista = []
    for _ in range(len(pozicije_sedenja)):
        lista.append(False)
    
    for i in range(broj_redova):
        matrica.append(lista)
    
    konkretni_let['zauzetost'] = matrica
    #return konkretni_let
"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretni_let: dict) -> list:
    matrica = konkretni_let['zauzetost']
    return matrica
"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta: dict, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str): #(dict, dict)
    matrica = matrica_zauzetosti(konkretni_let)

    '''danas = date.today()
    vremenska_razlika = konkretni_let['datum_i_vreme_polaska'].date() - danas
    #vremenska_razlika = vremenska_razlika.total_seconds() * 3600
    if vremenska_razlika <= timedelta(hours=48):
        raise Exception("Kasno za chekin")'''

    red -= 1    #red pocinje od 0
    pozicija = ord(pozicija) - 65   # 'A' = 65 (ascii)
    if red < 0 or red > len(matrica):
        raise Exception("Nevalidan red")
    
    if matrica[red][pozicija] == True:
        raise Exception("Vec zauzeto mjesto")
    
    novi_red = matrica[red][:]
    novi_red[pozicija] = True
    matrica[red] = novi_red
    karta['sediste'] = chr(pozicija + 65) + str(red + 1)  # A 4 = A4
    karta['status'] = konst.STATUS_REALIZOVANA_KARTA
    return konkretni_let, karta
    

def trazenje_10_najjeftinijih_letova(svi_letovi: dict, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str):
    lista = []
    lista_10 = []
    if sifra_odredisnog_aerodorma == '' and sifra_polazisnog_aerodroma == '': #if sifra_odredisnog_aerodorma is None and sifra_polazisnog_aerodroma is None:
        for let in svi_letovi:
            lista.append(svi_letovi[let])

        lista_10 = sorted(lista, key=lambda d: d['cena'])
        lista_10 = lista_10[:10] 
        lista_10.reverse()
        return lista_10
    elif sifra_odredisnog_aerodorma == '': #elif sifra_odredisnog_aerodorma is None:
        for let in svi_letovi:
            if svi_letovi[let]['sifra_polazisnog_aerodroma'] == sifra_polazisnog_aerodroma:
                lista.append(svi_letovi[let])
        lista_10 = sorted(lista, key=lambda d: d['cena'])
        lista_10 = lista_10[:10] 
        #lista_10.reverse()
        return lista_10
    elif sifra_polazisnog_aerodroma == '':    #elif sifra_polazisnog_aerodroma is None:
        for let in svi_letovi:
            if svi_letovi[let]['sifra_odredisnog_aerodorma'] == sifra_odredisnog_aerodorma:
                lista.append(svi_letovi[let])
        lista_10 = sorted(lista, key=lambda d: d['cena'])
        lista_10 = lista_10[:10] 
        return lista_10
    else:
        for let in svi_letovi:
            if svi_letovi[let]['sifra_polazisnog_aerodroma'] == sifra_polazisnog_aerodroma and svi_letovi[let]['sifra_odredisnog_aerodorma'] == sifra_odredisnog_aerodorma:
                lista.append(svi_letovi[let])
        lista_10 = sorted(lista, key=lambda d: d['cena'])
        if len(lista_10) > 10:
            lista_10 = lista_10[:10] 
        return lista_10

"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""

def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    lista = []
    for let in svi_konkretni_letovi:
        if svi_konkretni_letovi[let]['sifra'] == konkretni_let['sifra']:
            if svi_konkretni_letovi[let]['broj_leta'] != konkretni_let['broj_leta'] or svi_konkretni_letovi[let]['datum_i_vreme_polaska'] != konkretni_let['datum_i_vreme_polaska']  or svi_konkretni_letovi[let]['datum_i_vreme_dolaska'] != konkretni_let['datum_i_vreme_dolaska']:
                raise Exception("Let nepostojeci")
    polaziste = svi_letovi[konkretni_let['broj_leta']]['sifra_odredisnog_aerodorma']
    for let in svi_letovi.values():
        if let['sifra_polazisnog_aerodroma'] == polaziste:
            for k_let in svi_konkretni_letovi.values():
                if k_let['broj_leta'] == let['broj_leta']:
                    if k_let['datum_i_vreme_polaska'].date() == konkretni_let['datum_i_vreme_dolaska'].date():
                        delta = k_let['datum_i_vreme_polaska'] - konkretni_let['datum_i_vreme_dolaska']
                        if delta <= timedelta(minutes = 120):
                            lista.append(k_let)
    return lista

"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    prvi = datum_polaska - timedelta(days = broj_fleksibilnih_dana)  
    prvi = prvi.date()
    drugi = datum_polaska + timedelta(days = broj_fleksibilnih_dana) 
    drugi = drugi.date()
    lista = []
    while(prvi <= drugi):
        for k_let in konkretni_letovi:
            datum = konkretni_letovi[k_let]['datum_i_vreme_polaska'].date()
            if datum == prvi:
                for let in svi_letovi:
                    if svi_letovi[let]["broj_leta"] == konkretni_letovi[k_let]['broj_leta']:
                        if svi_letovi[let]["sifra_odredisnog_aerodorma"] == odrediste and svi_letovi[let]['sifra_polazisnog_aerodroma'] ==polaziste:
                            lista.append(konkretni_letovi[k_let])
        prvi += timedelta(days = 1)
    return lista