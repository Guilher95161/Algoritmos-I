import pygame

class Retangulo:
    def __init__(self, x, y, largura, altura, cor, velocidade):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.velocidade = velocidade

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))