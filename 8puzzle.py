# documentatie functii noi adaugate - https://github.com/Ptmlol/IATema1Part1/blob/main/addedfunctions.rst
# documentatie propriu zisa ( metoda de apelare ) https://github.com/Ptmlol/IATema1Part1/blob/main/documentatie.rst
import copy
import optparse
import sys
import os
import time
import numpy


class NodParcurgere:
    def __init__(self, nr_ordine, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h
        self.nr_ordine = nr_ordine

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False):
        l = self.obtineDrum()
        for nod in l:
            print("Nr. Ordine", str(nod.nr_ordine))
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

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        sir += "\n"
        return sir


def cautaElemMatr(matr, elem): # returneaza pozitia  unui element din matrice
    for i in range(len(matr)):
        for j in range(len(matr[i])):
            if int(matr[i][j]) == int(elem):
                return i, j


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sirFisier = f.read()
        self.verf_date_intrare(sirFisier)
        try:
            listaLinii = sirFisier.strip().split("\n")
            self.k = listaLinii.pop(0)
            self.start = []
            for linie in listaLinii:
                self.start.append([int(x) for x in linie.strip().split(" ")])
        except:
            print("Eroare la parsare!")
            sys.exit(0)
        self.restrict_matrix = [[0 for x in range(len(self.start[0]))] for y in range(len(self.start[0]))]# declaram o matrice goala de dimensiunea matricei noastre din fisier
        for i in range(len(self.start)): # cautam in matricea noastra din fisier pozitia in care se afla placuta libera ( 0 )
            for j in range(len(self.start[i])):
                if int(self.start[i][j]) == 0:
                    line_zero = i
                    column_zero = j

        try: # punem 1 acolo unde este placuta libera deoarece ea din start gazduieste placuta libera 1 data
            for i in range(len(self.start[0])):
                for j in range(len(self.start[0])):
                    if i == line_zero and j == column_zero:
                        self.restrict_matrix[i][j] = 1
        except Exception:
            pass

    def testeaza_scop(self, nodCurent):
        to_matrix = numpy.array(nodCurent.info)
        if int(to_matrix[-1][-1]) == 0:
            for i in range(0, len(to_matrix)):
                for j in range(0, len(to_matrix)):
                    if not i == j == len(to_matrix) - 1 and not i == j == 0:
                        if i == 0 and j >= 1:
                            if int(to_matrix[i][j - 1]) < int(to_matrix[i][j]):
                                pass
                            else:
                                return False
                        if i >= 1 and j == 0:
                            if int(to_matrix[i - 1][j]) < int(to_matrix[i][j]):
                                pass
                            else:
                                return False
                        if i >= 1 and j >= 1:
                            if int(to_matrix[i - 1][j]) < int(to_matrix[i][j]) and int(to_matrix[i][j - 1]) < int(to_matrix[i][j]):
                                pass
                            else:
                                return False
            return True
        else:
            return False

    @staticmethod
    def extract_digits(lst):
        res = []
        for el in lst:
            sub = el.split(', ')
            for strng in sub:
                sub_2 = strng.strip("'").split(" ")
                res.append(sub_2)
        return (res)

    def verf_date_intrare(self, sir_fisier):
        transforming = self.extract_digits(sir_fisier.split("\n")) # ['5', '1 2 3', '4 5 6', '7 8 0']  -> [['5'], ['1 2 3'], ['4 5 6'], ['7 8 0']] -> [['5'], ['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
        formated = [[int(x) for x in lst] for lst in transforming]
        if len(formated[0]) != 1:
            print("Datele de intrare nu au formatul corect!")
            exit()
        standard_len = len(formated[1])
        for i in range(2, len(formated)):
            if len(formated[i]) != standard_len:
                print("Datele de intrare nu au formatul corect!")
                exit()


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
        global nr_noduri, max_control, add
        listaSuccesori = []
        for lGol in range(len(nodCurent.info)):
            try:
                cGol = nodCurent.info[lGol].index(0)
                break
            except:
                pass
        try:
            directii = [[lGol, cGol - 1], [lGol, cGol + 1], [lGol - 1, cGol], [lGol + 1, cGol], [lGol + 1, cGol + 1], [lGol + 1, cGol - 1], [lGol - 1, cGol - 1], [lGol - 1, cGol + 1]]
            for index, (lPlacuta, cPlacuta) in enumerate(directii):
                if 0 <= lPlacuta < 3 and 0 <= cPlacuta < 3:
                    if int(self.restrict_matrix[lPlacuta][cPlacuta]) < int(self.k):
                        copieMatrice = copy.deepcopy(nodCurent.info)
                        copieMatrice[lGol][cGol] = copieMatrice[lPlacuta][cPlacuta]
                        copieMatrice[lPlacuta][cPlacuta] = 0
                        if not nodCurent.contineInDrum(copieMatrice):  # and not self.nuAreSolutii(copieMatrice):
                            if index < 4:
                                costArc = 1
                                nr_noduri += 1
                                add += 1
                                if nr_noduri > max_control:
                                    max_control = nr_noduri
                                listaSuccesori.append(NodParcurgere(add, copieMatrice, nodCurent, nodCurent.g + costArc,
                                                                    self.calculeaza_h(copieMatrice, tip_euristica)))
                            if index >= 4:
                                costArc = 2
                                nr_noduri += 1
                                add += 1
                                if nr_noduri > max_control:
                                    max_control = nr_noduri
                                listaSuccesori.append(NodParcurgere(add, copieMatrice, nodCurent, nodCurent.g + costArc,
                                                                    self.calculeaza_h(copieMatrice, tip_euristica)))
                        self.restrict_matrix[lPlacuta][cPlacuta] += 1
                    else:
                        pass

        except Exception:
            pass
        return listaSuccesori


    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            return 1
        elif tip_euristica == "euristica admisibila 1":
            h = 0
            for lPlacutaC in range(len(infoNod)):
                for cPlacutaC in range(len(infoNod[0])):
                    if infoNod[lPlacutaC][cPlacutaC] != 0:
                        placuta = infoNod[lPlacutaC][cPlacutaC]
                        lPlacutaF = (placuta - 1) // len(infoNod[0])
                        cPlacutaF = (placuta - 1) % len(infoNod[0])
                        h += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
            return h
        elif tip_euristica == "euristica admisibila 2":
            h = 0
            for lPlacutaC in range(len(infoNod)):
                for cPlacutaC in range(len(infoNod[0])):
                    if infoNod[lPlacutaC][cPlacutaC] != 0:
                        placuta = infoNod[lPlacutaC][cPlacutaC]
                        lPlacutaF = (placuta - 1) // len(infoNod[0])
                        cPlacutaF = (placuta - 1) % len(infoNod[0])
                        h += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
            return h
        elif tip_euristica == "euristica neadmisibila":
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


def a_star_opt(gr, nrSolutiiCautate, tip_euristica, timeoutss):
    global nr_noduri, add
    add = 1
    nr_noduri = 0
    # c are rolul listei Open (cu nodurile neexpandate)
    c = [NodParcurgere(0, gr.start, None, 0, gr.calculeaza_h(gr.start))]
    # lista closed contine nodurile deja expandate
    closed = []
    start_time = time.time()
    while len(c) > 0:
        exec_time = time.time()
        if round(exec_time) - round(start_time) >= int(timeoutss):
            print("Execution timed out")
            return
        nodCurent = c.pop(0)
        closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            print("Drum Solutie:\n", end="")
            nodCurent.afisDrum(afisCost=True)
            print("Numar total noduri calculate:", nr_noduri, "noduri")
            print("Maximul de noduri din memorie:", max_control)
            solution_found = time.time()
            print("Timp Solutie:", solution_found - start_time, "secunde")
            print("Matricea de restrictie:")
            print(gr.restrict_matrix)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitCoada = False
            for nodCoada in c:
                try:
                    if s.info == nodCoada.info:
                        gasitCoada = True
                        if s.f >= nodCoada.f:
                            lSuccesori.remove(s)
                        else:
                            c.remove(nodCoada)
                except Exception:
                    pass
            if not gasitCoada:
                for nodClosed in closed:
                    try:
                        if s.info == nodClosed.info:
                            if s.f >= nodClosed.f:
                                lSuccesori.remove(s)
                            else:
                                closed.remove(nodClosed)
                    except Exception:
                        pass

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


def a_star(gr, nrSolutiiCautate, tip_euristica, timeoutss):
    global nr_noduri, add
    nr_noduri = 0
    add = 1
    #c = [NodParcurgere(gr.indiceNod(), gr.start, None, 0, gr.calculeaza_h(gr.start))]
    c = [NodParcurgere(0, gr.start, None, 0, gr.calculeaza_h(gr.start))]
    if gr.nuAreSolutii(gr.start):
        print("Nu are solutii")
        return
    start_time = time.time()
    while len(c) > 0:
        exec_time = time.time()
        if round(exec_time) - round(start_time) >= int(timeoutss):
            print("Execution timed out")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            print("Drum Solutie: ")
            nodCurent.afisDrum(afisCost=True)
            print("Numar total noduri calculate:", nr_noduri, "noduri")
            print("Maximul de noduri din memorie:", max_control)
            solution_found = time.time()
            print("Timp Solutie:", solution_found - start_time, "secunde")
            print("Matricea de restrictie:")
            print(gr.restrict_matrix)
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


def uniform_cost(gr, nrSolutiiCautate, tip_euristica, timeoutss):
    global nr_noduri, add
    add = 1
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    nod_start = NodParcurgere(0, gr.start, None, 0, gr.calculeaza_h(gr.start))
    start_time = time.time()
    c = [nod_start]
    nr_noduri = 0
    while len(c) > 0:
        exec_time = time.time()
        if round(exec_time) - round(start_time) >= int(timeoutss):
            print("Execution timed out")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            print("Drum Solutie: ")
            nodCurent.afisDrum(True)
            print("Numar total noduri calculate:", nr_noduri, "noduri")
            print("Maximul de noduri din memorie:", max_control)
            solution_found = time.time()
            print("Timp Solutie:", solution_found - start_time, "secunde")
            print("Matricea de restrictie:")
            print(gr.restrict_matrix)
            print("\n----------------\n")
            nrSolutiiCautate -= 1

            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)

        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def ida_star(gr, nrSolutiiCautate, tip_euristica, timeoutss):
    nodStart = NodParcurgere(0, gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    start_time = time.time()
    while (True):
        exec_time = time.time()
        if round(exec_time) - round(start_time) >= int(timeoutss):
            print("Execution timed out")
            return
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, tip_euristica, timeoutss=timeoutss, start_time=start_time)
        if nrSolutiiCautate == -1 and rez == "timeout":
            return
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        #print(">>> Limita noua: ", limita)


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica, timeoutss, start_time):
    global nr_noduri, add
    add = 1
    exec_time = time.time()
    if round(exec_time) - round(start_time) >= int(timeoutss):
        print("Execution timed out")
        return (-1, 'timeout')
    if nodCurent.f > limita:
        return (nrSolutiiCautate, nodCurent.f)
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Drum Solutie: ")
        nodCurent.afisDrum(afisCost=True)
        print("Numar total noduri calculate:", nr_noduri, "noduri")
        print("Maximul de noduri din memorie:", max_control)
        solution_found = time.time()
        print("Timp Solutie:",solution_found - start_time, "secunde")
        print("Matricea de restrictie:")
        print(gr.restrict_matrix)
        print("Limita: ", limita)
        print("\n----------------\n")

        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return (nrSolutiiCautate, 'gata')
    nr_noduri = 0
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        (nrSolutiiCautate, rez) = construieste_drum(gr, s, limita, nrSolutiiCautate, tip_euristica, timeoutss, start_time)
        if nrSolutiiCautate == -1 and rez == "timeout":
            return (-1, 'timeout')
        if rez == 'gata':
            return (nrSolutiiCautate, 'gata')
        #print ('Compara ', rez, ' cu ', minim)
        if rez < minim:
            minim = rez
            #print ('Noul minim: ', minim)
    return (nrSolutiiCautate, minim)

#########

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input_path", dest="inputs_path", help="Path to the folder where inputs are located")
    parser.add_option("-o", "--output_path", dest="outputs_path", help="Path to the output folder")
    parser.add_option("-n", "--nsol", dest="nsol", help="Number of solutions")
    parser.add_option("-t", "--timeout", dest="timeouts", help="Timeout")
    (option, argument) = parser.parse_args()
    return option


global original
global nr_noduri
global max_control
if __name__ == "__main__":
    original = sys.stdout
    path_to_inputs = get_arguments().inputs_path
    path_to_outputs = get_arguments().outputs_path
    nsol = get_arguments().nsol
    timeout = get_arguments().timeouts
    arr = os.listdir(path_to_inputs)
    nr_noduri = 0
    max_control = 0
    add = 0
    for inputs in arr:
        sys.stdout = original
        file = open(path_to_outputs + "\\" + inputs.replace(inputs[len(inputs) - 3:], "out"), "a+")
        file.seek(0)
        file.truncate()
        sys.stdout = file
        gr = Graph(path_to_inputs + "\\" + inputs)
        print("Solutie cu UCS")
        uniform_cost(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 1", timeoutss=timeout)
        print("==============\n")
        print("Solutie cu A*")
        a_star(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 1", timeoutss=timeout)
        #a_star(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 2", timeoutss=timeout)
        print("==============\n")
        print("Solutie cu A* optimizat")
        a_star_opt(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 1", timeoutss=timeout)
        #a_star_opt(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 2", timeoutss=timeout)
        print("==============\n")
        print("Solutie cu IDA*")
        ida_star(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 1", timeoutss=timeout)
        #ida_star(gr, nrSolutiiCautate=int(nsol), tip_euristica="euristica admisibila 2", timeoutss=timeout)
    sys.stdout = original
    print("Done! Check '" + path_to_outputs + "' for solutions.")