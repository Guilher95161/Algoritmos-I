from classes.retangulo import Retangulo
import pygame
pygame.init()

# Configurações da tela
LARGURA = 800   
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
rodando = True
clock = pygame.time.Clock()

# Definindo cores
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Crie uma instância do retângulo
retangulo = Retangulo(100, 100, 120, 60, AZUL, 5)

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    retangulo.mover(teclas)

    tela.fill((128, 128, 128))
    retangulo.desenhar(tela)
    pygame.display.update()
    clock.tick(60)