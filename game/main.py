import neat
import pygame
import os
from game.bird import Passaro
from game.pipe import Cano
from game.ground import Chao

ai_jogando = True
geracao = 0

# Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800

# Inicialização do pygame
pygame.init()
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs', 'bg.png')))

# Fonte
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('comicsans', 40)

# Função para carregar imagens
def carregar_imagem(nome, escala):
    return pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', nome)))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))
    chao.desenhar(tela)
    pygame.display.update()

def main(genomas, config): #fitness function -> precisa dizer qual passaro esta indo melhor ou pior
    global geracao
    geracao += 1

    if ai_jogando:
        redes_neurais = []
        lista_genomas = []
        passaros = []

        for _, genoma in genomas:
            rede_neural = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes_neurais.append(rede_neural)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        indice_cano = 0
        if len(passaros) > 0:
            #descobrir qual cano olhar
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        #mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            #aumentar um pouquinho a fitness do passaro
            lista_genomas[i].fitness += 0.1
            output = redes_neurais[i].activate((passaro.y,
                                                abs(passaro.y - canos[indice_cano].altura),
                                                abs(passaro.y - canos[indice_cano].pos_base))) #ativa a rede neural
            # -1 e 1 -> se o output for > 0.5 então o passaro pula
            if output[0] > 0.5:
                passaro.pular()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes_neurais.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            if ai_jogando:
                for genoma in lista_genomas:
                    genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    lista_genomas.pop(i)
                    redes_neurais.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)
    populacao = neat.Population(config)

    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)

if __name__ == '__main__':
    caminho_config = os.path.join('../', 'config.txt')
    rodar(caminho_config)