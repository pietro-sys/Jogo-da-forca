import random
import os
import time
import threading

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    'Cachorro'
    ]

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
    ['É um ser vivo', 'É um animal doméstico muito comum', 'É considerado o melhor amigo do homem', 'Faz o som de latido', 'É um animal de quatro patas que abana o rabo', 'É um animal que pode ser encontrado em diversas raças e tamanhos, e é conhecido por sua lealdade e companheirismo']
]

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

# ─────────────────────────────────────────
# Configuração de níveis
# ─────────────────────────────────────────
NIVEIS = {
    '1': {'nome': 'Fácil',  'tempo': 90,  'bonus_vitoria': 60,  'penalidade_letra': 3,  'penalidade_palavra': 15},
    '2': {'nome': 'Médio',  'tempo': 60,  'bonus_vitoria': 100, 'penalidade_letra': 5,  'penalidade_palavra': 20},
    '3': {'nome': 'Difícil','tempo': 35,  'bonus_vitoria': 150, 'penalidade_letra': 8,  'penalidade_palavra': 30},
}

# ─────────────────────────────────────────
# Cronômetro em thread separada
# ─────────────────────────────────────────
tempo_esgotado = False
tempo_restante = 0

def iniciar_cronometro(segundos):
    """Decrementa tempo_restante a cada segundo numa thread paralela."""
    global tempo_esgotado, tempo_restante
    tempo_esgotado = False
    tempo_restante = segundos
    while tempo_restante > 0 and not tempo_esgotado:
        time.sleep(1)
        tempo_restante -= 1
    if tempo_restante <= 0:
        tempo_esgotado = True

def formatar_tempo(segundos):
    m, s = divmod(max(segundos, 0), 60)
    return f"{m:02d}:{s:02d}"

def barra_tempo(restante, total):
    """Barra visual proporcional ao tempo restante."""
    largura = 20
    preenchido = int((restante / total) * largura)
    barra = '█' * preenchido + '░' * (largura - preenchido)
    if restante > total * 0.5:
        cor = ''        # sem cor no terminal padrão
    return f"[{barra}] {formatar_tempo(restante)}"

# ─────────────────────────────────────────
# Entrada do jogador
# ─────────────────────────────────────────
player_name = input('Digite seu nome: ')

print('\n╔══════════════════════════════╗')
print('║       ESCOLHA O NÍVEL        ║')
print('╠══════════════════════════════╣')
for k, v in NIVEIS.items():
    print(f'║  ({k}) {v["nome"]:<8} — ⏱  {v["tempo"]}s          ║')
print('╚══════════════════════════════╝')
nivel_escolhido = input('Nível: ')
while nivel_escolhido not in NIVEIS:
    nivel_escolhido = input('Opção inválida. Escolha 1, 2 ou 3: ')

cfg = NIVEIS[nivel_escolhido]
TEMPO_LIMITE = cfg['tempo']

modo = input('\nEscolha o modo: (1) Normal  (2) Infinito: ')
while modo not in ['1', '2']:
    modo = input('Opção inválida. Escolha 1 ou 2: ')

jogar_novamente = 's'
pontuacao = 0
sequencia = 0

print(f'\nOlá, {player_name}! Bem-vindo ao Jogo da Forca!')
print(f'Nível: {cfg["nome"]} | Tempo por palavra: {TEMPO_LIMITE}s')
input('Pressione Enter para começar...')
limpar_tela()

# ─────────────────────────────────────────
# Loop principal
# ─────────────────────────────────────────
while jogar_novamente == 's':
    global tempo_esgotado
    tempo_esgotado = False

    indice = random.randint(0, len(palavra) - 1)
    palavra_sorteada   = palavra[indice]
    dicas_sorteada     = dicas[indice]

    letras_display = []
    for letra in palavra_sorteada:
        letras_display.append(' ' if letra == ' ' else '_')

    vidas                = 6
    palavra_sorteada_lower = palavra_sorteada.lower()
    contador_dicas       = -1
    letras_tentadas      = []

    # Inicia cronômetro em thread separada
    t = threading.Thread(target=iniciar_cronometro, args=(TEMPO_LIMITE,), daemon=True)
    t.start()

    rodada_encerrada = False

    while not rodada_encerrada:
        limpar_tela()

        # Cabeçalho com nível e cronômetro
        print(f'╔══ FORCA ══╗  Jogador: {player_name}  |  Nível: {cfg["nome"]}  |  Pontos: {pontuacao}')
        print(f'⏱  {barra_tempo(tempo_restante, TEMPO_LIMITE)}')
        print()

        # Exibe palavra mascarada
        print(' '.join(letras_display))
        print(boneco[6 - vidas])

        if letras_tentadas:
            print('Letras erradas:', ', '.join(letras_tentadas))

        # Verifica se o tempo acabou ANTES de pedir input
        if tempo_esgotado:
            print(f'\n⏰ Tempo esgotado! A palavra era: {palavra_sorteada}')
            pontuacao -= cfg['penalidade_palavra']
            print(f'Pontuação atual: {pontuacao}')
            input('Pressione Enter para continuar...')
            rodada_encerrada = True
            break

        palpite = input('\nDigite uma letra ou a palavra completa: ')
        palpite = palpite.lower()

        # Verifica novamente após o input (o timer pode ter zerado enquanto digitava)
        if tempo_esgotado:
            print(f'\n⏰ Tempo esgotado! A palavra era: {palavra_sorteada}')
            pontuacao -= cfg['penalidade_palavra']
            print(f'Pontuação atual: {pontuacao}')
            input('Pressione Enter para continuar...')
            rodada_encerrada = True
            break

        # ── Palpite de letra única ──
        if len(palpite) == 1:
            if palpite in palavra_sorteada_lower:
                for i, ch in enumerate(palavra_sorteada_lower):
                    if ch == palpite:
                        letras_display[i] = palavra_sorteada[i]
                pontuacao += 10
                print(f'✔ Letra correta! +10 pontos  |  Total: {pontuacao}')
            else:
                vidas -= 1
                contador_dicas += 1
                pontuacao -= cfg['penalidade_letra']
                letras_tentadas.append(palpite)
                print(f'✘ Letra errada! -{cfg["penalidade_letra"]} pontos  |  Total: {pontuacao}')
                if contador_dicas < len(dicas_sorteada):
                    print(f'💡 Dica: {dicas_sorteada[contador_dicas]}')

        # ── Palpite da palavra completa ──
        elif len(palpite) == len(palavra_sorteada_lower):
            if palpite == palavra_sorteada_lower:
                tempo_esgotado = True          # para o cronômetro
                bonus = cfg['bonus_vitoria'] + tempo_restante  # bônus extra pelo tempo restante
                pontuacao += bonus
                print(f'\n🎉 Palavra correta! +{bonus} pontos (inclui bônus de tempo)  |  Total: {pontuacao}')
                input('Pressione Enter para continuar...')
                rodada_encerrada = True
                sequencia += 1
                break
            else:
                vidas -= 5
                pontuacao -= cfg['penalidade_palavra']
                print(f'✘ Palavra errada! -{cfg["penalidade_palavra"]} pontos  |  Total: {pontuacao}')

        # ── Verificações de fim de rodada ──
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

        if vidas <= 0:
            tempo_esgotado = True
            print(f'\n💀 Game Over! A palavra era: {palavra_sorteada}')
            print(boneco[6])
            print(f'Pontuação atual: {pontuacao}')
            input('Pressione Enter para continuar...')
            rodada_encerrada = True
            break

        input('Pressione Enter para continuar...')

    # Aguarda a thread encerrar
    t.join(timeout=2)

    print(f'\nPontuação atual: {pontuacao}')

    # ── Controle modo infinito vs normal ──
    if modo == '2':
        if vidas <= 0 or (tempo_esgotado and '_' in letras_display):
            jogar_novamente = 'n'
            print(f'Sequência encerrada em {sequencia} vitória(s) consecutivas!')
        else:
            jogar_novamente = 's'
            print(f'🔥 Sequência de vitórias: {sequencia}')
    else:
        jogar_novamente = input('Deseja jogar novamente? (s/n): ').lower()
        while jogar_novamente not in ['s', 'n']:
            jogar_novamente = input('Opção inválida. Deseja jogar novamente? (s/n): ').lower()

limpar_tela()
print(f'Obrigado por jogar, {player_name}!')
print(f'Nível jogado: {cfg["nome"]}')
print(f'Pontuação final: {pontuacao}')
if modo == '2':
    print(f'Maior sequência de vitórias: {sequencia}')
