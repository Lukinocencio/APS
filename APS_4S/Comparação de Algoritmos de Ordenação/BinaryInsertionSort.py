from EntradaDados import Entrada
import timeit

def BuscaBinaria(ArrayBB, Valor, Inicio, Final):
    if Inicio == Final:
        if ArrayBB[Inicio] > Valor:
            return Inicio
        else:
            return Inicio + 1
    if Inicio > Final:
        return Inicio

    Meio = (Inicio + Final) // 2
    if ArrayBB[Meio] < Valor:
        return BuscaBinaria(ArrayBB, Valor, Meio + 1, Final)
    elif ArrayBB[Meio] > Valor:
        return BuscaBinaria(ArrayBB, Valor, Inicio, Meio - 1)
    else:
        return Meio 

def BinaryInsertionSort(ArrayBIS):
    for i in range(1, len(ArrayBIS)):
        Valor = ArrayBIS[i]
        Auxiliar = BuscaBinaria(ArrayBIS, Valor, 0, i - 1)
        ArrayBIS = ArrayBIS[:Auxiliar] + [Valor] + ArrayBIS[Auxiliar:i] + ArrayBIS[i + 1:]
    return ArrayBIS
        
def MedicaoTempo():
    ArrayBIS = BinaryInsertionSort(Entrada())
    TempoExecucao = timeit.timeit(lambda: BinaryInsertionSort(ArrayBIS), number = 10)
    print(TempoExecucao)

MedicaoTempo()