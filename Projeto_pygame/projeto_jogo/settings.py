# ==============================================================================
# --- CONFIGURAÇÕES DO JOGO ---
# ==============================================================================

# Dimensões da tela
LARGURA = 1200
ALTURA = 800

# Dimensões dos tanques
LARGURA_TANQUE = 60
ALTURA_TANQUE = 60

# Velocidades
VELOCIDADE_TANQUE = 3
VELOCIDADE_RECUO = 2
VELOCIDADE_PROJETIL = 8

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)

# Cores da interface
COR_FUNDO_MENU = (30, 30, 50)
COR_BOTAO_HOVER = (200, 200, 200)

# Controles dos jogadores
import pygame

CONTROLE_1 = {
    'frente': pygame.K_w,
    'tras': pygame.K_s,
    'esquerda': pygame.K_a,
    'direita': pygame.K_d,
    'atirar': pygame.K_SPACE
}

CONTROLE_2 = {
    'frente': pygame.K_UP,
    'tras': pygame.K_DOWN,
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT,
    'atirar': pygame.K_RETURN
}

# Configurações de áudio
VOLUME = 0.3