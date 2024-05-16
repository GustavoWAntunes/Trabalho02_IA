import random

# criar as peças do jogo
def criarPecas():
    return [(i, j) for i in range(7) for j in range(i, 7)]

# distribuir as peças para os jogadores
def distribuirPecas(pecas):
    random.shuffle(pecas)
    return pecas[:7], pecas[7:14], pecas[14:]

# ver qual jogador inicia a partida e quem tem a maior peça
def getPecaInicial(jogador1, jogador2):
    # Verificar se algum jogador possui uma peça dupla
    jogador1PecaDupla = [peca for peca in jogador1 if peca[0] == peca[1]]
    jogador2PecaDupla = [peca for peca in jogador2 if peca[0] == peca[1]]

    if jogador1PecaDupla and not jogador2PecaDupla:
        maiorPecaJogador1 = max(jogador1PecaDupla)
        return 1, maiorPecaJogador1, jogador1
    elif not jogador1PecaDupla and jogador2PecaDupla:
        maiorPecaJogador2 = max(jogador2PecaDupla)
        return 2, maiorPecaJogador2, jogador2
    elif jogador1PecaDupla and jogador2PecaDupla:
        maiorPecaJogador1 = max(jogador1PecaDupla)
        maiorPecaJogador2 = max(jogador2PecaDupla)
        if maiorPecaJogador1 > maiorPecaJogador2:
            return 1, maiorPecaJogador1, jogador1
        else:
            return 2, maiorPecaJogador2, jogador2
    else:
        # valida a maior peça
        maiorPecaJogador1 = max(jogador1, key=lambda x: sum(x))
        maiorPecaJogador2 = max(jogador2, key=lambda x: sum(x))
        if sum(maiorPecaJogador1) >= sum(maiorPecaJogador2):
            return 1, maiorPecaJogador1, jogador1
        else:
            return 2, maiorPecaJogador2, jogador2

# imprimir a mesa atual do jogo
def imprimirMesa(mesa):
    print("Mesa:", end=" ")
    for peca in mesa:
        print(f"[{peca[0]}/{peca[1]}]", end=" ")
    print("\n")

# verifucar qual peça do jogador pode ser jogada
def verificarPecaDisponivel(jogador, mesa):
    extremidades = {mesa[0][0], mesa[-1][1]}
    return [peca for peca in jogador if any(num in extremidades for num in peca)]

# jogar uma peça na mesa
def jogarPeca(jogador, peca, mesa):
    jogador.remove(peca)
    if mesa[0][0] == peca[1]:
        mesa.insert(0, peca)
    elif mesa[0][0] == peca[0]:
        peca = (peca[1], peca[0])
        mesa.insert(0, peca)
    elif mesa[-1][1] == peca[0]:
        mesa.append(peca)
    elif mesa[-1][1] == peca[1]:
        peca = (peca[1], peca[0])
        mesa.append(peca)

# comprar uma peça da pilha
def comprarPeca(jogador, pilha_compra):
    if not jogador:
        return None
    if not pilha_compra:
        return None
    peca_comprada = random.choice(pilha_compra)
    jogador.append(peca_comprada)
    pilha_compra.remove(peca_comprada)
    return peca_comprada

# contar quantas peças um jogador tem
def contarPecas(jogador):
    return len(jogador)

# imprimir o menu com as mãos dos jogadores e a pilha de compra
def imprimirMenu(jogador1, jogador2, pilha_compra, mesa=None):
    print("=" * 100)
    print("-" * 100)
    print("Mão do Jogador 1:", end=" ")
    for peca in jogador1:
        print(f"[{peca[0]}/{peca[1]}]", end=" ")
    print("\n")

    print("Mão do Jogador 2:", end=" ")
    for peca in jogador2:
        print(f"[{peca[0]}/{peca[1]}]", end=" ")
    print("\n")

    print("Pilha de Compra:", end=" ")
    for peca in pilha_compra:
        print(f"[{peca[0]}/{peca[1]}]", end=" ")
    print("\n")
    if mesa:
        imprimirMesa(mesa)

def main():
    # criar as peças e distribuir pros 2 jogadores
    pecas = criarPecas()
    jogador1, jogador2, pilha_compra = distribuirPecas(pecas)
    imprimirMenu(jogador1, jogador2, pilha_compra)

    # qual jogador inicia
    jogador_inicial, maior_peca, mao_jogador_inicial = getPecaInicial(jogador1, jogador2)
    mesa = [maior_peca]
    mao_jogador_inicial.remove(maior_peca)

    print(f"\nO jogador {jogador_inicial} inicia a partida.")
    imprimirMesa(mesa)

    # inicia o loop do jogo até um alguém ganhar ou empatar
    jogador_atual = 2 if jogador_inicial == 1 else 1
    while True:
        jogador = jogador1 if jogador_atual == 1 else jogador2
        print(f"Jogador {jogador_atual}:")
        disponiveis = verificarPecaDisponivel(jogador, mesa)
        if disponiveis:
            peca_jogada = random.choice(disponiveis)
            print(f"Jogador {jogador_atual} joga a peça: {peca_jogada}")
            jogarPeca(jogador, peca_jogada, mesa)
            imprimirMenu(jogador1, jogador2, pilha_compra, mesa)
            if not jogador:
                print(f"Jogador {jogador_atual} venceu!")
                break
        else:
            print(f"Jogador {jogador_atual} não tem peças disponíveis para jogar, comprando uma nova peça...")
            while True:
                peca_comprada = comprarPeca(jogador, pilha_compra)
                if peca_comprada:
                    print(f"Jogador {jogador_atual} comprou a peça: {peca_comprada}")
                    disponiveis = verificarPecaDisponivel(jogador, mesa)
                    if disponiveis:
                        peca_jogada = random.choice(disponiveis)
                        print(f"Jogador {jogador_atual} joga a peça: {peca_jogada}")
                        jogarPeca(jogador, peca_jogada, mesa)
                        imprimirMenu(jogador1, jogador2, pilha_compra, mesa)
                        break
                else:
                    print("Pilha de compra vazia.")
                    disponiveis1 = verificarPecaDisponivel(jogador1, mesa)
                    disponiveis2 = verificarPecaDisponivel(jogador2, mesa)
                    if not disponiveis1 and not disponiveis2:
                        print("Ambos os jogadores não possuem peças disponíveis para jogar. Contando peças dos jogadores....")
                        pecas_jogador1 = contarPecas(jogador1)
                        pecas_jogador2 = contarPecas(jogador2)
                        imprimirMenu(jogador1, jogador2, pilha_compra, mesa)
                        if pecas_jogador1 != pecas_jogador2:
                            print(f"Jogador {1 if pecas_jogador1 < pecas_jogador2 else 2} venceu!")
                        else:
                            print("Empate!")
                        return
                    else:
                        break

        jogador_atual = 2 if jogador_atual == 1 else 1

if __name__ == "__main__":
    main()