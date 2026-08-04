import os
import sys

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, "algoritmo"))

from algoritmo import miller_rabin

# Testes básicos do Miller-Rabin com números conhecidos: primos, compostos
# de fatores primos, números de Carmichael e primos de Mersenne.

# Com 40 rodadas a chance de erro é (1/4)^40, o que já é confiável mesmo
# pra números grandes (acima de 2^64).
RODADAS = 40


def teste_primos_conhecidos():
    primos_conhecidos = [101, 103, 997, 7919, 104729, 1299709, 15485863, 32452843, 49979687, 67867967, 86028121, 982451653]
    total_erros = 0

    titulo = "Testando Primos Conhecidos"
    print(f"{'-' * 60}")
    print(f"-{titulo:^58}-")
    print(f"{'-' * 60}")

    for primo in primos_conhecidos:
        if miller_rabin(primo, RODADAS):
            print(f" {f'{primo} é um número primo.':<58}")
        else:
            # não deveria acontecer, todos os números aqui são primos
            print(f" {f'{primo} é primo, mas foi classificado como composto.':<58}")
            total_erros += 1

    print(f"{'-' * 60}")
    print(f" {f'Total de falhas: {total_erros:>2} de {len(primos_conhecidos):>2} testes realizados.':<58}")


def teste_compostos_de_fatores_primos():
    compostos = [101 * 103, 104729 * 1299709, 32452843 * 49979687, 67867967 * 982451653]
    total_erros = 0

    titulo = "Testando Compostos de Fatores Primos"
    print(f"{'-' * 60}")
    print(f"-{titulo:^58}-")
    print(f"{'-' * 60}")

    for composto in compostos:
        if miller_rabin(composto, RODADAS):
            print(f" {f'{composto} é um número composto, mas foi classificado como primo.':<56}")
            total_erros += 1
        else:
            print(f" {f'{composto} é composto.':<56}")

    print(f"{'-' * 60}")
    print(f" {f'Total de falhas: {total_erros:>2} de {len(compostos):>2} testes realizados.':<56}")


# Números de Carmichael são compostos ímpares que passam no teste de Fermat
# pra todas as bases coprimas com eles, além de outros testes mais simples.
# O Miller-Rabin foi criado justamente pra pegar esses casos, mas vale
# lembrar que ainda existe uma chance pequena de algum passar, dependendo
# do número de rodadas e das bases sorteadas.
#
# Referências:
# https://files.cercomp.ufg.br/weby/up/1170/o/APChavesRO14.pdf
# https://en.wikipedia.org/wiki/Carmichael_number
def teste_numeros_de_carmichael():
    numeros_carmichael = [561, 1105, 1729, 2465, 2821, 6601, 8911, 162401, 172081, 188461, 41041, 62745, 63973]
    total_erros = 0

    titulo = "Testando Números de Carmichael"
    print(f"{'-' * 60}")
    print(f"-{titulo:^58}-")
    print(f"{'-' * 60}")

    for carmichael in numeros_carmichael:
        if miller_rabin(carmichael, RODADAS):
            print(f" {f'{carmichael} é um número composto de Carmichael, mas foi classificado como primo.':<58}")
            total_erros += 1
        else:
            print(f" {f'{carmichael} é composto.':<58}")

    print(f"{'-' * 60}")
    print(f" {f'Total de falhas: {total_erros:>2} de {len(numeros_carmichael):>2} testes realizados.':<58}")


# Primos de Mersenne têm a forma 2^p - 1 com p primo, mas nem todo expoente
# primo gera um primo de Mersenne (ex: 2^11 - 1 = 2047 = 23 * 89, composto).
#
# Referência: https://dma.uem.br/kit/jeepema-1/art3_1801.pdf
def teste_primos_de_mersenne():
    primos_mersenne = {
        "2 ** 61 - 1": 2305843009213693951,
        "2 ** 127 - 1": 170141183460469231731687303715884105727,
        "2 ** 89 - 1": 618970019642690137449562111,
        "2 ** 107 - 1": 162259276829213363391578010288127,
    }
    total_erros = 0

    titulo = "Testando Primos de Mersenne"
    print(f"{'-' * 60}")
    print(f"-{titulo:^58}-")
    print(f"{'-' * 60}")

    for primo, valor in primos_mersenne.items():
        print(f" {f'{primo} = {valor}':<58}")
        if miller_rabin(valor, RODADAS):
            print(f" {f'{primo} é um número primo.':<58}")
        else:
            print(f" {f'{primo} é primo, mas foi classificado como composto.':<58}")
            total_erros += 1

    print(f"{'-' * 60}")
    print(f" {f'Total de falhas: {total_erros:>2} de {len(primos_mersenne):>2} testes realizados.':<58}")


def main():
    print("\nTestes Básicos - Miller-Rabin\n")
    teste_primos_conhecidos()
    teste_compostos_de_fatores_primos()
    teste_numeros_de_carmichael()
    teste_primos_de_mersenne()
    print(f"{'-' * 60}")


if __name__ == "__main__":
    main()