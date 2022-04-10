import requests
import re
import Prevod

# ===========================================================================================================================
link_wiki = 'https://en.wikipedia.org/wiki/UEFA_Euro_2020'

def top_strelci(link):
    '''
    Funkcija iz spletne strani 'https://en.wikipedia.org/wiki/UEFA_Euro_2020' pobere vse strelce iz EURA 2020,
    ki so dosegli 3 gole ali več in jih shrani v slovar glede na to koliko golov so dosegli
    '''
    strelci = {}
    req = requests.get(link).text
    for i in range(5,2,-1):
        tabela = req.split('<p><b>' + str(i-1) + ' goals</b>')[0]
        igralci = re.findall(r'</a></span> <a href=".+">.+</a></li>', tabela)
        imena = [re.sub(r'<.*?>', '', oseba)[1:] for oseba in igralci]
        if i != 5: # ločimo primer ko bo v sez_strelcev gnezden seznam
            sez_strelcev = [strelec for igralci in list(strelci.values()) for strelec in igralci]
            strelci[i] = imena[len(sez_strelcev):]
        else: # ni gnezdenega seznama
            strelci[i] = imena
    return strelci     
     
# print(top_strelci(link_wiki))

# ===========================================================================================================================
def zasluzek_najvec(link):
    '''
    Funkcija iz spletne strani 'https://en.wikipedia.org/wiki/UEFA_Euro_2020' pobere podatke o tem katere države so iz
    EURA 2020 zaslužile največ in jih shrani v slovar kot vrednosti, glede na količino zaslužka od največjega do najmanjšega.
    '''
    drzave_zasluzek = dict()
    req = requests.get(link).text
    tabela = req.split('<caption>Prize money')[1]
    drzave = re.findall(r'</span><a href=".+">.+</a></span></td>', tabela)
    tab_drzav = [re.sub(r'<.*?>', '', drzava) for drzava in drzave]
    stevec = 1
    for drzava in tab_drzav:
        drzava = drzava.split('&#160;') # Znebimo so umesnih znakov, ki se pojavijo med imeni držav
        if '' in drzava:
            drzava.remove('') # prazne nize je potrebno odstraniti
        drzave_zasluzek[stevec] = drzava
        stevec += 1
    return drzave_zasluzek

slovar_drzav = zasluzek_najvec(link_wiki)
# print(zasluzek_najvec(link_wiki))

def zasluzek_koliko(link):
    '''Funkcija iz spletne strani 'https://en.wikipedia.org/wiki/UEFA_Euro_2020' pobere zaslužke iz EURA 2020.'''
    tab_zasluzkov = []
    req = requests.get(link).text
    tabela = req.split('<caption>Prize money')[1]
    podatki = re.findall(r'<td>.+', tabela)
    zasluzki = [re.sub(r'<.*?>', '', oseba) for oseba in podatki]
    for zasluzek in range(1, 30, 2):
        try: # na vsakem drugem mestu je znesek, ki predstavlja zasluzek
            tab_zasluzkov.append(float(zasluzki[zasluzek]))
        except:
            pass
    return tab_zasluzkov


tab_zasluzkov = zasluzek_koliko(link_wiki)
zasluzek_drzav = dict()    
# slovar kjer so ključi zaslužki, vrednosti pa države, ki so določen znesek zaslužile
for i in range(1,15):
     drzava = slovar_drzav[i]
     zasluzila = tab_zasluzkov[i-1]
     zasluzek_drzav[zasluzila] = drzava
# print(zasluzek_drzav)

# ===========================================================================================================================
def statistika_drzav(reprezentanca):
    '''
    Funkcija pobere najpomembnejšo statistiko ekip iz EURA 2020
    '''
    statistika = {}
    if reprezentanca not in list(Prevod.nastopajoce_drzave.values()):
        raise Exception('Reprezentanca, ki ste jo vnesli, ni nastopala na EURU 2020. Poskusite Znova.')
    with open('Statistika_drzav.txt', 'r', encoding = 'utf8') as file:
        for vrstica in file:
            tab = vrstica.strip().split(' = ')
            if tab[0] == reprezentanca:
                link = tab[1]
    req = requests.get(link).text
    for i in range(1,12):
        tabela = req.split('<pk-num-stat-item class="" variant="secondary">')[i]
        vrednost_podatka = re.findall(r'<div slot="stat-value">.+</div>', tabela)
        tab_vrednosti_podatkov = [re.sub(r'<.*?>', '', podatek) for podatek in vrednost_podatka]
        vrsta_podatka = re.findall(r'<div slot="stat-label">.+</div>', tabela)
        tab_vrste_podatkov = [re.sub(r'<.*?>', '', podatek) for podatek in vrsta_podatka]
        statistika[tab_vrste_podatkov[0]] = tab_vrednosti_podatkov[0]
    return statistika

# print(statistika_drzav('Severna makedonija'))

# ===========================================================================================================================
tab_let = [2000, 2004, 2008, 2012, 2016, 2020]

def statistika_preteklih_prvenstev(leto):
    '''
    Funkcija iz spletne strani pobere glavne podatke iz preteklih EURO tekmovanj od leta 2000 do leta 2016.
    '''
    slovar_podatkov = {}
    if leto not in tab_let:
        raise Exception('Tega leta ni bilo evropskega prvenstva. Poskusite ponovno.')
    with open('Statistika_preteklih_prvenstev.txt', 'r', encoding = 'utf8') as file:
        for vrstica in file:
            tab = vrstica.strip().split(' = ')
            if int(tab[0]) == leto:
                link = tab[1]
    req = requests.get(link).text
    tab = req.split('More league info</button>')[0]
    if link.split('/')[-1] == 'UEFA-Euro-Stats':
        podatki = re.findall(r'<p><strong>.+?</p>', tab)
        tab_podatkov = [re.sub(r'<.+?>', '', podatek) for podatek in podatki]
        tab_podatkov.pop(0)
        tab_podatkov.pop(0)
        for i in range(len(tab_podatkov)):
            razdeli = tab_podatkov[i].split(': ')
            if i == 0:
                slovar_podatkov[razdeli[0]] = razdeli[1][3:]
            else:
                igralci = razdeli[1].split(' - ')
                kdo = igralci[0]
                st_dosezenih = igralci[1]
                slovar_podatkov[razdeli[0]] = {kdo: st_dosezenih}
    else:
        podatki = re.findall(r'<p><strong>.+?</p>', tab)
        tab_podatkov = [re.sub(r'<.+?>', '', podatek) for podatek in podatki]
        tab_podatkov.pop(0)
        tab_podatkov.pop(1)
        for i in range(len(tab_podatkov)):
            urejen = tab_podatkov[i].replace('.', '')
            razdeli = urejen.split(': ')
            if i == 0:
                slovar_podatkov[razdeli[0]] = razdeli[1]
            elif i == 1:
                slovar_podatkov[razdeli[0]] = razdeli[1][3:]
            else:
                igralci = razdeli[1].split(' - ')
                kdo = igralci[0]
                st_dosezenih = igralci[1]
                slovar_podatkov[razdeli[0]] = {kdo: st_dosezenih}
    return slovar_podatkov

# print(statistika_preteklih_prvenstev(2008))

# ===========================================================================================================================
def stadioni(link):
    '''
    Funkcija iz spletne strani 'https://en.wikipedia.org/wiki/UEFA_Euro_2020' pobere
    podatke o lokaciji in kapaciteti stadionov, kjer so bile odigrane tekme EURA 2020. 
    '''
    stadioni_podatki = {}
    req = requests.get(link).text
    tabela = req.split('<table class="wikitable" style="text-align:center;">')[1]
    imena_stadionov = re.findall(r'<td><a href="/wiki/.+" title=".+">[A-Z a-záéță]+</a>', tabela)
    lokacije_stadionov = re.findall(r'</a></span> <a href="/wiki/.+" title=".+">[A-Z a-záéță]+</a>', tabela)
    kapacitete =  re.findall(r'<td>Capacity: <b>[\d\,]+</b>', tabela)
    tab_kapacitet = [re.sub(r'<.*?>', '', kapaciteta)[10:] for kapaciteta in kapacitete]
    tab_imen_stadionov = [re.sub(r'<.*?>', '', ime_stadiona) for ime_stadiona in imena_stadionov][:11]
    tab_lokacij_stadionov = [re.sub(r'<.*?>[ ]?', '', lokacija_stadiona) for lokacija_stadiona in lokacije_stadionov]
    for i in range(11):
        stadioni_podatki[tab_imen_stadionov[i]] = {'mesto' : tab_lokacij_stadionov[i]}
        stadioni_podatki[tab_imen_stadionov[i]]['kapaciteta'] = tab_kapacitet[i]
    return stadioni_podatki


# print(stadioni(link_wiki))

# ===========================================================================================================================
