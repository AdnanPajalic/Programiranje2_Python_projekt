import matplotlib.pyplot as plt
import re
import requests
import operator
import Podatki

stevilo_ljudi = []
for k,v in Podatki.stadioni(Podatki.link_wiki).items():
    stevilo_ljudi.append(v['kapaciteta'])

kapaciteta = []
for j in stevilo_ljudi:
    celo = int(j.replace(',',''))
    kapaciteta.append(celo)


imena = list(Podatki.stadioni(Podatki.link_wiki).keys())

slovar = dict(zip(imena,kapaciteta))

sortiran_slovar = dict(sorted(slovar.items(), key=operator.itemgetter(1), reverse=True))

imena_stadionov = list(Podatki.stadioni(Podatki.link_wiki).keys())
kapaciteta_ljudi = list(sortiran_slovar.values())

RED = [0.5,0.7,0.5]


fig = plt.figure(figsize = [20, 10])
plt.bar(imena_stadionov, kapaciteta_ljudi,width=0.5, color = RED, edgecolor = 'black')

plt.yscale('linear')
plt.ylim(30000,95000)


plt.ylabel("Kapaciteta", fontsize = 18)
plt.xlabel("Imena stadionov", fontsize = 15)
plt.close()
fig.savefig('Graf_satdionov.pdf', bbox_inches = 'tight')



