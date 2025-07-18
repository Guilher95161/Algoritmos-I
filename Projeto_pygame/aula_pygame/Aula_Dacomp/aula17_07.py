import pygame
#sempre deve fazer isso
pygame.init()
#Tamanho tela
screen = pygame.display.set_mode((800,600))
#FPS
clock = pygame.time.Clock()

#Fonte
font = pygame.font.SysFont("Arial",50)
texto_surface = font.render("Corra!",False,"Red")
#Surfaces
surfaceTeste = pygame.Surface((200,200))
surfaceTeste.fill("Red")
sky = pygame.image.load("sky.png").convert_alpha()
ground = pygame.image.load("ground.png").convert_alpha()
#Loop Principal
while True:
    #Manipulador de eventos
    for event in pygame.event.get():
        #Captura cada tipo de evento

        #Evento de saída
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(surfaceTeste,(0,0))
    screen.blit(texto_surface,(350,50))
    pygame.display.update()
    clock.tick(60)