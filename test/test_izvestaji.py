import os
import unittest
import copy

from common import konstante
from izvestaji import izvestaji
from test.test_utils import rand_datetime, rand_str, rand_time_str
import random
import string
from datetime import date, timedelta


class IzvestajiTest(unittest.TestCase):
    def setUp(self):
        self.modeli_aviona = {
            123: {"id": 123, "naziv": "Boeing747", "broj_redova": 44, "pozicija_sedista": "A"},
            124: {"id": 124, "naziv": "Boeing748", "broj_redova": 45, "pozicija_sedista": "B"}
        }
        self.pun_let = {
            "broj_leta": rand_str(4),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
            "sletanje_sutra": False,
            "prevoznik": rand_str(10),
            "dani": [konstante.CETVRTAK, konstante.NEDELJA],
            "model": self.modeli_aviona[123],
            "cena": 200
        }

        self.konkretan_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska" : rand_datetime(),
            "datum_dolaska": rand_datetime()
        }

        self.puna_karta = {
            "broj_karte": 1,
            "sifra_konkretnog_leta": self.konkretan_let["sifra"], #sifra konkretnog leta
            "sifra":1234,
            "kupac": ''.join(random.sample(string.ascii_lowercase, 6)),
            "prodavac": ''.join(random.sample(string.ascii_lowercase, 7)),
            "sifra_sedista": "b3",
            "datum_prodaje" : rand_datetime(),
            "obrisana": False
        }

        self.putanja = "test_karte.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_uspesan_izvestaj_prodatih_karata_za_dan_prodaje(self):
        dan_prodaje = rand_datetime().date()
        karte_prodate_na_dan = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje":dan_prodaje
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_prodaje
            }
        ]
        karte_prodata_na_drugi_dan = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date()
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date()
            }
        ]
        sve_karte = []
        sve_karte.extend(karte_prodate_na_dan)
        sve_karte.extend(karte_prodata_na_drugi_dan)
        sve_karte = {
            k["broj_karte"]: k for k in sve_karte
        }
        nadjene_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(
            sve_karte,
            dan_prodaje
        )
        self.assertIsNotNone(nadjene_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(karte_prodate_na_dan, nadjene_karte, msg="Sve karte su tu")

    def test_izvestaj_prodatih_karata_za_dan_polaska(self):
        dan_polaska = rand_datetime()
        konkretni_let_na_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": dan_polaska
        }
        konkretni_let_drugi_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime()
        }
        svi_konkretni_letovi = {
            konkretni_let_na_dan["sifra"]: konkretni_let_na_dan,
            konkretni_let_drugi_dan["sifra"]: konkretni_let_drugi_dan
        }
        karte_na_dan_polaska = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_polaska,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_polaska,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            }
        ]
        karte_na_drugi_dan_polaska = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            }
        ]
        sve_karte = []
        sve_karte.extend(karte_na_dan_polaska)
        sve_karte.extend(karte_na_drugi_dan_polaska)
        sve_karte = {
            k["broj_karte"]: k for k in sve_karte
        }
        nadjene_karte = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(
            sve_karte,
            svi_konkretni_letovi,
            dan_polaska.date()
        )
        self.assertIsNotNone(nadjene_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(karte_na_dan_polaska, nadjene_karte, msg="Sve karte su tu")


    def test_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(self):
        datum_prodaje = rand_datetime().date()
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = random.randint(100, 1000)
        karta1["datum_prodaje"] = datum_prodaje
        karta1["prodavac"] =''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = datum_prodaje
        karta2["broj_karte"] = random.randint(100, 1000)

        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
             self.puna_karta["datum_prodaje"],
            self.puna_karta["prodavac"]
        )
        referentne_karte = [self.puna_karta]
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(1, len(sve_karte), msg="Nema karata")
        self.assertEqual(referentne_karte, sve_karte, msg="Sve karte su tu")

    def test_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca_neuspesan(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_i_vreme_polaska"] = rand_datetime()
        karta1["prodavac"] = ''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_i_vreme_polaska"] = karta1["datum_i_vreme_polaska"]
        karta2["broj_karte"] = 3

        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
             karta1["datum_prodaje"] + timedelta(milliseconds=3),
            ''.join(random.sample(string.ascii_lowercase, 8)),
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(0, len(sve_karte), msg="Nema karata")


    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje(self):
        dan_prodaje = rand_datetime().date()
        korisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        nekorisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        svi_letovi = {
            korisceni_let["broj_leta"]: korisceni_let,
            nekorisceni_let["broj_leta"]: nekorisceni_let
        }
        konkretni_let_na_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime(),
            "broj_leta": korisceni_let["broj_leta"]
        }
        konkretni_let_drugi_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime(),
            "broj_leta": nekorisceni_let["broj_leta"]
        }
        svi_konkretni_letovi = {
            konkretni_let_na_dan["sifra"]: konkretni_let_na_dan,
            konkretni_let_drugi_dan["sifra"]: konkretni_let_drugi_dan
        }
        karte_prodate_na_dan = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_prodaje,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_prodaje,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            }
        ]
        karte_prodate_na_drugi_dan = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            }
        ]
        sve_karte = []
        sve_karte.extend(karte_prodate_na_dan)
        sve_karte.extend(karte_prodate_na_drugi_dan)
        sve_karte = {
            k["broj_karte"]: k for k in sve_karte
        }
        broj, suma = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(
            sve_karte,
            svi_konkretni_letovi,
            svi_letovi,
            dan_prodaje
        )
        self.assertIsNotNone(broj, msg="Nije vraćen broj karata")
        self.assertIsNotNone(suma, msg="Nije vraćena suma cena")
        self.assertEqual(len(karte_prodate_na_dan), broj, msg="Broj karata")
        ocekivana_suma = len(karte_prodate_na_dan)*korisceni_let["cena"]
        self.assertEqual(ocekivana_suma, suma, msg="Broj karata")

    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje_nepostojeci_dan(self):
        dan_prodaje = rand_datetime().date()
        datum = dan_prodaje + timedelta(days=3)

        korisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        nekorisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        svi_letovi = {
            korisceni_let["broj_leta"]: korisceni_let,
            nekorisceni_let["broj_leta"]: nekorisceni_let
        }
        konkretni_let_na_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime(),
            "broj_leta": korisceni_let["broj_leta"]
        }
        konkretni_let_drugi_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime(),
            "broj_leta": nekorisceni_let["broj_leta"]
        }
        svi_konkretni_letovi = {
            konkretni_let_na_dan["sifra"]: konkretni_let_na_dan,
            konkretni_let_drugi_dan["sifra"]: konkretni_let_drugi_dan
        }

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_i_vreme_polaska"] = rand_datetime().date()
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_i_vreme_polaska"] = karta1["datum_i_vreme_polaska"]
        karta2["broj_karte"] = 3

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            svi_konkretni_letovi,
            svi_letovi,
            datum
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertEqual(0, rezultat[0], msg="")# suma
        self.assertEqual(0, rezultat[1], msg="")#broj

    def test_izvestaj_ubc_prodatih_karata_za_dan_polaska(self):
        dan_polaska = rand_datetime()
        korisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        nekorisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        svi_letovi = {
            korisceni_let["broj_leta"]: korisceni_let,
            nekorisceni_let["broj_leta"]: nekorisceni_let
        }
        konkretni_let_na_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": dan_polaska,
            "broj_leta": korisceni_let["broj_leta"]
        }
        konkretni_let_drugi_dan = {
            "sifra": rand_str(2) + str(random.randint(10, 99)),
            "datum_i_vreme_polaska": rand_datetime(),
            "broj_leta": korisceni_let["broj_leta"]
        }
        svi_konkretni_letovi = {
            konkretni_let_na_dan["sifra"]: konkretni_let_na_dan,
            konkretni_let_drugi_dan["sifra"]: konkretni_let_drugi_dan
        }
        karte_na_dan_polaska = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_polaska,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": dan_polaska,
                "sifra_konkretnog_leta": konkretni_let_na_dan["sifra"]
            }
        ]
        karte_na_drugi_dan_polaska = [
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            },
            {
                "broj_karte": random.randint(1, 10000),
                "datum_prodaje": rand_datetime().date(),
                "sifra_konkretnog_leta": konkretni_let_drugi_dan["sifra"]
            }
        ]
        sve_karte = []
        sve_karte.extend(karte_na_dan_polaska)
        sve_karte.extend(karte_na_drugi_dan_polaska)
        sve_karte = {
            k["broj_karte"]: k for k in sve_karte
        }
        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(
            sve_karte,
            svi_konkretni_letovi,
            svi_letovi,
            dan_polaska
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertEqual(2, rezultat[0], msg="")
        self.assertEqual(korisceni_let["cena"]*2, rezultat[1], msg="")

    def test_izvestaj_ubc_prodatih_karata_za_dan_polaska_neuspesan(self):
        datum = rand_datetime()
        datum2 = datum + timedelta(days=3)
        konkretan_let1 = copy.deepcopy(self.konkretan_let)
        konkretan_let1["sifra"] = 1235
        konkretan_let1["datum_i_vreme_polaska"] = datum

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2

        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        karta2["sifra_konkretnogg_leta"] = 1235

        svi_konkretni_letovi = {
            self.konkretan_let["sifra"]: self.konkretan_let,
            konkretan_let1["sifra"]: konkretan_let1
        }

        korisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        nekorisceni_let = {
            "broj_leta": rand_str(2) + str(random.randint(10, 99)),
            "cena": random.randint(100, 1000)
        }
        svi_letovi = {
            korisceni_let["broj_leta"]: korisceni_let,
            nekorisceni_let["broj_leta"]: nekorisceni_let
        }

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            svi_konkretni_letovi,
            svi_letovi,
            datum2
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertEqual(0, rezultat[0], msg="")
        self.assertEqual(0, rezultat[1], msg="")


    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(self):
        karta1 = copy.deepcopy(self.puna_karta)
        datum = rand_datetime()
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = datum
        karta1["prodavac"] = ''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = datum
        karta2["prodavac"] = karta1["prodavac"]
        karta2["broj_karte"] = 3
        ukupna_cena = self.pun_let["cena"] *2
        sve_karte = {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2}

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
            sve_karte,
            {self.konkretan_let["sifra"]:self.konkretan_let},
            {self.pun_let["broj_leta"]: self.pun_let},
            datum,
            karta1["prodavac"]
        )

        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertEqual(2, rezultat[0], msg="")
        self.assertEqual(ukupna_cena, rezultat[1], msg="")


    def test_izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(self):
        today = date.today()
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = today.strftime("%d.%m.%Y.")
        karta1["prodavac"] = rand_str(5),
        karta1["prodavac"] = karta1["prodavac"][0]
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = today.strftime("%d.%m.%Y.")
        karta2["broj_karte"] = 3

        sve_karte = {self.puna_karta["broj_karte"]: self.puna_karta,
                     karta1["broj_karte"]: karta1,
                     karta2["broj_karte"]: karta2}

        self.puna_karta["datum_prodaje"] = today.strftime("%d.%m.%Y.")

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
            sve_karte,
            {self.konkretan_let["sifra"]: self.konkretan_let},
            {self.pun_let["broj_leta"]: self.pun_let}

        )

        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat.values()), msg="")
        for elem in rezultat.values():
            if karta1["prodavac"] == elem[2]:
                self.assertEqual(200, elem[1], msg="Lose izracunata ukupna cena")
            else:
                self.assertEqual(400, elem[1], msg="Lose izracunata ukupna cena")