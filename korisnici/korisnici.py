import common.konstante
from common import konstante
import csv 
"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    greska = 'Korisnicko ime vec postoji'

    for i in svi_korisnici: #da li novi korisnik unosi zauzeto postojece korime
        if svi_korisnici[i]['korisnicko_ime'] == korisnicko_ime:
           raise Exception("Postojece korisnicko ime")
           # return greska
    
    if azuriraj == True:
        if staro_korisnicko_ime in svi_korisnici:
                svi_korisnici[korisnicko_ime] = {}    
                svi_korisnici[korisnicko_ime]['korisnicko_ime'] = (korisnicko_ime) 
                svi_korisnici[korisnicko_ime]['lozinka'] = (lozinka)
                svi_korisnici[korisnicko_ime]['ime'] = (ime)   
                svi_korisnici[korisnicko_ime]['prezime'] = (prezime)
                svi_korisnici[korisnicko_ime]['uloga'] = (uloga)
                svi_korisnici[korisnicko_ime]['pasos'] = (str(pasos))   #nakon provjere da ga vratim u string
                svi_korisnici[korisnicko_ime]['drzavljanstvo'] = (drzavljanstvo)
                svi_korisnici[korisnicko_ime]['telefon'] = (str(telefon))
                svi_korisnici[korisnicko_ime]['email'] = (email)
                svi_korisnici[korisnicko_ime]['pol'] = (pol)
                return svi_korisnici
        #return greska #ako staro korisnicko ime nije medju kor imenima
        raise Exception("Postojece korisnicko ime")

    greska = 'Niste unjeli prave informacije za korisnika'
    if uloga == 'korisnik':     #ako je korisnik onda sve informacije moraju biti tu
        if azuriraj is None:
            raise Exception("Provera za nedostajucu vrednost: azuriraj")
        if ime is None:
            raise Exception("Provera za nedostajucu vrednost: ime")
        if prezime is None:
            raise Exception("Provera za nedostajucu vrednost: prezime")
        if korisnicko_ime is None:
            raise Exception("Provera za nedostajucu vrednost: korisnicko_ime")
        if lozinka is None:
            raise Exception("Provera za nedostajucu vrednost: lozinka")
        if email is None:
            raise Exception("Provera za nedostajucu vrednost: email")
        if telefon is None:
            raise Exception("Provera za nedostajucu vrednost: telefon")
        '''if drzavljanstvo is None:
            raise Exception("Provera za nedostajucu vrednost: drzavljanstvo")'''
        """ if pol is None:
            raise Exception("Provera za nedostajucu vrednost: pol")"""
        if uloga is None:
            raise Exception("Provera za nedostajucu vrednost: uloga")
        """        if pasos is None:
            raise Exception("Provera za nedostajucu vrednost: pasos")"""       
    else:   #ako je neka druga uloga onda vise informacija smiju biti prazne
        if azuriraj is None:    
            return greska
        if ime is None:
            return greska
        if prezime is None:
            return greska
        if korisnicko_ime is None:
            return greska
        if lozinka is None:
            return greska
        if uloga is None:
            raise Exception("Provera za nedostajucu vrednost: uloga")
            #return greska

    if uloga != 'korisnik' and uloga != 'admin' and uloga != 'prodavac':
        greska = 'Uloga nije validna'
        raise Exception("Broj telefona nebrojevni string")
        #return greska
        
    if email.count('@') == 1:   #mora imati @
        pomoc1 = email.split('.')   #marija@g   h
        pomoc2 = pomoc1[0].split('@')   #marija g
        if len(str(pomoc1[1]))== 0 or len(str(pomoc2[1])) == 0:
            greska = 'Pogresan email'
            raise Exception("Email provera bez @")
            #return greska
        if email.count('.') !=1:    #ne smje imati vise domena npr .gmail.com.yahoo
            greska = 'Pogresan email'
            raise Exception("Email provera bez @")
           #return greska
    else:
        greska = 'Pogresan email'
        raise Exception("Email provera bez @")
        #return greska    

    try:
        telefon = int(telefon)
    except:
        greska = 'Pogresno unjet telefon'
        raise Exception("Broj telefona nebrojevni string")
        #return greska
    if pasos != '':
        if len(str(pasos)) != 9:
            greska = 'Pogresno unjet pasos'
            raise Exception("Pasoš manje od 9 cifara")
            #return greska 
        
        try:
            pasos = int(pasos)  #da li je pasos broj
        except:
            greska = 'Pogresno unjet pasos'
            raise Exception("Pasos nebrojevni string")
            #return greska
    
    if azuriraj == False:
        svi_korisnici[korisnicko_ime] = {}    
        svi_korisnici[korisnicko_ime]['korisnicko_ime'] = (korisnicko_ime) 
        svi_korisnici[korisnicko_ime]['lozinka'] = (lozinka)
        svi_korisnici[korisnicko_ime]['ime'] = (ime)   
        svi_korisnici[korisnicko_ime]['prezime'] = (prezime)
        svi_korisnici[korisnicko_ime]['uloga'] = (uloga)
        svi_korisnici[korisnicko_ime]['pasos'] = (str(pasos))   #nakon provjere da ga vratim u string
        svi_korisnici[korisnicko_ime]['drzavljanstvo'] = (drzavljanstvo)
        svi_korisnici[korisnicko_ime]['telefon'] = (str(telefon))
        svi_korisnici[korisnicko_ime]['email'] = (email)
        svi_korisnici[korisnicko_ime]['pol'] = (pol)
        return svi_korisnici

"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    korisnici_lista = []    #moram dictionary prebaciti u listu
    for korisnicko_ime in svi_korisnici:
        korisnik = svi_korisnici[korisnicko_ime]
        korisnici_lista.append(korisnik)
    file = open(putanja, 'w')
    writer = csv.DictWriter(file, korisnici_lista[0], delimiter = separator)
    writer.writeheader()
    writer.writerows(korisnici_lista)
    file.close()


"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    svi_korisnici = {}
    file = open(putanja, 'r')
    reader = csv.DictReader(file, delimiter = separator)
    for korisnik in reader: #korisnik je linija
        korisnicko_ime = korisnik['korisnicko_ime'] #sve linije koje su kor ime nek budu key
        svi_korisnici[korisnicko_ime] = korisnik    
    file.close()
    return svi_korisnici


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
log = 0
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    global log
    greska = 'Korisnikove vrednosti nisu dobre'
    for i in svi_korisnici: #i je red
        if svi_korisnici[i]['korisnicko_ime'] == korisnicko_ime:
            if svi_korisnici[i]['lozinka'] == lozinka:
                log = svi_korisnici[i]
                return svi_korisnici[i]    #i je citav red korisnika
    #return greska
    raise Exception("Login nepostojeći")  

"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    log = 0     #resetujem na 0
    pass

