import pygame
import sys

pygame.init()

largura, altura = 400, 200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Janela com Botão")

branco = (255, 255, 255)
cinza = (200, 200, 200)
preto = (0, 0, 0)

sprite_sheet = pygame.image.load("Walk.png").convert_alpha()
num_quadros = 12
quadro_largura = sprite_sheet.get_width() // num_quadros
quadro_altura = sprite_sheet.get_height()

quadros = [sprite_sheet.subsurface((i * quadro_largura, 0, quadro_largura, quadro_altura)) for i in range(num_quadros)]

def desenha_botao(tela, cor, pos, tamanho, texto):
    fonte = pygame.font.Font(None, 36)
    pygame.draw.rect(tela, cor, (pos[0], pos[1], tamanho[0], tamanho[1]))
    texto_surface = fonte.render(texto, True, preto)
    texto_rect = texto_surface.get_rect(center=(pos[0] + tamanho[0] // 2, pos[1] + tamanho[1] // 2))
    tela.blit(texto_surface, texto_rect)

def verifica_colisao_com_borda(sprite_rect, tela_largura, tela_altura):
    if sprite_rect.left < 0:
        sprite_rect.left = 0
    if sprite_rect.right > tela_largura:
        sprite_rect.right = tela_largura
    if sprite_rect.top < 0:
        sprite_rect.top = 0
    if sprite_rect.bottom > tela_altura:
        sprite_rect.bottom = tela_altura
    return sprite_rect

def verifica_colisao_com_botao(sprite_rect, botao):
    if sprite_rect.colliderect(botao):
        return True
    return False

largura_botao, altura_botao = 100, 50
x_botao = largura - largura_botao - 10  
y_botao = altura - altura_botao - 10
botao = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)

indice_quadro = 0
tempo_animacao = 50 
ultimo_tempo = pygame.time.get_ticks()

pos_x = 10
pos_y = 10
movimento = 2
virado_para_esquerda = False

clock = pygame.time.Clock()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao.collidepoint(evento.pos):
                rodando = False

    teclas = pygame.key.get_pressed()
    mover = False

    sprite_rect = pygame.Rect(pos_x, pos_y, quadro_largura, quadro_altura)

    nova_pos_x = pos_x
    nova_pos_y = pos_y

    if teclas[pygame.K_RIGHT]:
        nova_pos_x += movimento
        virado_para_esquerda = False
        mover = True
    if teclas[pygame.K_LEFT]:
        nova_pos_x -= movimento
        virado_para_esquerda = True
        mover = True
    if teclas[pygame.K_UP]:
        nova_pos_y -= movimento
        mover = True
    if teclas[pygame.K_DOWN]:
        nova_pos_y += movimento
        mover = True

    novo_rect = pygame.Rect(nova_pos_x, nova_pos_y, quadro_largura, quadro_altura)

    novo_rect = verifica_colisao_com_borda(novo_rect, largura, altura)

    if not verifica_colisao_com_botao(novo_rect, botao):
        pos_x, pos_y = novo_rect.topleft

    agora = pygame.time.get_ticks()
    if mover and agora - ultimo_tempo > tempo_animacao:
        indice_quadro = (indice_quadro + 1) % num_quadros
        ultimo_tempo = agora

    tela.fill(branco)

    sprite = quadros[indice_quadro]
    if virado_para_esquerda:
        sprite = pygame.transform.flip(sprite, True, False)
    tela.blit(sprite, (pos_x, pos_y))

    desenha_botao(tela, cinza, botao.topleft, botao.size, "Sair")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
