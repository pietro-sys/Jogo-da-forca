import random
import os

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

player_name = input('Digite seu nome: ')
jogar_novamente = 's'
pontuacao = 0
print(f'Olá, {player_name}! Bem-vindo ao jogo de adivinhação de palavras!')
print('Vamos começar o jogo!')
limpar_tela()

while jogar_novamente == 's':
    indice = random.randint(0, 9)
    palavra_sorteada = palavra[indice]
    dicas_sorteada = dicas[indice]

    letras_display = []

    for letra in palavra_sorteada:
        if letra == ' ':
            letras_display.append(' ')
        else:
            letras_display.append('_')

    print(f'A palavra a ser adivinhada tem {len(palavra_sorteada)} letras. Boa sorte, {player_name}!')
    limpar_tela()

    vidas = 6
    palavra_sorteada_lower = palavra_sorteada.lower()
    contador_dicas = -1

    letras_tentadas = []
    while True:

        for letra in letras_display:
            print(letra, end=' ')

        print(boneco[6 - vidas])
        if letras_tentadas:
            print('Letras erradas:', letras_tentadas)
        palpite = input('\nDigite uma letra ou a palavra completa: ')
        palpite = palpite.lower()

        if len(palpite) == 1:
            if palpite in palavra_sorteada_lower:
                for i in range(len(palavra_sorteada_lower)):
                    if palavra_sorteada_lower[i] == palpite.lower():
                        letras_display[i] = palavra_sorteada[i]     
                print(f'Parabéns, {player_name}! Você acertou uma letra!')
                pontuacao += 10
                print('Pontuação atual:', pontuacao)
                input('Pressione Enter para continuar...')
                limpar_tela()
            else:
                vidas -= 1
                contador_dicas += 1
                print(f'Ops, {player_name}! A letra não está na palavra.')
                pontuacao -= 5
                print('Dica:', dicas_sorteada[contador_dicas])
                letras_tentadas.append(palpite)      
                print('Pontuação atual:', pontuacao)
                input('Pressione Enter para continuar...')
                limpar_tela()    

        elif len(palpite) == len(palavra_sorteada_lower):
            if palpite == palavra_sorteada_lower:
                print(f'Parabéns, {player_name}! Você acertou a palavra completa!')
                pontuacao += 50
                print('Pontuação atual:', pontuacao)
                input('Pressione Enter para continuar...')
                limpar_tela()
                break
            else:
                vidas -= 5
                print(f'Ops, {player_name}! A palavra digitada está incorreta.')
                pontuacao -= 20
                print('Pontuação atual:', pontuacao)
                input('Pressione Enter para continuar...')
                limpar_tela()
        
        if '_' not in letras_display:
            print(f'Parabéns, {player_name}! Você adivinhou a palavra:', palavra_sorteada)
            print('Pontuação atual:', pontuacao)
            input('Pressione Enter para continuar...')
            limpar_tela()
            break
        
        if vidas <= 0:
            print('Game Over! Você perdeu todas as suas vidas.')
            print(boneco[6])
            print('A palavra correta era:', palavra_sorteada)
            print('Pontuação atual:', pontuacao)
            input('Pressione Enter para continuar...')
            limpar_tela()
            break
    print(f'Sua pontuação atual é: {pontuacao}')
    jogar_novamente = input('Deseja jogar novamente? (s/n): ')
    while jogar_novamente not in ['s', 'n']:
        jogar_novamente = input('Opção inválida. Deseja jogar novamente? (s/n): ')
print(f'Obrigado por jogar, {player_name}! Sua pontuação final é: {pontuacao}. Até a próxima!')
limpar_tela()

