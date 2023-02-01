import os
import unittest
import copy
import random

from model_aviona import model_aviona
from test.test_utils import rand_str, rand_valid_model_aviona, gen_rand_valid_model_aviona


class ModelMvionaTest(unittest.TestCase):
    def setUp(self):
        self.pun_model_aviona = rand_valid_model_aviona()
        self.putanja = "test_model_aviona.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_validan_model_aviona(self):
        model = copy.deepcopy(self.pun_model_aviona)
        svi_modeli_aviona = model_aviona.kreiranje_modela_aviona(
            {},
            self.pun_model_aviona["naziv"],
            self.pun_model_aviona["broj_redova"],
            self.pun_model_aviona["pozicije_sedista"])
        model["id"]=svi_modeli_aviona[0]["id"]
        self.assertIsNotNone(svi_modeli_aviona, msg="Nije vraćena kolekcija modela")
        self.assertEqual(1, len(svi_modeli_aviona.keys()), msg="Model nije u kolekciji")
        for k in svi_modeli_aviona.keys():
            for km in svi_modeli_aviona[k]:
                self.assertEqual(model[km], svi_modeli_aviona[k][km], msg=f"key {km}")
            self.assertDictEqual(
                model,
                svi_modeli_aviona[k],
                msg="Vrednosti od modela nisu dobre"
            )


    def test_kreiraj_prazni(self):
        # Prodji kroz sve kljuceve, postavi jedan na None, pa pozovi funkciju
        for key in self.pun_model_aviona:
            if key == "id":
                continue
            model = copy.deepcopy(self.pun_model_aviona)
            model[key] = None
            with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: {key}"):
                model_aviona.kreiranje_modela_aviona(
                    {},
                    model["naziv"],
                    model["broj_redova"],
                    model["pozicije_sedista"]
                   )

    def test_kreiraj_modela_prazan_string(self):
        with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: naziv"):
            model_aviona.kreiranje_modela_aviona(
                {},
                "",
                self.pun_model_aviona["broj_redova"],
                self.pun_model_aviona["pozicije_sedista"]
            )

    def testiraj_aerodromi_fajl(self):
        referentni_modeli = {
            aerodrom["id"]: aerodrom for aerodrom in gen_rand_valid_model_aviona(10)
        }
        model_aviona.sacuvaj_modele_aviona(self.putanja, "|", referentni_modeli)

        ucitani_modeli = model_aviona.ucitaj_modele_aviona(self.putanja, "|")
        self.assertIsNotNone(ucitani_modeli, msg="Nisu učitani aerodromi iz fajla")
        self.assertEqual(len(referentni_modeli), len(ucitani_modeli),
                         msg="Dužine učitanih aerodroma nisu jednake")
        for id in ucitani_modeli:
            ucitan_aerodrom = ucitani_modeli[id]
            self.assertDictEqual(referentni_modeli[id], ucitani_modeli[id],
                                 msg="Učitani aerodromi se ne poklapaju")

if __name__ == '__main__':
    unittest.main()
