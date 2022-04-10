import requests
import re
import operator as op
import Prevod
import Podatki
import Razred_nogometas
import Razred_reprezentanca
import time
import Graf_stadioni
import matplotlib.pyplot as plt
import operator

# nastopajoce_drzave = Prevod.nastopajoce_drzave
# del nastopajoce_drzave['Greece'] # Grčija ne nastopa na evropskem prvenstvu 2020

# ============================================================================================================================================================
print('DOBRODOŠLI V PREDSTAVITVI EVROPSKEGA PRVENSTVA V NOGOMETU 2020.')
time.sleep(1)
while True:
    print('')
    print('POZDRAVLJENI NA ZAČETKU PROGRAMA')
    print('Izbirate lahko med različnimi podatki. Vnesite sledečo številko, če vas zanima: ')
    time.sleep(1)
    print('1) Zgodovina Evropskih prvenstev')
    print('2) Statistika nastopajočih reprezentanc na EURU 2020')
    print('3) Statistika najboljših strelcev na EURU 2020')
    print('4) Podatki o štadionih z EURA 2020')
    print('5) Končaj')

    while True:
        try:
            stevilo = int(input('\nŠtevilo: '))
            break
        except:
            print('Vnesli ste napačno številko. Poskusite ponovno.')
    
    if stevilo == 1:
        print('Na voljo so ključni podatki o evropskih prvenstvih med leti 2000 in 2020.')
        time.sleep(1)
        print('Vnesite leto evropskega prvesntva. Na voljo so sledeča leta:')
        time.sleep(1)
        print('1) 2000')
        print('2) 2004')
        print('3) 2008')
        print('4) 2012')
        print('5) 2016')
        print('5) 2020')
        
        tab_moznih_let = [2000, 2004, 2008, 2012, 2016, 2020]
        
        while True:
            leto = int(input('\nLeto: '))
        
            if leto in tab_moznih_let:
                slovar_podatkov = Podatki.statistika_preteklih_prvenstev(leto)
                
                print("{:>50s} | {}".format('Leto evropskega prvenstva', leto))
                try:
                    if len(slovar_podatkov['Host Country'].split(', ')) == 1:
                        print("{:>50s} | {}".format('Država gostiteljica', Prevod.nastopajoce_drzave[slovar_podatkov['Host Country']]))
                    else:
                        gostiteljice = slovar_podatkov['Host Country'].split(', ')
                        prevod = [Prevod.nastopajoce_drzave[drzava] for drzava in gostiteljice]
                        print("{:>50s} | {}".format('Države gostiteljice', ', '.join(prevod)))
                except:
                    pass
                print("{:>50s} | {}".format('Zmagovalec evropskega prvenstva', Prevod.nastopajoce_drzave[slovar_podatkov['Champion']]))
                if len(list(slovar_podatkov['Most Goals'].keys())[0].split(', ')) == 1:
                    print("{:>50s} | {} (št. golov: {})".format('Igralec z največ doseženimi goli', list(slovar_podatkov['Most Goals'].keys())[0], list(slovar_podatkov['Most Goals'].values())[0]))
                else:
                    print("{:>50s} | {} (št. golov: {})".format('Igralci z največ doseženimi goli', list(slovar_podatkov['Most Goals'].keys())[0], list(slovar_podatkov['Most Goals'].values())[0]))
                try:
                    if len(list(slovar_podatkov['Most Assists'].keys())[0].split(', ')) == 1:
                        print("{:>50s} | {} (št. asistenc: {})".format('Igralec z največ doseženimi asistencami', list(slovar_podatkov['Most Assists'].keys())[0], list(slovar_podatkov['Most Assists'].values())[0]))
                    else:
                        print("{:>50s} | {} (št. asistenc: {})".format('Igralci z največ doseženimi asistencami', list(slovar_podatkov['Most Assists'].keys())[0], list(slovar_podatkov['Most Assists'].values())[0]))
                except:
                    pass
                if len(list(slovar_podatkov['Most Clean Sheets'].keys())[0].split(', ')) == 1:
                    print("{:>50s} | {} (št. nedotaknjenih mrež: {})".format('Golman, ki je ohranil največ nedotaknjenih mrež', list(slovar_podatkov['Most Clean Sheets'].keys())[0], list(slovar_podatkov['Most Clean Sheets'].values())[0]))
                else:
                    print("{:>50s} | {} (št. nedotaknjenih mrež: {})".format('Golmani, ki so ohranili največ nedotaknjenih mrež', list(slovar_podatkov['Most Clean Sheets'].keys())[0], list(slovar_podatkov['Most Clean Sheets'].values())[0]))
                
                time.sleep(4)
                vnos = input('\nŽelite podatke še za katero drugo leto? Vnesite DA/NE: ')
                if vnos != 'DA':
                    break
            else:
                print('\nVnseli ste napačno leto. Poskusite ponovno.')
            
    if stevilo == 2:
        print('\nNa voljo so nekateri statistični podatki o reprezentacah, ki so nastopale na evropskem prvenstvu 2020.')
        print('Vnesite reprezentanco (v slovenščini), iz evropskega prvenstva 2020, ki vas zanima. (primer: Francija)')
        
        while True:
            try:
                reprezentanca = input('\nReprezentanca: ')
                
                drzava = Razred_reprezentanca.Reprezentanca(reprezentanca)
                
                print('\nAli vas zanimajo statistični podatki o ' + drzava.ime[:-1] + 'i. Vnesite DA/NE')
                vnos = input('\nVnos: ')
                
                if vnos == 'DA':
                    print(drzava)
                    time.sleep(1)
                    ponovno = input('\nŽelite statistične podatke še katere druge reprezentance? Vnesite DA/NE: ')
                    if ponovno != 'DA':
                        pass
                    else:
                        continue
                
                vnos = input('\nVas zanima denarna nagrada reprezentance na evropskem prvenstvu? Vnesite DA/NE: ')
                if vnos != 'DA':
                    pass
                else:
                    print('\n' + drzava.zasluzek())
                    time.sleep(1)
                
                vnos = input('\nŽelite primerjati pretekle medsebojne obračune z nekatero drugo reprezentanco iz EURA 2020? Vnesite DA/NE: ')
                if vnos == 'DA':
                    while True:
                        try:
                            drzava2 = input('\nVnesite reprezentanco s katero bi želeli primerjati prvo reprezentanco: ')
                            print('\n' + drzava.primerjava_reprezentanc(Razred_reprezentanca.Reprezentanca(drzava2)))
                            ponovno = input('\nŽelite prvo reprezentanco primerjati še z katero drugo? Vnesite DA/NE: ')
                            if ponovno != 'DA':
                                break
                            else:
                                drzava2 = input('\nVnesite reprezentanco s katero bi želeli primerjati prvo reprezentanco: ')
                                print('\n' + drzava.primerjava_reprezentanc(Razred_reprezentanca.Reprezentanca(drzava2)))
                        except:
                            print('\nVnesli ste napačno ime reprezentance. Poskusite ponovno.')
                elif vnos == 'NE':
                    break
            except:
                print('\nVnesli ste napačno ime reprezentance. Poskusite ponovno.')
                
        
    if stevilo == 3:
        print('\nNa voljo so podatki o najboljših strelcih, ki so nastopali na evropskem prvenstvu 2020.')
        print('Vnesite igralca, iz evropskega prvenstva 2020, za katerega vas zanimajo podatki. (primer: Cristiano Ronaldo)')
        
        while True:
            vnesi = input('\nIgralec: ')
            try:
                igralec = Razred_nogometas.Nogometas(vnesi)
                
                print('\nAli vas zanimajo statistični podatki o vnesenem igralcu? Vnesite DA/NE')
                vnos = input('Vnos: ')
                
                if vnos == 'DA':
                    print(igralec)
                    time.sleep(1)
                    ponovno = input('\nŽelite podatke še za katerega drugega igralca? Vnesite DA/NE: ')
                    if ponovno != 'DA':
                        pass
                    else:
                        continue
            except:
                print('Vnesli ste napačno ime igralca. Ste morda želeli vnesti ' + str(Razred_nogometas.vrni_najpodobnejse(vnesi)))
                continue
            break
    
    if stevilo == 4:
        print('\nNa voljo so podatki o stadionih na katerih so bile odigrane tekme evropskega prvenstva 2020')
          
        vnos = input('Te zanimajo, kje v katerih mestih so bile igrane tekme in kapacitete stadionov? DA/NE: ')
          
        if vnos == 'DA':
            print('\n')
            for stadion, podatki in Podatki.stadioni(Podatki.link_wiki).items():
                print("{:>50s} | Kapacieta: {:>5s} | {}".format(stadion, podatki['kapaciteta'], podatki['mesto']))
            Graf_stadioni.fig.savefig('Graf_satdionov.pdf', bbox_inches = 'tight')
            # Na pdf datoteko smo shranili sliko.
            continue
        else:
            continue
    
    elif stevilo == 5:
        print('HVALA. LEP POZDRAV')
            
    else:
        continue
    break

            
            