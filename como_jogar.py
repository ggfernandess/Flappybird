import pygame
import sys

pygame.init()  

# CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)  

def como_jogar(tela, largura_tela, altura_tela):
    clock = pygame.time.Clock()  # controla o FPS 
    fonte_texto = pygame.font.Font('fonte/pressstart.ttf', 25)  #fonte do texto da tela

    fundo = pygame.image.load("imagens/comojogar.webp").convert_alpha()  # carrega a imagem de fundo
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))  # redimensiona para caber na tela
    fundo.set_alpha(40)  # deixa o fundo mais transparente 0 é total e 255 opaco

    texto = [
        "Como Jogar:",                    
        "- Use espaço para pular",       
        "- Evite os obstáculos",
        "- Pontue o máximo possível",
        "",
        "Pressione ESC para voltar"     
    ]

    run = True 
    while run:
        tela.blit(fundo, (0, 0))  # desenha a imagem de fundo

        y = 250  # posição vertical inicial do texto
        espaco = 40  # espaço entre cada linha de texto

        for linha in texto:  # percorre cada linha da lista de textos
            render = fonte_texto.render(linha, True, PRETO)  
            tela.blit(render, (50, y))  # desenha o texto na tela
            y += espaco  # atualiza a posição vertical para a próxima linha

        for evento in pygame.event.get():  
            if evento.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:  # verifica se uma tecla foi pressionada
                if evento.key == pygame.K_ESCAPE:  # se a tecla ESC for pressionada, sai da tela
                    run = False

        pygame.display.update() 
        clock.tick(60)  # limita a 60 atualizações por segundo
