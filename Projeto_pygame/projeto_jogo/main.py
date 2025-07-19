'''
O que falta fazer:
2. Fazer com que possa ter mais de um retângulo na tela, ou seja, 
2.1. Fazer o movimento do retangulo não ser só com WASD
3. Fazer com que o retangulo atire
4. Fazer com que o retangulo tenha vida
5. Fazer com que o retangulo tenha animação de morte
7. canhão que atire projéteis
8. Fazer uma classe de projétil que se mova e colida com o tanque ou obstáculos
9. Fazer classe de obstáculo que colida com o tanque e projéteis

'''
from classes.classes import Tanque
import pygame
# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 800   
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
rodando = True
clock = pygame.time.Clock()
pygame.display.set_caption("Jogo com Retângulo")
ground_surface = pygame.image.load("D:\\guilh\\Downloads\\map.png").convert_alpha()


# Cria uma instância do retângulo
tanque = Tanque(100, 100, 64, 64,5,LARGURA, ALTURA)

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    tanque.mover(teclas)

    tela.blit(ground_surface, (0, 0))
    imagem,ret = tanque.desenhar()
    tela.blit(imagem, ret)
        
    pygame.display.update()
    clock.tick(60)