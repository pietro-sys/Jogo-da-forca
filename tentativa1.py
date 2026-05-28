# Importa bibliotecas necessárias
import random      # Para sortear palavras aleatórias
import os          # Para limpar a tela do terminal
import time        # Para trabalhar com tempo/cronômetro
import threading   # Para criar uma thread separada para o cronômetro
import os.path 
import sys

# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

if not os.path.exists("Palavras.txt"):
    print("Arquivo Palavras.txt não encontrado!")
    exit()

palavra = []
dicas = []

arquivo = open("Palavras.txt", "r", encoding="utf-8")

for linha in arquivo.readlines():

    parte = linha.strip().split("#")

    palavra.append(parte[0])        # palavra

    dicas.append(parte[1:])         # lista de dicas

arquivo.close()

# Desenhos da forca conforme o jogador erra
boneco = [
'''
  _____
 |     |
 |      
 |      
 |      
_|_
''',

'''
  _____
 |     |
 |     O
 |      
 |      
_|_
''',

'''
  _____
 |     |
 |     O
 |     |
 |      
_|_
''',

'''
  _____
 |     |
 |     O
 |    /|
 |      
_|_
''',

'''
  _____
 |     |
 |     O
 |    /|\\
 |      
_|_
''',

'''
  _____
 |     |
 |     O
 |    /|\\
 |    / 
_|_
''',

'''
  _____
 |     |
 |     O
 |    /|\\
 |    / \\
_|_
'''
]

# =========================================================
# CONFIGURAÇÃO DOS NÍVEIS
# =========================================================

# Dicionário contendo as configurações de cada nível
NIVEIS = {

    # Nível fácil
    '1': {
        'nome': 'Fácil',
        'tempo': 90,               # Tempo total da rodada
        'bonus_vitoria': 60,       # Pontos ao vencer
        'penalidade_letra': 3,     # Pontos perdidos por letra errada
        'penalidade_palavra': 15   # Pontos perdidos por palavra errada
    },

    # Nível médio
    '2': {
        'nome': 'Médio',
        'tempo': 60,
        'bonus_vitoria': 100,
        'penalidade_letra': 5,
        'penalidade_palavra': 20
    },

    # Nível difícil
    '3': {
        'nome': 'Difícil',
        'tempo': 35,
        'bonus_vitoria': 150,
        'penalidade_letra': 8,
        'penalidade_palavra': 30
    },
}

# =========================================================
# VARIÁVEIS DO CRONÔMETRO
# =========================================================

tempo_esgotado = False   # Indica se o tempo acabou
tempo_restante = 0       # Tempo restante da rodada


# Função do cronômetro
def iniciar_cronometro(segundos):

    """
    Decrementa o tempo restante a cada segundo.
    Roda em uma thread separada.
    """

    global tempo_esgotado, tempo_restante

    tempo_esgotado = False
    tempo_restante = segundos

    # Enquanto ainda houver tempo
    while tempo_restante > 0 and not tempo_esgotado:
        time.sleep(1)
        tempo_restante -= 1

    # Quando o tempo acabar
    if tempo_restante <= 0:
        tempo_esgotado = True


# Função para formatar o tempo em MM:SS
def formatar_tempo(segundos):
    m, s = divmod(max(segundos, 0), 60)
    return f"{m:02d}:{s:02d}"


# Função para exibir barra visual do tempo
def barra_tempo(restante, total):

    largura = 20

    # Calcula quanto da barra deve estar preenchida
    preenchido = int((restante / total) * largura)

    # Cria a barra visual
    barra = '█' * preenchido + '░' * (largura - preenchido)

    return f"[{barra}] {formatar_tempo(restante)}"


# =========================================================
# ENTRADA DO JOGADOR
# =========================================================

# Solicita nome do jogador
player_name = input('Digite seu nome: ')

# Menu de escolha de nível
print('\n╔══════════════════════════════╗')
print('║       ESCOLHA O NÍVEL        ║')
print('╠══════════════════════════════╣')

# Exibe os níveis disponíveis
for k, v in NIVEIS.items():
    print(f'║  ({k}) {v["nome"]:<8} — ⏱  {v["tempo"]}s       ║')

print('╚══════════════════════════════╝')

# Lê o nível escolhido
nivel_escolhido = input('Nível: ')

# Validação da escolha
while nivel_escolhido not in NIVEIS:
    nivel_escolhido = input('Opção inválida. Escolha 1, 2 ou 3: ')

# Carrega configurações do nível
cfg = NIVEIS[nivel_escolhido]

# Tempo máximo da rodada
TEMPO_LIMITE = cfg['tempo']


# Escolha do modo de jogo
modo = input('\nEscolha o modo: (1) Normal  (2) Infinito: ')

# Validação do modo
while modo not in ['1', '2']:
    modo = input('Opção inválida. Escolha 1 ou 2: ')

# Variáveis gerais do jogo
jogar_novamente = 's'
pontuacao = 0
sequencia = 0
palavras_usadas = []

# Mensagem inicial
print(f'\nOlá, {player_name}! Bem-vindo ao Jogo da Forca!')
print(f'Nível: {cfg["nome"]} | Tempo por palavra: {TEMPO_LIMITE}s')

input('Pressione Enter para começar...')

limpar_tela()

# =========================================================
# LOOP PRINCIPAL DO JOGO
# =========================================================

while jogar_novamente == 's':

    tempo_esgotado = False

    # =====================================================
    # SORTEIO SEM REPETIÇÃO
    # =====================================================

    # Verifica se todas as palavras já foram usadas
    if len(palavras_usadas) == len(palavra):

        limpar_tela()

        print('🎉 PARABÉNS!')
        print('Você completou todas as palavras do jogo!')

        print(f'\nPontuação final: {pontuacao}')

        import sys
        sys.exit()

    # Sorteia até encontrar uma palavra ainda não usada
    while True:

        indice = random.randint(0, len(palavra) - 1)

        if indice not in palavras_usadas:

            palavras_usadas.append(indice)

            break

    # Define palavra e dicas
    palavra_sorteada = palavra[indice]
    dicas_sorteada = dicas[indice]

        # Cria os "_" da palavra
    letras_display = []

    for letra in palavra_sorteada:
        letras_display.append(' ' if letra == ' ' else '_')

    # Configurações iniciais da rodada
    vidas = 6
    palavra_sorteada_lower = palavra_sorteada.lower()
    contador_dicas = 0
    letras_tentadas = []

    # Inicia thread do cronômetro
    t = threading.Thread(
        target=iniciar_cronometro,
        args=(TEMPO_LIMITE,),
        daemon=True
    )

    t.start()

    rodada_encerrada = False

    # =====================================================
    # LOOP DA RODADA
    # =====================================================

    while not rodada_encerrada:

        limpar_tela()

        # Cabeçalho do jogo
        print(f'╔══ FORCA ══╗  Jogador: {player_name}  |  Nível: {cfg["nome"]}  |  Pontos: {pontuacao}')

        # Exibe barra do tempo
        print(f'⏱  {barra_tempo(tempo_restante, TEMPO_LIMITE)}')

        print()

        # Mostra palavra escondida
        print(' '.join(letras_display))

        # Mostra desenho da forca
        print(boneco[6 - vidas])

        # Mostra letras erradas
        if letras_tentadas:
            print('Letras erradas:', ', '.join(letras_tentadas))

        # Verifica se o tempo acabou antes do input
        if tempo_esgotado:

            print(f'\n⏰ Tempo esgotado! A palavra era: {palavra_sorteada}')

            pontuacao -= cfg['penalidade_palavra']

            print(f'Pontuação atual: {pontuacao}')

            input('Pressione Enter para continuar...')

            rodada_encerrada = True

            break

        # Entrada do jogador
        palpite = input('\nDigite uma letra ou a palavra completa: ')
        palpite = palpite.lower()

        # Verifica novamente o tempo
        if tempo_esgotado:

            print(f'\n⏰ Tempo esgotado! A palavra era: {palavra_sorteada}')

            pontuacao -= cfg['penalidade_palavra']

            print(f'Pontuação atual: {pontuacao}')

            input('Pressione Enter para continuar...')

            rodada_encerrada = True

            break

        # =================================================
        # PALPITE DE UMA LETRA
        # =================================================

        if len(palpite) == 1:

            # Se a letra existir na palavra
            if palpite in palavra_sorteada_lower:

                # Revela todas ocorrências da letra
                for i, ch in enumerate(palavra_sorteada_lower):

                    if ch == palpite:
                        letras_display[i] = palavra_sorteada[i]

                pontuacao += 10

                print(f'✔ Letra correta! +10 pontos  |  Total: {pontuacao}')

            else:

                # Penaliza erro
                vidas -= 1

                pontuacao -= cfg['penalidade_letra']

                letras_tentadas.append(palpite)

                print(f'✘ Letra errada! -{cfg["penalidade_letra"]} pontos  |  Total: {pontuacao}')

                # Exibe dica
                if contador_dicas < len(dicas_sorteada):
                    print(f'💡 Dica: {dicas_sorteada[contador_dicas]}')
                    contador_dicas += 1


        # =================================================
        # PALPITE DA PALAVRA COMPLETA
        # =================================================

        elif len(palpite) == len(palavra_sorteada_lower):

            # Acertou a palavra
            if palpite == palavra_sorteada_lower:

                tempo_esgotado = True

                # Calcula bônus
                bonus = cfg['bonus_vitoria'] + tempo_restante

                pontuacao += bonus

                print(f'\n🎉 Palavra correta! +{bonus} pontos (inclui bônus de tempo)  |  Total: {pontuacao}')

                input('Pressione Enter para continuar...')

                rodada_encerrada = True

                sequencia += 1

                break

            else:

                # Errou a palavra
                vidas -= 5

                pontuacao -= cfg['penalidade_palavra']

                print(f'✘ Palavra errada! -{cfg["penalidade_palavra"]} pontos  |  Total: {pontuacao}')

        # =================================================
        # VERIFICAÇÕES DE FIM DE RODADA
        # =================================================

        # Jogador venceu
        if '_' not in letras_display:

            tempo_esgotado = True

            bonus = cfg['bonus_vitoria'] + tempo_restante

            pontuacao += bonus

            print(f'\n🎉 Parabéns! Você adivinhou: {palavra_sorteada}')

            print(f'+{bonus} pontos (inclui bônus de tempo)  |  Total: {pontuacao}')

            input('Pressione Enter para continuar...')

            rodada_encerrada = True

            sequencia += 1

            break
            
        # Jogador perdeu
        if vidas <= 0:

            tempo_esgotado = True

            print(f'\n💀 Game Over! A palavra era: {palavra_sorteada}')

            print(boneco[6])

            print(f'Pontuação atual: {pontuacao}')

            input('Pressione Enter para continuar...')

            rodada_encerrada = True

            break

        input('Pressione Enter para continuar...')

    # Aguarda thread finalizar
    t.join(timeout=2)

    print(f'\nPontuação atual: {pontuacao}')

    # =====================================================
    # CONTROLE DE MODOS
    # =====================================================

    # Modo infinito
    if modo == '2':

        # Encerra sequência se perder
        if vidas <= 0 or (tempo_esgotado and '_' in letras_display):

            jogar_novamente = 'n'

            print(f'Sequência encerrada em {sequencia} vitória(s) consecutivas!')

        else:

            jogar_novamente = 's'

            print(f'🔥 Sequência de vitórias: {sequencia}')

    # Modo normal
    else:
        jogar_novamente = input('Deseja jogar novamente? (s/n): ').lower()

        while jogar_novamente not in ['s', 'n']:

            jogar_novamente = input('Opção inválida. Deseja jogar novamente? (s/n): ').lower()


# =========================================================
# FIM DO JOGO
# =========================================================

limpar_tela()

print(f'Obrigado por jogar, {player_name}!')

print(f'Nível jogado: {cfg["nome"]}')

print(f'Pontuação final: {pontuacao}')

# Exibe sequência no modo infinito
if modo == '2':
    print(f'Maior sequência de vitórias: {sequencia}')
