=====================================
Tema 1 - Cautarea Informata - 8Puzzle
=====================================

    **Metoda de apelare:**

Programul se apeleaza din linia de comanda (terminal) folosind urmatoarea sintaxa:
``python [numeProgram] -i [PathToInputFolder] -o [PathToOutputFolder] -n [NumberOfSolutions] -t [Timeout(seconds)]``

sau

``python [numeProgram] --input_path [PathToInputFolder] --output_path [PathToOutputFolder] --nsol [NumberOfSolutions] --timeout [Timeout(seconds)]``

Aceasta modalitate de citire a argumentelor a fost realizata cu ajutorul modulului ``optparse`` si implementat cu urmatoarea sintaxa:

.. code-block:: python

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input_path", dest="inputs_path", help="Path to the folder where inputs are located")
    parser.add_option("-o", "--output_path", dest="outputs_path", help="Path to the output folder")
    parser.add_option("-n", "--nsol", dest="nsol", help="Number of solutions")
    parser.add_option("-t", "--timeout", dest="timeouts", help="Timeout")

*Exemplu:* python 8puzzle.py -i D:\Python\TemeIA\IATema1\Inputs -o D:\Python\TemeIA\IATema1\Outputs -n 1 -t 10

    **Euristica:**

.. code-block:: python

    tip_euristica == "euristica admisibila 1":
                h = 0
                for lPlacutaC in range(len(infoNod)):
                    for cPlacutaC in range(len(infoNod[0])):
                        if infoNod[lPlacutaC][cPlacutaC] != 0:
                            placuta = infoNod[lPlacutaC][cPlacutaC]
                            lPlacutaF = (placuta - 1) // len(infoNod[0])
                            cPlacutaF = (placuta - 1) % len(infoNod[0])
                            h += abs(lPlacutaF - lPlacutaC) + abs(cPlacutaF - cPlacutaC)
                return h

Aceasta euristica incearca sa calculeze numarul minim de mutari pentru stiind ...