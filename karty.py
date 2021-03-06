# -*- coding: utf-8 -*-
# pokusny komentar

import random
import inspect

class Balik:
    """Balíček karet se kterým se hraje,
asi ho bude standardně vytvářet nějaká funkce objektu Hra.
Při vytváření objektu se předá počet karet - 32, 52, 104, 108 listů"""
    def __init__(self, pocet):
        self.pocet_karet(pocet)
            
        
    def pocet_karet(self, pocet=None):
        if pocet is not None:
            # nastavit nový počet karet v balíku
            self.karty = []
            if pocet == 32:
                self.info = "mariasky"
                self._vloz_mariasky()
                self._pocet = pocet
            else:
                self._pocet = 0
        return self._pocet

    def _vloz_mariasky(self):
        point = 0
        for barva in ["CE","ZE","ZA","KU"]:
            for hodnota in range(7,15):
                self.karty.append([barva,hodnota])
                
    def zamichej(self):
        # zamíchání karet v balíku
        pomkarty = self.karty[:]
        self.karty = []
        while len(pomkarty) > 0:
            # náhodný výběr karty a přesun do balíku
            i = random.randint(0, len(pomkarty) - 1)
            self.karty.append(pomkarty[i])
            pomkarty.remove(pomkarty[i])
            
class Hrac:
    """Účastník hry"""
    def __init__(self, jmeno):
        self.jmeno(jmeno)
        self.karty = []
        self._hra = None        # aktuální hra 
        self._poradi = None     # pořadí hráče: 0 = forhont
        self._typ = "auto"      # typ hráče: "auto", "manual"

    def jmeno(self, jmeno=None):
        """Zjištění - nastavení jména hráče"""
        if jmeno is not None:
            self._jmeno = jmeno
        return self._jmeno

    def hra(self, hra=None):
        """zaregistrování hráče do hry"""
        # kontrola, jestli se pokouší vlézt do validní hry
        if hra.__class__.__name__ == "Hra" and \
                       self._hra is None:
            i = hra.hra(self)
            if i.__class__.__name__ == "int":
                self._hra = hra
                self._poradi = i
        return self._hra

    def poradi(self, poradi=None):
        # zjištění - nastavení pořadí hráče - měla by to dělat jenom inst. Hra
        if poradi.__class__.__name__ == "int":
            self._poradi = poradi
        return self._poradi

    def hraj(self):
        # kontrola, jestli je hrac opravnen hrat
        ireturn = False
        if self.hra().token() == self:
            ireturn = True
            # hrac odehraje a vrati token sve hre
            self.hra().token(self.hra())
        return ireturn

    def odevzdat_token(self):
        self.hra().prevzit_token()
    
class Hra:
    """Hra, informace o hre"""
    def __init__(self, nazev, typ="prsi"):
        self.pocet_hracu = 0
        self.hraci = []
        self._jmeno = nazev
        self.stav_hry = "prihlasovani_hracu"
        self.typ_hry = typ
        self._balik = None
        self._odehrane = []
        self._aktbarva = None
        self._akthodnota = None
        self._poradi_hracu = []
        self._pocet_karet = 4
        self._rozdavat_po = 2
        self._stouchy = []      # průběh hry (hráč, vynesené karty,
                                # líznuté karty, renoncy)
        self._token = self      # kdo je aktivni v dane hre
        self._last_player = None # naposledy hrajici hrac 

    def hra(self, hrac):
        """Přidá hráče do hry - vrátí jeho index"""
        # kontrola, jestli je objekt instancí třídy Hrac
        if hrac.__class__.__name__ == "Hrac":
            # kontrola, jestli už hráč není ve hře
            if self.hraci.count(hrac) == 0:
                # kontrola, jestli je hra v přípustném stavu
                if self.stav_hry == "prihlasovani_hracu":
                    self.hraci.append(hrac)
                    self.pocet_hracu += 1
                    self._poradi_hracu.append(self.pocet_hracu - 1)
                    ireturn = self.hraci.index(hrac)
                else:
                    ireturn = "nelze pridavat hrace"
            else: 
                ireturn = self.hraci.index(hrac)
        else:
            ireturn = "neni instance tridy Hrac" 
        return ireturn

    def balik(self, balik=None):
        """ nastaví nebo zjistí balík karet """
        if balik.__class__.__name__ == "Balik":
            self._balik = balik
        return self._balik

    def forhont(self, cis_hrace=None):
        """ změna nebo zjištění forhonta """
        if cis_hrace.__class__.__name__ == "int" and \
                       cis_hrace < self.pocet_hracu:
            # změna forhonta
            iforh = cis_hrace
            for i in range(self.pocet_hracu):
                self._poradi_hracu[i] = iforh
                iforh = (iforh + 1) % self.pocet_hracu
        return self._poradi_hracu[0]
                
    def rozdej_karty(self):
        """ rozdání karet """
        if self.typ_hry == "prsi" and self.pocet_hracu in range(2,6) and \
                       self.balik().__class__.__name__ == "Balik" and \
                       self.stav_hry == "zacatek_hry":
            ipock = self._pocet_karet

            # vratit karty od hracu a vynesene karty
            self._seber_karty()
            # rozdávat v pořadí podle self._poradi_hracu
            while ipock > 0:
                for ihr in self._poradi_hracu:
                    for i in range(self._rozdavat_po): 
                        self.hraci[ihr].karty.append(self.balik().karty.pop())
                ipock -= self._rozdavat_po
            # vyneseni prvni karty
            stouch = {"hrac": (self.forhont()-1) % self.pocet_hracu, \
                      "vynesene":[], "liznute": [], "renonc": []}
            self._odehrane.append(self.balik().karty.pop())
            stouch["vynesene"].append(self._odehrane[len(self._odehrane)-1])
            self._aktbarva = self._odehrane[len(self._odehrane)-1][0]
            self._akthodnota = self._odehrane[len(self._odehrane)-1][1]
            # ošetření vyneseného svrška 
            if self._akthodnota == 12:
                self._aktbarva = self._balik.karty[0][0]
                self._akthodnota = None
                stouch["vynesene"].append([self._aktbarva, self._akthodnota])
            self._stouchy.append(stouch)
            self.token(self.hraci[self.forhont()])
            ireturn = True
        else:
            ireturn = False
        return ireturn

    def _seber_karty(self):
            # kontrola, aby měli hráči prázdnou pazouru
            # případné karty vrátit do balíku
            for hrac in self.hraci:
                for ik in hrac.karty: 
                    self._balik.karty.insert(0,ik)
                hrac.karty = []
            # sebrat odehrané karty
            for ik in self._odehrane:
                self._balik.karty.insert(0, ik)
            self._odehrane = []

    def token(self, objekt=None):
        if objekt is not None:
            self._token = objekt
        return self._token

    def jmeno(self, jmeno=None):
        """Zjištění - nastavení jména hry"""
        if jmeno is not None:
            self._jmeno = jmeno
        return self._jmeno

    def hraj(self):
        # kontrola, jestli ma hra token
        ireturn = False
        if self.hra().token() == self:
            ireturn = True
            # hra udela cinnosti, ktere ma
            # a preda token hraci, ktery je na rade 
            self.hra().token(self.hra())
        return ireturn

    def prevzit_token(self):
        print inspect.stack()[1]
    

        
def pro_ucely_testovani(): 
    global b, hra, h1, h2

    b = Balik(32)
    b.zamichej()
    hra = Hra("prsi")
    h1 = Hrac("jarda")
    h2 = Hrac("carda")
    h1.hra(hra)
    h2.hra(hra)
    hra.balik(b)
    hra.rozdej_karty()
    hra.stav_hry = "zacatek_hry"
    hra.rozdej_karty()



if __name__ == '__main__':
    pro_ucely_testovani()

