# PySnake Teste 1 com lib curses

import curses
import time
import random
import time

# método para criar a borda da tela
def draw_screen(window):
    window.clear()
    window.border(0)

# método para criar o personagem
def draw_actor(actor, window, char):
    try:
        window.addch(actor[0], actor[1], char) # Pensonagem
    except curses.error:
        pass  # evita crash em terminais pequenos

# método para desenhar snake
def draw_snake(snake, window):
    #cabeça de um jeito
    head = snake[0]
    draw_actor(actor=head, window=window, char="@")

    # corpo de outro
    body = snake[1:]

    for body_part in body:
        draw_actor(actor=body_part, window=window, char="s")


# método para definir a direção do personagem
def get_new_direction(window, timeout):
    window.timeout(timeout)
    direction = window.getch()

    if direction in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        return direction
    else:
        return None

# método para mover o personagem de posição
def mover_actor(actor, direction):
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_RIGHT:
            actor[1] += 1
        case _: # Pessoa não apertou a tecla ou apertou outra tecla
            pass

# método para mover a snake
def move_snake(snake, direction, snake_ate_fruit):
    head = snake[0].copy()
    mover_actor(actor=head, direction=direction)
    snake.insert(0, head)
    # se não comeu a fruta, então remove. Caso coma a Fruta, a snake aumenta de tamanho
    if not snake_ate_fruit:
        snake.pop()

# método que verifica se o personagem bateu nas bordas
def actor_hit_borders(actor, window):

    # altura e largura
    height, width = window.getmaxyx()

    # se se personagem está fora do eixo Y
    if (actor[0]<= 0) or (actor[0]>= height-1):
        return True
    # se se personagem está fora do eixo X
    if (actor[1]<= 0) or (actor[1]>= width-1):
        return True
    
    return False

# método testa se apenas a cabeça da snake bateu nas bordas
def snake_hit_borders(snake, window):
    head = snake[0]
    return actor_hit_borders(actor=head, window=window)

# método de criação da fruta para a snake comer
def get_new_fruit(window, snake):
    # altura e largura
    height, width = window.getmaxyx()
    # para evitar que a fruta nasça em cima da snake
    while True:
        fruit = [random.randint(1, height-2), # valor aleatório para eixo Y
            random.randint(1, width-2) # valor aleatório para eixo X
            ]
        if fruit not in snake:
            return fruit

# Método testa se apenas a cabeça da snake bateu na Fruta para comer e gerar uma nova
def snake_hit_fruit(snake, fruit):
    return fruit in snake

# método testa se a snake bateu nela mesma
def snake_hit_itself(snake):
    head = snake[0]
    body = snake[1:]
    return head in body

# método testa se a snake está indo na direção oposta
def direction_is_opposite(direction, current_direction):
    match direction:
        case curses.KEY_UP:
            return current_direction == curses.KEY_DOWN
        case curses.KEY_DOWN:
            return current_direction == curses.KEY_UP
        case curses.KEY_LEFT:
            return current_direction == curses.KEY_RIGHT
        case curses.KEY_RIGHT:
            return current_direction == curses.KEY_LEFT
        case _: # Pessoa não apertou a tecla ou apertou outra tecla
            return False

# mostra placar
def draw_score(window, score):
    try:
        window.addstr(0, 2, f" Pontos: {score} ")
    except curses.error:
        pass

# Método finaliza o jogo exibindo a pontuação
def finish_game(score, window):
    height, width = window.getmaxyx()
    s = f'Você perdeu! Mas comeu {score} frutas!!' # mensagem para o usuário

    #posicionamento na tela da mensagem para o usuário
    y = int(height/2)
    x = int((width - len(s))/2) # ideia é centralizar o texto
    try:
        window.addstr(y, x, s)
        window.refresh()
    except curses.error:
        pass
    time.sleep(2)

# método principal do jogo snake
def game_loop(window, game_speed):
    # limpa a tela no início
    window.clear()
    # setup inicial
    curses.curs_set(0) # faz com que o cursor não apareceça

    # nosso personagem
    snake = [ 
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15],
    ]

    # criação da fruta para a snake comer
    fruit = get_new_fruit(window=window, snake=snake)
    current_direction = curses.KEY_DOWN # Direção inicial do personagem
    snake_ate_fruit = False # inicia que não comeu a fruta
    score = 0 # pontuação, quantas frutas a snake comeu
   
    while True:
        draw_screen(window=window)
        draw_snake(snake=snake, window=window) # cria a snake
        draw_actor(actor=fruit, window=window, char=curses.ACS_DIAMOND) # cria a fruta na tela
        draw_score(window, score)
        
        direction = get_new_direction(window=window, timeout=game_speed)

        # se direção None, assume a direção corrente
        if direction is None:
            direction = current_direction

        # testa se a snake está indo na direção oposta
        if direction_is_opposite(direction=direction, current_direction=current_direction):
            """
            Faz com que a snake não vá na direção oposta
            segue a direção anterior
            """
            direction = current_direction 
        
        #sempre move o personagem
        move_snake(snake=snake, direction=direction, snake_ate_fruit=snake_ate_fruit)

        # testa se apenas a cabeça da snake bateu nas bordas
        if snake_hit_borders(snake=snake, window=window):
            break
        
        # testa se a snake bateu nela mesma
        if snake_hit_itself(snake=snake):
            break

        # testa se apenas a cabeça da snake bateu na Fruta para comer e gerar uma nova
        if snake_hit_fruit(snake=snake, fruit=fruit):
            snake_ate_fruit = True
            fruit = get_new_fruit(window=window, snake=snake)
            score += 1 # conta a fruta que a snake comeu
            game_speed = max(30, game_speed - 5)  # aumenta velocidade
        else:
            snake_ate_fruit = False
        
        #atualiza a direção corrente
        current_direction = direction

    # finaliza o jogo exibindo a pontuação
    finish_game(score=score, window=window)

def select_difficulty():
    difficulty = {
        '1': 1000,
        '2': 500,
        '3': 250,
        '4': 125,
        '5': 60,
    }
    while True:
        aswer = input('Selecione a dificuldade de 1 à 5:')
        game_speed = difficulty.get(aswer)
        if game_speed is not None:
            return game_speed
        print('Opção inválida!')

if __name__ == "__main__":
    curses.wrapper(game_loop, game_speed=select_difficulty())


