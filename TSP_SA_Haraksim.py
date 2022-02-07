'''
created by: Daniel Haraksim
project: Travelling Salesman Problem solved by simmulated annealing
description: Solving TSP with simmulated annealing algorithm. Cities were generated randomly in intervals of 0 to 200km
'''
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

#definovanie parametrov
pocet_miest = 20
startT = 30
poklesT = 0.99
finalT = 0.01
pocet_iteracii = int ((pocet_miest*(pocet_miest-1))/2)

#vytvorenie mesta a ich getterov
class Mesto:
    def __init__(self,x,y,nazov):
        self.x = x
        self.y = y
        self.nazov = nazov

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_nazov(self):
        return self.nazov

#nahodne vygenerovanie miest, ktore ma obchodnik navstivit v nahodnom poradi
def generuj():
    list = []
    for i in range(pocet_miest):
        #za ucelom testovania som si vytvoril zaciatocnu mapu aby som vedel skoro konzistentne porovnavat vysledky
        #toto pri realnom programe sa nevyuziva
        #x_list = [27, 14, 23, 80, 91, 133, 27, 24, 87, 161, 130, 6, 108, 27, 155, 157, 143, 16, 55, 14, 128, 196, 191, 128, 168, 87, 174, 91, 153, 39]
        #y_list = [128, 196, 191, 128, 168, 87, 174, 91, 153, 39, 28, 74, 118, 157, 198, 163, 63, 139, 156, 136, 27, 14, 23, 80, 91, 133, 27, 24, 87, 161]
        #x = x_list[i]
        #y = y_list[i]

        #generovanie suradnic x a y od 0 az 200km
        x = random.randint(0,200)
        y = random.randint(0,200)

        #ako nazov sme si urcili index mesta
        nazov = i+1
        #objekty mesta sme si ulozili do listu co reprezentovalo nasu cestu
        list.append(Mesto(x,y,nazov))
    #zamiesanie cesty
    random.shuffle(list)
    return list

#vypocet vzdialenosti medzi 2 mestami pomocou euklidoveho vzorca
def vzdialenost(a,b):
    return math.sqrt((a.get_x()-b.get_x())**2+(a.get_y()-b.get_y())**2)

#vypocet celkovej dlzky cesty
def cela_dlzka(list):
    dlzka = 0
    #scitanie vzdialenosti medzi kazdymi mestami
    for i in range(pocet_miest-1):
        dlzka += vzdialenost(list[i],list[i+1])
    #priratanie vzdialenosti medzi poslednym a prvym mestom
    dlzka += vzdialenost(list[-1],list[0])
    return dlzka

#generovanie susedov
def vymen_mesta(list):
    susedne_cesty = []
    nova_cesta = []
    #vyber nahodneho mesta, ktore budeme zamienat
    a = random.randint(0,pocet_miest-1)
    #vymena vybraneho mesta s kazdym jednym mestom na mape okrem sameho seba
    for i in range(pocet_miest):
        if i == a:
            continue
        nova_cesta = list[:]
        nova_cesta[i], nova_cesta[a] = list[a], list[i]
        susedne_cesty.append(nova_cesta)
    #returnujem list vsetkych moznych susedov od cesty v argumente
    return susedne_cesty

#vypis cesty v tvare (a,b,c) co znamena, a->b->c->a
def vypis(list):
    print("(", end="")
    for i in range(pocet_miest):
        if i != pocet_miest - 1:
            print(list[i].nazov, end=",")
        else:
            print(list[i].nazov, end="")
    print(")")

#vygenerovanie startovacej cesty
cesta = []
cesta = generuj()

print("Zaciatocna cesta:")
vypis(cesta)
print("Dlzka zaciatocnej cesty:")
print(cela_dlzka(cesta))

#premenne na ukladanie si aktualnej cesty od ktorej budeme generovat a najlepsej co sme za chod programu nasli
akt_cesta = cesta[:]
top_cesta = cesta[:]
dlzka_top = int(cela_dlzka(top_cesta))
dlzka_akt = int(cela_dlzka(akt_cesta))

#zadefinovanie teploty
teplota = startT

#pomocne premenne na nakreslenie line chart grafu
graf_y = []

start_time = time.time()
#algoritmus simulovaneho zihania
while teplota > finalT:

    #vygenerovanie susedov
    nova_cesta = vymen_mesta(akt_cesta)

    #iterovanie v jednej teplote
    for i in range(pocet_iteracii):
        #nahodne vybranie susednej cesty zo vsetkych moznych kombinacii
        novy_sused = random.choice(nova_cesta)
        #vypocet dlzky cesty vybraneho suseda
        dlzka_nova = cela_dlzka(novy_sused)

        #ak je dlzka cesty suseda lepsia ako aktualna cesta tak nahradime aktualnu cestu susedom
        if dlzka_akt > dlzka_nova:
            akt_cesta = novy_sused[:]
            dlzka_akt = int(cela_dlzka(akt_cesta))
            #kontrolujeme ci je aktualna cesta lepsia ako najlepsia cesta co sme nasli
            if dlzka_akt < dlzka_top:
                top_cesta = akt_cesta[:]
                dlzka_top = dlzka_akt
        #ak nie tak pod urcitou pravdepodobnostou nahradime aktualnu cestu horsim susedom
        else:
            #vypocet pravdepodobnosti podla vzorca
            pravdepodobnost = math.exp((dlzka_akt - dlzka_nova) / teplota)
            random_cislo = random.uniform(0,1)
            #ak je pravdepodobnost vacsia ako nahodne cislo od 0 po 1 tak cesty vymenime
            if pravdepodobnost > random_cislo:
                akt_cesta = novy_sused[:]
                dlzka_akt = int(cela_dlzka(akt_cesta))
                # kontrolujeme ci je aktualna cesta lepsia ako najlepsia cesta co sme nasli
                if dlzka_akt < dlzka_top:
                    top_cesta = akt_cesta[:]
                    dlzka_top = dlzka_akt

    graf_y.append(dlzka_akt)
    #znizenie teploty
    teplota = teplota * poklesT

print("-------------------------------------------------------------")
print("Konecna cesta:")
vypis(top_cesta)
print("Dlzka konecnej cesty:")
print(cela_dlzka(top_cesta))

print("Cas programu: %s" % (time.time() - start_time))

#vizualizacia miest a cesty, vlavo zaciatocna vpravo konecna
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

for first, second in zip(cesta[:-1], cesta[1:]):
    ax1.plot([first.get_x(), second.get_x()], [first.get_y(), second.get_y()], 'b')
ax1.plot([cesta[0].get_x(), cesta[-1].get_x()], [cesta[0].get_y(), cesta[-1].get_y()], 'b')
for i in cesta:
    ax1.plot(i.get_x(), i.get_y(), 'ro')

for first, second in zip(top_cesta[:-1], top_cesta[1:]):
    ax2.plot([first.get_x(), second.get_x()], [first.get_y(), second.get_y()], 'b')
ax2.plot([top_cesta[0].get_x(), top_cesta[-1].get_x()], [top_cesta[0].get_y(), top_cesta[-1].get_y()], 'b')
for i in top_cesta:
    ax2.plot(i.get_x(), i.get_y(), 'ro')

normalizovany_graf = NormalizeData(graf_y)
#nakreslenie line chartu
plot2 = plt.figure(2)
plt.plot(normalizovany_graf)
plt.ylabel("Distance")
plt.xlabel("Stage")
plt.show()




















