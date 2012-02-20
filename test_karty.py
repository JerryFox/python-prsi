# -*- coding: utf-8 -*-

import unittest

from karty import Balik, Hra, Hrac


class TestPrsi(unittest.TestCase):
    def setUp(self):
        self.b = Balik(32)
        self.b.zamichej()
        self.hra = Hra("prsi")
        self.h1 = Hrac("jarda")
        self.h2 = Hrac("carda")
        self.h1.do_hry(self.hra)
        self.h2.do_hry(self.hra)
        self.hra.balik(self.b)
        self.hra.stav_hry = "zacatek_hry"
        self.hra.rozdej_karty()

    def test_hrac_ma_rozdano(self):
        for h in self.hra.hraci:
            self.assertEqual(4, len(h.karty))

    def test_balik_ma_spravny_pocet_karet(self):
        self.assertEqual(32, self.b._pocet)
        self.assertEqual("mariasky", self.b.info)

    def test_michani(self):
        ibalik = Balik(32)
        nezamich_karty = ibalik.karty[:]
        ibalik.zamichej()
        zamich_karty = ibalik.karty[:]
        # zamichane a nezamichane karty - ruzne seznamy
        # (teoreticky by ty seznamy mohly byt stejne)
        self.assertNotEqual(nezamich_karty, zamich_karty)
        # setridene nezamichane a zamichane - stejne seznamy
        nezamich_karty.sort()
        zamich_karty.sort()
        self.assertEqual(nezamich_karty, zamich_karty)

    def test_rozdavani_karet(self):
        rozdane_karty = []  # seznam rozdaných karet jednotlivých hráčů
        for i in range(len(self.hra.hraci)):
            rozdane_karty.append([])
            rozdane_karty[i].append(self.hra.hraci[i].karty)
        self.hra._seber_karty()
        ikarty = self.hra.balik().karty[:]
        ikarty.sort()
        for i in range(10):
            self.hra.rozdej_karty()
            for i in range(len(self.hra.hraci)):
                # otestovat, že má hráč jiné karty než
                # v předešlých hrách
                for k in rozdane_karty[i]:
                    self.assertNotEqual(self.hra.hraci[i].karty, k)
                rozdane_karty[i].append(self.hra.hraci[i].karty)
        self.hra._seber_karty()
        self.hra.balik().karty.sort()
        self.assertEqual(ikarty, self.hra.balik().karty)

    def test_poradi_hracu(self):
        """otestovat, ze ma kazdy hrac jine poradi v rozsahu
        0 - <pocet hracu - 1>"""
        iporadi = []
        for h in self.hra.hraci:
            iporadi.append(h.poradi())
        iporadi.sort()
        self.assertEqual(iporadi, list(range(len(self.hra.hraci))))

