import random
 
 
def gerar_numero(bits):
    # Gera um número aleatório ímpar com exatamente a quantidade de bits pedida.
    # O OR com 1 garante que seja ímpar (número par > 2 já é composto) e o OR
    # com o bit mais alto garante que o número realmente tenha esse tamanho —
    # sem isso, getrandbits podia devolver algo menor.
    numero = random.getrandbits(bits)
    numero |= 1
    numero |= (1 << (bits - 1))
    return numero