import requests
import re

link = 'https://ling-app.com/sl/country-names-in-slovenian/'

def prevod_drzav(link):
    '''Funkcija iz spletne strani 'https://ling-app.com/sl/country-names-in-slovenian/' pobere prevode držav iz angleščine v slovenščino.'''
    drzave_zasluzek = dict()
    req = requests.get(link).text
    tabela = req.split('alt="Country Names In Slovenian"')[2]
    drzave = re.findall(r'<tr><td>.+</td></tr>', tabela)
    tab_drzav = [re.sub(r'<.*?>', '', drzava) for drzava in drzave]
    tabela_prevodov = tab_drzav[0].split('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    return tabela_prevodov

# Tabelo, ki jo vrne funkcija prevod_drzav je potrebno spraviti na datoteko, saj potrebuje preveč časa, da vzame podatke s spletne strani.
# Do podatkov iz tabele bo na ta način veliko hitreje dostopati:
# ========================================================================================================================================
# tabela = prevod_drzav(link)
# with open('Seznam_prevodov.txt', 'w') as f:
#     for element in tabela:
#         f.write(element + '\n')

slovar_drzav_id = {'Belgium' : 1, 'France' : 2, 'Croatia' : 3, 'Russia' : 4, 'Sweden' : 5, 'Spain' : 9, 'England' : 10,'Switzerland' : 15,
                'Denmark' : 21, 'Poland' : 24, 'Germany' : 25, 'Portugal' : 27, 'Wales' : 767, 'Italy' : 768, 'Hungary' : 769,
                'Czech Republic' : 770, 'Ukraine' : 772, 'Slovakia' : 773, 'Austria' : 775, 'Turkey' : 777,'Finland' : 1099,
                'North Macedonia' : 1105, 'Scotland' : 1108,'Netherlands' : 1118}

slovar_prevodov = {}
with open('Seznam_prevodov.txt', 'r') as g:
    # Prvih pet vrstic se znebimo, saj nas te države ne zanimajo
    for _ in range(5):
        g.readline()
    tabela = g.readlines()[:-1]
    for i in range(1, len(tabela), 2):
        slovar_prevodov[tabela[i-1][:-1]] = tabela[i][:-1]
    # Dodamo reprezentance, ki so nastopale na EURU 2020, a jih na spletni strani ni v seznamu prevodov
    slovar_prevodov['England'] = 'Anglija'
    slovar_prevodov['Wales'] = 'Wales'
    slovar_prevodov['North Macedonia'] = 'Severna Makedonija'
    slovar_prevodov['Scotland'] = 'Škotska'
    slovar_prevodov['Czech Republic'] = 'Češka'
    
# V slovar spravimo države v angleščini (kot ključe) in slovenska imena držav (kot vrednosti)
nastopajoce_drzave = {}
for drzava in slovar_drzav_id:
    nastopajoce_drzave[drzava] = slovar_prevodov[drzava]
#print(nastopajoce_drzave)

nastopajoce_drzave['Greece'] = 'Grčija'


        
    
