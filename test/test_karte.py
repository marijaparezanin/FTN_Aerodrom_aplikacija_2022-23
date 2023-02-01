import os
import unittest
import copy

from karte import karte
from letovi import letovi
from test.test_utils import *
import random
from datetime import datetime

class KarteTest(unittest.TestCase):
    def setUp(self):
        self.modeli_aviona = {
            123: {
                "id": 123,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicije_sedista": rand_seat_positions()
            },
            124: {
                "id": 124,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicije_sedista": rand_seat_positions()
            }
        }

        dani = list({random.randint(0, 6): True for n in range(random.randint(1, 7))}.keys())
        dani.sort()
        broj_leta = rand_str(4)
        self.pun_let = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": rand_str(3), #pitanje, da li je u redu da stavim ovako nazive, ili nekako drugacije?
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),#pitanje, da li je u redu da stavim ovako vreme, ili nekako drugacije?
            "vreme_sletanja": rand_time_str(),
            "sletanje_sutra": False,
            "prevoznik": rand_str(10),
            "dani": dani,
            "model": self.modeli_aviona[123],
            "cena": 100 + random.random() * 200
        }
        self.pun_korisnik = rand_valid_user()

        self.svi_letovi = {
            broj_leta: self.pun_let
        }

        self.konkretan_let = {
            "sifra": 1234,
            "broj_leta": broj_leta,
            "datum_i_vreme_polaska": rand_date_str(),
            "datum_i_vreme_dolaska": rand_date_str()
        }

        self.svi_konkretni_letovi = {
            self.konkretan_let["sifra"]: self.konkretan_let
        }

        pozicije_sedista = self.modeli_aviona[123]["pozicije_sedista"]
        odabrano_sediste = rand_seat(
            self.modeli_aviona[123]["broj_redova"],
            len(pozicije_sedista)-1
        )

        self.puna_karta = {
            "broj_karte": 1,
            "sifra_leta": 1234, #sifra konkretnog leta
             "sifra_konkretnog_leta": 1234,
            "kupac": rand_str(10), # k ime od kupca
            "prodavac": rand_str(10),
            "sifra_sedista": odabrano_sediste,
            "datum_prodaje": rand_date_str(end=self.konkretan_let['datum_i_vreme_polaska']),
            "obrisana": False
        }

        self.putanja = "test_karte.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kupovina_validna(self):
        konkretan_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(),
            "datum_i_vreme_dolaska": rand_datetime(),
        }
        svi_konkretni_letovi = {
            konkretan_let["sifra"]: konkretan_let
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretan_let)

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_KORISNIK
        }
        prodavac = {
            "id": 111,
            "uloga": konstante.ULOGA_PRODAVAC
        }
        ocekivana_karta = {
            "broj_karte": karte.sledeci_broj_karte,
            "putnici": [korisnik],
            "sifra_konkretnog_leta": konkretan_let["sifra"],
            "status": konstante.STATUS_NEREALIZOVANA_KARTA,
            "kupac": korisnik,
            "prodavac": prodavac,
            "datum_prodaje": datetime.now(),
            "obrisana": False
        }
        karta, sve_karte = karte.kupovina_karte(
            {},
            svi_konkretni_letovi,
            konkretan_let["sifra"],
            [korisnik],
            letovi.matrica_zauzetosti(konkretan_let),
            korisnik,
            prodavac=ocekivana_karta["prodavac"],
            datum_prodaje=ocekivana_karta["datum_prodaje"]
        )
        self.assertEqual(ocekivana_karta, karta, "Karta nije kreirana")
        self.assertIn(karta["broj_karte"], sve_karte, "Karta nije dodata u sve karte")
        self.assertEqual(sve_karte[karta["broj_karte"]], karta, "Karta u svim kartama nije ona koja se očekuje")


    def test_kupovina_nema_mesta(self):
        konkretan_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(),
            "datum_i_vreme_dolaska": rand_datetime(),
        }
        svi_konkretni_letovi = {
            konkretan_let["sifra"]: konkretan_let
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretan_let)

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_KORISNIK
        }
        with self.assertRaises(Exception, msg=f"Nema mesta"):
            karte.kupovina_karte(
                {},
                svi_konkretni_letovi,
                konkretan_let["sifra"],
                [korisnik],
                [[True for _ in podlista] for podlista in letovi.matrica_zauzetosti(konkretan_let)],
                korisnik
            )

    def test_kupovina_nevalidne_uloga(self):
        konkretan_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(),
            "datum_i_vreme_dolaska": rand_datetime(),
        }
        svi_konkretni_letovi = {
            konkretan_let["sifra"]: konkretan_let
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretan_let)

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_PRODAVAC
        }
        with self.assertRaises(Exception, msg=f"Prodavac ne može da kupi kartu"):
            karte.kupovina_karte(
                {},
                svi_konkretni_letovi,
                konkretan_let["sifra"],
                [korisnik],
                letovi.matrica_zauzetosti(konkretan_let),
                korisnik
            )

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_ADMIN
        }
        with self.assertRaises(Exception, msg=f"Admin ne može da kupi kartu"):
            karte.kupovina_karte(
                {},
                svi_konkretni_letovi,
                konkretan_let["sifra"],
                [korisnik],
                letovi.matrica_zauzetosti(konkretan_let),
                korisnik
            )

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_KORISNIK
        }
        with self.assertRaises(Exception, msg=f"Prodavac mora da proda kartu"):
            karte.kupovina_karte(
                {},
                svi_konkretni_letovi,
                konkretan_let["sifra"],
                [korisnik],
                letovi.matrica_zauzetosti(konkretan_let),
                korisnik,
                prodavac=korisnik
            )

    def test_kupovina_nepostojeci_let(self):
        konkretan_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(),
            "datum_i_vreme_dolaska": rand_datetime(),
        }
        svi_konkretni_letovi = {
            konkretan_let["sifra"]: konkretan_let
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretan_let)

        korisnik = {
            "id": 123,
            "uloga": konstante.ULOGA_KORISNIK
        }
        with self.assertRaises(Exception, msg=f"Provera za nepostojeći let"):
            karte.kupovina_karte(
                {},
                svi_konkretni_letovi,
                321,
                [korisnik],
                letovi.matrica_zauzetosti(konkretan_let),
                korisnik
            )

    def test_pretraga_nerealizovanih_karata(self):
        sve_karte = [
            {
                "broj_karte": 1,
                "putnici": [self.pun_korisnik, {"korisnicko_ime": rand_str(10)}],
                "konretni_let": self.konkretan_let,
                "status": konstante.STATUS_NEREALIZOVANA_KARTA
            },
            {
                "broj_karte": 1,
                "putnici": [self.pun_korisnik, {"korisnicko_ime": rand_str(10)}],
                "konretni_let": self.konkretan_let,
                "status": konstante.STATUS_REALIZOVANA_KARTA
            },
            {
                "broj_karte": 2,
                "putnici": [{"korisnicko_ime": rand_str(10)}, {"korisnicko_ime": rand_str(10)}],
                "konretni_let": self.konkretan_let,
                "status": konstante.STATUS_NEREALIZOVANA_KARTA
            },
        ]

        ocekivane_karte = [
            sve_karte[0]
        ]
        nerealizovane_karte = karte.pregled_nerealizovanaih_karata(self.pun_korisnik, sve_karte)
        self.assertListEqual(ocekivane_karte, nerealizovane_karte)


    def test_brisanje_karte_prodavac(self):
        karta = copy.deepcopy(self.puna_karta)
        ocekivana_karta = copy.deepcopy(karta)
        ocekivana_karta["obrisana"] = True

        broj_karte = self.puna_karta["broj_karte"]
        sve_karte = karte.brisanje_karte(
            {"uloga": konstante.ULOGA_PRODAVAC},
            {broj_karte: self.puna_karta},
            self.puna_karta["broj_karte"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            ocekivana_karta,
            sve_karte[karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_brisanje_karte_admin(self):
        karta = copy.deepcopy(self.puna_karta)
        ocekivana_karta = copy.deepcopy(karta)
        ocekivana_karta["obrisana"] = True

        broj_karte = self.puna_karta["broj_karte"]
        sve_karte = karte.brisanje_karte(
            {"uloga": konstante.ULOGA_ADMIN},
            {broj_karte: self.puna_karta},
            self.puna_karta["broj_karte"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertTrue(broj_karte not in sve_karte)

    def test_brisanje_karte_nevalidni_slucajevi(self):
        broj_karte = self.puna_karta["broj_karte"]
        with self.assertRaises(Exception, msg=f"Običan korisnik ne može da obriše kartu"):
            karte.brisanje_karte(
                {"uloga": konstante.ULOGA_KORISNIK},
                {broj_karte: self.puna_karta},
                self.puna_karta["broj_karte"]
            )
        with self.assertRaises(Exception, msg=f"Brisanje nepostojeće karte"):
            karte.brisanje_karte(
                {"uloga": konstante.ULOGA_PRODAVAC},
                {broj_karte: random.randint(10, 100)},
                self.puna_karta["broj_karte"]
            )

    def testiraj_karte_fajl(self):
        odaberi_sediste = lambda : rand_seat(100, ord('H') - ord('A'))
        prodavac = rand_valid_user()
        prodavac["uloga"] = konstante.ULOGA_PRODAVAC
        kupac = rand_valid_user()
        referentne_karte = {
            i: {
                "broj_karte": i,
                "sifra_konkretnog_leta": random.randint(1000, 10000),
                "kupac": rand_valid_user(),  # k ime od kupca
                "prodavac": prodavac,
                "sediste": odaberi_sediste(),
                "datum_prodaje": rand_date_str(end=self.konkretan_let['datum_i_vreme_polaska']),
                "obrisana": False,
                "putnici": [kupac] + [rand_valid_user() for _ in range(3)]
            } for i in range(100)
        }
        karte.sacuvaj_karte(referentne_karte, self.putanja, "|")
        ucitane_karte = karte.ucitaj_karte_iz_fajla(self.putanja, "|")
        self.assertIsNotNone(ucitane_karte, msg="Nisu učitane karte iz fajla")
        self.assertEqual(len(referentne_karte), len(ucitane_karte), msg="Dužine učitanih karata nisu jednake")
        for k in ucitane_karte:
            ucitana_karta = ucitane_karte[k]
            self.assertDictEqual(referentne_karte[k], ucitana_karta, msg="Učitane karte se ne poklapaju")

    def test_izmena_karte(self):
        karta = copy.deepcopy(self.puna_karta)
        ocekivana_karta = copy.deepcopy(karta)
        ocekivana_karta["obrisana"] = True

        nov_konkretan_let = {
            "sifra": self.konkretan_let["sifra"]+1,
            "broj_leta": rand_str(4),
            "datum_i_vreme_polaska": rand_date_str(),
            "datum_i_vreme_dolaska": rand_date_str()
        }
        self.svi_konkretni_letovi[nov_konkretan_let["sifra"]] = nov_konkretan_let

        broj_karte = self.puna_karta["broj_karte"]
        sve_karte = karte.izmena_karte(
            {broj_karte: self.puna_karta},
            self.svi_konkretni_letovi,
            self.puna_karta["broj_karte"],
            nov_konkretan_let["sifra"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertTrue(broj_karte in sve_karte)

    def test_izmena_karte_datum_polaska(self):
        karta = copy.deepcopy(self.puna_karta)
        ocekivana_karta = copy.deepcopy(karta)
        ocekivana_karta["obrisana"] = True

        nov_konkretan_let = {
            "sifra": self.konkretan_let["sifra"]+1,
            "broj_leta": rand_str(4),
            "datum_i_vreme_polaska": rand_date_str(),
            "datum_i_vreme_dolaska": rand_date_str()
        }
        self.svi_konkretni_letovi[nov_konkretan_let["sifra"]] = nov_konkretan_let

        broj_karte = self.puna_karta["broj_karte"]
        sve_karte = karte.izmena_karte(
            {broj_karte: self.puna_karta},
            self.svi_konkretni_letovi,
            self.puna_karta["broj_karte"],
            None,
            nov_konkretan_let["datum_i_vreme_polaska"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertTrue(broj_karte in sve_karte)

if __name__ == '__main__':
    unittest.main()
