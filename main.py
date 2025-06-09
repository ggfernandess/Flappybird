import pygame
import sys
from como_jogar import como_jogar
from jogo import *

pygame.init()

largura_tela = 800
altura_tela = 800

tela = pygame.display.set_mode((largura_tela, altura_tela))


titulo = pygame.image.load("imagens/titulo.png").convert_alpha()
titulo = pygame.transform.scale(titulo, (400, 100))  

fundo = pygame.image.load("imagens/inicial.png") #carrega a imagem de fundo
fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela)) #essa linha redimensiona a escala da imagem para que caiba na tela

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)  #cores
AZUL = (0, 120, 215)

fonte_titulo = pygame.font.Font('fonte/pressstart.ttf', 54)  #fonte que peguei externamente, sendo assim usa somente o "FONT"
fonte_botao = pygame.font.SysFont('Vergana', 36) #fonte normal, usando o SysFont

def desenhar_botao(texto, x, y, largura, altura):
    retangulo = pygame.Rect(x, y, largura, altura)
    mouse = pygame.mouse.get_pos()  #pega a posição do mouse
    clique = pygame.mouse.get_pressed() #pega se alguma tecla for pressionada

    mouse_em_cima = retangulo.collidepoint(mouse) #esse aqui serve pra ver se o mouse passou no botão, ou seja, colidiu.

    cor = AZUL if mouse_em_cima else BRANCO #A COR ORIGINAL DO BOTAO É BRANCA, MAS QUANDO PASSA O MOUSE FICA AZUL

    pygame.draw.rect(tela, cor, retangulo) #desenha um retangulo

    texto_render = fonte_botao.render(texto, True, PRETO) # cria a imagem do texto para exibir na tela

    texto_rect = texto_render.get_rect(center=retangulo.center) # centraliza o texto dentro do retângulo do botão
    tela.blit(texto_render, texto_rect) #exibe o texto
    return mouse_em_cima and clique[0] #aqui ta falando que se o mouse estiver no botão e o clique do botão esquerdo for pressionado, vai entrar na tela escolhida

def tela_inicial():
    while True:
        tela.blit(fundo, (0, 0))

        
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 80)) #centraliza o título no topo da tela

        if desenhar_botao("Jogar", 300, 250, 200, 60): #aqui fala que se clicar no botao jogar, vai levar direto pro jogo
            jogo(tela,largura_tela,altura_tela,tela_inicial) 

        if desenhar_botao("Como jogar", 300, 350, 200,60): #desenha o botao como jogar e se clicar no mesmo, leva pra def como_jogar
            como_jogar(tela,largura_tela,altura_tela)

        if desenhar_botao("Sair", 300, 650, 200, 60):  #desenha o botao como jogar e se clicar no mesmo, o jogo fecha
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

tela_inicial()
