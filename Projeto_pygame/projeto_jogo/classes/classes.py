import pygame
import math
class Tanque:
    def __init__(self, x, y, largura, altura,velocidade,largura_tela,altura_tela):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.angulo = 0
        self.velocidade = velocidade
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.imagem = pygame.image.load(
            r"D:\guilh\Desktop\Escola\UFMA\Algoritmos I\Projeto_pygame\projeto_jogo\imagens\kenney_topdownTanksRedux\PNG\Default_size\k_green.png"
        ).convert_alpha()
    def mover(self, teclas):
        if self.x < 0:
            self.x = 0
        if self.x + self.largura > self.largura_tela:
            self.x = self.largura_tela - self.largura
        if self.y < 0:
            self.y = 0
        if self.y + self.altura > self.altura_tela:
            self.y = self.altura_tela - self.altura
        if teclas[pygame.K_LEFT]:
            self.angulo -= 0.05
        if teclas[pygame.K_RIGHT]:
            self.angulo += 0.05
        if teclas[pygame.K_UP]:
            self.x += math.cos(self.angulo) * self.velocidade
            self.y += math.sin(self.angulo) * self.velocidade
        if teclas[pygame.K_DOWN]:
            self.x -= math.cos(self.angulo) * self.velocidade
            self.y -= math.sin(self.angulo) * self.velocidade

    def desenhar(self):
        image_rotacionada = pygame.transform.rotate(self.imagem, -math.degrees(self.angulo))
        ret = image_rotacionada.get_rect(center=(self.x + self.largura // 2, self.y + self.altura // 2))
        return image_rotacionada, ret