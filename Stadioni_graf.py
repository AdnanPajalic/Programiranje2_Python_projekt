import matplotlib.pyplot as plt
import re
import requests
import operator

link = 'https://en.wikipedia.org/wiki/UEFA_Euro_2020'

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

stevilo_ljudi = []
for k,v in stadioni(link).items():
    stevilo_ljudi.append(v['kapaciteta'])

kapaciteta = []
for j in stevilo_ljudi:
    celo = int(j.replace(',',''))
    kapaciteta.append(celo)

imena = list(stadioni(link).keys())

slovar = dict(zip(imena,kapaciteta))

sortiran_slovar = dict(sorted(slovar.items(), key=operator.itemgetter(1), reverse=True))

imena_stadionov = list(stadioni(link).keys())
kapaciteta_ljudi = list(sortiran_slovar.values())

RED = [0.73,0.33,0.33]


fig = plt.figure(figsize = [20, 7])
plt.bar(imena_stadionov, kapaciteta_ljudi,width=0.5, color = RED, edgecolor = 'black')

plt.yscale('linear')
plt.ylim(30000,95000)


plt.ylabel("Kapaciteta", fontsize = 18)
plt.xlabel("Imena stadionov", fontsize = 15)
plt.show()