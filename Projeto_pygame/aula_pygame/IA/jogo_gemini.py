import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Constantes
LARGURA = 1000
ALTURA = 700
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)
VERDE_ESCURO = (0, 128, 0)

class Projetil:
    def __init__(self, x, y, angulo, velocidade=8):
        self.x = x
        self.y = y
        self.vel_x = math.cos(angulo) * velocidade
        self.vel_y = math.sin(angulo) * velocidade
        self.raio = 3
        self.ativo = True
    
    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Verificar se saiu da tela
        if self.x < 0 or self.x > LARGURA or self.y < 0 or self.y > ALTURA:
            self.ativo = False
    
    def desenhar(self, tela):
        pygame.draw.circle(tela, AMARELO, (int(self.x), int(self.y)), self.raio)

class Tanque:
    def __init__(self, x, y, cor, controles):
        self.x = x
        self.y = y
        self.angulo = 0
        self.vida = 100
        self.vida_max = 100
        self.largura = 30
        self.altura = 20
        self.velocidade = 3
        self.cor = cor
        self.controles = controles
        self.projeteis = []
        self.ultimo_tiro = 0
        self.cooldown_tiro = 500  # milissegundos
        
    def mover(self, teclas):
        # Movimento baseado nos controles
        if teclas[self.controles['esquerda']]:
            self.angulo -= 0.05
        if teclas[self.controles['direita']]:
            self.angulo += 0.05
        if teclas[self.controles['frente']]:
            self.x += math.cos(self.angulo) * self.velocidade
            self.y += math.sin(self.angulo) * self.velocidade
        if teclas[self.controles['tras']]:
            self.x -= math.cos(self.angulo) * self.velocidade
            self.y -= math.sin(self.angulo) * self.velocidade
            
        # Manter dentro da tela
        self.x = max(self.largura//2, min(LARGURA - self.largura//2, self.x))
        self.y = max(self.altura//2, min(ALTURA - self.altura//2, self.y))
    
    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cooldown_tiro:
            # Posição da ponta do canhão
            ponta_x = self.x + math.cos(self.angulo) * (self.largura//2 + 10)
            ponta_y = self.y + math.sin(self.angulo) * (self.largura//2 + 10)
            
            projetil = Projetil(ponta_x, ponta_y, self.angulo)
            self.projeteis.append(projetil)
            self.ultimo_tiro = agora
    
    def atualizar_projeteis(self):
        for projetil in self.projeteis[:]:
            projetil.atualizar()
            if not projetil.ativo:
                self.projeteis.remove(projetil)
    
    def verificar_colisao_projetil(self, outros_projeteis):
        for projetil in outros_projeteis[:]:
            if projetil.ativo:
                # Verificar distância entre projétil e tanque
                dist = math.sqrt((projetil.x - self.x)**2 + (projetil.y - self.y)**2)
                if dist < self.largura//2 + projetil.raio:
                    self.vida -= 20
                    projetil.ativo = False
                    outros_projeteis.remove(projetil)
                    return True
        return False
    
    def desenhar(self, tela):
        # Calcular pontos do tanque rotacionado
        pontos = []
        cos_a = math.cos(self.angulo)
        sin_a = math.sin(self.angulo)
        
        # Retângulo do tanque
        w, h = self.largura, self.altura
        vertices = [(-w//2, -h//2), (w//2, -h//2), (w//2, h//2), (-w//2, h//2)]
        
        for vx, vy in vertices:
            px = self.x + vx * cos_a - vy * sin_a
            py = self.y + vx * sin_a + vy * cos_a
            pontos.append((px, py))
        
        pygame.draw.polygon(tela, self.cor, pontos)
        
        # Canhão
        canhao_x = self.x + math.cos(self.angulo) * (self.largura//2 + 10)
        canhao_y = self.y + math.sin(self.angulo) * (self.largura//2 + 10)
        pygame.draw.line(tela, PRETO, (self.x, self.y), (canhao_x, canhao_y), 4)
        
        # Desenhar projéteis
        for projetil in self.projeteis:
            projetil.desenhar(tela)
    
    def desenhar_vida(self, tela, x, y):
        # Barra de vida
        largura_barra = 100
        altura_barra = 10
        
        # Fundo da barra
        pygame.draw.rect(tela, VERMELHO, (x, y, largura_barra, altura_barra))
        
        # Vida atual
        vida_largura = (self.vida / self.vida_max) * largura_barra
        pygame.draw.rect(tela, VERDE, (x, y, vida_largura, altura_barra))
        
        # Contorno
        pygame.draw.rect(tela, PRETO, (x, y, largura_barra, altura_barra), 2)

def main():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Tanques 2D")
    clock = pygame.time.Clock()
    
    # Criar fonte
    fonte = pygame.font.Font(None, 36)
    
    # Controles dos jogadores
    controles_jogador1 = {
        'frente': pygame.K_w,
        'tras': pygame.K_s,
        'esquerda': pygame.K_a,
        'direita': pygame.K_d,
        'atirar': pygame.K_SPACE
    }
    
    controles_jogador2 = {
        'frente': pygame.K_UP,
        'tras': pygame.K_DOWN,
        'esquerda': pygame.K_LEFT,
        'direita': pygame.K_RIGHT,
        'atirar': pygame.K_RETURN
    }
    
    # Criar tanques
    tanque1 = Tanque(150, 150, AZUL, controles_jogador1)
    tanque2 = Tanque(LARGURA - 150, ALTURA - 150, VERDE_ESCURO, controles_jogador2)
    
    # Variáveis do jogo
    jogo_ativo = True
    vencedor = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not jogo_ativo:
                    # Reiniciar jogo
                    tanque1 = Tanque(150, 150, AZUL, controles_jogador1)
                    tanque2 = Tanque(LARGURA - 150, ALTURA - 150, VERDE_ESCURO, controles_jogador2)
                    jogo_ativo = True
                    vencedor = None
        
        if jogo_ativo:
            teclas = pygame.key.get_pressed()
            
            # Movimentar tanques
            tanque1.mover(teclas)
            tanque2.mover(teclas)
            
            # Atirar
            if teclas[controles_jogador1['atirar']]:
                tanque1.atirar()
            if teclas[controles_jogador2['atirar']]:
                tanque2.atirar()
            
            # Atualizar projéteis
            tanque1.atualizar_projeteis()
            tanque2.atualizar_projeteis()
            
            # Verificar colisões
            tanque1.verificar_colisao_projetil(tanque2.projeteis)
            tanque2.verificar_colisao_projetil(tanque1.projeteis)
            
            # Verificar vencedor
            if tanque1.vida <= 0:
                vencedor = "Jogador 2 (Verde)"
                jogo_ativo = False
            elif tanque2.vida <= 0:
                vencedor = "Jogador 1 (Azul)"
                jogo_ativo = False
        
        # Desenhar tudo
        tela.fill(CINZA)
        
        if jogo_ativo:
            tanque1.desenhar(tela)
            tanque2.desenhar(tela)
            
            # Desenhar barras de vida
            tanque1.desenhar_vida(tela, 10, 10)
            tanque2.desenhar_vida(tela, LARGURA - 110, 10)
            
            # Labels dos jogadores
            texto1 = fonte.render("Jogador 1 (WASD + Espaço)", True, AZUL)
            texto2 = fonte.render("Jogador 2 (Setas + Enter)", True, VERDE_ESCURO)
            tela.blit(texto1, (10, 30))
            tela.blit(texto2, (LARGURA - 280, 30))
            
        else:
            # Tela de fim de jogo
            texto_vencedor = fonte.render(f"{vencedor} Venceu!", True, PRETO)
            texto_reiniciar = fonte.render("Pressione R para reiniciar", True, PRETO)
            
            tela.blit(texto_vencedor, (LARGURA//2 - 100, ALTURA//2 - 50))
            tela.blit(texto_reiniciar, (LARGURA//2 - 130, ALTURA//2))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()