import random

from algoritmo import decomposicao
from algoritmo import testemunha

PRIMOS = [
    2, 3, 5, 7, 11, 13, 17, 19,
    23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79,
    83, 89, 97, 101, 103, 107
]

def miller_rabin(numero, quantidade_de_rodadas):

    # Casos base.
    # Todo número menor que 2 ou par
    # (tirando o próprio 2) é composto.
    if numero < 2:
        return False

    # Verificamos se o número é um dos primos pequenos.
    if numero in PRIMOS:
        return True

   # Depois verificamos se ele é divisível por algum deles.
   # Como a lista possui tamanho fixo, essa etapa possui 
   # custo constante em relação ao tamanho da entrada. 
   # Assim, conseguimos eliminar rapidamente vários números 
   # compostos antes mesmo de executar o Miller-Rabin.
    for primo in PRIMOS:
        if numero % primo == 0:
            return False

    # Fazemos a decomposição:
    #
    # n - 1 = 2^s * d
    expoente_da_decomposicao, parte_impar_da_decomposicao = decomposicao(numero)

    # Vamos repetir o teste várias vezes.
    # A cada rodada escolhemos uma base diferente.
    for _ in range(quantidade_de_rodadas):

        # Escolhemos uma testemunha aleatória.
        #
        # Quanto mais rodadas fizermos,
        # menor fica a chance de um número composto
        # passar pelo teste.
        base_aleatoria = random.randrange(2, numero - 1)

        # Basta uma única testemunha provar
        # que o número é composto para encerrarmos
        # o algoritmo.
        if not testemunha(
            base_aleatoria,
            numero,
            expoente_da_decomposicao,
            parte_impar_da_decomposicao
        ):
            return False

    # Se nenhuma testemunha conseguiu provar
    # que o número é composto,
    # então ele é considerado provavelmente primo.
    #
    # A probabilidade máxima de erro é:
    #
    # (1/4)^k
    #
    # onde k é a quantidade de rodadas.
    return True
