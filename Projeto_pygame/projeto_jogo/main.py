import math
import pygame
import settings

# ==============================================================================
# --- CLASSES DO JOGO ---
# ==============================================================================

class Tanque(pygame.sprite.Sprite):
    #Construtor da classe Tanque
    def __init__(self, x, y, angulo, controles, imagem_path, morto_imagem_path, jogador_id):
        #Construtor da classe Sprite
        super().__init__()
        # Carrega as imagens do tanque e do tanque morto
        self.original_image = pygame.image.load(imagem_path).convert_alpha()
        self.morto_image = pygame.image.load(morto_imagem_path).convert_alpha()
        
        #self.image é a imagem do tanque, que pode ser rotacionada
        self.image = self.original_image
        #self.rect é o retângulo que envolve a imagem
        self.rect = self.image.get_rect(center=(x, y))

        # Posição e angulo do tanque
        self.x = x
        self.y = y
        self.angulo = angulo

        # Posições iniciais para reset
        self.pos_inicial_x = x
        self.pos_inicial_y = y
        self.angulo_inicial = angulo
        
        # Atributos de Jogo
        self.velocidade = settings.VELOCIDADE_TANQUE
        self.velocidade_recuo = settings.VELOCIDADE_RECUO
        self.jogador_id = jogador_id
        self.controles = controles

        #tempo para o tanque atirar
        self.pode_atirar = settings.TEMPO_TIRO

        # Recuo do tanque, o zero indica que não está recuando, se for maior que zero, está recuando
        self.recuo_ativo = 0
        
        #Indica se o tanque está vivo ou morto
        self.vivo = True
        
        # Vidas do tanque, para o modo assistente
        self.vidas = 3

        # Cria uma máscara para colisões
        self.mask = pygame.mask.from_surface(self.image)

    # Método para mover o tanque
    def mover(self, teclas, modo_assistente=False):
        # Se tanque não está vivo, não se move. Mas, tem que atualizar a imagem de morto
        if not self.vivo:
            '''
            Atualiza a imagem do tanque para a imagem de morto, mantendo a posição(rect) e ângulo(rotate). 
            Vale ressaltar, que o self.angulo está negativo no rotate porque o rotacionamento do Pygame é no sentido anti-horário,
            mas a orientação do tanque é no sentido horário.
            '''
            self.image = pygame.transform.rotate(self.morto_image, -self.angulo)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        #Se não está morto, está vivo, então se move
        else:
            #Pode ser no modo assistente, onde o tanque só se move verticalmente, ou no modo normal, onde o tanque se move normalmente
            #IF para o modo assistente, onde o tanque só se move verticalmente
            if modo_assistente:
                # Movimento vertical apenas (cima e baixo)
                if teclas[self.controles['tras']]:
                    self.y += self.velocidade
                if teclas[self.controles['frente']]:
                    self.y -= self.velocidade
                    
                # Manter dentro da tela (vertical) 
                   #Se o y do tanque for menor que a metade da altura do tanque, o y é igual a metade da altura do tanque
                   #Para o tanque não sair da tela de forma vertical na parte de cima
                if self.y < settings.ALTURA_TANQUE / 2:
                    self.y = settings.ALTURA_TANQUE / 2
                    #Se o y do tanque for maior que a altura da tela menos a metade da altura do tanque, 
                    #o y é igual a altura da tela menos a metade da altura do tanque
                    #É tipo o oposto do if acima, mas esse para o tanque não sair da tela de forma vertical na parte de baixo
                elif self.y > settings.ALTURA - settings.ALTURA_TANQUE / 2:
                    self.y = settings.ALTURA - settings.ALTURA_TANQUE / 2

                #Verifica se o tanque é o jogador 1 ou 2, para rotacionar a imagem, conforme o jogador
                #Para um ficar olhando pro outro
                if self.jogador_id == 1:
                    self.image = pygame.transform.rotate(self.original_image, 0)
                else:
                    self.image = pygame.transform.rotate(self.original_image, 180)
                self.rect = self.image.get_rect(center=(self.x, self.y))
            #Se não for no modo assistente, o tanque se move normalmente
            else:
                #Verifica se o tanque não está recuando, se não estiver, pode rotacionar
                if self.recuo_ativo <= 0:
                    #Basicamente rotaciona o tanque conforme as teclas pressionadas, de forma horária
                    #Tentei fazer o tanque rotacionar no sentido anti-horário, mas o movimento ficou estranho
                    if teclas[self.controles['esquerda']]:
                        self.angulo -= 5
                    if teclas[self.controles['direita']]:
                        self.angulo += 5
                # Mantém o ângulo dentro de 0-360 graus
                self.angulo %= 360
                # Converte o ângulo para radianos para o cálculo do movimento
                angulo_rad = math.radians(self.angulo)

                # Movimento
                # Se o tanque está recuando, move para trás
                if self.recuo_ativo > 0:
                    # Move para trás (recuo)
                    self.x -= math.cos(angulo_rad) * self.velocidade_recuo
                    self.y -= math.sin(angulo_rad) * self.velocidade_recuo
                    self.recuo_ativo -= 1
                # Se não está recuando, move normalmente
                else:
                    # Ve se movimenta para frente ou para trás
                    # A ideia é que a velocidade é tipo a tangente de um triângulo, onde o ângulo é o ângulo do tanque
                    # e o self.x e o self.y são incrementados aos catetos desse triangulo
                    if teclas[self.controles['frente']]:
                        self.x += math.cos(angulo_rad) * self.velocidade
                        self.y += math.sin(angulo_rad) * self.velocidade
                    if teclas[self.controles['tras']]:
                        self.x -= math.cos(angulo_rad) * self.velocidade
                        self.y -= math.sin(angulo_rad) * self.velocidade

                # Mantém o tanque dentro dos limites da tela horizontalmente

                # Se o x do tanque for menor que a metade da largura do tanque, o x é igual a metade da largura do tanque
                # Para o tanque não sair da tela de forma horizontal para a esquerda
                if self.x < settings.LARGURA_TANQUE / 2:
                    self.x = settings.LARGURA_TANQUE / 2

                # Se o x do tanque for maior que a largura da tela menos a metade da largura do tanque, 
                # o x é igual a largura da tela menos a metade da largura do tanque
                # Para o tanque não sair da tela de forma horizontal para a direita
                # Isso é tipo o oposto do if acima.
                elif self.x > settings.LARGURA - settings.LARGURA_TANQUE / 2:
                    self.x = settings.LARGURA - settings.LARGURA_TANQUE / 2

                # Mantém o tanque dentro dos limites da tela verticalmente, já explicado acima no modo assistente
                if self.y < settings.ALTURA_TANQUE / 2:
                    self.y = settings.ALTURA_TANQUE / 2
                elif self.y > settings.ALTURA - settings.ALTURA_TANQUE / 2:
                    self.y = settings.ALTURA - settings.ALTURA_TANQUE / 2

                # Atualiza a imagem rotacionada e o rect
                self.image = pygame.transform.rotate(self.original_image, -self.angulo)
                self.rect = self.image.get_rect(center=(self.x, self.y))
            
            #A máscara é atualizada conforme a rotação da imagem
            #A máscara é usada para colisões, então é importante que ela seja atualizada sempre
            self.mask = pygame.mask.from_surface(self.image)
    
    #Metodo para atirar
    #O método atirar recebe o grupo de balas, o modo assistente e o alvo (se houver)
    #Se o modo assistente estiver ativo, o tanque mira automaticamente no alvo
    #Se o modo assistente não estiver ativo, o tanque atira na direção do ângulo atual

    def atirar(self, balas_grupo, modo_assistente=False, alvo=None):
        #Se o tanque pode atirar (tempo de recarga) e está vivo
        if self.pode_atirar >= 30 and self.vivo:

            #Se o modo assistente estiver ativo e houver um alvo, calcula o ângulo para o alvo

            if modo_assistente and alvo:
                # Mira assistida - calcula ângulo para o alvo
                # Calcula a diferença entre a posição do tanque e a posição do alvo
                dx = alvo.x - self.x
                dy = alvo.y - self.y
                #Usa um pouco de trigonometria para calcular o ângulo, como?
                #Bem, já sabendo o delta x e delta y, podemos achar o angulo que forma a tangente, que é o menor segmento de reta que liga o tanque ao alvo
                #A tangente é dada por tan(angulo) = dy/dx
                #Portanto, o ângulo é dado por arctan(dy/dx) = angulo
                #O método math.atan2(dy, dx) retorna o ângulo em radianos
                #O ângulo é calculado em radianos, mas depois é convertido para graus
                angulo_tiro = math.degrees(math.atan2(dy, dx))

            #Se não estiver no modo assistente, o tanque atira na direção do ângulo atual
            else:
                angulo_tiro = self.angulo
            
            #Converte o ângulo para radianos para o cálculo da posição do projétil
            angulo_rad = math.radians(angulo_tiro)

            # Calcula a posição do canhão do tanque

            distancia_canhao = settings.LARGURA_TANQUE / 2
            # A posição do canhão é calculada a partir da posição do tanque e do ângulo
            # A posição do canhão é a posição do tanque mais a distância do canhão multiplicada pelo cosseno e seno do ângulo atual
            # Isso é feito para que o projétil saia da ponta do canhão do tanque
            pos_x = self.x + math.cos(angulo_rad) * distancia_canhao
            pos_y = self.y + math.sin(angulo_rad) * distancia_canhao

            # Cria uma instancia do projetil com a posição do canhão, o ângulo de tiro e o ID do jogador
            # O ID do jogador é usado para identificar de quem é a bala, para verificar colisões depois
            # A bala é adicionada ao grupo de balas
            bala = Projetil(pos_x, pos_y, angulo_tiro, self.jogador_id)
            balas_grupo.add(bala)

            # Toca o som de tiro
            som_tiro.play()

            # Caso o tanque não esteja no modo assistente, ativa o recuo
            if not modo_assistente:
                # Ativa o recuo do tanque
                self.recuo_ativo = 8

            # Reseta o tempo de recarga do tanque
            self.pode_atirar = 0

    # Método para atualizar o tanque
    # recebe o grupo de balas, o modo assistente e o alvo (se houver)
    def update(self, balas_grupo, modo_assistente=False, alvo=None):
        # Ve se alguma tecla está pressionada e a atribui para a variável teclas
        teclas = pygame.key.get_pressed()

        # Chama o método mover do tanque, passando as teclas e o modo assistente
        self.mover(teclas, modo_assistente)
        
        # Se a tecla de atirar estiver pressionada, chama o método atirar do tanque
        if teclas[self.controles['atirar']]:
            # passa o grupo de balas, o modo assistente e o alvo (se houver)
            self.atirar(balas_grupo, modo_assistente, alvo)
        
        # Caso o tanque esteja recarregando o tiro, aumenta o valor de pode_atirar
        if self.pode_atirar < 30:
            self.pode_atirar += 1

    # Método para matar o tanque
    def morrer(self):
        self.vivo = False

    # Metodo que diminui a vida do tanque
    def levar_dano(self):
        #Para o modo assistente - diminui uma vida
        self.vidas -= 1
        if self.vidas <= 0:
            self.morrer()

    #Metodo para resetar o tanque
    def reset(self):
        self.velocidade_recuo = settings.VELOCIDADE_RECUO
        self.velocidade = settings.VELOCIDADE_TANQUE
        self.x = self.pos_inicial_x
        self.y = self.pos_inicial_y
        self.angulo = self.angulo_inicial
        self.vivo = True
        self.vidas = 3
        self.pode_atirar = 30
        self.recuo_ativo = 0
        self.image = self.original_image

#Classe Projetil
#Representa a bala que o tanque atira
class Projetil(pygame.sprite.Sprite):
    #Construtor da classe Projetil
    def __init__(self, x, y, angulo, jogador_id):
        #Construtor da classe Sprite
        super().__init__()
        
        # carrega a imagem da bala
        if jogador_id==1:
            self.image = pygame.image.load("imagens//bala_verde.png").convert_alpha()
        else:
            self.image = pygame.image.load("imagens//bala_azul.png").convert_alpha()
        
        # Rotaciona a imagem da bala conforme o ângulo
        self.image = pygame.transform.rotate(self.image, -angulo)

        # Define o retângulo da imagem da bala
        self.rect = self.image.get_rect(center=(x, y))

        # Define a velocidade da bala, o ângulo e a posição inicial
        self.velocidade = settings.VELOCIDADE_PROJETIL
        self.angulo = angulo
        self.x = x
        self.y = y

        # Define o ID do jogador que atirou a bala
        # Isso é importante para verificar colisões depois
        self.jogador_id = jogador_id

        # Cria uma máscara para colisões
        # A máscara é usada para verificar colisões entre a bala e os tanques, entre balas e balas
        self.mask = pygame.mask.from_surface(self.image)

    # Método para mover a bala
    def mover(self):
        angulo_rad = math.radians(self.angulo)
        # Entra aquela mesma história da tangente, lá do tanque, só que aqui o movimento é fixo 
        # para o angulo da bala, dado que pelo tanque
        self.x += math.cos(angulo_rad) * self.velocidade
        self.y += math.sin(angulo_rad) * self.velocidade
        self.rect.center = (self.x, self.y)

        # retangulo da tela para verificar se a bala saiu da tela
        tela_rect = pygame.Rect(0, 0, settings.LARGURA, settings.ALTURA)
        
        # Se bala sai do retangulo da tela(para de colidir com a tela), remove do grupo
        if not self.rect.colliderect(tela_rect):
            #Som da explosão
            som_explosao.play()
            self.kill()

    # Método para atualizar a bala
    def update(self):
        self.mover()

# ==============================================================================
# --- FUNÇÕES AUXILIARES E DE INTERFACE ---
# ==============================================================================

def verificar_colisoes_bala_bala(balas_grupo):
    """
    Verifica colisões entre balas de jogadores diferentes
    e remove ambas as balas se colidirem
    """
    # Converte o grupo de balas em uma lista para evitar problemas de modificação durante a iteração
    # Isso é necessário porque o pygame não permite modificar um grupo enquanto itera sobre ele
    balas_lista = list(balas_grupo)
    
    # Loop duplo para verificar colisões entre todas as balas diferentes
    for i in range(len(balas_lista)):
        for j in range(i + 1, len(balas_lista)):
            bala1 = balas_lista[i]
            bala2 = balas_lista[j]
            
            # Só verifica colisão entre balas de jogadores diferentes
            if bala1.jogador_id != bala2.jogador_id:
                # Verifica se ainda estão no grupo (não foram removidas)
                if bala1 in balas_grupo and bala2 in balas_grupo:
                    if pygame.sprite.collide_mask(bala1, bala2):
                        #Som da explosão
                        som_explosao.play()
                        # Remove ambas as balas
                        bala1.kill()
                        bala2.kill()
                        break  # Sai do loop interno
    
def verificar_colisoes_bala_tanque(balas_grupo, tanques_grupo, modo_assistente=False):
    '''
    Verifica colisões entre balas e tanques
    Se uma bala colide com um tanque, a bala é removida e o tanque leva dano ou morre
    '''
    balas_lista = list(balas_grupo)
    tanques_lista = list(tanques_grupo)
    # Loop por cada bala no grupo de balas
    for bala in balas_lista:
        # loop por cada tanque no grupo de tanques
        for tanque in tanques_lista:
            # Verifica se a bala não é do mesmo jogador do tanque e se o tanque está vivo
            if bala.jogador_id != tanque.jogador_id and tanque.vivo:
                # Verifica se a bala colide com o tanque usando a máscara
                if pygame.sprite.collide_mask(bala, tanque):
                    #Som da explosão
                    som_explosao.play()
                    # Remove a bala do grupo
                    bala.kill()
                    # Se o modo assistente estiver ativo, o tanque leva dano
                    if modo_assistente:
                        tanque.levar_dano()
                        # Verifica se ainda há tanques vivos
                        if tanque.vidas <= 0:
                            return bala.jogador_id  # Retorna o ID do jogador que venceu (o que atirou)
                    # Se não estiver no modo assistente, o tanque morre
                    else:
                        tanque.morrer()
                        return bala.jogador_id  # Retorna o ID do jogador que venceu (o que atirou)
    # Se não houver colisões, retorna None
    return None

# Funções de desenho para a interface do jogo
# Essas funções são usadas para desenhar textos, botões e HUD na tela

def desenhar_texto(surface, texto, tamanho, x, y, cor=settings.BRANCO, font_name=None):
    font = pygame.font.Font(font_name, tamanho)
    text_surface = font.render(texto, True, cor)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def desenhar_botao(surface, rect, texto):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        cor_fundo = settings.COR_BOTAO_HOVER
    else:
        cor_fundo = settings.CINZA
    
    pygame.draw.rect(surface, cor_fundo, rect, border_radius=10)
    desenhar_texto(surface, texto, 40, rect.centerx, rect.centery, settings.PRETO)

def desenhar_hud(modo_assistente=False):
    if modo_assistente:
        # Jogador 1 - lado esquerdo superior
        desenhar_texto(tela, "Jogador 1", 30, 100, 20, settings.VERDE)
        desenhar_texto(tela,"WS | Espaço",30, 100, 50, settings.VERDE)
        desenhar_coracoes(tanque1, 60, 80)
        
        # Jogador 2 - lado direito superior  
        desenhar_texto(tela, "Jogador 2", 30, settings.LARGURA - 100, 20, settings.AZUL)
        desenhar_texto(tela,"Setas | Enter",30, settings.LARGURA - 100, 50, settings.AZUL)
        desenhar_coracoes(tanque2, settings.LARGURA - 140, 80)
    else:
        # Jogador 1 - lado esquerdo superior
        desenhar_texto(tela, "Jogador 1", 30, 80, 25, settings.VERDE)
        desenhar_texto(tela,"WASD | Espaço",30, 80,55, settings.VERDE)

        #Jogador 2 - lado direito superior
        desenhar_texto(tela, "Jogador 2", 30, settings.LARGURA - 80, 25, settings.AZUL)
        desenhar_texto(tela,"Setinhas | Enter", 30, settings.LARGURA - 80, 55, settings.AZUL)

def desenhar_coracoes(tanque, x, y):
    """Desenha os corações representando as vidas do tanque"""
    # Desenha 3 corações, um para cada vida do tanque
    for i in range(3):
        # se o i for menor que o número de vidas do tanque, desenha um coração vermelho
        # se não, desenha um coração cinza
        if i<tanque.vidas:
            cor = settings.VERMELHO
        else:
            cor = settings.CINZA
        # separa a posição do coração, no eixo x, de acordo com o i
        coracao_x = x + (i * 35)
        # Desenha um coração simples usando círculos e triângulo
        pygame.draw.circle(tela, cor, (coracao_x, y), 10)
        pygame.draw.circle(tela, cor, (coracao_x + 10, y), 10)
        pygame.draw.polygon(tela, cor, [(coracao_x - 10, y + 5), (coracao_x + 20, y + 5), (coracao_x + 5, y + 20)])

#Função para reiniciar o jogo
def reiniciar_jogo(modo_assistente=False):
    # Esvazia o grupo de balas 
    balas_sprites.empty()
    
    #Reseta os tanques para suas posições iniciais
    tanque1.reset()
    tanque2.reset()

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
pygame.mixer.music.set_volume(settings.VOLUME) # 30% do volume máximo
pygame.mixer.music.play(-1)

# Carrega os efeitos sonoros
som_tiro = pygame.mixer.Sound("audios//som_tiro.mp3")  # ou .mp3
som_explosao = pygame.mixer.Sound("audios//som_explosao.mp3")  # ou .mp3

# Ajusta o volume dos efeitos sonoros (opcional)
som_tiro.set_volume(settings.VOLUME+0.3)  # 60% do volume máximo
som_explosao.set_volume(settings.VOLUME+0.3)  # 60% do volume máximo

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
            # Verifica a posição do mouse para clicar nos botões
            mouse_pos = pygame.mouse.get_pos()
            if estado_jogo == "MENU":
                # Verifica se o mouse clicou em algum dos botões do menu
                # Se o mouse clicou no botão de iniciar, muda o estado do jogo para JOGO_PRINCIPAL
                # e desativa o modo assistente, que é o modo onde os tanques não miram
                if btn_iniciar_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    modo_assistente = False
                    reiniciar_jogo(modo_assistente)
                # Se o mouse clicou no botão de assistente, muda o estado do jogo para JOGO_PRINCIPAL
                # e ativa o modo assistente, que é o modo onde os tanques miram
                elif btn_assistente_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    modo_assistente = True
                    # Mantém a tela normal para o modo vertical
                    reiniciar_jogo(modo_assistente)
                # Se o mouse clicou no botão de sair, encerra o jogo
                elif btn_sair_rect.collidepoint(mouse_pos):
                    rodando = False
            elif estado_jogo == "FIM_DE_JOGO":
                # Verifica se o mouse clicou em algum dos botões de fim de jogo
                # Se o mouse clicou no botão de jogar novamente, muda o estado do jogo para JOGO_PRINCIPAL
                # e reinicia o jogo no modo assistente ou não, dependendo do estado do modo_assistente
                if btn_jogar_novamente_rect.collidepoint(mouse_pos):
                    estado_jogo = "JOGO_PRINCIPAL"
                    reiniciar_jogo(modo_assistente)
                # Se o mouse clicou no botão de voltar ao menu, muda o estado do jogo para MENU
                # e desativa o modo assistente, que é o modo onde os tanques não miram
                elif btn_voltar_menu_rect.collidepoint(mouse_pos):
                    estado_jogo = "MENU"
                    modo_assistente = False

    # --- Lógica de cada estado do Jogo ---
    if estado_jogo == "MENU":
        # Desenha o fundo do menu
        tela.fill(settings.COR_FUNDO_MENU)
        # Desenha os botões do menu
        desenhar_texto(tela, "Batalha de Tanques", 100, settings.LARGURA / 2, settings.ALTURA / 4, settings.AMARELO)
        desenhar_botao(tela, btn_iniciar_rect, "Jogo Principal")
        desenhar_botao(tela, btn_assistente_rect, "Assistente de Mira")
        desenhar_botao(tela, btn_sair_rect, "Sair")

    elif estado_jogo == "JOGO_PRINCIPAL":
        tela.blit(chao_principal, (0, 0))
        
        if modo_assistente:
            # No modo assistente, os tanques miram automaticamente um no outro
            #Por isso, é passa o modo_assistente e o alvo (o outro tanque) para o método update dos tanques
            tanque1.update(balas_sprites, modo_assistente, tanque2)
            tanque2.update(balas_sprites, modo_assistente, tanque1)
            balas_sprites.update()
        else:
            # No modo normal, os tanques se movem e atiram normalmente
            # Por isso, não precisa passar o modo_assistente e o alvo para o método update dos tanques
            # ai faz o update do sprite dos tanques e balas
            tanques_sprites.update(balas_sprites)
            balas_sprites.update()
        
        # Verifica colisões entre balas e tanques
        verificar_colisoes_bala_bala(balas_sprites)
        
        # Verifica colisões entre balas e tanques
        # Se houver um vencedor, o estado do jogo muda para FIM_DE_JOGO
        # Caso não haja um vencedor, ou seja, vencedor for None, o jogo continua normalmente
        vencedor = verificar_colisoes_bala_tanque(balas_sprites, tanques_sprites, modo_assistente)
        if vencedor is not None:
            estado_jogo = "FIM_DE_JOGO"
        # Desenha o HUD (Heads-Up Display) com as informações dos tanques
        # Desenha os tanques e as balas na tela
        desenhar_hud(modo_assistente)
        tanques_sprites.draw(tela)
        balas_sprites.draw(tela)
        
    elif estado_jogo == "FIM_DE_JOGO":
        # Continua desenhando o jogo no fundo
        tela.blit(chao_principal, (0, 0))
        desenhar_hud(modo_assistente)

        #Deixa os tanques parados
        if not tanque1.vivo:
            tanque2.velocidade = 0
            tanque2.pode_atirar = 0
        else:
            tanque1.velocidade = 0
            tanque1.pode_atirar = 0
        # Atualiza os tanques para mostrar imagem de morto
        tanques_sprites.update(balas_sprites)
        balas_sprites.update()

        # Desenha os tanques e as balas na tela
        tanques_sprites.draw(tela)
        balas_sprites.draw(tela)

        # Sobreposição escura
        sobreposicao = pygame.Surface((settings.LARGURA, settings.ALTURA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 180))
        tela.blit(sobreposicao, (0, 0))

        # Mensagens e botões
        if vencedor == 1:
            cor_vencedor = settings.VERDE
        else: 
            cor_vencedor = settings.AZUL
        # Desenha o texto de fim de jogo e o vencedor
        desenhar_texto(tela, "Fim de Jogo", 100, settings.LARGURA / 2, settings.ALTURA / 4, settings.BRANCO)
        desenhar_texto(tela, f"Jogador {vencedor} Venceu!", 60, settings.LARGURA / 2, settings.ALTURA / 2 - 50, cor_vencedor)
        # Desenha os botões de jogar novamente e voltar ao menu
        desenhar_botao(tela, btn_jogar_novamente_rect, "Jogar Novamente")
        desenhar_botao(tela, btn_voltar_menu_rect, "Voltar ao Menu")

    # --- Atualização Final da Tela ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()