# Jogo do Flappy Bird com Inteligência Artificial

## Descrição

Este jogo é um clone do Flappy Bird, um jogo simples e viciante em que o jogador controla um pássaro que deve voar e passar entre canos. O jogo foi implementado em Python usando a biblioteca Pygame.

## Estrutura da aplicação

A aplicação é dividida em 4 arquivos principais:

•*bird.py:* Contém a classe Bird que representa o pássaro no jogo, com seus atributos e métodos para movimento, animação e colisão.

•*pipe.py:* Contém a classe Pipe que representa os canos, com seus atributos e métodos para movimento e colisão.

•*ground.py:* Contém a classe Ground que representa o chão do jogo, com seus métodos para movimento e desenho.

•*main.py:* Este arquivo contém o código principal do jogo, responsável por:

1. *Inicializar o Pygame e carregar as imagens.*
2. *Definir as constantes do jogo (largura, altura, velocidade, etc.).*
3. *Criar as instâncias de Bird, Pipe e Ground.*
4. *Implementar a lógica principal do jogo, incluindo:*
     * *Movimentação dos objetos.*
     * *Detecção de colisões.*
     * *Desenho na tela.*
     * *Controle da IA (se estiver ativada).*
     * *Atualização de pontuação.*

## Tecnologias utilizadas

•*Python:* linguagem de programação utilizada para implementar o jogo.

•*Pygame:* biblioteca gráfica utilizada para desenhar os gráficos do jogo.

•*NEAT:* biblioteca de inteligência artificial utilizada para treinar o modelo de inteligência artificial do jogo.

## Inteligência Artificial

O jogo também pode ser usado para treinar um modelo de inteligência artificial para jogar o Flappy Bird. O modelo de inteligência artificial é treinado usando um algoritmo genético, que é uma técnica de aprendizado de máquina que simula o processo de evolução natural.

### NEAT

O NEAT (NeuroEvolution of Augmenting Topologies) é um algoritmo genético específico para redes neurais. Ele é projetado para criar redes neurais complexas que são capazes de aprender tarefas difíceis.

O NEAT funciona da seguinte forma:

1. Uma população inicial de redes neurais é gerada aleatoriamente.
2. Cada rede neural é avaliada em uma tarefa.
3. As redes neurais com o melhor desempenho são selecionadas para reprodução.
4. As redes neurais filhas são geradas cruzando os genes das redes neurais pais.
5. As redes neurais filhas são submetidas a mutações aleatórias.
6. O processo é repetido várias vezes, até que uma rede neural seja capaz de realizar a tarefa com sucesso.

### Características dos pássaros

Os pássaros são representados por um conjunto de genes, que determinam suas características, como:

•A altura do salto
•A velocidade de voo
•A sensibilidade ao controle do jogador

## Conclusão

A inteligência artificial é uma ferramenta poderosa que pode ser usada para criar jogos mais desafiadores e envolventes. Este jogo é um exemplo de como a IA pode ser usada para criar um jogo simples, mas viciante.