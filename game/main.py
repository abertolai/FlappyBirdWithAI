import neat
import pygame
import os
from game.bird import Bird
from game.pipe import Pipe
from game.ground import Ground

ai_playing = False
generation = 0

# Constantes
WIDTH_SCREEN = 500
HEIGHT_SCREEN = 800
FPS = 30

# Inicialização do pygame
pygame.init()
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs', 'bg.png')))

# Fonte
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('comicsans', 40)

def draw_screen(screen, birds, pipes, ground, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)
    text = POINTS_FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH_SCREEN - 10 - text.get_width(), 10))

    if ai_playing:
        text = POINTS_FONT.render(f"Geração: {generation}", 1, (255, 255, 255))
        screen.blit(text, (10, 10))
    ground.draw(screen)
    pygame.display.update()

def main(genomas, config): #fitness function -> precisa dizer qual bird esta indo melhor ou pior
    global generation
    generation += 1

    if ai_playing:
        neural_networks = []
        list_genomas = []
        birds = []

        for _, genoma in genomas:
            rede_neural = neat.nn.FeedForwardNetwork.create(genoma, config)
            neural_networks.append(rede_neural)
            genoma.fitness = 0
            list_genomas.append(genoma)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]
    ground = Ground(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        #interação com o usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if not ai_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        index_pipe = 0
        if len(birds) > 0:
            #descobrir qual pipe olhar
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                index_pipe = 1
        else:
            running = False
            break

        #mover as coisas
        for i, bird in enumerate(birds):
            bird.move()

            if ai_playing:
                #aumentar um pouquinho a fitness do bird
                list_genomas[i].fitness += 0.1
                output = neural_networks[i].activate((bird.y,
                                                    abs(bird.y - pipes[index_pipe].height),
                                                    abs(bird.y - pipes[index_pipe].pos_base))) #ativa a rede neural
                # -1 e 1 -> se o output for > 0.5 então o bird pula
                if output[0] > 0.5:
                    bird.jump()
        ground.move()

        add_pipe = False
        remove_pipe = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    if ai_playing:
                        list_genomas[i].fitness -= 1
                        list_genomas.pop(i)
                        neural_networks.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True

            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipe.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
            if ai_playing:
                for genoma in list_genomas:
                    genoma.fitness += 5

        for pipe in remove_pipe:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0:
                birds.pop(i)
                if ai_playing:
                    list_genomas.pop(i)
                    neural_networks.pop(i)

        draw_screen(screen, birds, pipes, ground, points)

def run(path_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                path_config)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    if ai_playing:
        population.run(main, 50)
    else:
        main(None, None)

if __name__ == '__main__':
    path_config = os.path.join('../', 'config.txt')
    run(path_config)