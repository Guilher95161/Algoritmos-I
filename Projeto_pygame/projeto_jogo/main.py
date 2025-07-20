'''
O que falta fazer:
3. Fazer com que o retangulo atire
4. Fazer com que o retangulo tenha vida
5. Fazer com que o retangulo tenha animação de morte
7. canhão que atire projéteis
8. Fazer uma classe de projétil que se mova e colida com o tanque ou obstáculos
9. Fazer classe de obstáculo que colida com o tanque e projéteis
10. Fazer os tanques terem imagens diferentes
'''
import pygame
import math

import pygame
import math

class Tanque(pygame.sprite.Sprite):
    IMAGEM_BASE = pygame.image.load(
        r"D:\guilh\Desktop\Escola\UFMA\Algoritmos I\Projeto_pygame\projeto_jogo\imagens\kenney_topdownTanksRedux\PNG\Default_size\k_green.png"
    )

    def __init__(
        self, x, y, largura, altura, velocidade, largura_tela, altura_tela,
        teclas=None
    ):
        super().__init__()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.angulo = 0
        self.velocidade = velocidade
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.imagem = pygame.transform.rotozoom(self.IMAGEM_BASE, 0, 1)
        self.tiro = False
        self.cooldown_tiro = 0
        self.pos_anterior = (x, y)
        if teclas is None:
            self.teclas = {
                "esquerda": pygame.K_LEFT,
                "direita": pygame.K_RIGHT,
                "cima": pygame.K_UP,
                "baixo": pygame.K_DOWN,
                "atirar":pygame.K_RETURN
            }
        else:
            self.teclas = teclas

    def mover(self, teclas):
        if teclas[self.teclas["esquerda"]]:
            self.angulo -= 0.05
        if teclas[self.teclas["direita"]]:
            self.angulo += 0.05
        if teclas[self.teclas["cima"]]:
            self.rect.x += math.cos(self.angulo) * self.velocidade
            self.rect.y += math.sin(self.angulo) * self.velocidade
        if teclas[self.teclas["baixo"]]:
            self.rect.x -= math.cos(self.angulo) * self.velocidade
            self.rect.y -= math.sin(self.angulo) * self.velocidade
        self._verificar_limites()

    def _verificar_limites(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > self.largura_tela:
            self.rect.x = self.largura_tela - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.height > self.altura_tela:
            self.rect.y = self.altura_tela - self.rect.height

    def atirar(self, teclas):
        if self.teclas.get("atirar") and teclas[self.teclas["atirar"]]:
            self.tiro = True
            self.esta_atirando()
        else: 
            self.tiro = False

    def esta_atirando(self):
        if self.cooldown_tiro == 0:
            self.cooldown_tiro = 20
            self.projetil = Projetil(self.rect.x, self.rect.y, self.angulo)

    def desenhar(self):
        imagem_rotacionada = pygame.transform.rotate(self.imagem, -math.degrees(self.angulo))
        rect_rotacionado = imagem_rotacionada.get_rect(center=self.rect.center)
        return imagem_rotacionada, rect_rotacionado

    def atualizar(self, teclas):
        self.mover(teclas)
        self.atirar(teclas)
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1
        return self.desenhar()

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, velocidade=10):
        super().__init__()
        self.image = pygame.image.load(
            "D:\\guilh\\Desktop\\Escola\\UFMA\\Algoritmos I\\Projeto_pygame\\projeto_jogo\\imagens\\kenney_topdownTanksRedux\\PNG\\Default_size\\bulletGreen2.png"
        ).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.x_vel = math.cos(angulo) * velocidade
        self.y_vel = math.sin(angulo) * velocidade
        self.angulo = angulo
        self.velocidade = velocidade
        self.raio = 5
        self.ativo = True

    def movimento_bala(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        self.movimento_bala()

    def atualizar(self):
        if self.ativo:
            self.x += math.cos(self.angulo) * self.velocidade
            self.y += math.sin(self.angulo) * self.velocidade

    def desenhar(self, tela):
        if self.ativo:
            pygame.draw.circle(tela, (255, 0, 0), (int(self.x), int(self.y)), self.raio)

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 800   
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
rodando = True
clock = pygame.time.Clock()
pygame.display.set_caption("Batalha de Tanques")
ground_surface = pygame.image.load("D:\\guilh\\Downloads\\map.png").convert_alpha()


# Cria duas instâncias da classe Tanque
teclas_tanque2 = {
    "esquerda": pygame.K_a,
    "direita": pygame.K_d,
    "cima": pygame.K_w,
    "baixo": pygame.K_s,
    "atirar": pygame.K_SPACE
}
tanque1 = Tanque(100, 100, 50, 50,5,LARGURA, ALTURA)
tanque2 = Tanque(300, 300, 50, 50,5,LARGURA, ALTURA,teclas_tanque2)

sprite_todos_grupos = pygame.sprite.Group()
projetil_grupo = pygame.sprite.Group()
sprite_todos_grupos.add(tanque1)
sprite_todos_grupos.add(tanque2)

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    
    tela.blit(ground_surface, (0, 0))
    imagem1,ret1 = tanque1.atualizar(teclas)
    tela.blit(imagem1, ret1)
    imagem2,ret2 = tanque2.atualizar(teclas)
    tela.blit(imagem2, ret2)
    # pygame.draw.rect(tela, (255, 0, 0), ret1, 2)
    # pygame.draw.rect(tela, (0, 255, 0), tanque1.rect, 2)
    # if tanque1.colidiu_com(tanque2):
    #     tanque1.resolver_colisao_com(tanque2)
    # if tanque2.colidiu_com(tanque1):
    #     tanque2.resolver_colisao_com(tanque1)
        
    pygame.display.update()
    clock.tick(60)