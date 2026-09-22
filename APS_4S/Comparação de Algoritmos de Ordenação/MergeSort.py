from EntradaDados import Entrada
import timeit

def MergeSort(ArrayMS):
    if len(ArrayMS) > 1:
        Meio = len(ArrayMS) // 2
        Esquerda = ArrayMS[:Meio]
        Direita = ArrayMS[Meio:]

        MergeSort(Esquerda)
        MergeSort(Direita)

        IndiceEsquerda = 0
        IndiceDireita = 0
        IndiceLista = 0

        while IndiceEsquerda < len(Esquerda) and IndiceDireita < len(Direita):
            if Esquerda[IndiceEsquerda] < Direita[IndiceDireita]:
                ArrayMS[IndiceLista] = Esquerda[IndiceEsquerda]
                IndiceEsquerda += 1
            else:
                ArrayMS[IndiceLista] = Direita[IndiceDireita]
                IndiceDireita += 1 
            IndiceLista += 1       

        while IndiceEsquerda < len(Esquerda):
            ArrayMS[IndiceLista] = Esquerda[IndiceEsquerda]
            IndiceEsquerda += 1
            IndiceLista += 1

        while IndiceDireita < len(Direita):
            ArrayMS[IndiceLista] = Direita[IndiceDireita]
            IndiceDireita += 1
            IndiceLista += 1


def MedicaoTempo():
    ArrayMS = Entrada()
    TempoExecucao = timeit.timeit(lambda: MergeSort(ArrayMS), number = 10)
    print(TempoExecucao)

MedicaoTempo()