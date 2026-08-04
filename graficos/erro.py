import matplotlib.pyplot as plt
from testes import executar_teste_carmichael


def grafico_taxa_de_erro():
    resultados = executar_teste_carmichael(repeticoes_por_rodada=1000)

    rodadas = [r.rodadas for r in resultados]
    # quando dá zero falso positivo, usamos um valor mínimo só pra conseguir
    # plotar no eixo logarítmico (log de 0 não existe)
    taxas_experimentais = [max(r.taxa_erro, 1e-10) for r in resultados]
    taxas_teoricas = [(1 / 4) ** r * 100 for r in rodadas]

    plt.figure(figsize=(8, 5))
    plt.plot(rodadas, taxas_experimentais, marker="o", label="Taxa experimental")
    plt.plot(rodadas, taxas_teoricas, marker="s", linestyle="--", label="Limite teórico (1/4)^k")
    plt.title("Taxa de erro do Miller-Rabin")
    plt.xlabel("Quantidade de rodadas (k)")
    plt.ylabel("Probabilidade de erro (%)")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    grafico_taxa_de_erro()