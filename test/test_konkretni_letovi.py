import os
import unittest
import copy
import random

from datetime import datetime, timedelta

from random import randint

from konkretni_letovi import konkretni_letovi
from test.test_utils import rand_str, rand_valid_konkretan_let, gen_rand_valid_konkretan_let,  rand_str, rand_valid_user, rand_time_str, rand_seat_positions, rand_datetime


class KonkretanLetTest(unittest.TestCase):
    def setUp(self):

        broj_leta = rand_str(2) + str(randint(10, 99))
        dani = list({random.randint(0, 6): True for n in range(random.randint(1, 7))}.keys())
        dani.sort()

        pocetak = rand_datetime()
        self.pun_let = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
            "datum_pocetka_operativnosti": pocetak,
            "datum_kraja_operativnosti": pocetak+ timedelta(days = 7),
            "sletanje_sutra": False,
            "prevoznik": rand_str(10),
            "dani": dani,
        }
        vreme = int(self.pun_let["vreme_poletanja"].split(":")[0]) * 60 + int(self.pun_let["vreme_poletanja"].split(":")[1])
        self.pun_konkretan_let = {
            "sifra": random.randint(0,100),
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": self.pun_let["datum_pocetka_operativnosti"] - timedelta(minutes=self.pun_let["datum_pocetka_operativnosti"].minute) - timedelta(hours=self.pun_let["datum_pocetka_operativnosti"].hour) + timedelta(minutes=vreme),
            "datum_i_vreme_dolaska": self.pun_let["datum_pocetka_operativnosti"]
        }
        self.putanja = "test_konkretan_let.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_validan_konkretan_let(self):
        konkretan_let = copy.deepcopy(self.pun_konkretan_let)
        svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(
            {},
            self.pun_let)
        konkretan_let["sifra"]=svi_konkretni_letovi[list(svi_konkretni_letovi.keys())[0]]["sifra"]
        self.assertIsNotNone(svi_konkretni_letovi, msg="Nije vraćena kolekcija konkretnih letova")
        self.assertEqual(len(self.pun_let["dani"]), len(svi_konkretni_letovi.keys()), msg="let nije u kolekciji")
        self.assertIn(konkretan_let["sifra"], svi_konkretni_letovi, msg="nedostaje let")
        self.assertEqual(konkretan_let["broj_leta"],  svi_konkretni_letovi[konkretan_let["sifra"]]["broj_leta"])
        self.assertEqual(konkretan_let["datum_i_vreme_polaska"].hour,
                         svi_konkretni_letovi[konkretan_let["sifra"]]["datum_i_vreme_polaska"].hour, msg="Nisu dobro sati")
        self.assertEqual(konkretan_let["datum_i_vreme_polaska"].minute,
                         svi_konkretni_letovi[konkretan_let["sifra"]]["datum_i_vreme_polaska"].minute, msg="Nisu dobro minuti")


    def testiraj_konkretan_let_fajl(self):
        referentni_konkretni_letovi = {
            let["sifra"]: let for let in gen_rand_valid_konkretan_let(10)
        }
        konkretni_letovi.sacuvaj_kokretan_let(self.putanja, "|", referentni_konkretni_letovi)

        ucitani_letovi = konkretni_letovi.ucitaj_konkretan_let(self.putanja, "|")
        self.assertIsNotNone(ucitani_letovi, msg="Nisu učitani konkretni letovi iz fajla")
        self.assertEqual(len(referentni_konkretni_letovi), len(ucitani_letovi),
                         msg="Dužine učitanih konkretnih letova nisu jednake")
        for id in ucitani_letovi:
            '''ucitan_aerodrom = ucitani_letovi[id]
            referentni_konkretni_letovi = {
                let["sifra"]: let for let in gen_rand_valid_konkretan_let(10)
            }
            konkretni_letovi.sacuvaj_kokretan_let(self.putanja, "|", referentni_konkretni_letovi)'''

            ucitani_letovi = konkretni_letovi.ucitaj_konkretan_let(self.putanja, "|")
            self.assertIsNotNone(ucitani_letovi, msg="Nisu učitani konkretni letovi iz fajla")
            self.assertEqual(len(referentni_konkretni_letovi), len(ucitani_letovi),
                             msg="Dužine učitanih konkretnih letova nisu jednake")

            self.assertEqual(referentni_konkretni_letovi[id]["broj_leta"], ucitani_letovi[id]["broj_leta"],
                             msg="Učitani konkretni letovi se ne poklapaju")
            self.assertEqual(referentni_konkretni_letovi[id]["datum_i_vreme_dolaska"],
                             ucitani_letovi[id]["datum_i_vreme_dolaska"],
                             msg="Učitani konkretni letovi se ne poklapaju")
            self.assertEqual(referentni_konkretni_letovi[id]["datum_i_vreme_polaska"],
                             ucitani_letovi[id]["datum_i_vreme_polaska"],
                             msg="Učitani konkretni letovi se ne poklapaju")
            self.assertEqual(referentni_konkretni_letovi[id]["sifra"], ucitani_letovi[id]["sifra"],
                             msg="Učitani konkretni letovi se ne poklapaju")


if __name__ == '__main__':
    unittest.main()
