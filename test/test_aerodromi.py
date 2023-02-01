import os
import unittest
import copy
import random

from aerodromi import aerodromi
from test.test_utils import rand_str, rand_valid_aerodrom, gen_rand_valid_aerodrom


class AerodromTest(unittest.TestCase):
    def setUp(self):
        self.pun_aerodrom = rand_valid_aerodrom()
        self.putanja = "test_aerodrom.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_validan_aerodrom(self):
        aerodrom_sa_novim_id = copy.deepcopy(self.pun_aerodrom)
        svi_aerodromi = aerodromi.kreiranje_aerodroma(
            {},
            self.pun_aerodrom["skracenica"],
            self.pun_aerodrom["pun_naziv"],
            self.pun_aerodrom["grad"],
            self.pun_aerodrom["drzava"])
        self.assertIsNotNone(svi_aerodromi, msg="Nije vraćena kolekcija aerodroma")
        self.assertEqual(1, len(svi_aerodromi.keys()), msg="Aerodrom nije u kolekciji")
        for k in svi_aerodromi.keys():
            self.assertDictEqual(
                self.pun_aerodrom,
                svi_aerodromi[k],
                msg="Vrednosti od aerodroma nisu dobre"
            )


    def test_kreiraj_prazni(self):
        # Prodji kroz sve kljuceve, postavi jedan na None, pa pozovi funkciju
        for key in self.pun_aerodrom:
            aerodrom = copy.deepcopy(self.pun_aerodrom)
            aerodrom[key] = None
            with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: {key}"):
                aerodromi.kreiraj_aerodrom(
                    {},
                    aerodrom["skracenica"],
                    aerodrom["pun_naziv"],
                    aerodrom["grad"],
                    aerodrom["drzava"],
                   )

    def test_kreiraj_aerodrom_prazan_string(self):
        # Prodji kroz sve kljuceve, postavi jedan na None, pa pozovi funkciju
        for key in self.pun_aerodrom:
            aerodrom = copy.deepcopy(self.pun_aerodrom)
            aerodrom[key] = ""
            with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: {key}"):
                aerodromi.kreiranje_aerodroma(
                    {},
                    aerodrom["skracenica"],
                    aerodrom["pun_naziv"],
                    aerodrom["grad"],
                    aerodrom["drzava"],
                )



    def testiraj_aerodromi_fajl(self):
        referentni_aerodromi = {
            aerodrom["skracenica"]: aerodrom for aerodrom in gen_rand_valid_aerodrom(10)
        }
        aerodromi.sacuvaj_aerodrome(self.putanja, "|", referentni_aerodromi)

        ucitani_aerodromi = aerodromi.ucitaj_aerodrom(self.putanja, "|")
        self.assertIsNotNone(ucitani_aerodromi, msg="Nisu učitani aerodromi iz fajla")
        self.assertEqual(len(referentni_aerodromi), len(ucitani_aerodromi),
                         msg="Dužine učitanih aerodroma nisu jednake")
        for id in ucitani_aerodromi:
            ucitan_aerodrom = ucitani_aerodromi[id]
            self.assertDictEqual(referentni_aerodromi[id], ucitani_aerodromi[id],
                                 msg="Učitani aerodromi se ne poklapaju")

if __name__ == '__main__':
    unittest.main()
