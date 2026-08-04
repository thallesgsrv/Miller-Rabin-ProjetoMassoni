import os
import sys
import matplotlib.pyplot as plt

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, "testes"))

from testes import executar_comparacao


def gerar_grafico():
    resultados = executar_comparacao(repeticoes=100)

    bits = [r.bits for r in resultados]
    tempos_miller = [r.tempo_miller for r in resultados]
    tempos_ingenuo = [r.tempo_ingenuo for r in resultados]

    plt.figure(figsize=(8, 5))
    plt.plot(bits, tempos_miller, marker="o", label="Miller-Rabin")
    plt.plot(bits, tempos_ingenuo, marker="s", label="Teste Ingênuo")
    plt.title("Comparação de desempenho: Miller-Rabin x Teste Ingênuo")
    plt.xlabel("Tamanho do número (bits)")
    plt.ylabel("Tempo médio (segundos)")
    plt.yscale("log")  # o ingênuo cresce muito mais rápido, log ajuda a ver a diferença
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    gerar_grafico()