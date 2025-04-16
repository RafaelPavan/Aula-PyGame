import pygame
import sys
from collections import deque

pygame.init()

largura, altura = 600, 200
tela = pygame.display.set_mode((largura, altura))

fundo = pygame.image.load("background.jpg").convert()
fundo = pygame.transform.scale(fundo, (largura, altura))
pygame.display.set_caption("Janela com Fila de Animações")

x_fundo = 0
velocidade_fundo = 1
fundo_em_movimento = False  

branco = (255, 255, 255)
cinza = (200, 200, 200)
preto = (0, 0, 0)


animacoes = {}

def carregar_animacao(nome, caminho, num_quadros, corte_y=52, tempo=100):
    sprite_sheet = pygame.image.load(caminho).convert_alpha()
    largura_quadro = sprite_sheet.get_width() // num_quadros
    altura_quadro = sprite_sheet.get_height()
    
    quadros = [
        sprite_sheet.subsurface((i * largura_quadro, corte_y, largura_quadro, altura_quadro - corte_y))
        for i in range(num_quadros)
    ]
    animacoes[nome] = {
        "quadros": quadros,
        "tempo": tempo
    }

carregar_animacao("idle", "Idle.png", 9)
carregar_animacao("dialogue", "Dialogue.png", 11)
carregar_animacao("attack", "Attack.png", 8)
carregar_animacao("walk", "Walk.png", 12)
carregar_animacao("book", "Book.png", 10, corte_y=0)


fila_animacoes = deque()
animacao_atual = "idle"
indice_quadro = 0
ultimo_tempo = pygame.time.get_ticks()


largura_botao, altura_botao = 100, 50
x_botao = largura - largura_botao - 10
y_botao = altura - altura_botao - 10

def desenha_botao(tela, cor, pos, tamanho, texto):
    fonte = pygame.font.Font(None, 36)
    pygame.draw.rect(tela, cor, (pos[0], pos[1], tamanho[0], tamanho[1]))
    texto_surface = fonte.render(texto, True, preto)
    texto_rect = texto_surface.get_rect(center=(pos[0] + tamanho[0] // 2, pos[1] + tamanho[1] // 2))
    tela.blit(texto_surface, texto_rect)


def tocar_animacao(nome, substituir=False):
    if substituir:
        fila_animacoes.clear()
    fila_animacoes.append(nome)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:

            if botao.collidepoint(evento.pos):
                tocar_animacao("dialogue")
                tocar_animacao("walk")
                tocar_animacao("attack")
                tocar_animacao("book")
                tocar_animacao("idle")  
                
    
    if fundo_em_movimento:
        x_fundo -= velocidade_fundo

        
        if x_fundo <= -largura:
            x_fundo = 0

    tela.blit(fundo, (x_fundo, 0))  
    tela.blit(fundo, (x_fundo + largura, 0))  

    agora = pygame.time.get_ticks()
    anim_data = animacoes[animacao_atual]

    if agora - ultimo_tempo > anim_data["tempo"]:
        indice_quadro += 1
        if indice_quadro >= len(anim_data["quadros"]):
            if fila_animacoes:
                proxima = fila_animacoes.popleft()
                
                if proxima == "walk":
                    fundo_em_movimento = True
                
                if proxima == "attack":
                    fundo_em_movimento = False

                if proxima == "book":
                    fundo_em_movimento = True
                
                if proxima == "idle":
                    fundo_em_movimento = False

                animacao_atual = proxima
                indice_quadro = 0
            else:
                animacao_atual = "idle"
                indice_quadro = 0
        ultimo_tempo = agora

    y_chao = 150
    tela.blit(animacoes[animacao_atual]["quadros"][indice_quadro], (10, 82))

    botao = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)
    desenha_botao(tela, cinza, botao.topleft, botao.size, "Ação")

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
