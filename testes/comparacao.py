import os
import sys
import math
import time
from dataclasses import dataclass

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, "algoritmo"))
sys.path.append(os.path.join(DIRETORIO_BASE, "utils"))

from algoritmo import miller_rabin
from numeros import gerar_numero

TAMANHOS_BITS = [16, 20, 24, 28, 32]


@dataclass
class ResultadoComparacao:
    bits: int
    tempo_miller: float
    tempo_ingenuo: float


def teste_ingenuo(numero):
    # Método clássico: procura um divisor até √n. Todo composto tem pelo
    # menos um divisor <= √n, então não precisa testar além disso.
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False

    limite = math.isqrt(numero)
    for divisor in range(3, limite + 1, 2):
        if numero % divisor == 0:
            return False
    return True


def executar_comparacao(repeticoes=100):
    resultados = []

    for bits in TAMANHOS_BITS:
        tempo_miller = 0
        tempo_ingenuo = 0

        for _ in range(repeticoes):
            numero = gerar_numero(bits)

            inicio = time.perf_counter()
            miller_rabin(numero, 10)
            tempo_miller += time.perf_counter() - inicio

            inicio = time.perf_counter()
            teste_ingenuo(numero)
            tempo_ingenuo += time.perf_counter() - inicio

        resultados.append(ResultadoComparacao(bits, tempo_miller / repeticoes, tempo_ingenuo / repeticoes))

    return resultados


def main():
    resultados = executar_comparacao()

    print("\nComparação Miller-Rabin x Ingênuo\n")
    print(f"{'Bits':<10}{'Miller-Rabin':<20}{'Ingênuo'}")
    for r in resultados:
        print(f"{r.bits:<10}{r.tempo_miller:<20.8f}{r.tempo_ingenuo:.8f}")


if __name__ == "__main__":
    main()