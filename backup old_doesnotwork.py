# class Graph:  # graful problemei
#     def __init__(self, path_to_input): # creeam lista de start si lista scop ( modificari conform problemei noastre)
#         f = open(path_to_input, "r")
#         continutfisier = f.read()
#         f.close()
#         listaLinii = continutfisier.split("\n")  # listaLinii=["4 1 8","7 2 3","5 6 0"]
#         self.start = []
#         for sirLinie in listaLinii:
#             self.start.append(sirLinie.split())
#
#         print("Start: " + str(self.start) + "\n")
#
#
#     # @staticmethod
#     # def nuAreSolutii(infoNod): # verifica daca se poate trebuie pe cerinta
#     #     listaPiese = []
#     #     for linie in infoNod:
#     #         listaPiese.extend(linie)
#     #     nrInversiuni = 0
#     #     for i in range(len(listaPiese)-1):
#     #         if listaPiese[i] == '0':
#     #             continue
#     #         for j in range(i + 1, len(listaPiese)-1):
#     #             if listaPiese[j] == '0':
#     #                 continue
#     #             if listaPiese[j] < listaPiese[i]:
#     #                 nrInversiuni += 1
#     #
#     #     #if nrInversiuni % 2 == 1:
#     #         #return True
#     #     return False
#
#     def testeaza_scop(self, nodCurent):
#         to_matrix = numpy.array(nodCurent.info)
#         if int(to_matrix[-1][-1]) == 0:
#             #print("PRINTAM NODCURENT.INFO", nodCurent.info)
#             for i in range(0, len(to_matrix)):
#                 for j in range(0, len(to_matrix)):
#                     if not i == j == len(to_matrix) - 1 and not i == j == 0:
#                         if i == 0 and j >= 1:
#                             if int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
#                                 pass
#                             else:
#                                 return False
#                         if i >= 1 and j == 0:
#                             if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]):
#                                 pass
#                             else:
#                                 return False
#                         if i >= 1 and j >= 1:
#                             if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]) and int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
#                                 pass
#                             else:
#                                 return False
#             return True
#         else:
#             return False
#     # va genera succesorii sub forma de noduri in arborele de parcurgere
#
#     def genereazaSuccesori_2(self, nodCurent, tip_euristica="euristica banala"):
#         listaSuccesori = []
#         lGol, cGol = cautaElemMatr(nodCurent.info, '0') # pozitia lui 0 type: i,j
#         directii = [[0, -1], [1, -1], [0, 1],  [-1, 1], [-1, 0],  [-1, -1], [1, 0], [1, 1]]
#         for dl, dc in directii:
#             lPlacuta = lGol + dl # 1
#             cPlacuta = cGol + dc # 1
#             if 0 <= lPlacuta < len(nodCurent.info) and 0 <= cPlacuta < len(nodCurent.info[0]):
#                 copieInfo = copy.deepcopy(nodCurent.info)
#                 copieInfo[lGol][cGol] = copieInfo[lPlacuta][cPlacuta]
#                 copieInfo[lPlacuta][cPlacuta] = '0'
#                 if not nodCurent.contineInDrum(copieInfo):
#                     if dl == 0 or dc == 0:
#                         costArc = 1
#                         listaSuccesori.append(NodParcurgere(copieInfo, nodCurent, nodCurent.g + costArc,
#                                                             self.calculeaza_h(copieInfo, tip_euristica)))
#                     elif dl != 0 and dc != 0:
#                         costArc = 2
#                         listaSuccesori.append(NodParcurgere(copieInfo, nodCurent, nodCurent.g + costArc,
#                                                             self.calculeaza_h(copieInfo, tip_euristica)))
#
#         return listaSuccesori
#
#     def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
#         listaSuccesori = []
#         for lGol in range(len(nodCurent.info)):
#             try:
#                 cGol = nodCurent.info[lGol].index(0)
#                 break
#             except:
#                 pass
#         try:
#             directii = [[lGol, cGol - 1], [lGol, cGol + 1], [lGol - 1, cGol], [lGol + 1, cGol], [lGol + 1, cGol +1 ], [lGol + 1, cGol - 1], [lGol - 1, cGol - 1], [lGol - 1, cGol + 1]]
#             for lPlacuta, cPlacuta in directii:
#                 if 0 <= lPlacuta < 3 and 0 <= cPlacuta < 3:
#                     copieMatrice = copy.deepcopy(nodCurent.info)
#                     copieMatrice[lGol][cGol] = copieMatrice[lPlacuta][cPlacuta]
#                     copieMatrice[lPlacuta][cPlacuta] = 0
#                     if not nodCurent.contineInDrum(copieMatrice):  # and not self.nuAreSolutii(copieMatrice):
#                         costArc = 1
#                         listaSuccesori.append(NodParcurgere(copieMatrice, nodCurent, nodCurent.g + costArc,
#                                                             self.calculeaza_h(copieMatrice, tip_euristica)))
#         except Exception:
#             pass
#         return listaSuccesori
#
#     # euristica banala
#     # def calculeaza_h_2(self, infoNod, tip_euristica="euristica banala"):
#     #     if tip_euristica == "euristica banala":
#     #         return 1
#     #     else:
#     #         hTotal = 0
#     #         for lPlacutaC in range(len(infoNod)):  # linia placutei curente
#     #             for cPlacutaC in range(len(infoNod[lPlacutaC])):  # coloana placutei curente
#     #                 nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])
#     #                 # deducem linia si coloana pentru placuta in starea finala, folosindu-ne de nr ei si de faptul ca matricea e 3x3
#     #
#     #                 # linia si coloana placutei in starea finala
#     #                 lPlacutaF = (nrPlacuta - 1) // 3
#     #                 cPlacutaF = (nrPlacuta - 1) % 3
#     #                 hTotal += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
#     #         return hTotal
#
#     def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
#         if tip_euristica == "euristica banala":
#             return 1
#         else:
#             h = 0
#             for lPlacutaC in range(len(infoNod)):
#                 for cPlacutaC in range(len(infoNod[0])):
#                     if infoNod[lPlacutaC][cPlacutaC] != 0:
#                         placuta = infoNod[lPlacutaC][cPlacutaC]
#                         lPlacutaF = (placuta - 1) // len(infoNod[0])
#                         cPlacutaF = (placuta - 1) % len(infoNod[0])
#                         h += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
#             return h
#
#     def __repr__(self):
#         sir = ""
#         for (k, v) in self.__dict__.items():
#             sir += "{} = {}\n".format(k, v)
#         return sir
#
#
# def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
#     #print ('A ajuns la: ', nodCurent)
#     if nodCurent.f > limita:
#         return (nrSolutiiCautate, nodCurent.f)
#     if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
#         print("Solutie: ")
#         nodCurent.afisDrum()
#         print(limita)
#         print("\n----------------\n")
#
#         nrSolutiiCautate -= 1
#         if nrSolutiiCautate == 0:
#             return (nrSolutiiCautate, 'gata')
#     lSuccesori = gr.genereazaSuccesori(nodCurent)
#     minim = float('inf')
#     for s in lSuccesori:
#         (nrSolutiiCautate, rez) = construieste_drum(gr, s, limita,
#                 nrSolutiiCautate)
#         if rez == 'gata':
#             return (nrSolutiiCautate, 'gata')
#         #print ('Compara ', rez, ' cu ', minim)
#         if rez < minim:
#             minim = rez
#             #print ('Noul minim: ', minim)
#     return (nrSolutiiCautate, minim)
#
#
#
# def a_star(gr, nrSolutiiCautate, tip_euristica):
#     #c = [NodParcurgere(gr.indiceNod(), gr.start, None, 0, gr.calculeaza_h(gr.start))]
#     c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
#     #if gr.nuAreSolutii(gr.start):
#         #print("Nu are solutii")
#         #return
#     while len(c) > 0:
#         nodCurent = c.pop(0)
#         if gr.testeaza_scop(nodCurent):
#             print("Drum Solutie: ")
#             nodCurent.afisDrum(afisCost=True, afisLung=True)
#             print("\n----------------\n")
#             nrSolutiiCautate -= 1
#             if nrSolutiiCautate == 0:
#                 return
#         lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
#         for s in lSuccesori:
#             i = 0
#             gasit_loc = False
#             for i in range(len(c)):
#                 if c[i].f >= s.f:
#                     gasit_loc = True
#                     break
#             if gasit_loc:
#                 c.insert(i, s)
#             else:
#                 c.append(s)
#     return
#
#
# def ida_star(gr, nrSolutiiCautate, tip_euristica, timeoutss=None):
#     nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
#     limita = nodStart.f
#
#     while (True):
#         print("Limita de pornire: ", limita)
#         nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
#         if rez == "gata":
#             break
#         if rez == float('inf'):
#             print("Nu exista solutii!")
#             break
#         limita = rez
#         print(">>> Limita noua: ", limita)
#
#
# def a_star_opt(gr, nrSolutiiCautate, tip_euristica):
#     # c are rolul listei Open (cu nodurile neexpandate)
#     c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
#     # lista closed contine nodurile deja expandate
#     closed = []
#
#     while len(c) > 0:
#         print("Coada actuala: " + str(c))
#         nodCurent = c.pop(0)
#         closed.append(nodCurent)
#
#         if gr.testeaza_scop(nodCurent):
#             print("Solutie: ", end="")
#             nodCurent.afisDrum()
#             print("\n----------------\n")
#             nrSolutiiCautate -= 1
#             if nrSolutiiCautate == 0:
#                 return
#         lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
#         for s in lSuccesori:
#             gasitCoada = False
#             for nodCoada in c:
#                 if s.info == nodCoada.info:
#                     gasitCoada = True
#                     if s.f >= nodCoada.f:
#                         lSuccesori.remove(s)
#                     else:
#                         c.remove(nodCoada)
#
#             if not gasitCoada:
#                 for nodClosed in closed:
#                     if s.info == nodClosed.info:
#                         if s.f >= nodClosed.f:
#                             lSuccesori.remove(s)
#                         else:
#                             closed.remove(nodClosed)
#
#         for s in lSuccesori:
#             i = 0
#             gasit_loc = False
#             for i in range(len(c)):
#                 if c[i].f >= s.f:
#                     gasit_loc = True
#                     break
#             if gasit_loc:
#                 c.insert(i, s)
#             else:
#                 c.append(s)
#
#
# def uniform_cost(gr, nrSolutiiCautate, tip_euristica, timeoutss):
#     # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
#     c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
#
#     while len(c) > 0:
#         print("Coada actuala: " + str(c))
#         nodCurent = c.pop(0)
#
#         if gr.testeaza_scop(nodCurent):
#             print("Solutie: ", end="")
#             nodCurent.afisDrum()
#             print("\n----------------\n")
#             nrSolutiiCautate -= 1
#             if nrSolutiiCautate == 0:
#                 return
#         lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
#         for s in lSuccesori:
#             i = 0
#             gasit_loc = False
#             for i in range(len(c)):
#                 # ordonez dupa cost(notat cu g aici și în desenele de pe site)
#                 if c[i].g > s.g:
#                     gasit_loc = True
#                     break
#             if gasit_loc:
#                 c.insert(i, s)
#             else:
#                 c.append(s)
#