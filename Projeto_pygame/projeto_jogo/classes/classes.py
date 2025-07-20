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
        """
        Inicializa o tanque.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.angulo = 0
        self.velocidade = velocidade
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.imagem = pygame.transform.rotozoom(self.IMAGEM_BASE, 0, 1)
        self.tiro = False
        self.cooldown_tiro = 0
        
        # Posição anterior para rollback em caso de colisão
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

    # def salvar_posicao(self):
    #     """Salva a posição atual para poder voltar em caso de colisão"""
    #     self.pos_anterior = (self.rect.x, self.rect.y)

    # def voltar_posicao_anterior(self):
    #     """Volta para a posição anterior"""
    #     self.rect.x, self.rect.y = self.pos_anterior

    def mover(self, teclas):
        """
        Move o tanque conforme as teclas pressionadas.
        """
        # Salvar posição antes de mover
        # self.salvar_posicao()
        
        # Rotação
        if teclas[self.teclas["esquerda"]]:
            self.angulo -= 0.05
        if teclas[self.teclas["direita"]]:
            self.angulo += 0.05
            
        # Movimento
        if teclas[self.teclas["cima"]]:
            self.rect.x += math.cos(self.angulo) * self.velocidade
            self.rect.y += math.sin(self.angulo) * self.velocidade
        if teclas[self.teclas["baixo"]]:
            self.rect.x -= math.cos(self.angulo) * self.velocidade
            self.rect.y -= math.sin(self.angulo) * self.velocidade

        # Verificar limites da tela
        self._verificar_limites()

    def _verificar_limites(self):
        """Verifica e ajusta a posição do tanque dentro dos limites da tela"""
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > self.largura_tela:
            self.rect.x = self.largura_tela - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.height > self.altura_tela:
            self.rect.y = self.altura_tela - self.rect.height

    # def get_direcao_movimento(self):
    #     """Retorna o vetor de direção baseado no ângulo atual"""
    #     return (math.cos(self.angulo), math.sin(self.angulo))

    # def aplicar_impulso(self, impulso_x, impulso_y):
    #     """Aplica um impulso ao tanque"""
    #     self.rect.x += impulso_x
    #     self.rect.y += impulso_y
    #     self._verificar_limites()

    def atirar(self, teclas):
        """
        Método para atirar. Implementar lógica de tiro aqui.
        """
        if self.teclas.get("atirar") and teclas[self.teclas["atirar"]]:
            # Aqui você pode implementar a lógica de tiro, como criar um projétil
            self.tiro = True
            self.esta_atirando()
        else: 
            self.tiro = False
    def esta_atirando(self):
        if self.cooldown_tiro == 0:
            self.cooldown_tiro = 20
            self.projetil = Projetil(self.rect.x,self.rect.y, self.angulo)

    def desenhar(self):
        """
        Retorna a imagem rotacionada e o retângulo para desenhar na tela.
        """
        imagem_rotacionada = pygame.transform.rotate(self.imagem, -math.degrees(self.angulo))
        rect_rotacionado = imagem_rotacionada.get_rect(center=self.rect.center)
        return imagem_rotacionada, rect_rotacionado

    def atualizar(self, teclas):
        """
        Atualiza o estado do tanque.
        """
        self.mover(teclas)
        self.atirar(teclas)
        if self.cooldown_tiro>0:
            self.cooldown_tiro -= 1
        return self.desenhar()

    # def colidiu_com(self, outro_tanque):
    #     """Verifica colisão com outro tanque"""
    #     return self.rect.colliderect(outro_tanque.rect)

    # def resolver_colisao_com(self, outro_tanque):
    #     """
    #     Resolve colisão com outro tanque de forma mais elegante
    #     """
    #     # Calcular vetor de separação
    #     dx = self.rect.centerx - outro_tanque.rect.centerx
    #     dy = self.rect.centery - outro_tanque.rect.centery
    #     distancia = math.sqrt(dx**2 + dy**2)
        
    #     if distancia == 0:
    #         dx, dy = 1, 0
    #         distancia = 1
        
    #     # Normalizar
    #     dx_norm = dx / distancia
    #     dy_norm = dy / distancia
        
    #     # Calcular impulso de separação
    #     impulso = 3.0
        
    #     # Aplicar impulsos opostos
    #     self.aplicar_impulso(dx_norm * impulso, dy_norm * impulso)
    #     outro_tanque.aplicar_impulso(-dx_norm * impulso, -dy_norm * impulso)

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, velocidade=10):
        super().__init__()
        self.image = pygame.image.load("D:\\guilh\\Desktop\\Escola\\UFMA\\Algoritmos I\\Projeto_pygame\\projeto_jogo\\imagens\\kenney_topdownTanksRedux\\PNG\\Default_size\\bulletGreen2.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect= self.image.get_rect()
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