# Importa as bibliotecas que vamos usar: pygame para o jogo, random para gerar valores aleatórios
import pygame
import random
import sys

# Essa função serve para mostrar textos centralizados na tela, linha por linha
def mostrar_texto(tela, texto, fonte, cor, x, y, espacamento=5):
    linhas = texto.split('\n')  # Divide o texto em várias linhas, se tiver "\n"
    for i, linha in enumerate(linhas):
        img_texto = fonte.render(linha, True, cor) 
        pos_x = x - img_texto.get_width() // 2  # Centraliza o texto na horizontal
        pos_y = y + i * (img_texto.get_height() + espacamento)  # Posiciona uma linha abaixo da outra
        tela.blit(img_texto, (pos_x, pos_y))  # desenha o texto na tela

# Função principal do jogo, recebe a tela, largura, altura e uma função para voltar à tela inicial
def jogo(tela, largura, altura, tela_inicial):
    relogio = pygame.time.Clock()  # Cria um "relógio" para controlar o FPS
    FPS = 60  # Define o número de frames por segundo

    # cores
    AZUL = (135, 206, 235)  # Cor do fundo (céu)
    VERDE = (0, 200, 0)     # Cor dos canos

    # Define o tamanho do pássaro
    passaro_largura = 80
    passaro_altura = 60

    # Carrega a imagem do pássaro e redimensiona para o tamanho desejado
    passaro_img = pygame.image.load("imagens/passaro.png").convert_alpha()
    passaro_img = pygame.transform.scale(passaro_img, (passaro_largura, passaro_altura))

    # Define a posição inicial do pássaro
    passaro_x = 100
    passaro_y = altura // 2  # Começa no meio da tela

    # Variáveis da física do pássaro (gravidade e força do pulo)
    velocidade = 0
    gravidade = 0.5
    pulo = -10

    # Define a largura dos canos e a distância entre o topo e o cano de baixo
    largura_cano = 80
    distancia_canos = 200
    canos = []  # Lista que vai guardar os canos

    # Cria dois canos com altura aleatória
    for i in range(2):
        altura_cano = random.randint(150, 450)  # Altura do cano de cima
        x_cano = largura + i * 300  # Posição horizontal inicial dos canos
        canos.append({
            "topo": pygame.Rect(x_cano, 0, largura_cano, altura_cano),  # Cano de cima
            "base": pygame.Rect(x_cano, altura_cano + distancia_canos, largura_cano, altura),  # Cano de baixo
            "pontuado": False  # Marca se o jogador já ganhou ponto nesse cano
        })

    # Fontes usadas no jogo
    fonte = pygame.font.SysFont('Verdana', 36)
    fonte_pontuacao = pygame.font.SysFont('Verdana', 40)

    pontuacao = 0  # Começa com 0 pontos

    jogando = True  # Controle do loop do jogo
    while jogando:
        tela.fill(AZUL)  # Preenche o fundo com azul

        # Lê os eventos do teclado ou do sistema
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()  # Sai do pygame
                sys.exit()     # Encerra o programa
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                velocidade = pulo  # Quando aperta espaço, o pássaro "pula"

        # Aplica a gravidade e move o pássaro para baixo
        velocidade += gravidade
        passaro_y += velocidade

        # Cria o retângulo que representa o pássaro (usado para colisão)
        passaro_rect = pygame.Rect(passaro_x, int(passaro_y), passaro_largura, passaro_altura)

        for cano in canos:
            # Move os canos para a esquerda
            cano["topo"].x -= 5
            cano["base"].x -= 5

            # Quando o cano sair da tela, ele reaparece com nova altura
            if cano["topo"].right < 0:
                altura_cano = random.randint(150, 450)
                cano["topo"].x = largura
                cano["base"].x = largura
                cano["topo"].height = altura_cano
                cano["base"].y = altura_cano + distancia_canos
                cano["pontuado"] = False

            # Se o pássaro passou o cano e ainda não marcou ponto
            if not cano["pontuado"] and cano["topo"].right < passaro_x:
                pontuacao += 1  # Ganha um ponto
                cano["pontuado"] = True

            # Desenha os canos na tela
            pygame.draw.rect(tela, VERDE, cano["topo"])
            pygame.draw.rect(tela, VERDE, cano["base"])

            # Verifica colisão com os canos
            if passaro_rect.colliderect(cano["topo"]) or passaro_rect.colliderect(cano["base"]):
                jogando = False  # Se colidir, o jogo acaba

        # Desenha o pássaro na tela
        tela.blit(passaro_img, (passaro_x, int(passaro_y)))

        # Verifica se o pássaro saiu da tela (em cima ou embaixo)
        if passaro_y < 0 or passaro_y + passaro_altura > altura:
            jogando = False

        # Mostra a pontuação no canto superior esquerdo
        texto_pontuacao = fonte_pontuacao.render(f"Pontuação: {pontuacao}", True, (0, 0, 0))
        tela.blit(texto_pontuacao, (20, 20))

        # Atualiza a tela e controla o FPS
        pygame.display.update()
        relogio.tick(FPS)

    # -----------------------------------------
    # A partir daqui é a tela de GAME OVER
    # -----------------------------------------

    # Fontes para os textos da tela de fim de jogo
    fonte_titulo = pygame.font.SysFont('Verdana', 48, bold=True)
    fonte_texto = pygame.font.SysFont('Verdana', 28)

    # Texto de título e instruções
    mensagem_titulo = "VOCÊ PERDEU!"
    mensagem_texto = [
        f"Pontuação final: {pontuacao}",
        "Pressione R para reiniciar",
        "ou ESC para sair"
    ]

    # Fundo preto semi-transparente para deixar o texto mais visível
    fundo_mensagem = pygame.Surface((500, 200))
    fundo_mensagem.set_alpha(180)
    fundo_mensagem.fill((0, 0, 0))

    # Loop da tela de fim de jogo
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    jogo(tela, largura, altura, tela_inicial)  # Reinicia o jogo
                    return
                if evento.key == pygame.K_ESCAPE:
                    tela_inicial()  
                    return

        tela.fill(AZUL) 

        # Desenha os canos e o pássaro parado (congelado)
        for cano in canos:
            pygame.draw.rect(tela, VERDE, cano["topo"])
            pygame.draw.rect(tela, VERDE, cano["base"])
        tela.blit(passaro_img, (passaro_x, int(passaro_y)))

        # Mostra o fundo escuro atrás do texto
        tela.blit(fundo_mensagem, (largura // 2 - 250, altura // 3 - 40))

        # Mostra o título ("Você perdeu!") em vermelho
        mostrar_texto(tela, mensagem_titulo, fonte_titulo, (255, 0, 0), largura // 2, altura // 3 - 30)

        # Mostra as instruções em branco, uma linha por vez
        for i, linha in enumerate(mensagem_texto):
            mostrar_texto(tela, linha, fonte_texto, (255, 255, 255), largura // 2, altura // 3 + 40 + i * 35)

        # Atualiza a tela e reduz o FPS da tela final para economizar
        pygame.display.update()
        relogio.tick(30)
