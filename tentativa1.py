# Importa bibliotecas necessárias
import random      # Para sortear palavras aleatórias
import os          # Para limpar a tela do terminal
import time        # Para trabalhar com tempo/cronômetro
import threading   # Para criar uma thread separada para o cronômetro


# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Lista de palavras possíveis do jogo
palavra = [
    'Valorant', 
    'Six Seven',
    'Fallen',
    'Bob Esponja',
    'Snorlax',
    'Freddie Mercury',
    'Goku',
    'Fatec',
    'Python',
    'Cachorro',
    'Vaso',
    'Quasar',
    'Pederneira',
    'Carambola',
    'Preguiça'
    ]

# Lista de dicas relacionadas às palavras
# Cada índice corresponde à palavra da mesma posição
dicas = [
    ['É um tipo de mídia de entretenimento digital', 'Envolve competição entre jogadores', 'É um jogo eletrônico do estilo tático de tiro', 'Foi desenvolvido pela Riot Games', 'Possui agentes com habilidades especiais', 'O melhor jogador do mundo é brasileiro e se chama Aspas'],

    ['É um termo usado em esportes', 'Tem relação com números', 'É uma altura medida em pés e polegadas', 'Equivale a aproximadamente 2 metros', 'É uma altura comum em jogadores de basquete', 'É a altura do jogador brasileiro de basquete Anderson Varejão'],

    ['É uma palavra em inglês', 'Tem relação com o mundo dos games competitivos', 'É um jogador profissional brasileiro', 'É conhecido como o professor', 'É um lendário jogador de CS:GO', 'É o melhor jogador de CS:GO de todos os tempos'],

    ['É um personagem fictício', 'Vive debaixo do mar', 'Trabalha como cozinheiro', 'Mora em uma abacaxi', 'Possui uma risada marcante', 'É uma esponja amarela e quadrada'],

    ['É um personagem fictício japonês', 'Aparece em uma famosa franquia de jogos e anime', 'É conhecido por dormir muito', 'É um Pokemon do tipo Normal', 'É um Pokemon enorme e gordo de cor azul', 'É o melhor pokemon para dormir'],

    ['Foi uma pessoa famosa no século XX', 'Era britânico nascido em Zanzibar', 'Era conhecido por suas apresentações ao vivo energéticas', 'Foi vocalista de uma banda de rock famosa', 'Foi o vocalista do Queen', 'É considerado um dos maiores cantores de todos os tempos'],

    ['É um personagem fictício japonês', 'Aparece em um anime famoso dos anos 80', 'Tem o cabelo espetado e muda de cor quando fica forte', 'Usa uma roupa laranja e azul', 'Seu nome completo é Kakarot', 'É um dos personagens mais icônicos da cultura pop mundial'],

    ['É uma instituição brasileira', 'Oferece cursos de nível superior', 'É uma faculdade pública gratuita', 'Está presente em diversas cidades de São Paulo', 'É uma faculdade de tecnologia do estado de São Paulo', 'É conhecida por seus cursos de tecnologia'],

    ['É um termo que pode ter vários significados', 'Na natureza, é um tipo de animal', 'Na tecnologia, é algo muito utilizado por profissionais', 'É uma das linguagens de programação mais populares do mundo', 'É a linguagem de programação que você está usando agora', 'É uma linguagem de programação conhecida por sua simplicidade e versatilidade'],

    ['É um ser vivo', 'É um animal doméstico muito comum', 'É considerado o melhor amigo do homem', 'Faz o som de latido', 'É um animal de quatro patas que abana o rabo', 'É um animal que pode ser encontrado em diversas raças e tamanhos, e é conhecido por sua lealdade e companheirismo'],
    
    ['É um objeto muito comum em casas', 'Pode ser feito de vidro, cerâmica ou plástico', 'É usado principalmente para decoração', 'Muitas vezes contém flores ou plantas', 'Pode ficar sobre mesas ou estantes', 'Serve para colocar flores, plantas ou enfeites'],

    ['Tem relação com o universo', 'É um objeto estudado pela astronomia', 'Fica extremamente distante da Terra', 'Libera uma enorme quantidade de energia', 'Está ligado à presença de buracos negros supermassivos', 'É um dos objetos mais brilhantes do universo'],

    ['É um objeto encontrado na natureza', 'Tem relação com fogo', 'Foi muito usada na antiguidade', 'Pode produzir faíscas quando atritada', 'Era utilizada para acender fogueiras e armas antigas', 'É uma pedra usada para gerar faíscas'],

    ['É um alimento natural', 'Pode ser encontrada em árvores', 'Tem sabor agridoce', 'Quando cortada possui formato de estrela', 'É uma fruta tropical bastante conhecida', 'É uma fruta amarela chamada fruta-estrela'],

    ['É um animal', 'Vive em árvores', 'É conhecido por seus movimentos lentos', 'Possui garras longas para se pendurar', 'Passa grande parte do tempo dormindo', 'É um mamífero famoso pela lentidão']
]

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
    print(f'║  ({k}) {v["nome"]:<8} — ⏱  {v["tempo"]}s          ║')

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

    # Sorteia uma palavra aleatória
    indice = random.randint(0, len(palavra) - 1)

    palavra_sorteada = palavra[indice]
    dicas_sorteada = dicas[indice]

    # Cria os "_" da palavra
    letras_display = []

    for letra in palavra_sorteada:
        letras_display.append(' ' if letra == ' ' else '_')

    # Configurações iniciais da rodada
    vidas = 6
    palavra_sorteada_lower = palavra_sorteada.lower()
    contador_dicas = -1
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
                contador_dicas += 1

                pontuacao -= cfg['penalidade_letra']

                letras_tentadas.append(palpite)

                print(f'✘ Letra errada! -{cfg["penalidade_letra"]} pontos  |  Total: {pontuacao}')

                # Exibe dica
                if contador_dicas < len(dicas_sorteada):
                    print(f'💡 Dica: {dicas_sorteada[contador_dicas]}')

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
