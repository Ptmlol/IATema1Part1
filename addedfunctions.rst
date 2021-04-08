    **Functii adaugate sau completate:**

.. code-block:: python

    def __init__(self, nr_ordine, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h
        self.nr_ordine = nr_ordine



In aceasta metode de initializare din cadrul clasei ``class Graph`` am adaugat variabila ``self.nr_ordine``
care are ca scop retinerea numarului de ordine al nodului in graf.

Variabila este afisata impreuna cu drumul atunci cand solutia este gasita

.. code-block:: python

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

Functia de testare scop a fost complet reimplementata in felul urmator:

.. code-block:: python

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

Functia primeste ca parametrul nodul curent care contine o configuratie la un moment dat.

Transformam configuratia intr-o matrice utilizand metoda ``.array()`` din  modulul ``numpy``.

Stim din cerinta ca o stare scop are obligatoriu ``0`` pe ultima pozitie din matrice, asadar verificam intai daca
aceasta conditie este indeplinita pentru a nu verifica degeaba conditiile complexe.

Parcurgem matricea si testam pe fiecare pozitie, exceptand prima pozitie si ultima, daca este indeplinita conditia de stare scop.
Returnam ``True`` doar atunci cand am reusit sa parcurgem cu succes toate elementele din matrice fara sa
iesim din prima functie  ``for`` inainte ca aceasta sa fie iterata complet, altfel returnam ``False``.


Pentru verificarea corectitudinii datelor de intrare am implementat doua metode:

.. code-block:: python

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


Metoda ``extract_digits`` este folosita pentru a formata lista ``['5', '1 2 3', '4 5 6', '7 8 0']`` primita ca argument ``lst`` in lista ``[['5'], ['1 2 3'], ['4 5 6'], ['7 8 0']]``,

Introducem rezultatul acestei functii in variabila ``transforming`` si o formatam transformand fiecare tip de data ``str`` in ``int``.

Variabila ``formated`` este variabila care contine lista finala pe care se vor aplica verificari ``[['5'], ['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]``.

Ne folosim de faptul ca stim ca prima linie trebuie sa contina un singur numar si testam aceasta conditie, apoi stim ca
urmatoarele liste din lista trebuie sa aiba aceeasi dimensiune deoarece matricea noastra este patratica, asadar atribuim unei variabile
lungimea primei linii din matrice si apoi parcurgem restul listei si verificam daca liniile au aceeasi dimensiune.

Programul returneaza un mesaj si se opreste daca una din aceste doua conditii este indeplinita.

Aceste date de intrare sunt verificate in momentul citirii lor din fisier.


.. code-block:: python

    class Graph:  # graful problemei
        def __init__(self, nume_fisier):
            f = open(nume_fisier, "r")
            sirFisier = f.read()
            self.verf_date_intrare(sirFisier)



In cadrul constructorului din clasa ``graph`` am construit matricea de restrictie:

.. code-block:: python

    try:
            listaLinii = sirFisier.strip().split("\n")
            self.k = listaLinii.pop(0)
            self.start = []
            for linie in listaLinii:
                self.start.append([int(x) for x in linie.strip().split(" ")])
        except:
            print("Eroare la parsare!")
            sys.exit(0)
        self.restrict_matrix = [[0 for x in range(len(self.start[0]))] for y in range(len(self.start[0]))]
        for i in range(len(self.start)):
            for j in range(len(self.start[i])):
                if int(self.start[i][j]) == 0:
                    line_zero = i
                    column_zero = j

        try:
            for i in range(len(self.start[0])):
                for j in range(len(self.start[0])):
                    if i == line_zero and j == column_zero:
                        self.restrict_matrix[i][j] = 1
        except Exception:
            pass


Am retinut in ``self.k`` primul element din fisier care reprezinta numarul maxim de pozitionari ale placutei goale pe un loc in configurare.

Am declarat apoi o matrice goala de dimensiunile matricei noastre din fisier.

Cautam in matricea noastra din fisier pozitia in care se afla placuta libera si retinem coordonatele in cele doua variabile denumite ``line_zero`` pentru linie si ``column_zero`` pentru coloana.

Acolo unde gasim placuta libera punem ``1`` in matricea de restrictie deoarece din start acolo exista elementul ``0`` o data.


.. code-block:: python

    for index, (lPlacuta, cPlacuta) in enumerate(directii):
        if 0 <= lPlacuta < 3 and 0 <= cPlacuta < 3:
            if int(self.restrict_matrix[lPlacuta][cPlacuta]) < int(self.k):

In metoda de generare a succesorilor ``genereazaSuccesori`` verificam inainte sa generam succesori daca conditia din enunt este indeplinita, anume daca se permite placutei libere sa ocupe locul liber in urmatoarea configuratie.

Dupa ce am generat succesorii crestem pentru configuratia care corespunde succesorului generat, contorul de pe pozitia placutei libere ``self.restrict_matrix[lPlacuta][cPlacuta] += 1``.


Pentru retinerea numarului maxim de noduri am declarat o variabila globala ``max_control`` care este actualizata la fiecare generare de succesori:

.. code-block:: python

    nr_noduri += 1
    if nr_noduri > max_control:
        max_control = nr_noduri

Variabila ``nr_noduri`` este asemenea globala si retine numarul de noduri dintr-un drum, aceasta creste la generare si este reintializata cu 0 la inceputul fiecarui algoritm cu care generam solutii:

.. code-block:: python

    def uniform_cost(gr, nrSolutiiCautate, tip_euristica, timeoutss):
        nr_noduri = 0

Variabila ``add`` este si ea globala si ne foloseste la retinerea numarului de index al fiecarui nod din drum, ea este initializata cu ``1`` la inceputul fiecarui algoritm si creste la generarea succesorilor:

.. code-block:: python

    def a_star_opt(gr, nrSolutiiCautate, tip_euristica, timeoutss):
        add = 1

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
    ...
    ...
        add += 1
        if nr_noduri > max_control:
            max_control = nr_noduri
        listaSuccesori.append(NodParcurgere(add, copieMatrice, nodCurent, nodCurent.g + costArc,
                                            self.calculeaza_h(copieMatrice, tip_euristica)))

In clasa ``NodParcurgere`` la generarea unei configuratii pentru configuratia respectiva crestem variabila ``add`` cu ``1``.
