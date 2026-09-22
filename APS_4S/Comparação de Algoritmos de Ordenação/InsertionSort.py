from EntradaDados import Entrada
import timeit

def InsertionSort(ArrayIS):
    QuantidadeLista = len(ArrayIS)
    for i in range(QuantidadeLista):
        Numero = ArrayIS[i]
        Auxiliar = i - 1
        while Auxiliar >= 0 and Numero < ArrayIS[Auxiliar]:
            ArrayIS[Auxiliar + 1 ] = ArrayIS[Auxiliar]
            Auxiliar = Auxiliar -1
        ArrayIS[Auxiliar + 1] = Numero

def MedicaoTempo():
    ArrayIS = Entrada()
    TempoExecucao = timeit.timeit(lambda: InsertionSort(ArrayIS), number = 10)
    print(TempoExecucao)

MedicaoTempo()