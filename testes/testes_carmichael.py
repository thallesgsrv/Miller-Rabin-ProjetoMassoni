import os
import sys
from dataclasses import dataclass

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, "algoritmo"))

from algoritmo import miller_rabin

# Números de Carmichael passam no teste de Fermat pra várias bases, então
# são um bom caso difícil pra ver se o Miller-Rabin realmente pega esses
# compostos que enganam testes mais simples.
NUMEROS_DE_CARMICHAEL = (
    561, 1105, 1729, 2465, 2821,
    6601, 8911, 10585, 15841, 29341,
    41041, 46657, 52633, 62745,
    63973, 75361, 101101, 115921,
    126217, 162401, 172081, 188461,
    252601, 278545, 294409, 314821
)

RODADAS_MILLER_RABIN = (1, 2, 3, 5, 10, 20, 40)


@dataclass
class ResultadoCarmichael:
    rodadas: int
    falsos_positivos: int
    total_testes: int
    taxa_erro: float
    limite_teorico: float
    falsos_esperados: float


def executar_teste_carmichael(repeticoes_por_rodada=1000):
    print("Teste com números de Carmichael\n")
    print(f"{'Rodadas':<10}{'Falsos':<12}{'Total':<12}{'Erro (%)':<15}{'Limite (%)':<18}{'Esperado'}")

    resultados = []

    for quantidade_rodadas in RODADAS_MILLER_RABIN:
        falsos_positivos = 0
        total_testes = 0

        for numero in NUMEROS_DE_CARMICHAEL:
            for _ in range(repeticoes_por_rodada):
                total_testes += 1
                if miller_rabin(numero, quantidade_rodadas):
                    falsos_positivos += 1  # todo número dessa lista é composto, então isso é erro

        taxa_erro = (falsos_positivos / total_testes) * 100
        limite_teorico = ((1 / 4) ** quantidade_rodadas) * 100
        falsos_esperados = total_testes * ((1 / 4) ** quantidade_rodadas)

        resultado = ResultadoCarmichael(
            quantidade_rodadas, falsos_positivos, total_testes,
            taxa_erro, limite_teorico, falsos_esperados
        )
        resultados.append(resultado)

        print(
            f"{resultado.rodadas:<10}{resultado.falsos_positivos:<12}{resultado.total_testes:<12}"
            f"{resultado.taxa_erro:<15.8f}{resultado.limite_teorico:<18.8f}{resultado.falsos_esperados:.6f}"
        )

    return resultados


def main():
    executar_teste_carmichael(1000)


if __name__ == "__main__":
    main()