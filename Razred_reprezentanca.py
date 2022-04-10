import requests
import Podatki
import Prevod


url = "https://api-football-beta.p.rapidapi.com/fixtures/headtohead"

# ===================================================================================================================================
# Slovar, kjer je kot ključ shranjena država v angleščini vrednost pa njen prevod v slovenščini
slovar_prevod_drzav = Prevod.nastopajoce_drzave

# Slovar, kjer so ključi reprezentance, vrednosti pa id reprezentanc, ki jih določa API-football
slovar_drzav_id = {'Belgium' : 1, 'France' : 2, 'Croatia' : 3, 'Russia' : 4, 'Sweden' : 5, 'Spain' : 9, 'England' : 10,'Switzerland' : 15,
                'Denmark' : 21, 'Poland' : 24, 'Germany' : 25, 'Portugal' : 27, 'Wales' : 767, 'Italy' : 768, 'Hungary' : 769,
                'Czech Republic' : 770, 'Ukraine' : 772, 'Slovakia' : 773, 'Austria' : 775, 'Turkey' : 777,'Finland' : 1099,
                'North Macedonia' : 1105, 'Scotland' : 1108,'Netherlands' : 1118}

# ===================================================================================================================================
class Reprezentanca:
    def __init__(self, drzava):
        slovar_podatkov = Podatki.statistika_drzav(drzava)
        self.ime = drzava
        for anglesko_ime, slo_ime in Prevod.nastopajoce_drzave.items():
            if slo_ime == drzava:
                self.anglesko_ime = anglesko_ime
        self.goli = int(slovar_podatkov['Goals'])
        self.prejeti_goli = int(slovar_podatkov['Goals conceded'])
        self.posest_zoge = float((slovar_podatkov['Possession (%)'])[:-1])
        self.natancnost_podaj = float((slovar_podatkov['Passing accuracy (%)'])[:-1])
        self.odvzete_zoge = int(slovar_podatkov['Balls recovered'])
        self.dobljeni_dvoboji = int(slovar_podatkov['Tackles won'])
        self.st_nedotaknjenih_mrez = int(slovar_podatkov['Clean sheets'])
        self.obrambe = int(slovar_podatkov['Saves'])
        self.preteceni_km = float(slovar_podatkov['Distance covered (km)'])
        self.rumeni_kartoni = int(slovar_podatkov['Yellow cards'])
        self.rdeci_kartoni = int(slovar_podatkov['Red cards'])
    
    
    def __str__(self):
        niz = ''
        niz += "{:>50s} | '{:s}'\n".format('REPREZENTANCA', self.ime)
        niz += "{:>50s} | {:d}\n".format('Doseženi goli', self.goli)
        niz += "{:>50s} | {:d}\n".format('Prejeti goli', self.prejeti_goli)
        niz += "{:>50s} | {:2.2f}\n".format('Posest žoge (%)', self.posest_zoge)
        niz += "{:>50s} | {:2.2f}\n".format('Natančnost podaj (%)', self.natancnost_podaj)
        niz += "{:>50s} | {:d}\n".format('Odvzete žoge', self.odvzete_zoge)
        niz += "{:>50s} | {:d}\n".format('Dobljeni dvoboji', self.dobljeni_dvoboji)
        niz += "{:>50s} | {:d}\n".format('Nedotaknjene mreže', self.st_nedotaknjenih_mrez)
        niz += "{:>50s} | {:d}\n".format('Obrambe', self.obrambe)
        niz += "{:>50s} | {:2.2f}\n".format('Pretečena razdalja (km)', self.preteceni_km)
        niz += "{:>50s} | {:d}\n".format('Rumeni kartoni', self.rumeni_kartoni)
        niz += "{:>50s} | {:d}".format('Rdeči kartoni', self.rdeci_kartoni)
        return niz
 
 
    def zasluzek(self):
        '''Funkcija vrne znesek, ki ga je država zaslužila EURU 2020'''
        zasluzki = Podatki.zasluzek_drzav
        for zasluzek, drzave in zasluzki.items():
            if self.anglesko_ime in drzave:
                self.zasluzek = zasluzek
        return("{:>25s} | {:2.2f} milijonov".format(self.ime, self.zasluzek))
    
    
    def primerjava_reprezentanc(self, other):
        '''Funkcija primerja stitistiko preteklih tekem med dvema reprezentancama'''
        prva_ekipa = slovar_drzav_id[self.anglesko_ime]
        druga_ekipa = slovar_drzav_id[other.anglesko_ime]
        querystring = {"h2h":str(prva_ekipa) + '-' + str(druga_ekipa),"status":"ft","last":"10"}
        headers = {"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com",
                   "X-RapidAPI-Key": "fafef7c6b6msh31857524ed1c052p17234cjsn053c47ccafad"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        goli_domaci = 0
        goli_gostje = 0
        ekipa1 = 0
        ekipa2 = 0
        izenaceno = 0
        skupno_st_golov = 0
        
        slovar = response.json()
        stevilo_medsebojnih_tekem = slovar['results']
        tabela = slovar['response']
        for i in range(len(tabela)):
            el_tab = tabela[i]
            ekipe = el_tab['teams']
            dom = ekipe['home']
            gos = ekipe['away']
            domaci = dom['name']
            gostje = gos['name']
            goli = el_tab['goals']
            goli_domaci += goli['home']
            goli_gostje += goli['away']
            skupno_st_golov += (goli_domaci + goli_gostje)
            if domaci == self.anglesko_ime and gostje == other.anglesko_ime:
                if goli_domaci > goli_gostje:
                    ekipa1 += 1
                elif goli_domaci < goli_gostje:
                    ekipa2 += 1
                else:
                    izenaceno += 1
            elif domaci == other.anglesko_ime and gostje == self.anglesko_ime:
                if goli_domaci > goli_gostje:
                    ekipa2 += 1
                elif goli_domaci < goli_gostje:
                    ekipa1 += 1
                else:
                    izenaceno += 1
            goli_domaci = 0
            goli_gostje = 0
        niz = ''
        niz += 'Ekipi sta odigrali ' + str(stevilo_medsebojnih_tekem) + ' skupnih tekem.\n'
        if ekipa1 > ekipa2:
            niz += 'Več skupnih zmag ima ' + self.ime + ', na vseh tekmah je bilo skupno število golov: ' + str(skupno_st_golov)
            return niz
        elif ekipa2 > ekipa1:
            niz += 'Več skupnih zmag ima ' + other.ime + ', na vseh tekmah je bilo skupno število golov: ' + str(skupno_st_golov)
            return niz
        elif ekipa1 == ekipa2:
            niz += 'Obe ekipi imata enako število zmag, na vseh tekmah je bilo skupno število golov: ' + str(skupno_st_golov)
            return niz
        
# ===================================================================================================================================
# POSKUSNE FUNKCIJE:

# reprezentanca1 = Reprezentanca('Severna Makedonija')
# # print(reprezentanca1)
# print(reprezentanca1.zasluzek())
# print(reprezentanca1.primerjava_reprezentanc(Reprezentanca('Francija')))


        

