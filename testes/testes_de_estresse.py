import sys
import os
import random
import time
from sympy import isprime

DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DIRETORIO_BASE, 'algoritmo'))

from algoritmo import miller_rabin

# Realizando testes de estresse do algoritmo Miller-Rabin.
# O objetivo é comparar a performance do algoritmo com a 
# função isprime() da biblioteca sympy, serão usados números
# aleatórios de 8 até 4096 bits, coletando informações de
# acertos e tempo de execução.

# Tamanhos em bits para os testes
TAMANHO_EM_BITS = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

# Quantidade de números aleatórios testados por tamanho.
# Números maiores levam mais tempo, o número de amostras
# diminui a medida que o tamanha dos números testados
# crescem.
def quantidade_de_testes_por_tamanho(tamanho):
    if tamanho <= 16:
        return 1000
    elif tamanho <= 32:
        return 500
    elif tamanho <= 64:
        return 200
    elif tamanho <= 128:
        return 200
    elif tamanho <= 256:
        return 100
    elif tamanho <= 512:
        return 50
    elif tamanho <= 2048: 

        # quantidade de testes para números de 1024 e 2048 bits.
        return 20
    else:
        return 10

def gerar_numero(bits):
    
    # Gera um número aleatório com a quantidade
    # de bits desejada.
    numero = random.getrandbits(bits)


    # O Miller-Rabin trabalha melhor com números ímpares,
    # pois números pares maiores que 2 já são compostos.
    numero |= 1


    # Garante que o número realmente possua
    # a quantidade de bits escolhida.
    #
    # Sem isso, o gerador poderia retornar
    # números menores que o tamanho esperado.
    numero |= (1 << (bits - 1))


    return numero


def teste_estresse(repeticoes=40):
    total_testes = total_diferencas = 0

    print (f" {'Bits':<10}"
        f"{'Tempo médio Miller-Rabin':<25}"
        f"{'Tempo médio sympy.isprime':<26}"
        f"{'Diferenças':<10}")

    # Testando cada tamanho da sequência
    for bits in TAMANHO_EM_BITS:

        # Quantidade de repetições para cada número de bits
        quantidade_testes = quantidade_de_testes_por_tamanho(bits)

        # Quantidade de divergências entre Miller_Rabin e a função isprime()
        diferencas = 0

        # Listas que guardam o tempo de execução de cada uma das funções.
        tempos_mr = []
        tempos_sp = []

        for _ in range(quantidade_testes):
            total_testes += 1
            numero = gerar_numero(bits)

            # Medição do tempo de Miller-Rabin
            inicio_mr = time.perf_counter()
            resultado_mr = miller_rabin(numero, repeticoes)
            fim_mr = time.perf_counter()
            tempos_mr.append(fim_mr - inicio_mr)

            # Medição do tempo da função isprime()
            inicio_sp = time.perf_counter()
            resultado_sp = isprime(numero)
            fim_sp = time.perf_counter()
            tempos_sp.append(fim_sp - inicio_sp)

            # Comparando os resultados 
            if resultado_mr != resultado_sp:
                diferencas += 1

        # Calculo da Média dos tempos de execução de cada algoritmo
        # media de tempo é dada por: 
        # soma dos tempo de resposta / quantidade de números.
        media_tempo_mr = sum(tempos_mr) / len(tempos_mr)
        media_tempo_sp = sum(tempos_sp) / len(tempos_sp)


        print (
            f" {bits:<10}"
            f"{media_tempo_mr:<25.8f}"
            f"{media_tempo_sp:<26.8f}"
            f"{diferencas:<10}")

        total_diferencas += diferencas
    
    print(f"{'-' * 73}")
    print (f"\nTotal de testes realizados: {total_testes}")
    print (f"Total de diferenças encontradas: {total_diferencas}")
    print (f"Percentual de acertos: {((total_testes - total_diferencas) / total_testes) * 100:.2f}%")
    print(f"{'-' * 73}")


def main():
    print("\nTeste de Estresse - Miller-Rabin x sympy.isprime\n")
    print(f"{'-' * 73}")
    print (f"-{'Comparação (Miller-Rabin x sympy.isprime) - Base 40':^71}-")
    print(f"{'-' * 73}")
    teste_estresse()

if __name__ == "__main__":
    main()

# Sobre a função isprime().
# a função isprime() contida na biblioteca sympy testa se um dado
# número n é primo ou não, tendo uma resposta definitiva para n < 2^34.
#
# Para números maiores é relizado um teste BPSW forte, o Baillie-PSW é
# um algoritmo é um algoritmo matemático altamente eficiente na deter -
# minação de um números primos. Ele combina um teste de primalidade de
# Fermat/Miller-Rabin na base 2 com um teste de Lucas forte. O teste 
# não possui contraexemplos desde sua publicação, o que torna a função
# altamente confiável para os nossos teste.
# 
# Referências: https://docs.sympy.org/latest/modules/ntheory.html
# Tópico: isprime()