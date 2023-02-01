import csv

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    provjera = [skracenica, pun_naziv, grad, drzava]
    for i in range(len(provjera)):
        if len(provjera[i]) == 0:
            raise Exception("nedostaje")
    aer = {}
    aer['skracenica'] = skracenica
    aer['pun_naziv'] = pun_naziv
    aer['grad'] = grad
    aer['drzava'] = drzava
    svi_aerodromi[skracenica] = aer
    return svi_aerodromi
"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    aer_lista = []    #moram dictionary prebaciti u listu
    for aer in svi_aerodromi:
        pomoc = svi_aerodromi[aer]
        aer_lista.append(pomoc)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, aer_lista[0])
    writer.writeheader()
    writer.writerows(aer_lista)
    file.close()

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    svi_aerodromi = {}
    file = open(putanja)
    reader = csv.DictReader(file)
    for aerodrom in reader: #korisnik je linija
        skracenica = aerodrom['skracenica'] #sve linije koje su kor ime nek budu key
        svi_aerodromi[skracenica] = aerodrom    
    file.close()
    return svi_aerodromi