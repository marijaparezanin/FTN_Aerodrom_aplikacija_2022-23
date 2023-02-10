import os
from time import sleep
from datetime import datetime, timedelta, date, time
from korisnici import korisnici
from letovi import letovi
from model_aviona import model_aviona
from karte import karte
from konkretni_letovi import konkretni_letovi
from izvestaji import izvestaji
from common import konstante as konst

uloga_kor = ''
kor_ime = ''
ulogovan = False
los_unos = False
svi_korisnici = {}
svi_letovi = {}
svi_konkretni_letovi = {}
sve_karte = {}

def ucitaj_iz_fajla():
    global sve_karte, svi_konkretni_letovi, svi_letovi, svi_korisnici
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi.csv', ',')
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnik.csv', ',')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('letovi.csv', ',')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte.csv', ',')

def unesite_bilo_koji_karakter():
    unos = input("\nUnesite bilo koji karakter za izlaz ")
    uvodna_poruka()

def clear():
    os.system('cls')

def uvodna_poruka():
    global uloga_kor, kor_ime, los_unos
    clear()
    print('_'*80 + '\n')
    print (f"{'':<20}{'Dobrodosli u aplikaciju Projekat2023!':<40}")
    print('_'*80)
    broj_ponuda = 6
    if uloga_kor != '':
        print("\n    Ulogovani ste kao " + kor_ime + ': ' + uloga_kor)
        print('-'*80)

    print("\n Izaberite jednu od sljedecih opcija:")
    print (f"{'':<5}{'1. Prijava na sistem':<40}")
    print (f"{'':<5}{'2. Pregled nerealizovanih letova':<40}")
    print (f"{'':<5}{'3. Pretraga letova':<40}")
    print (f"{'':<5}{'4. Prikaz 10 najjeftinijih letova':<40}")
    print (f"{'':<5}{'5. Fleksibilni polasci':<40}")

    if not ulogovan:
        print (f"{'':<5}{'6. Registracija':<40}")
        broj_ponuda = 7
    else:
        print (f"{'':<5}{'6. Odjava sa sistema':<40}")
        if uloga_kor == konst.ULOGA_KORISNIK:
            print (f"{'':<5}{'7. Kupovina karata':<40}")
            print (f"{'':<5}{'8. Pregled nerealizovanih karti':<40}")
            print (f"{'':<5}{'9. Check-in':<40}")
            broj_ponuda = 10
        elif uloga_kor == konst.ULOGA_PRODAVAC:
            print (f"{'':<5}{'7. Prodaja karata':<40}")
            print (f"{'':<5}{'8. Prijava na let (check-in)':<40}")
            print (f"{'':<5}{'9. Izmena karte':<40}")
            print (f"{'':<5}{'10. Brisanje karte':<40}")
            print (f"{'':<5}{'11. Pretraga prodatih karata':<40}")
            broj_ponuda = 12
        elif uloga_kor == konst.ULOGA_ADMIN:
            print (f"{'':<5}{'7. Pretraga prodatih karata':<85}")
            print (f"{'':<5}{'8. Registracija novih prodavaca':<40}")
            print (f"{'':<5}{'9. Kreiranje letova':<40}")
            print (f"{'':<5}{'10. Izmena letova':<40}")    
            print (f"{'':<5}{'11. Brisanje karata':<40}")
            print (f"{'':<5}{'12. Izveštavanje':<40}")
            broj_ponuda = 13
    print (f"{'':<5}{'x. Izlazak iz aplikacije':<40}")
    meni_izbor(broj_ponuda)

def meni_izbor(broj_ponuda):
    global kor_ime, uloga_kor, los_unos, sve_karte, svi_konkretni_letovi, svi_korisnici, svi_letovi
    ucitaj_iz_fajla()
    pocetni_unos = input("     : ")
    if pocetni_unos == 'x' or pocetni_unos == 'X':
        izlaz()
    try:
        pocetni_unos = int(pocetni_unos)                  #provjera za inicijalni unos
        if pocetni_unos not in range(1, broj_ponuda):
            los_unos = True
    except:
        los_unos = True
    
    if not los_unos:                              
        if pocetni_unos == 1:                             #zajednicke funkcije (1-5)
            prijava_na_sistem()
        if pocetni_unos ==2: 
            pregled_nerealizovanih_letova()
        if pocetni_unos == 3:
            pretraga_letova()
        if pocetni_unos == 4:
            najjeftinijih_10()
        if pocetni_unos == 5:
            fleksibilni_polasci()

        if uloga_kor == konst.ULOGA_KORISNIK:
            if pocetni_unos == 6:
                odjava()
            elif pocetni_unos == 7:
                kupovina_karata()
            elif pocetni_unos == 8:      
                pregled_nerealizovanih_karti()            
            else:
                checkin()
        elif uloga_kor == konst.ULOGA_ADMIN:
            if pocetni_unos == 6:
                odjava()
            elif pocetni_unos == 7:
                clear()
                print('-'*80)
                print(f"\n{'Pretraga karti':^80}")
                print('\n' + '-'*80)
                pretraga_karata()
                unesite_bilo_koji_karakter()
            elif pocetni_unos == 8: #Registracija novih prodavaca
                registracija()
            elif pocetni_unos == 9:
                kreiraj_let()
            elif pocetni_unos == 10:
                izmjena_letova()
            elif pocetni_unos ==11:
                brisanje_karte()
            elif pocetni_unos == 12:
                izvjestavanje()
        elif uloga_kor == konst.ULOGA_PRODAVAC:
            if pocetni_unos == 6:
                odjava()
            if pocetni_unos == 7:   #Prodaja karata
                kupovina_karata()
            if pocetni_unos == 8:   #Prijava na let (check-in)
                checkin()
            if pocetni_unos == 9:
                izmjena_karti()
            if pocetni_unos == 10:  
                brisanje_karte()
            if pocetni_unos == 11:
                clear()
                print('-'*80)
                print(f"\n{'Pretraga karti':^80}")
                print('\n' + '-'*80)
                pretraga_karata()
                unesite_bilo_koji_karakter()
        else:   #nije registrovan kupac
            if pocetni_unos == 6:   
                registracija()
    else:
        print('\n      Pogresan unos, pokusajte ponovo!')
        sleep(1)
        clear()
        los_unos = False
        uvodna_poruka()        

def ispis_konkretni_lista(lista):
    global svi_letovi, svi_konkretni_letovi
    ucitaj_iz_fajla()
    print('_'*85)
    print('\nBr leta' + '  ' + 'Sifra' + ' '*8 + 'Datum i vrijeme polaska/dolaska' + ' '*10 + 'Cena' + ' '*4 + 'Sifra AER\n' + '_'*85 + '\n')
    for i in range(len(lista)):
        d = lista[i]
        for let in svi_letovi:      #hocu da imam dodatno i cijenu i sifre, a dati su mi konkretni
            if svi_letovi[let]['broj_leta'] == d['broj_leta']:
                cena = svi_letovi[let]['cena']
                sifra_odredisnog_aerodorma = svi_letovi[let]['sifra_odredisnog_aerodorma'] 
                sifra_polazisnog_aerodroma = svi_letovi[let]['sifra_polazisnog_aerodroma'] 
        print(str(d['broj_leta'])+ ' '*5 + str(d['sifra']) + '  ', d['datum_i_vreme_polaska'],'    ', d['datum_i_vreme_dolaska'], '  ' + str(cena) + '  ' + sifra_polazisnog_aerodroma + ' '*4 + sifra_odredisnog_aerodorma)
    print("_"*85)

def ispis_karte_lista(lista):
    print('\n' + '-'*80 + '\n Br karte' + ' '*2 + 'Datum prodaje' + ' '*2+ 'Sifra leta' + ' '*2 + 'Korisnicko ime kupca\n' + '-'*80)
    for i in range(len(lista)):
        x = 3
        if lista[i]['broj_karte'] > 9: x = 2
        print(' '*x,lista[i]['broj_karte'],' '*5,lista[i]['datum_prodaje'],' '*5, lista[i]['sifra_konkretnog_leta'], ' '*4, lista[i]['kupac']['korisnicko_ime'])

def checkin():
    global sve_karte, svi_konkretni_letovi, svi_letovi, kor_ime, uloga_kor, svi_korisnici
    ucitaj_iz_fajla()
    clear()
    print('_'*80)
    print(f"\n{'Check - in':^80}")
    print('_'*80 + '\n')
    unos = input("  1. Pretraga karata\n  2. Direktni unos\n  3. Izlaz\n  : ")
    if unos == '3':
        uvodna_poruka()
    elif unos == '1':
        pretraga_karata()
    elif unos != '2':
        print('\nPogresan unos!')
        unesite_bilo_koji_karakter()
    broj_karte = input("\nUnesite broj karte: ")
    try:
        if broj_karte.isnumeric():
            broj_karte = int(broj_karte)
        else: raise Exception
        if broj_karte not in sve_karte.keys():
            raise Exception
        trazena_karta = sve_karte[broj_karte]
        if sve_karte[broj_karte]['status'] == konst.STATUS_REALIZOVANA_KARTA: 
            print('Vec ste cekirani!')
            unesite_bilo_koji_karakter()
    except:
        print('\nNevalidan broj karte.')
        unesite_bilo_koji_karakter()
    trenutno_datum_vrijeme = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    trenutno_datum_vrijeme = datetime.strptime(trenutno_datum_vrijeme, '%Y-%m-%d %H:%M:%S')
    if trenutno_datum_vrijeme < svi_konkretni_letovi[sve_karte[broj_karte]['sifra_konkretnog_leta']]['datum_i_vreme_polaska']:
        vremenska_razlika = svi_konkretni_letovi[sve_karte[broj_karte]['sifra_konkretnog_leta']]['datum_i_vreme_polaska'] - trenutno_datum_vrijeme
        sati = vremenska_razlika.total_seconds() // 3600
        if sati > 48:
            print('Checkin se radi 48h prije leta. Molim Vas sacekajte.\n')
            unesite_bilo_koji_karakter()
    else:
        print("Let se vec desio. Checkin nije moguc.")
        unesite_bilo_koji_karakter()
    p = False
    while not p:
        ime = input('\nUnesite ime kupca: ')
        prezime = input('Unesite prezime kupca: ')
        if sve_karte[broj_karte]['kupac']['ime'] == ime and sve_karte[broj_karte]['kupac']['prezime'] == prezime:
            p = True
        else:
            unos = input('Ime i prezime ne odgovara kupcu!\nUnesite 1 za izlaz ili drugi karakter za ponovan unos: ')
            if unos == '1':
                uvodna_poruka()
    t = True
    if len(sve_karte[broj_karte]['kupac']) == 4:
        while(t):
            korisnicko_ime = input('\nZa dalju potvrdu potrebne su nam dodatne informacije:\nIzaberite korisnicko ime: ')
            lozinka = input('Unesite lozinku: ')
            br_tel = input('Unesite broj telefona: ')
            email = input('Unesite email: ')
            pasos = input('Unesite broj pasosa(opciono):')
            drzavljanstvo = input('Unesite svoje drzavljanstvo(opciono): ')
            pol = input('Unesite pol(opciono): ')
            try:
                svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konst.ULOGA_KORISNIK, '', korisnicko_ime, lozinka, sve_karte[broj_karte]['kupac']['ime'], sve_karte[broj_karte]['kupac']['prezime'], email, pasos, drzavljanstvo, br_tel, pol)
                korisnici.sacuvaj_korisnike('korisnik.csv', ',', svi_korisnici)
                sve_karte[broj_karte]['kupac'] = svi_korisnici[korisnicko_ime]
                karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
                t = False
            except Exception as x:
                print('\n',x, '\n Unesite ponovo!\n')
    else:
        while(t):
            lozinka = input('\nDa bi potvrdili identitet kupca karte molimo unesite lozinku: ')
            for korisnik in svi_korisnici.values():
                if korisnik['ime'] == ime and korisnik['prezime'] == prezime:
                    korisnicko_ime = korisnik['korisnicko_ime']
            if svi_korisnici[korisnicko_ime]['lozinka'] != lozinka:
                print('Pogresna lozinka pokusajte ponovo!')
            else:
                t = False
        while not t:
            if svi_korisnici[korisnicko_ime]['pasos'] == '': 
                pasos = input("Sada je neophodno unjeti pasos: ")
                t = True
            if svi_korisnici[korisnicko_ime]['pol'] == '': 
                pol = input("Sada je neophodno unjeti pol: ")
                t = True
            if svi_korisnici[korisnicko_ime]['drzavljanstvo'] == '': 
                drzavljanstvo = input("Sada je neophodno unjeti drzavljanstvo: ")
                t = True
            if not t:
                break
            if t:
                try:
                    svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, True, svi_korisnici[korisnicko_ime]['uloga'], '', korisnicko_ime, lozinka, svi_korisnici[korisnicko_ime]['ime'], svi_korisnici[korisnicko_ime]['prezime'], svi_korisnici[korisnicko_ime]['email'], pasos, drzavljanstvo, str(svi_korisnici[korisnicko_ime]['telefon']), pol)
                    for karta in sve_karte.values():
                        if karta['kupac']['korisnicko_ime'] == korisnicko_ime:
                            karta['kupac'] = svi_korisnici[korisnicko_ime]
                    karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
                    korisnici.sacuvaj_korisnike('korisnik.csv', ',', svi_korisnici)
                except:
                    print("\nPogresan unos unesite ponovo!")
                    t = False
    petlja = True
    while petlja:
        print('\nZauzeta mjesta su prikazana sa X: ')
        tabela = []
        for i in range(len(svi_konkretni_letovi[trazena_karta['sifra_konkretnog_leta']]['zauzetost'])):
            linija = '        ' + str(i+1) + ': '
            for j in range(len(svi_konkretni_letovi[trazena_karta['sifra_konkretnog_leta']]['zauzetost'][i])):
                if svi_konkretni_letovi[trazena_karta['sifra_konkretnog_leta']]['zauzetost'][i][j] == True: linija += '  ' + 'X'
                else: linija += '  ' + chr(j+65)   
            print(linija)
        t = False
        while not t:
            unos = list(input('\nUnesite sjediste koje zelite zauzeti (A4): '))
            try:
                if len(unos)!= 2: raise Exception
                red = int(unos[1])
                pozicija = unos[0]
                if not unos[0].isalpha(): raise Exception
                t = True
            except:
                print('Pogresan format unosa! Unesite ponovo\n')
        try:
            svi_konkretni_letovi[trazena_karta['sifra_konkretnog_leta']], sve_karte[broj_karte] = letovi.checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[trazena_karta['sifra_konkretnog_leta']], red, pozicija)
            karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
            konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi.csv',',',svi_konkretni_letovi)
            print('\nUspjesan checkin!')
        except Exception as x: print('\n', x)
        l = True
        for karta in sve_karte.values():
            if l:
                if karta['kupac'] == svi_korisnici[korisnicko_ime] and karta['status'] != konst.STATUS_REALIZOVANA_KARTA:
                    trenutno_datum_vrijeme = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                    trenutno_datum_vrijeme = datetime.strptime(trenutno_datum_vrijeme, '%Y-%m-%d %H:%M:%S')
                    if trenutno_datum_vrijeme < svi_konkretni_letovi[karta['sifra_konkretnog_leta']]['datum_i_vreme_polaska']:
                        vremenska_razlika = svi_konkretni_letovi[sve_karte[broj_karte]['sifra_konkretnog_leta']]['datum_i_vreme_polaska'] - trenutno_datum_vrijeme
                        sati = vremenska_razlika.total_seconds() // 3600
                        if sati < 48:
                            unos = input('\nTakodje ste kupili kartu broj ' + str(karta['broj_karte']) + ' da li se zelite cekirati i za nju? ').lower()
                            if unos != 'da':
                                petlja == False
                                break
                            else:
                                trazena_karta = karta
                                broj_karte = karta['broj_karte']
                            l = False
        if l: break 
    unesite_bilo_koji_karakter()

def brisanje_karte():
    global kor_ime, sve_karte, svi_korisnici, svi_letovi, svi_konkretni_letovi, uloga_kor
    ucitaj_iz_fajla()
    clear()
    print('_'*80)
    print(f"\n{'Brisanje karte':^80}")
    print('_'*80 + '\n')
    if uloga_kor == konst.ULOGA_ADMIN:
        unos = input("   1. Ponisti brisanje karte\n   2. Brisanje svih oznacenih karti\n   3. Ostalo\n   :")
        lista = []
        for karta in sve_karte.values():
            if karta['obrisana'] == True:
                lista.append(karta)
        
        if unos == '1':
            if len(lista) != 0:
                ispis_karte_lista(lista)
                p = True
                while(p):
                    unos = input('\n   Unesite broj karte koji zelite promjeniti: ')
                    for karta in sve_karte.values():
                        if str(karta['broj_karte']) == unos:
                            p = False
                            karta['obrisana'] = False
                    if p:
                        print('   Pogresan unos!')
                    else: print('   Uspjesna promjena!')
                    p = True
                    unos1 = input('\n   Da li zelite promjeniti jos karti? ').lower()
                    if unos1 == 'da': p = True
                    else: p = False
            else:
                print('Ne postoje oznacene karte.')
        elif unos == '2':
            if len(lista) != 0:
                ispis_karte_lista(lista)
                lista = []
                for karta in sve_karte.values():
                    if karta['obrisana'] == True: 
                        lista.append(karta['broj_karte'])
                for i in range(len(lista)):
                    del sve_karte[lista[i]]
                print('\n   Uspjesno izbrisano!') 
            else: print('Ne postoje oznacene karte.')
        elif unos != '3':
            print('   Pogresan unos!\n')
            sleep(1)
            uvodna_poruka()
    karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
    unos = input('\n  Opcije:\n   1. Pretraga karti\n   2. Prikaz svih karti\n   3. Direktan unos\n   4. Izlaz\n   :')
    if unos == '1': 
        pretraga_karata()
    elif unos == '2':
        lista_karte = []
        for i in sve_karte.values():
            lista_karte.append(i)
        ispis_karte_lista(lista_karte)
    elif unos == '4':
        uvodna_poruka()
    elif unos != '3':
        print('Pogresan unos!')
        uvodna_poruka()
    try:
        broj_karte = int(input("\nUnesite broj karte koju zelite izbrisati: "))
    except:
        print('\nPogresan unos!')
        unos = input('Unesite 1 za ponovan unos: ')
        if unos == '1':
            brisanje_karte()
        else:
            uvodna_poruka()
    for kor in svi_korisnici.values():
        if kor['korisnicko_ime'] == kor_ime:
            korisnik = kor
    try:
        sve_karte = karte.brisanje_karte(korisnik, sve_karte, broj_karte)
        karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
        if uloga_kor == konst.ULOGA_ADMIN:
            print("\nUspjesno obrisana karta!\n")
            potvrda = True
            while potvrda:
                drugi = input('Da li zelite izbrisati jos karata? ').lower()
                if drugi == 'da':
                    try:
                        broj_karte = int(input("\nUnesite broj karte koju zelite izbrisati: "))
                        sve_karte = karte.brisanje_karte(korisnik, sve_karte, broj_karte)
                        karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
                        print("\nUspjesno obrisana karta!\n")
                    except:
                        print('\nPogresan unos!')
                        unesite_bilo_koji_karakter()
                else:
                    potvrda = False
        else:
            print('\nUspjesno promjenjen status karte!')
        unesite_bilo_koji_karakter()
    except:
        print('\nPogresan unos!')
        sleep(1)
        uvodna_poruka()

def pregled_nerealizovanih_karti():
    global kor_ime, svi_korisnici, sve_karte
    ucitaj_iz_fajla()
    clear()
    print('-'*50)
    print(f"\n{'Pregled nerealizovanih karti':^50}")
    print('\n' + '-'*50)
    korisnik = svi_korisnici[kor_ime]
    lista_sve_karte = []    #zato sto ce mi pasti test, jer test mu prosljedjuje listu umjesto dic
    for karta in sve_karte.values():
        lista_sve_karte.append(karta)
    lista = karte.pregled_nerealizovanaih_karata(korisnik, lista_sve_karte)
    if len(lista) == 0:
        print('\nNemate neralizovanih karata.')
        unesite_bilo_koji_karakter()
    print('\n' + ' '*5 + 'Br. karte' + ' '*3 + 'Sifra leta' + ' '*4 + 'Datum prodaje\n')
    for i in range(len(lista)):
        d = lista[i]
        x = 8
        if d['broj_karte'] > 9: #radi dvocefrenog broja da ljepse izgleda
            x = 7
        print(' '*7,d['broj_karte'], ' '*x, d['sifra_konkretnog_leta'],' '*7,d['datum_prodaje'])
    print()
    unesite_bilo_koji_karakter()

def pretraga_karata():
    global sve_karte, svi_konkretni_letovi, svi_letovi
    ucitaj_iz_fajla()
    polaziste = input('\nUnesite sifru polaska: ')
    odrediste = input('Unesite sifru odredista: ')
    datum_polaska = input('Unesite datum i vrijeme polaska (Y-M-d H-M-S): ')
    datum_dolaska = input('Unesite datum i vrijeme dolaska (Y-M-d H-M-S): ')
    korisnicko_ime = input('Unesite korisnicko ime kupca: ')
    try:
        if datum_polaska != '':
            datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S') #funkcija trazi da je dolazak string
    except:
        print('Pogresno unesen datum polaska! ')
        unesite_bilo_koji_karakter()
    lista = karte.pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, korisnicko_ime)
    if len(lista) == 0:
        print('\nNema karata sa unjetim podacima.')
        unesite_bilo_koji_karakter()
    ispis_karte_lista(lista)
    
def kupovina_karata():
    global sve_karte, svi_konkretni_letovi, svi_korisnici, svi_letovi, uloga_kor, kor_ime
    ucitaj_iz_fajla()
    clear()
    putnici = []
    prodavac = {}
    kupac = {}
    print('-'*85)
    if uloga_kor == konst.ULOGA_PRODAVAC:
        print(f"\n{'Prodaja karata':^85}")
        print('\n' + '-'*85 + '\n')
        ime = input('Unesite ime saputnika: ')
        prezime = input("Unesite prezime saputnika: ")
        kupac = {'ime': ime, 'prezime': prezime, 'uloga': konst.ULOGA_KORISNIK, 'korisnicko_ime': ime + prezime}
        putnici.append(kupac)
    else:
        print(f"\n{'Kupovina karata':^85}")
        print('\n' + '-'*85 + '\n')
        unos = input("Da li kupujete kartu za sebe (da/ne)? ").lower()
        if unos == 'da':
            for korisnik in svi_korisnici.values():
                if korisnik['korisnicko_ime'] == kor_ime:
                    putnici.append(korisnik)
                    kupac = korisnik
        elif unos != 'ne':
            print("Greska! Pogresan unos!")
            sleep(2)
            unesite_bilo_koji_karakter()
        else:
            print("Unesite informacije o saputniku:")
            ime = input('Unesite ime saputnika: ')
            prezime = input("Unesite prezime saputnika: ")
            kupac = {}
            for korisnik in svi_korisnici.values():
                if korisnik['ime'] == ime and korisnik['prezime'] == prezime:
                    kupac = korisnik
            if len(kupac) == 0:
                kupac = {'ime': ime, 'prezime': prezime, 'uloga': konst.ULOGA_KORISNIK, 'korisnicko_ime': ime + prezime}
            putnici.append(kupac)

    potvrda = True
    while potvrda:
        unos = input("\nDa li imate jos saputnika?").lower()
        if unos == 'da':
            ime = input("Unesite ime saputnika: ")
            prezime = input("Unesite prezime saputnika: ")
            saputnik = {'ime': ime, 'prezime': prezime, 'korisnicko_ime': ime + prezime}
            for korisnik in svi_korisnici.values():
                if korisnik['ime'] == ime and korisnik['prezime'] == prezime:   #da li je postojeci saputnik
                    saputnik = korisnik
            putnici.append(saputnik)
        else:
            potvrda = False

    while not potvrda:
        print('\n' + '-' * 85 + '\n')
        print('1. Zelim ispis svih konkretnih letova\n2. Zelim ispis prvih 50 konkretnih letova\n3. Zelim pretragu')
        unos = input(': ')
        if unos == '1' or unos == '2':
            i = 0
            print('\nBr leta' + '  ' + 'Sifra' + ' '*8 + 'Datum i vrijeme polaska/dolaska' + ' '*10 + 'Cena' + ' '*4) 
            for k_let in svi_konkretni_letovi.values():
                if i < 50 or unos == '1':
                    i += 1
                    for let in svi_letovi.values():      #hocu da imam dodatno i cijenu i prevoznika, a dati su mi konkretni
                        if let['broj_leta'] == k_let['broj_leta']:
                            cena = let['cena']
                    print(str(k_let['broj_leta'])+ ' '*5 + str(k_let['sifra']) + '  ', k_let['datum_i_vreme_polaska'],'    ', k_let['datum_i_vreme_dolaska'], '  ' + str(cena) + '  ')
            print("_"*85)
            potvrda = True
        elif unos == '3':
            potvrda = True
            sifra_polazisnog_aerodroma = input('Unesite sifru polazisnog aerodroma: ')
            sifra_odredisnog_aerodorma = input('Unesite sifru odredisnog aerodroma: ')
            lista = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, None, None, '', '', '')
            if len(lista) == 0:
                print('\nNema letova sa unjetim osobinama.')
                unesite_bilo_koji_karakter()
            ispis_konkretni_lista(lista)
        else:
            print('Pogresan unos!\n') #potvrda nastavlja biti false
            
    sifra = input("Unesite sifru konkretnog leta: ")
    try:
        sifra = int(sifra)
    except:
        print('\nPogresna sifra!')
        unesite_bilo_koji_karakter()
    if int(sifra) not in svi_konkretni_letovi.keys():
        print('Konkretan let ne postoji!\n')
        unesite_bilo_koji_karakter()
    for k in svi_konkretni_letovi.values():
        if k['sifra'] == sifra:
            konkretan = k
    provjera = False
    for i in range(len(konkretan['zauzetost'])):
        for j in range(len(konkretan['zauzetost'][i])):
            if konkretan['zauzetost'][i][j] == False:
                provjera = True
    if not provjera:
        print('Nema slobodnih mjesta!')
        unesite_bilo_koji_karakter()
    if uloga_kor == konst.ULOGA_PRODAVAC:
        prodavac1 = {"kor_ime": kor_ime, "uloga": konst.ULOGA_PRODAVAC}
    else:
        prodavac1 = {"kor_ime": 'Onlajn prodavac', "uloga": konst.ULOGA_PRODAVAC}
    matrica = letovi.matrica_zauzetosti(konkretan)
    karta, sve_karte = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra, putnici, svi_konkretni_letovi[sifra]["zauzetost"], kupac,prodavac = prodavac1, datum_prodaje = date.today())
    karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
    if uloga_kor == konst.ULOGA_PRODAVAC:
        print("Uspjesno prodata karta!")
    else:
        print("Uspjesno kupljena karta!")

    lista = povezani(konkretan)
    if len(lista) == 0:
        print('Za ovaj let ne postoje povezani letovi.')
        unesite_bilo_koji_karakter()
    unos = input('\nZa Vas let postoje povezani letovi. Da li zelite kupiti karte i za njih? ').lower()

    if unos != 'da':
        sleep(1)
        uvodna_poruka()
    ispis_konkretni_lista(lista)
    sifra = input("Unesite sifru konkretnog leta: ")
    try:
        sifra = int(sifra)
    except:
        print('\nPogresna sifra!')
        unesite_bilo_koji_karakter()
    if int(sifra) not in svi_konkretni_letovi.keys():
        print('Konkretan let ne postoji!\n')
        unesite_bilo_koji_karakter()
    for k in svi_konkretni_letovi.values():
        if k['sifra'] == sifra:
            konkretan = k
    matrica = letovi.matrica_zauzetosti(konkretan)
    karta, sve_karte = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra, putnici, svi_konkretni_letovi[sifra]["zauzetost"], kupac, prodavac = prodavac1, datum_prodaje = date.today())
    karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
    if uloga_kor == konst.ULOGA_PRODAVAC:
        print("Uspjesno prodata karta!")
    else:
        print("Uspjesno kupljena karta!")
    unesite_bilo_koji_karakter()

def izmjena_karti():
    global sve_karte, svi_letovi, svi_konkretni_letovi
    clear()
    print('-'*80)
    print(f"\n{'Izmjena karti':^80}")
    print('\n' + '-'*80 + '\n')
    unos = input("  1. Pretraga karata\n  2. Direktni unos\n  3. Izlaz\n  : ")
    if unos == '3':
        uvodna_poruka()
    elif unos == '1':
        pretraga_karata()
    elif unos != '2':
        print('\nPogresan unos!')
        unesite_bilo_koji_karakter()
    broj_karte = input("\nUnesite broj karte: ")
    try:
        broj_karte = int(broj_karte)
        if broj_karte not in sve_karte.keys():
            raise Exception
    except:
        print('\nNepostojeci broj karte!')
        unesite_bilo_koji_karakter()
    try:
        nova_sifra = input('Unesite novu sifru konkretnog leta: ')
        novi_datum = input('Unesite novi datum i vrijeme polaska: ')
        if nova_sifra == '' and novi_datum == '':
            print('Morate unjeti bar jedan parametar!')
            unesite_bilo_koji_karakter()
        sve_karte = karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte, nova_sifra, novi_datum)
        sve_karte = karte.sacuvaj_karte(sve_karte, 'karte.csv', ',')
        print('\nUspjesna izmjena karte!')
        unesite_bilo_koji_karakter()
    except Exception as x:
        print(x)
        unesite_bilo_koji_karakter()

def izvjestaji_pogresan_unos(poruka):
    print("\n" + poruka + ' ')
    unos = input('Unesite bilo koji karakter za izlaz ')
    izvjestavanje()

def izvjestavanje():
    global svi_konkretni_letovi, sve_karte, svi_korisnici, svi_letovi
    ucitaj_iz_fajla()
    clear()
    print('-'*80)
    print(f"\n{'Izvjestaji':^80}")
    print('\n' + '-'*80)
    print(""*5 + ' 1. Lista prodanih za datum prodaje')
    print(""*5 + ' 2. Lista prodanih za datum polaska')
    print(""*5 + ' 3. Lista prodanih za dan i prodavca')
    print(""*5 + ' 4. Ukupan broj i cena prodatih karata za izabrani dan prodaje')
    print(""*5 + ' 5. Ukupan broj i cena prodatih karata za izabrani dan polaska')
    print(""*5 + ' 6. Ukupan broj i cena prodatih karata za izabrani dan prodaje i prodavca')
    print(""*5 + ' 7. Ukupan broj i cena prodatih karata u poljednjih 30 dana po prodavcima')
    print(""*5 + ' *. Nazad')
    try:
        izbor = (input(" : "))
        if izbor == '*':
            uvodna_poruka()
        if izbor.isnumeric():
            izbor = int(izbor)
        if izbor not in range(1, 8):
            raise Exception
        if izbor == 1: 
            clear()
            print("_"*80 + '\n\n' + ' '*23 + 'Lista prodanih za datum prodaje' + '\n' + "_"*80 + '\n')
            datum = input('Unesite datum prodaje (Y-M-d): ')
            try:
                if len(izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, datum))!=0:
                    ispis_karte_lista(izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, datum))
            except:
                izvjestaji_pogresan_unos('Pogresan unos')
            izvjestaji_pogresan_unos('')
        elif izbor ==2:
            clear()
            print("_"*80 + '\n\n' + ' '*23 + 'Lista prodanih za datum polaska' + '\n' + "_"*80 + '\n')
            datum = input('Unesite datum polaska (Y-M-d): ')
            lista = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, datum)
            if len(lista) == 0:
                izvjestaji_pogresan_unos('Nema letova sa unjetim datumom polaska.')
            ispis_karte_lista(lista)
            izvjestaji_pogresan_unos('')
        elif izbor == 3:
            clear()
            print("_"*80 + '\n\n' + ' '*18 + 'Lista prodanih za dan i prodavca' + '\n' + "_"*80 + '\n')
            datum = input('Unesite datum prodaje (Y-M-d): ')
            prodavac = input('Unesite korisnicko ime prodavca: ')
            prodavac = str({'kor_ime': prodavac, 'uloga': konst.ULOGA_PRODAVAC})
            try:
                if datum == '' or prodavac == '':
                    izvjestaji_pogresan_unos('Pogresan unos')
                lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, datum, prodavac)
                if len(lista) == 0: 
                    izvjestaji_pogresan_unos('Ne postoje karte sa unjetim uslovima.')
                ispis_karte_lista(lista)
            except Exception as c:
                print('Ne postoje karte sa unjetim uslovima.')
            izvjestaji_pogresan_unos('')
        elif izbor == 4:
            clear()
            print("_"*70 + '\n\n' + ' '*10 + 'Ukupan broj i cena prodatih karata za datum prodaje' + '\n' + "_"*70 + '\n')
            datum = input('Unesite datum prodaje (Y-M-d): ')
            try:
                broj, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi, datum)
            except:
                izvjestaji_pogresan_unos('Pogresan unos')
            if broj == 0:
                izvjestaji_pogresan_unos("Nema karti prodanih na ovaj datum")
            print('\n\nBroj karata' + ' '*5 + 'Datum prodaje' + ' '*5 + 'Cijena\n' + '-'*70)
            x = 5
            if broj > 9:
                x = 4
            print(' '*x, broj,' '*8, datum, ' '*5, suma)
            izvjestaji_pogresan_unos('')
        elif izbor == 5:    #morala sam pisati opet jer test ne valja
            clear()
            print("_"*60 + '\n\n' + ' '*7 + 'Broj i cena prodatih karata za dan polaska' + '\n' + "_"*60 + '\n')
            datum = input('Unesite datum polaska (Y-M-d): ')
            try:
                broj, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi, datum)
            except:
                izvjestaji_pogresan_unos('Pogresan unos')
            if broj == 0:
                izvjestaji_pogresan_unos("Nema karti sa datim polaskom")
            print("\nBroj karata" +' '*5 + 'Datum polaska' + ' '*5 + 'Cijena\n' + '-'*60)
            x = 5
            if broj > 9:
                x = 4
            print(' '*x, broj,' '*7, datum, ' '*6, suma)
            izvjestaji_pogresan_unos('')
        elif izbor == 6:
            clear()
            print("_"*60 + '\n\n' + ' '*7 + 'Ukupan broj i cena prodatih karata za datum prodaje' + '\n' + "_"*60 + '\n')
            datum = input('Unesite datum prodaje (Y-M-d): ')
            prodavac = input('Unesite korisnicko ime prodavca: ')
            if prodavac == '' or datum == '':
                izvjestaji_pogresan_unos('Pogresan unos!')
            sve_karte_1 = sve_karte
            for karta in sve_karte_1.values():
                karta['prodavac'] = karta['prodavac']['kor_ime']    #test prosljedjuje funkciji prodavca kao string kor ime a ne kao dict
            broj, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte_1, svi_konkretni_letovi, svi_letovi, datum, prodavac)
            if broj == 0:
                izvjestaji_pogresan_unos("Nema karata sa unjetim osobinama.")
            print("\nBroj karata" +' '*5 + 'Datum polaska' + ' '*5 + 'Cijena\n' + '-'*60)
            x = 5
            if broj > 9:
                x = 4
            print(' '*x, broj,' '*7, datum, ' '*6, suma)
            izvjestaji_pogresan_unos('')
        elif izbor == 7:
            clear()
            print("_"*70 + '\n\n' + ' '*10 + 'Ukupan broj i cena prodatih karata po prodavcima' + '\n' + "_"*70 + '\n')
            sve_karte_1 = sve_karte
            for karta in sve_karte.values():
                karta['prodavac'] = karta['prodavac']['kor_ime']    #test prosljedjuje funkciji prodavca kao string kor ime a ne kao dict
            rjecnik = {}
            try:
                rjecnik = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi, svi_letovi)
            except:
                izvjestaji_pogresan_unos("Pogresan unos")
            if len(rjecnik) == 0:
                izvjestaji_pogresan_unos("Ovaj prodavac nije prodao nijednu kartu.")
            print('\n    Broj karti' + ' '*10 + 'Ukupna cijena' + ' '*7 + 'Prodavac\n' + '-'*70)
            for i in rjecnik:           #{'prodavac':[br, cijena, 'prodavac']}
                lista = rjecnik[i]
                c = 7
                if lista[0] > 9:
                    c = 6
                print(' '*c, lista[0],' '*15,lista[1],' '*(17 - len(str(lista[1]))), i)
            izvjestaji_pogresan_unos('')
    except Exception as x:
        print(x)
        print('Pogresan unos!')
        sleep(1)
        izvjestavanje()

def fleksibilni_polasci():
    global svi_letovi, svi_konkretni_letovi
    ucitaj_iz_fajla()
    clear()
    print('-'*85)
    print(f"\n{'Fleksibilni polasci':^85}")
    print('\n' + '-'*85 + '\n')
    polaziste = input("Unesite polaziste: ")
    odrediste = input("Unesite odrediste: ")
    datum_polaska = input('Unesite datum polaska (Y-M-D): ')
    datum_dolaska = input("Unesite datum dolaska (Y-M-D): ")
    broj_fleksibilnih_dana = input("Unesite broj fleksibilnih dana: ")
    try:
        datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d')
        datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d')
        broj_fleksibilnih_dana = int(broj_fleksibilnih_dana)
    except:
        print("Pogresan unos! ")
        unesite_bilo_koji_karakter()
    lista_fleksibilnih = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, broj_fleksibilnih_dana, datum_dolaska)
    if len(lista_fleksibilnih) == 0:
        print("Nema letova koji odgovaraju unjetim podacima!")
        unesite_bilo_koji_karakter()
    for i in lista_fleksibilnih:
        for j in svi_letovi:
            if i['broj_leta'] == svi_letovi[j]['broj_leta']:
                cena = svi_letovi[j]['cena']
        i['cena'] = cena
    lista_fleksibilnih = sorted(lista_fleksibilnih, key=lambda i: i['cena'])
    ispis_konkretni_lista(lista_fleksibilnih)
    unesite_bilo_koji_karakter()

def najjeftinijih_10():
    global svi_letovi
    ucitaj_iz_fajla()
    clear()
    print('-'*80)
    print(f"\n{'Prikaz 10 najjeftinijih letova':^80}")
    print('\n' + '-'*80 + '\n')
    sifra_polazisnog_aerodroma = input("Unesite sifru polazisnog aerodroma: ")
    sifra_odredisnog_aerodorma = input('Unesite sifru odredisnog aerodroma: ')
    print()
    lista_10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma)
    
    if len(lista_10) == 0:
        print('Nema letova sa ovim osobinama!')
        pokusaj = input("Unesite 1 za ponovan unos: ")
        if pokusaj == '1':
            najjeftinijih_10()
        else:
            uvodna_poruka()
    else:
        print(' '*4 + 'Br leta' + ' '*2 + 'Polazni/odredisni aerodrom' + ' '*4 + 'Vrijeme poljetanja\sljetanja' + ' '*2 + 'Cena')
        p = 1
        x = 2
        for i in lista_10:
            if p == 10: #samo radi ljepote jer je 10 dvocifren pa mi pomjeri u stranu
                x = 1
            print(str(p)+'.' + ' '*x, i['broj_leta'], ' '*8, i['sifra_polazisnog_aerodroma'],' '*6,i['sifra_odredisnog_aerodorma'],' '*12,i['vreme_poletanja'],' '*7,i['vreme_sletanja'],' '*5,i['cena'])
            p +=1
        unesite_bilo_koji_karakter()

def povezani(konkretni):
    global svi_konkretni_letovi, svi_letovi, sve_karte
    ucitaj_iz_fajla()
    lista = letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, konkretni)
    return lista

def pregled_nerealizovanih_letova():
    global svi_letovi
    ucitaj_iz_fajla()
    clear()
    print("_"*90 + '\n')
    print(' '*35 + 'Pregled letova' + ' '*35)
    print("_"*90 + '\n')
    lista_nerealizovanih = letovi.pregled_nerealizoivanih_letova(svi_letovi)
    if len(lista_nerealizovanih) == 0:
        print('Nema nerealizovanih letova.')
        sleep(3)
        uvodna_poruka()
    print(' '*13 + "Br leta" + ' '*8 + 'Datum pocetka i kraja operativnosti' + ' '*8 + 'Cena\n')
    for i in range(0, len(lista_nerealizovanih)):
        d = lista_nerealizovanih[i]
        print(' '*13, d['broj_leta'], ' '*4, d['datum_pocetka_operativnosti'], ' '*2, d['datum_kraja_operativnosti'], ' '*3 + str(d['cena']))
    unesite_bilo_koji_karakter()

def pretraga_letova():
    global svi_letovi, svi_konkretni_letovi
    ucitaj_iz_fajla()
    clear()
    print("_"*85 + '\n')
    print(' '*30 + 'Pretraga letova' + ' '*30)
    print("_"*85 + '\n')
    prevoznik = input("Unesite prevoznika: ") 
    polaziste = input("Unesite polaziste: ")
    odrediste = input("Unesite odrediste: ")
    vreme_poletanja = input("Unesite vrijeme poljetanja (HH:MM): ")
    vreme_sletanja = input("Unesite vrijeme sletanja (HH:MM): ")
    datum_polaska = input("Unesite datum i vrijeme polaska: ")
    datum_dolaska = input('Unesite datum i vrijeme dolaska:')
    try:
        if datum_polaska != '':
            datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S')
        if datum_dolaska != '':
            datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d %H:%M:%S')
        if datum_polaska == '':
            datum_polaska = None
        if datum_dolaska == '':
            datum_dolaska = None
    except:
        print("Pogresno unjet datum i vrijeme")
        druga_sansa = input("Ako zelite napustiti unesite 1: ")
        if druga_sansa != '1':
            pretraga_letova()
        else:
            uvodna_poruka()
    lista_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    if len(lista_pretrage) == 0:
        print('\nNema letova sa unjetim osobinama.')
        sleep(2)
        uvodna_poruka()
    ispis_konkretni_lista(lista_pretrage)
    unesite_bilo_koji_karakter()
    
def izmjena_letova():
    clear()
    global svi_letovi
    ucitaj_iz_fajla()
    print('-'*80)
    print(f"\n{'Izmjena letova':^75}")
    print('\n' + '-'*80)
    unos = input('\n   1. Pretraga letova\n   2. Direktan unos\n   3. Izlaz\n   :')
    if unos == '1':
        polaziste = input('\nUnesite sifru polaska: ')
        odrediste = input('Unesite sifru odredista:')
        lista = []
        for let in svi_letovi.values():
            if (let['sifra_polazisnog_aerodroma'] == polaziste or polaziste == '') and (let['sifra_odredisnog_aerodorma'] == odrediste or odrediste == ''):
                lista.append(let)
        if len(lista) == 0:
            print('Nema letova sa ovim informacijama.')
            sleep(1)
            izmjena_letova()
        print('\n' + ' Br leta' + ' '*10 + 'Polaziste/odrediste' + ' '*10 + 'Vrijeme' + ' '*10 + 'Cijena\n' + '-'*80)
        for i in range(len(lista)):
            d = lista[i]
            print(' ', d['broj_leta'], ' '*11, d['sifra_polazisnog_aerodroma'], ' '*8, d['sifra_odredisnog_aerodorma'], ' '*6, d['vreme_poletanja'], ' '*3, d['vreme_sletanja'], ' '*4, d['cena'])
    elif unos == '3':
        uvodna_poruka()
    elif unos != '2':
        print('Pogresan unos!')
        izmjena_letova()
    broj_leta = input("\nUnesite broj leta koji pripada letu koga zelite izmjeniti: ")
    try:
        model_id = (input("Unesite id modela aviona (0/1): "))
        if model_id == '':
            model = svi_letovi[broj_leta]['model']
        else:
            modeli = model_aviona.ucitaj_modele_aviona('model_let.csv', ',')
            model = modeli[model_id]
    except:
        print("Model nije dobro unesen!")
        sleep(1)
        drugi_pokusaj = input('\nNeuspjesna izmjena leta. Unesite 1 ako zelite izmjeniti let ponovo: ')
        if drugi_pokusaj == '1':
            izmjena_letova()
        uvodna_poruka()
    sifra_polazisnog_aerodroma = input("Unesite sifru polazisnog aerodroma: ")
    sifra_odredisnog_aerodorma = input("Unesite sifru odredisnog aerodroma: ")
    vreme_poletanja = input("Unesite vrijeme poljetanja (H:M): ") 
    vreme_sletanja = input("Unesite vrijeme sljetanja (H:M): ") 
    sletanje_sutra = input("Da li ovaj let sljece sutradan? (da\ne)? ").lower()
    prevoznik = input("Unesite prevoznika: ")
    dani = (input("Unesite dane u formatu [x, y, z]: "))
    cena = (input("Unesite cijenu: "))
    try:
        if cena != '':cena = float(cena)
        if dani != '': dani = eval(dani)
    except:
        drugi_pokusaj = input('\nNije validan unos\nNeuspjesna izmjena leta. Unesite 1 ako zelite izmjeniti let ponovo: ')
        if drugi_pokusaj == '1':
            izmjena_letova()
        uvodna_poruka()
    datum_pocetka_operativnosti = input("Unesite datum i vrijeme pocetka operativnosti: (Y-m-d H:M:S): ")
    datum_kraja_operativnosti = input("Unesite datum i vrijeme kraja operativnosti: (Y-m-d H:M:S): "  )
    if datum_pocetka_operativnosti != '':
        datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, '%Y-%m-%d %H:%M:%S')
    if datum_kraja_operativnosti != '':
        datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%Y-%m-%d %H:%M:%S')
    lista = [sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti]
    lista1 = ['sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik', 'dani', 'cena', 'datum_pocetka_operativnosti', 'datum_kraja_operativnosti']
    for i in range(len(lista)):
        if lista[i] == '':
            lista[i] = svi_letovi[broj_leta][lista1[i]]
    if lista[4] == 'da': lista[4] = True
    elif lista[4] == 'ne': lista[4] = False
    elif lista[4] != True and lista[4] != False:
        drugi_pokusaj = input('\nNije validan unos za sletanje sutra\nNeuspjesna izmjena leta. Unesite 1 ako zelite izmjeniti let ponovo: ')
        if drugi_pokusaj == '1':
            izmjena_letova()
        uvodna_poruka()
    try:
        svi_letovi = letovi.izmena_letova(svi_letovi, broj_leta, lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], model, lista[7], lista[8], lista[9])
    except Exception as x:
        print(x)
        sleep(2)
        drugi_pokusaj = input('\n\nNeuspjesna izmjena leta. Unesite 1 ako zelite izmjeniti let ponovo: ')
        if drugi_pokusaj == '1':
            izmjena_letova()
        uvodna_poruka()
    print("Uspjesna izmjena leta!")
    sleep(1)
    letovi.sacuvaj_letove('letovi.csv', ',', svi_letovi)
    uvodna_poruka()

def kreiraj_let():
    clear()
    global svi_letovi
    ucitaj_iz_fajla()
    '''naziv = 'M-43'   #kreiranje modela
    broj_redova = 2
    pozicija_sjedista = ['A', 'B', 'C']
    modeli = model_aviona.ucitaj_modele_aviona('model_let.csv', ',')
    modeli = model_aviona.kreiranje_modela_aviona(modeli, naziv, broj_redova, pozicija_sjedista)
    model_aviona.sacuvaj_modele_aviona('model_let.csv', ',', modeli)
    '''  
    try:
        print('-'*60)
        print(f"\n{'Kreiranje leta':^50}")
        print('\n' + '-'*60)
        broj_leta = input("\nUnesite broj leta (xxxx): ")
        sifra_polazisnog_aerodroma = input("Unesite sifru polazisnog aerodroma: ")
        sifra_odredisnog_aerodorma = input("Unesite sifru odredisnog aerodroma: ")
        vreme_poletanja = input("Unesite vrijeme poljetanja (H:M): ") 
        vreme_sletanja = input("Unesite vrijeme sljetanja (H:M): ").lower() 
        sletanje_sutra = input("Da li ovaj let sljece sutradan? (da\ne)? ")
        prevoznik = input("Unesite prevoznika: ")
        dani = eval(input("Unesite dane u formatu [x, y, z]: "))
        model_id = int(input("Unesite id modela aviona (0/1): "))
        modeli = model_aviona.ucitaj_modele_aviona('model_let.csv', ',')
        model = modeli[model_id]
        cena = float(input("Unesite cijenu: "))
        datum_pocetka_operativnosti = input("Unesite datum i vrijeme pocetka operativnosti: (Y-m-d H:M:S): ")
        datum_kraja_operativnosti = input("Unesite datum i vrijeme kraja operativnosti: (Y-m-d H:M:S): "  )#DATUM OPERATIVNOSTI JE DATE TIME
        datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, '%Y-%m-%d %H:%M:%S')
        datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%Y-%m-%d %H:%M:%S')
        if sletanje_sutra == 'da':
            sletanje_sutra = True
        elif sletanje_sutra == 'ne':
            sletanje_sutra = False
        else:
            raise Exception("Nije vallidan unos za sletanje sutra")
    except Exception as x:
        drugi_pokusaj = input('\nNeuspjesna registracija leta. Unesite 1 ako zelite kreirati let ponovo: ')
        if drugi_pokusaj == '1':
            kreiraj_let()
        uvodna_poruka()
    try:
        svi_letovi = letovi.kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti,datum_kraja_operativnosti)
        letovi.sacuvaj_letove('letovi.csv', ',', svi_letovi)
        print(f"\n{'Uspjesno kreiranje!':^10}")
        #konkretni letovi kreiranje
        k = {} 
        for let in svi_letovi.values():
            k = konkretni_letovi.kreiranje_konkretnog_leta(k,let)
        for m in k.values():
            letovi.podesi_matricu_zauzetosti(svi_letovi,m)
        konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi.csv', ',', k)
        sleep(1)
        uvodna_poruka()
    except Exception as ex:
        print(ex)
        sleep(2)
        drugi_pokusaj = input('\nNeuspjesna registracija leta. Unesite 1 ako zelite kreirati let ponovo: ')
        if drugi_pokusaj == '1':
            kreiraj_let()
        uvodna_poruka()
    
def registracija():
    global uloga_kor, kor_ime, svi_korisnici
    ucitaj_iz_fajla()
    clear()
    try:
        print('-'*40)
        print(f"\n{'Registracija':^40}")
        print('\n' + '-'*40)
        ime = input("\n    Unesite ime:")
        prezime = input("    Unesite prezime:")
        kor_ime = input("\n    Unesite korisnicko ime:")
        lozinka = input("    Unesite lozinku:")
        email = input("    Unesite email:")
        telefon = input("    Unesite telefon:")
        pasos = input("    Unesite pasos (opciono):")
        drzavljanstvo = input("    Unesite drzavljanstvo (opciono):")
        pol = input("    Unesite pol (m/z) (opciono):")
        if uloga_kor == konst.ULOGA_ADMIN:    #tj ako je vec ulogovan admin, to znaci da on hoce da kreira prodavce
            uloga = konst.ULOGA_PRODAVAC
        else:
            uloga = konst.ULOGA_KORISNIK
    except:
        print("\nPogresno unjete informacije!")
        ponovo = input("Unesite 1 ako zelite napustiti registraciju: ")
        if ponovo != '1':
            registracija()
        else:
            uvodna_poruka()
    azuriraj = False    #za sad ovako
    try:
        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, azuriraj, uloga, '', kor_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        korisnici.sacuvaj_korisnike('korisnik.csv', ',', svi_korisnici)
        print()
        print(f"{'Uspjesna registracija!':^40}")
        odmah_na_prijavu = input("Unesite 1 ako zelite odmah da se prijavite: ")
        if odmah_na_prijavu == '1':
            prijava_na_sistem()
        else:
            uvodna_poruka()
    except Exception as ex:
        print('\n' + str(ex))
        ponovo = input("Unesite 1 ako zelite napustiti registraciju: ")
        if ponovo != '1':
            registracija()
        else:
            uvodna_poruka()

def prijava_na_sistem():    #login
    global uloga_kor, kor_ime, ulogovan, svi_korisnici
    ucitaj_iz_fajla()
    clear()
    if ulogovan:
        print('_'*80)
        print(f"\n{'Vec ste ulogovani, prvo se morate odjaviti!':^80}")
        print('_'*80)
        sleep(1)
        uvodna_poruka()
    print('-'*40)
    print(f"\n{'Prijava':^40}")
    print('\n' + '-'*40)
    korisnicko_ime = input("\n    Unesite korisnicko ime:")
    lozinka = input("    Unesite lozinku:")
    try:
        ulogovani_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        kor_ime = ulogovani_korisnik["korisnicko_ime"]
        uloga_kor = ulogovani_korisnik['uloga']
        print()
        print (f"{'':<3}{' Uspjesno ste se ulogovali!':<40}")
        ulogovan = True
        sleep(1.3)
        uvodna_poruka()
    except Exception as x:
        print('\n' + str(x))
        dalja_prijava = input("\nUnesite 1 ako zelite da odustanete od prijave: ")
        if dalja_prijava != '1':
            prijava_na_sistem()
        else:
            uvodna_poruka() 

def odjava():
    global uloga_kor, kor_ime, ulogovan
    clear()
    print('-'*65)
    print(f"\n{'Odjava':^55}")
    print('\n' + '-'*65)
    zelis_li_se_odjaviti = input("Da li zelite da se odjavite iz aplikacije? (da/ne) ").lower()
    if zelis_li_se_odjaviti == 'da':
        ulogovan = False
        uloga_kor = ''
        kor_ime = ''
        clear()
        uvodna_poruka()
    elif zelis_li_se_odjaviti == 'ne':
        sleep(0.5)
        uvodna_poruka()
    else:
        print("Nevalidan unos, unesite pravilno!")
        sleep(1)
        clear()
        odjava()

def izlaz():
    clear()
    print('_'*80)
    print (f"\n{'Hvala sto ste izabrali nasu aplikaciju!':^80}")
    print('_'*80)
    sleep(10)
    exit()

#--------------------------------------------------------------------------------------------main
uvodna_poruka()
