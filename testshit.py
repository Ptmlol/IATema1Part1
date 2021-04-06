"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) .
"""

import copy
import sys
import numpy

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        sir += "\n"
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sirFisier = f.read()
        try:
            listaLinii = sirFisier.strip().split("\n")
            self.start = []
            for linie in listaLinii:
                self.start.append([int(x) for x in linie.strip().split(" ")])
        except:
            print("Eroare la parsare!")
            sys.exit(0)  # iese din program


    def testeaza_scop(self, nodCurent):
        to_matrix = numpy.array(nodCurent.info)
        if int(to_matrix[-1][-1]) == 0:
            #print("PRINTAM NODCURENT.INFO", nodCurent.info)
            for i in range(0, len(to_matrix)):
                for j in range(0, len(to_matrix)):
                    if not i == j == len(to_matrix) - 1 and not i == j == 0:
                        if i == 0 and j >= 1:
                            if int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
                                pass
                            else:
                                return False
                        if i >= 1 and j == 0:
                            if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]):
                                pass
                            else:
                                return False
                        if i >= 1 and j >= 1:
                            if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]) and int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
                                pass
                            else:
                                return False
            return True
        else:
            return False


    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def nuAreSolutii(self, infoNod):
        listaMatrice = sum(infoNod, [])
        nrInversiuni = 0
        for i in range(len(listaMatrice)):
            if listaMatrice[i] != 0:
                for j in range(i + 1, len(listaMatrice)):
                    if listaMatrice[j] != 0:
                        if listaMatrice[i] > listaMatrice[j]:
                            nrInversiuni += 1
        return nrInversiuni % 2 == 1

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        for lGol in range(len(nodCurent.info)):
            try:
                cGol = nodCurent.info[lGol].index(0)
                break
            except:
                pass
        # stanga, dreapta, sus, jos
        directii = [[lGol, cGol - 1], [lGol, cGol + 1], [lGol - 1, cGol], [lGol + 1, cGol], [lGol + 1, cGol +1 ], [lGol + 1, cGol - 1], [lGol - 1, cGol - 1], [lGol - 1, cGol + 1]]
        for lPlacuta, cPlacuta in directii:
            if 0 <= lPlacuta < 3 and 0 <= cPlacuta < 3:
                copieMatrice = copy.deepcopy(nodCurent.info)
                copieMatrice[lGol][cGol] = copieMatrice[lPlacuta][cPlacuta]
                copieMatrice[lPlacuta][cPlacuta] = 0
                if not nodCurent.contineInDrum(copieMatrice):  # and not self.nuAreSolutii(copieMatrice):
                    costArc = 1
                    listaSuccesori.append(NodParcurgere(copieMatrice, nodCurent, nodCurent.g + costArc,
                                                        self.calculeaza_h(copieMatrice, tip_euristica)))

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            return 1
        else:
            h = 0
            for lPlacutaC in range(len(infoNod)):
                for cPlacutaC in range(len(infoNod[0])):
                    if infoNod[lPlacutaC][cPlacutaC] != 0:
                        placuta = infoNod[lPlacutaC][cPlacutaC]
                        lPlacutaF = (placuta - 1) // len(infoNod[0])
                        cPlacutaF = (placuta - 1) % len(infoNod[0])
                        h += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
            return h

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def a_star_opt(gr, nrSolutiiCautate, tip_euristica):
    # c are rolul listei Open (cu nodurile neexpandate)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    # lista closed contine nodurile deja expandate
    closed = []

    while len(c) > 0:
        #print("Coada actuala: " + str(c))
        nodCurent = c.pop(0)
        closed.append(nodCurent)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitCoada = False
            for nodCoada in c:
                if s.info == nodCoada.info:
                    gasitCoada = True
                    if s.f >= nodCoada.f:
                        lSuccesori.remove(s)
                    else:
                        c.remove(nodCoada)

            if not gasitCoada:
                for nodClosed in closed:
                    if s.info == nodClosed.info:
                        if s.f >= nodClosed.f:
                            lSuccesori.remove(s)
                        else:
                            closed.remove(nodClosed)

        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    #c = [NodParcurgere(gr.indiceNod(), gr.start, None, 0, gr.calculeaza_h(gr.start))]
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    # if gr.nuAreSolutii(gr.start):
    #     print("Nu are solutii")
    #     return
    while len(c) > 0:
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            print("Drum Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    return


def ida_star(gr, nrSolutiiCautate, tip_euristica):
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f

    while (True):
        #print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        #print(">>> Limita noua: ", limita)



def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
    #print ('A ajuns la: ', nodCurent)
    if nodCurent.f > limita:
        return (nrSolutiiCautate, nodCurent.f)
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print("\n----------------\n")

        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return (nrSolutiiCautate, 'gata')
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    minim = float('inf')
    for s in lSuccesori:
        (nrSolutiiCautate, rez) = construieste_drum(gr, s, limita,
                nrSolutiiCautate)
        if rez == 'gata':
            return (nrSolutiiCautate, 'gata')
        #print ('Compara ', rez, ' cu ', minim)
        if rez < minim:
            minim = rez
            #print ('Noul minim: ', minim)
    return (nrSolutiiCautate, minim)



gr = Graph("input.txt")

print("\n\n##################\nSolutii obtinute cu A*:")
#a_star_opt(gr, nrSolutiiCautate=1, tip_euristica="euristica nebanala")
print("SOL A STAR")
a_star(gr, nrSolutiiCautate=2, tip_euristica="euristica nebanala")
print("SOL IDA")
ida_star(gr, nrSolutiiCautate=2, tip_euristica="euristica nebanala")