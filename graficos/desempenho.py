import sys
import os
import time
import matplotlib.pyplot as plt
from dataclasses import dataclass

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, "algoritmo"))
sys.path.append(os.path.join(DIRETORIO_BASE, "utils"))

from algoritmo import miller_rabin
from numeros import gerar_numero

# Mede como o tempo de execução escala com o tamanho da entrada (em bits),
# pra ver na prática se acompanha a complexidade teórica O(log n) por rodada.
TAMANHOS_BITS = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]


@dataclass
class ResultadoDesempenho:
    bits: int
    tempo_medio: float


def teste_desempenho(repeticoes):
    resultado = []

    for bits in TAMANHOS_BITS:
        soma_tempos = 0
        for _ in range(repeticoes):
            numero = gerar_numero(bits)
            inicio = time.perf_counter()
            miller_rabin(numero, 10)  # k=10 é só pra ter uma execução realista, não importa a confiabilidade aqui
            soma_tempos += time.perf_counter() - inicio

        resultado.append(ResultadoDesempenho(bits, soma_tempos / repeticoes))

    return resultado


def plotar_grafico(resultados):
    bits = [r.bits for r in resultados]
    tempos = [r.tempo_medio for r in resultados]

    plt.plot(bits, tempos, marker="o", label="Miller-Rabin")
    plt.title("Desempenho do Miller-Rabin em função do tamanho da entrada")
    plt.xlabel("Tamanho da entrada (bits)")
    plt.ylabel("Tempo de execução (s)")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.show()


def grafico_desempenho():
    resultados = teste_desempenho(1000)
    plotar_grafico(resultados)


if __name__ == "__main__":
    grafico_desempenho()