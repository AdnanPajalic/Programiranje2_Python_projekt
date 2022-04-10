import requests
import operator as op

url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"

querystring = {"league":"4","season":"2020"}

headers = {
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "fafef7c6b6msh31857524ed1c052p17234cjsn053c47ccafad"}

response = requests.request("GET", url, headers=headers, params=querystring)
a = response.json()
tabela_imen = a['response']

# ========================================================================================================
# Ustvarimo tabelo, kjer so elementi slovarji, v katerih so shranjeni ključni podatki o najboljših strelcih

slovar_igralcev_s_podatki = {}

for slovar in tabela_imen:
    igralec_podatki = {}
    for igralec, podatki in slovar.items():
        if igralec == 'player':
            if slovar['player']['firstname'] == 'Cristiano Ronaldo':
                igralec_podatki['ime'] = 'Cristiano Ronaldo'
            else:
                igralec_podatki['ime'] = slovar['player']['firstname'] + ' ' + slovar['player']['lastname']
            igralec_podatki['starost'] = slovar[igralec]['age']
            igralec_podatki['datum rojstva'] = slovar[igralec]['birth']['date']
            igralec_podatki['mesto rojstva'] = slovar[igralec]['birth']['place']
            igralec_podatki['nacionalnost'] = slovar[igralec]['nationality']
            igralec_podatki['višina'] = slovar[igralec]['height']
            igralec_podatki['teža'] = slovar[igralec]['weight']
        elif igralec == 'statistics':
            podatki = podatki[0]
            igralec_podatki['reprezentanca'] = podatki['team']['name']
            igralec_podatki['nastopi'] = podatki['games']['appearences']
            igralec_podatki['odigrane minute'] = podatki['games']['minutes']
            igralec_podatki['ocena na prvenstvu'] = podatki['games']['rating']
            igralec_podatki['streli na gol'] = podatki['shots']['total']
            igralec_podatki['streli v okvir'] = podatki['shots']['on']
            igralec_podatki['goli'] = podatki['goals']['total']
    slovar_igralcev_s_podatki[igralec_podatki['ime']] = igralec_podatki

# print(slovar_igralcev_s_podatki)

# ========================================================================================================
# Na tem koraku sva si izposodila kodo za preverjanje katero ime, ki ga uporbnik vnese, se najbolj ujema z
# imenom, ki je shranjeno v tabeli najboljših strelcev evropskega prvenstva.

seznam_najboljsih_strelcev = list(slovar_igralcev_s_podatki.keys())


def edit_dist(fst, snd):
  """
  Compute Levenshtein or edit distance between given two strings.
  Function returns number of operations needed to traverse one string to another.
  """
  dist = [[0 for _ in range(len(snd) + 1)] for _ in range(len(fst) + 1)]
  for i in range(len(fst) + 1):
    dist[i][0] = i
  for j in range(len(snd) + 1):
    dist[0][j] = j
  for j in range(1, len(snd) + 1):
    for i in range(1, len(fst) + 1):
      dist[i][j] = min(dist[i - 1][j - 1] if fst[i - 1] == snd[j - 1] else dist[i - 1][j - 1] + 1, dist[i - 1][j] + 1, dist[i][j - 1] + 1)
  return dist[len(fst)][len(snd)]

def vrni_najpodobnejse(ime):
    ''''''
    razdalja = {}
    for nogometas in seznam_najboljsih_strelcev:
        razdalja[nogometas] = edit_dist(ime, nogometas)
        sortiran = sorted(razdalja.items(), key = op.itemgetter(1))
    return sortiran[0][0]
                
#print(vrni_najpodobnejse('Haris Seferovic'))

# ========================================================================================================
class Nogometas:
    def __init__(self, nogometas):
        if nogometas not in seznam_najboljsih_strelcev:
            raise ValueError('Nogometaš, ki ste ga vnesli ni v tabeli. Ste morda želeli vnesti: ' + str(vrni_najpodobnejse(nogometas)))
        self.nogometas = slovar_igralcev_s_podatki[nogometas]['ime']
        self.starost = slovar_igralcev_s_podatki[nogometas]['starost']
        self.datum_rojstva = slovar_igralcev_s_podatki[nogometas]['datum rojstva']
        self.mesto_rojstva = slovar_igralcev_s_podatki[nogometas]['mesto rojstva']
        self.nacionalnost = slovar_igralcev_s_podatki[nogometas]['nacionalnost']
        self.visina = slovar_igralcev_s_podatki[nogometas]['višina']
        self.teza = slovar_igralcev_s_podatki[nogometas]['teža']
        self.nastopi = slovar_igralcev_s_podatki[nogometas]['nastopi']
        self.odigrane_minute = slovar_igralcev_s_podatki[nogometas]['odigrane minute']
        self.ocena = float(slovar_igralcev_s_podatki[nogometas]['ocena na prvenstvu'])
        self.streli_na_gol = slovar_igralcev_s_podatki[nogometas]['streli na gol']
        self.streli_v_okvir = slovar_igralcev_s_podatki[nogometas]['streli v okvir']
        self.goli = slovar_igralcev_s_podatki[nogometas]['goli']
        self.goli_vs_na_gol = slovar_igralcev_s_podatki[nogometas]['goli'] / slovar_igralcev_s_podatki[nogometas]['streli na gol'] * 100 #razmerje med  goli in streli na gol
        self.razmerje_strelov_v_okvir = slovar_igralcev_s_podatki[nogometas]['streli v okvir'] / slovar_igralcev_s_podatki[nogometas]['streli na gol'] * 100 #razmerje med streli na gol in vsemi streli
        
    def __str__(self):
        niz = ''
        niz += "{:>50s} | '{:s}'\n".format('Ime', self.nogometas)
        niz += "{:>50s} |  {:d}\n".format('Starost', self.starost)
        niz += "{:>50s} | '{:s}'\n".format('Datum rojstva', self.datum_rojstva)
        niz += "{:>50s} | '{:s}'\n".format('Mesto rojstva', self.mesto_rojstva)
        niz += "{:>50s} | '{:s}'\n".format('Nacionalnost', self.nacionalnost)
        niz += "{:>50s} |  {:s}\n".format('Visina', self.visina)
        niz += "{:>50s} |  {:d}\n".format('Goli', self.goli)
        niz += "{:>50s} |  {:s}\n".format('Teža', self.teza)
        niz += "{:>50s} |  {:d}\n".format('Nastopi', self.nastopi)
        niz += "{:>50s} |  {:d}\n".format('Odigrane minute', self.odigrane_minute)
        niz += "{:>50s} |  {:2.2f}\n".format('Ocena na prvenstvu (1-10)', self.ocena)
        niz += "{:>50s} |  {:d}\n".format('Streli na gol', self.streli_na_gol)
        niz += "{:>50s} |  {:d}\n".format('Streli v okvir', self.streli_v_okvir)
        niz += "{:>50s} |  {:2.2f}\n".format('Razmerje med goli in streli na gol (%)', self.goli_vs_na_gol)
        niz += "{:>50s} |  {:2.2f}\n".format('Razmerje med streli na gol in vsemi streli (%)', self.razmerje_strelov_v_okvir)
        return niz


#k = Nogometas('Cristiano Ronaldo')
#print(k)
# ===========================================================================================================================