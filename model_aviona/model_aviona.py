import csv
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
sljedeci_id = 0

def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicije_sedista: list = []
) -> dict:
    if broj_redova is None or len(pozicije_sedista) == 0 or len(naziv) == 0:
        raise Exception('Prazan unos')
        
    global sljedeci_id
    model = {}
    model['id'] = sljedeci_id
    model['broj_redova'] = broj_redova
    model['naziv'] = naziv
    model['pozicije_sedista'] = pozicije_sedista
    svi_modeli_aviona[sljedeci_id] = model
    sljedeci_id += 1

    return svi_modeli_aviona

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    modeli_lista = []    #moram dictionary prebaciti u listu
    for let in svi_aerodromi:
        pomoc = svi_aerodromi[let]
        modeli_lista.append(pomoc)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, modeli_lista[0])
    writer.writeheader()
    writer.writerows(modeli_lista)
    file.close()


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    svi_modeli = {}

    file = open(putanja)
    reader = csv.DictReader(file)
    for model in reader: 
        model['id'] = int(model['id']) 
        model['broj_redova'] = int(model['broj_redova']) 
        #model['pozicije_sedista'] = model['pozicije_sedista'].strip('][').split('", "') #["'A', 'B', 'C', 'D', 'E', 'F', 'G'"]
        model['pozicije_sedista'] = eval(model['pozicije_sedista'])
        #model['pozicije_sedista'] = model['pozicije_sedista'].strip('[]').replace('"', ' ').split(',')
        '''
        #model['pozicije_sedista'] = (model['pozicije_sedista']).strip('][').split('", "')
        #model['pozicije_sedista'] = model['pozicije_sedista'].strip('')
        #pomoc = len(list(model['pozicije_sedista']))
        pomoc = (model['pozicije_sedista']).strip('[]').split('", "')
        #model['pozicije_sedista'] = pomoc[0].replace(',', 'x')
        """pomoc = pomoc[0].split(", ")
        for i in range(0,len(pomoc)):
            pomoc[i] = pomoc[i].replace('"', '')"""
        pomoc1 = list(pomoc[0])
        for i in range(0, len(pomoc1)):
            if ord(pomoc1[i]) == 39: # 34, 39, 44
                del pomoc1[i] 
        
        model['pozicije_sedista'] = (pomoc)
        #model['pozicije_sedista'] = (model['pozicije_sedista']).strip('[]').split('", "')
        #model['pozicije_sedista'] = model['pozicije_sedista'].replace('"', '')
        
        for i in range(len(model['pozicije_sedista'])):
            model['pozicije_sedista'][i].replace('A','x')        '''
        id = model['id'] #sve linije koje su id nek budu key
        svi_modeli[id] = model    
    file.close()
    return svi_modeli
