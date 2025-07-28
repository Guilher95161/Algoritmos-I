import math
import pygame
import settings

# ==============================================================================
# --- CLASSES DO JOGO ---
# ==============================================================================

class Tanque(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, controles, imagem_path, morto_imagem_path, jogador_id):
        super().__init__()

        self.original_image = pygame.image.load(imagem_path).convert_alpha()
        self.morto_image = pygame.image.load(morto_imagem_path).convert_alpha()
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Posição e Rotação
        self.x = x
        self.y = y
        self.angulo = angulo
        self.pos_inicial_x = x
        self.pos_inicial_y = y
        self.angulo_inicial = angulo
        
        # Atributos de Jogo
        self.velocidade = settings.VELOCIDADE_TANQUE
        self.velocidade_recuo = settings.VELOCIDADE_RECUO
        self.jogador_id = jogador_id
        self.controles = controles
        self.pode_atirar = 30
        self.recuo_ativo = 0
        self.vivo = True
        self.vidas = 3  # Para o modo assistente
        self.mask = pygame.mask.from_surface(self.image)

    def mover(self, teclas, modo_assistente=False):
        if not self.vivo:
            self.image = pygame.transform.rotate(self.morto_image, -self.angulo)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            if modo_assistente:
                # Movimento vertical apenas (cima e baixo)
                if teclas[self.controles['tras']]:
                    self.y -= self.velocidade
                if teclas[self.controles['frente']]:
                    self.y += self.velocidade
                    
                # Manter dentro da tela (vertical) - CORREÇÃO DO BUG
                self.y = max(settings.ALTURA_TANQUE / 2, min(settings.ALTURA - settings.ALTURA_TANQUE / 2, self.y))
                
                # Rotacionar tanque para posição vertical
                if self.jogador_id == 1:
                    self.image = pygame.transform.rotate(self.original_image, 0)
                else:
                    self.image = pygame.transform.rotate(self.original_image, 180)
                self.rect = self.image.get_rect(center=(self.x, self.y))
            else:
                # Rotação (só permite se não houver recuo)
                if self.recuo_ativo <= 0:
                    if teclas[self.controles['esquerda']]:
                        self.angulo -= 5
                    if teclas[self.controles['direita']]:
                        self.angulo += 5
                
                self.angulo %= 360
                angulo_rad = math.radians(self.angulo)

                # Movimento
                if self.recuo_ativo > 0:
                    # Move para trás (recuo)
                    self.x -= math.cos(angulo_rad) * self.velocidade_recuo
                    self.y -= math.sin(angulo_rad) * self.velocidade_recuo
                    self.recuo_ativo -= 1
                else:
                    # Movimento normal
                    if teclas[self.controles['frente']]:
                        self.x += math.cos(angulo_rad) * self.velocidade
                        self.y += math.sin(angulo_rad) * self.velocidade
                    if teclas[self.controles['tras']]:
                        self.x -= math.cos(angulo_rad) * self.velocidade
                        self.y -= math.sin(angulo_rad) * self.velocidade

                # Manter dentro da tela Mudar isso daqui
                self.x = max(settings.LARGURA_TANQUE / 2, min(settings.LARGURA - settings.LARGURA_TANQUE / 2, self.x))
                self.y = max(settings.ALTURA_TANQUE / 2, min(settings.ALTURA - settings.ALTURA_TANQUE / 2, self.y))

                # Atualiza a imagem rotacionada e o rect
                self.image = pygame.transform.rotate(self.original_image, -self.angulo)
                self.rect = self.image.get_rect(center=(self.x, self.y))
            
            self.mask = pygame.mask.from_surface(self.image)

    def atirar(self, balas_grupo, modo_assistente=False, alvo=None):
        if self.pode_atirar >= 30 and self.vivo:
            if modo_assistente and alvo:
                # Mira assistida - calcula ângulo para o alvo
                dx = alvo.x - self.x
                dy = alvo.y - self.y
                angulo_tiro = math.degrees(math.atan2(dy, dx))
            else:
                angulo_tiro = self.angulo
            
            angulo_rad = math.radians(angulo_tiro)
            distancia_canhao = settings.LARGURA_TANQUE / 2

            pos_x = self.x + math.cos(angulo_rad) * distancia_canhao
            pos_y = self.y + math.sin(angulo_rad) * distancia_canhao

            bala = Projetil(pos_x, pos_y, angulo_tiro, self.jogador_id)
            balas_grupo.add(bala)

            if not modo_assistente:
                self.recuo_ativo = 8
            self.pode_atirar = 0

    def update(self, balas_grupo, modo_assistente=False, alvo=None):
        teclas = pygame.key.get_pressed()
        self.mover(teclas, modo_assistente)
        
        if teclas[self.controles['atirar']]:
            self.atirar(balas_grupo, modo_assistente, alvo)
        
        if self.pode_atirar < 30:
            self.pode_atirar += 1

    def morrer(self):
        self.vivo = False

    def levar_dano(self):
        #Para o modo assistente - diminui uma vida
        self.vidas -= 1
        if self.vidas <= 0:
            self.morrer()

    def reset(self, x=None, y=None, angulo=None, modo_assistente=False):
        self.x = self.pos_inicial_x
        self.y = self.pos_inicial_y
        self.angulo = self.angulo_inicial
        self.vivo = True
        self.vidas = 3
        self.pode_atirar = 30
        self.recuo_ativo = 0
        self.image = self.original_image

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, jogador_id):
        super().__init__()
        
        # carrega a imagem da bala
        self.image = pygame.image.load("imagens/bala_verde.png").convert_alpha()

        self.image = pygame.transform.rotate(self.image, -angulo)
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidade = settings.VELOCIDADE_PROJETIL
        self.angulo = angulo
        self.x = float(x)
        self.y = float(y)
        self.jogador_id = jogador_id
        self.mask = pygame.mask.from_surface(self.image)

    def mover(self, largura_limite=None):
        angulo_rad = math.radians(self.angulo)
        self.x += math.cos(angulo_rad) * self.velocidade
        self.y += math.sin(angulo_rad) * self.velocidade
        self.rect.center = (round(self.x), round(self.y))

        
        largura_tela = largura_limite if largura_limite else settings.LARGURA
        tela_rect = pygame.Rect(0, 0, largura_tela, settings.ALTURA)
        
        # Se bala sai do retangulo da tela, remove do grupo
        if not self.rect.colliderect(tela_rect):
            self.kill()

    def update(self, largura_limite=None):
        self.mover(largura_limite)

# ==============================================================================
# --- FUNÇÕES AUXILIARES E DE INTERFACE ---
# ==============================================================================

def verificar_colisoes_bala_bala(balas_grupo):
    """
    Verifica colisões entre balas de jogadores diferentes
    e remove ambas as balas se colidirem
    """
    balas_lista = list(balas_grupo)
    
    for i in range(len(balas_lista)):
        for j in range(i + 1, len(balas_lista)):
            bala1 = balas_lista[i]
            bala2 = balas_lista[j]
            
            # Só verifica colisão entre balas de jogadores diferentes
            if bala1.jogador_id != bala2.jogador_id:
                # Verifica se ainda estão no grupo (não foram removidas)
                if bala1 in balas_grupo and bala2 in balas_grupo:
                    if pygame.sprite.collide_mask(bala1, bala2):
                        # Remove ambas as balas
                        bala1.kill()
                        bala2.kill()
                        break  # Sai do loop interno
    
def verificar_colisoes_bala_tanque(balas_grupo, tanques_grupo, modo_assistente=False):
    for bala in balas_grupo:
        for tanque in tanques_grupo:
            if bala.jogador_id != tanque.jogador_id and tanque.vivo:
                if pygame.sprite.collide_mask(bala, tanque):
                    bala.kill()
                    if modo_assistente:
                        tanque.levar_dano()
                        # Verifica se ainda há tanques vivos
                        tanques_vivos = [t for t in tanques_grupo if t.vivo]#mudar isso daqui
                        if len(tanques_vivos) == 1:
                            return tanques_vivos[0].jogador_id
                    else:
                        tanque.morrer()
                        return bala.jogador_id  # Retorna o ID do jogador que venceu (o que atirou)
    return None

def desenhar_texto(surface, text, size, x, y, color=settings.BRANCO, font_name=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def desenhar_botao(surface, rect, text):
    mouse_pos = pygame.mouse.get_pos()
    cor_fundo = settings.COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else settings.CINZA#tira esse operador ternário
    
    pygame.draw.rect(surface, cor_fundo, rect, border_radius=10)
    desenhar_texto(surface, text, 40, rect.centerx, rect.centery, settings.PRETO)

def desenhar_hud(modo_assistente=False):
    if modo_assistente:
        # Jogador 1 - lado esquerdo superior
        desenhar_texto(tela, "Jogador 1", 30, 100, 50, settings.VERDE)
        desenhar_coracoes(tanque1, 20, 80)
        
        # Jogador 2 - lado direito superior  
        desenhar_texto(tela, "Jogador 2", 30, settings.LARGURA - 100, 50, settings.AZUL)
        desenhar_coracoes(tanque2, settings.LARGURA - 140, 80)
    else:
        desenhar_texto(tela, "Jogador 1", 30, 80, 25, settings.VERDE)
        desenhar_texto(tela, "Jogador 2", 30, settings.LARGURA - 80, 25, settings.AZUL)

def desenhar_coracoes(tanque, x, y):
    """Desenha os corações representando as vidas do tanque"""
    for i in range(3):
        cor = settings.VERMELHO if i < tanque.vidas else settings.CINZA
        coracao_x = x + (i * 35)
        # Desenha um coração simples usando círculos e triângulo
        pygame.draw.circle(tela, cor, (coracao_x, y), 10)
        pygame.draw.circle(tela, cor, (coracao_x + 10, y), 10)
        pygame.draw.polygon(tela, cor, [(coracao_x - 10, y + 5), (coracao_x + 20, y + 5), (coracao_x + 5, y + 20)])

def reiniciar_jogo(modo_assistente=False):
    balas_sprites.empty()
    
    if modo_assistente:
        # Posicionamento vertical: Jogador 1 no topo, Jogador 2 embaixo
        tanque1.reset(settings.LARGURA / 2, 100, 90, modo_assistente)  # Topo da tela
        tanque2.reset(settings.LARGURA / 2, settings.ALTURA - 100, 270, modo_assistente)  # Fundo da tela
    else:
        tanque1.reset(200, settings.ALTURA / 2, 0)
        tanque2.reset(settings.LARGURA - 200, settings.ALTURA / 2, 180)

# ==============================================================================
# --- INICIALIZAÇÃO E SETUP DO JOGO ---
# ==============================================================================

pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((settings.LARGURA, settings.ALTURA))
pygame.display.set_caption("Batalha de Tanques")
clock = pygame.time.Clock()

# Carrega a música de fundo
pygame.mixer.music.load("audios//musica_fundo.mp3")
pygame.mixer.music.set_volume(settings.VOLUME)
pygame.mixer.music.play(-1)

# Instâncias dos tanques
tanque1 = Tanque(200, settings.ALTURA / 2, 0, settings.CONTROLE_1, "imagens//tanque_verde.png", "imagens//tanque_morto.png", 1)
tanque2 = Tanque(settings.LARGURA - 200, settings.ALTURA / 2, 180, settings.CONTROLE_2, "imagens//tanque_azul.png", "imagens//tanque_morto.png", 2)

# Chão 
chao_principal = pygame.image.load("imagens//mapa.png").convert_alpha()

# Grupos de Sprites
tanques_sprites = pygame.sprite.Group(tanque1, tanque2)
balas_sprites = pygame.sprite.Group()

# Retângulos dos botões (para verificação de clique)
btn_iniciar_rect = pygame.Rect(settings.LARGURA/2 - 150, settings.ALTURA/2 - 50, 300, 50)
btn_assistente_rect = pygame.Rect(settings.LARGURA/2 - 150, settings.ALTURA/2 + 10, 300, 50)
btn_sair_rect = pygame.Rect(settings.LARGURA/2 - 150, settings.ALTURA/2 + 70, 300, 50)
btn_jogar_novamente_rect = pygame.Rect(settings.LARGURA/2 - 150, settings.ALTURA/2 + 50, 300, 50)
btn_voltar_menu_rect = pygame.Rect(settings.LARGURA/2 - 150, settings.ALTURA/2 + 120, 300, 50)

# Variáveis de controle de estado
estado_jogo = "MENU"
modo_assistente = False
rodando = True
vencedor = None

# ==============================================================================
# --- LOOP PRINCIPAL ---
# ==============================================================================
while rodando:
    # --- Processamento de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if estado_jogo == "MENU":
                if btn_iniciar_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    modo_assistente = False
                    reiniciar_jogo(modo_assistente)
                elif btn_assistente_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    modo_assistente = True
                    # Mantém a tela normal para o modo vertical
                    reiniciar_jogo(modo_assistente)
                elif btn_sair_rect.collidepoint(mouse_pos):
                    rodando = False
            elif estado_jogo == "FIM_DE_JOGO":
                if btn_jogar_novamente_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    reiniciar_jogo(modo_assistente)
                elif btn_voltar_menu_rect.collidepoint(mouse_pos):
                    estado_jogo = "MENU"
                    modo_assistente = False

    # --- Lógica de cada estado do Jogo ---
    if estado_jogo == "MENU":
        tela.fill(settings.COR_FUNDO_MENU)
        desenhar_texto(tela, "Batalha de Tanques", 100, settings.LARGURA / 2, settings.ALTURA / 4, settings.AMARELO)
        desenhar_botao(tela, btn_iniciar_rect, "Jogo Principal")
        desenhar_botao(tela, btn_assistente_rect, "Assistente de Mira")
        desenhar_botao(tela, btn_sair_rect, "Sair")

    elif estado_jogo == "JOGO_PRINCIPAL":
        tela.blit(chao_principal, (0, 0))
        
        if modo_assistente:
            # No modo assistente, os tanques miram automaticamente um no outro
            tanque1.update(balas_sprites, modo_assistente, tanque2)
            tanque2.update(balas_sprites, modo_assistente, tanque1)
            balas_sprites.update()
        else:
            tanques_sprites.update(balas_sprites)
            balas_sprites.update()
        
        # NOVA FUNCIONALIDADE: Verificar colisões entre balas
        verificar_colisoes_bala_bala(balas_sprites)
        
        vencedor = verificar_colisoes_bala_tanque(balas_sprites, tanques_sprites, modo_assistente)
        if vencedor is not None:
            estado_jogo = "FIM_DE_JOGO"

        desenhar_hud(modo_assistente)
        tanques_sprites.draw(tela)
        balas_sprites.draw(tela)
        
    elif estado_jogo == "FIM_DE_JOGO":
        # Continua desenhando o jogo no fundo
        tela.blit(chao_principal, (0, 0))
        desenhar_hud(modo_assistente)

        # Atualiza os tanques para mostrar imagem de morto
        if modo_assistente:
            tanque1.update(balas_sprites, modo_assistente, tanque2)
            tanque2.update(balas_sprites, modo_assistente, tanque1)
            balas_sprites.update()
        else:
            tanques_sprites.update(balas_sprites)
            balas_sprites.update()

        tanques_sprites.draw(tela)
        balas_sprites.draw(tela)

        # Sobreposição escura
        overlay = pygame.Surface((settings.LARGURA, settings.ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        # Mensagens e botões
        cor_vencedor = settings.VERDE if vencedor == 1 else settings.AZUL
        desenhar_texto(tela, "Fim de Jogo", 100, settings.LARGURA / 2, settings.ALTURA / 4, settings.BRANCO)
        desenhar_texto(tela, f"Jogador {vencedor} Venceu!", 60, settings.LARGURA / 2, settings.ALTURA / 2 - 50, cor_vencedor)
        
        desenhar_botao(tela, btn_jogar_novamente_rect, "Jogar Novamente")
        desenhar_botao(tela, btn_voltar_menu_rect, "Voltar ao Menu")

    # --- Atualização Final da Tela ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()