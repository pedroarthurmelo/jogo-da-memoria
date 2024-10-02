import turtle
import random
import time


# Função para criar a matriz principal e a matriz de exibição de acordo com a dificuldade
def criar_matriz(dificuldade):
    if dificuldade == 1:
        tamanho = 4
    elif dificuldade == 2:
        tamanho = 6
    elif dificuldade == 3:
        tamanho = 8

    # Gera as letras e embaralha
    letras = [chr(i) for i in range(65, 65 + (tamanho * tamanho) // 2)] * 2
    for i in range(len(letras) - 1, 0, -1):
        j = random.randint(0, i)
        letras[i], letras[j] = letras[j], letras[i]

    # Cria a matriz principal e a matriz de exibição
    mat = [[letras.pop() for _ in range(tamanho)] for _ in range(tamanho)]
    mat_exib = [['#' for _ in range(tamanho)] for _ in range(tamanho)]

    return mat, mat_exib, tamanho


# Função para atualizar a matriz de exibição se os pares correspondem
def atualiza(pos1, pos2, mat, mat_exib):
    x1, y1 = pos1
    x2, y2 = pos2

    if mat[x1][y1] == mat[x2][y2]:
        mat_exib[x1][y1] = mat[x1][y1]
        mat_exib[x2][y2] = mat[x2][y2]

    return mat, mat_exib


# Função para desenhar a matriz usando Turtle
def desenhar_matriz(mat_exib, tamanho):
    turtle.clear()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.tracer(0, 0)

    cell_size = 50
    start_x = -cell_size * tamanho // 2
    start_y = cell_size * tamanho // 2

    # Desenha cada célula da matriz
    for i in range(tamanho):
        for j in range(tamanho):
            x = start_x + j * cell_size
            y = start_y - i * cell_size
            turtle.penup()
            turtle.goto(x, y)
            turtle.pendown()
            turtle.color('black', 'blue')
            turtle.begin_fill()
            for _ in range(4):
                turtle.forward(cell_size)
                turtle.right(90)
            turtle.end_fill()
            turtle.penup()
            turtle.goto(x + cell_size // 4, y - cell_size * 0.75)
            turtle.color('white')
            turtle.write(mat_exib[i][j], align="left", font=("Arial", 18, "normal"))

    desenhar_texto_informativo(tamanho)
    turtle.update()


# Função para desenhar o texto informativo
def desenhar_texto_informativo(tamanho):
    cell_size = 50
    start_x = -cell_size * tamanho // 2
    start_y = cell_size * tamanho // 2

    turtle.penup()
    turtle.goto(start_x, start_y + cell_size)
    turtle.color('black')
    texto = "Para exibir por 3 segundos as respostas, pressione 'v'.\nLembre-se que só pode usar duas vezes."
    turtle.write(texto, align="left", font=("Arial", 12, "bold"))


# Função para entender os cliques do usuário
def clique(x, y, estado):
    mat, mat_exib, tamanho, primeiro_clique, segundo_clique, acertos, total_pares, exibir_contagem = estado

    cell_size = 50
    start_x = -cell_size * tamanho // 2
    start_y = cell_size * tamanho // 2

    coluna = int((x - start_x) // cell_size)
    linha = int((start_y - y) // cell_size)

    # Verifica se o clique está dentro da matriz
    if 0 <= linha < tamanho and 0 <= coluna < tamanho:
        if mat_exib[linha][coluna] == '#':
            if primeiro_clique is None:
                primeiro_clique = (linha, coluna)
                mat_exib[linha][coluna] = mat[linha][coluna]
                desenhar_matriz(mat_exib, tamanho)
            elif segundo_clique is None:
                segundo_clique = (linha, coluna)
                mat_exib[linha][coluna] = mat[linha][coluna]
                desenhar_matriz(mat_exib, tamanho)
                if mat[primeiro_clique[0]][primeiro_clique[1]] == mat[segundo_clique[0]][segundo_clique[1]]:
                    acertos += 1
                else:
                    time.sleep(1)
                    mat_exib[primeiro_clique[0]][primeiro_clique[1]] = '#'
                    mat_exib[segundo_clique[0]][segundo_clique[1]] = '#'
                primeiro_clique = None
                segundo_clique = None
                desenhar_matriz(mat_exib, tamanho)

                # Verifica se o jogador ganhou
                if acertos == total_pares:
                    exibir_vitoria()  # Chama a função de exibição de vitória

    estado = (mat, mat_exib, tamanho, primeiro_clique, segundo_clique, acertos, total_pares, exibir_contagem)
    return estado


# Função para exibir a matriz completa por 3 segundos, até duas vezes por jogo
def exibir_respostas(estado):
    mat, mat_exib, tamanho, primeiro_clique, segundo_clique, acertos, total_pares, exibir_contagem = estado

    if exibir_contagem > 0:
        desenhar_matriz(mat, tamanho)
        time.sleep(3)
        desenhar_matriz(mat_exib, tamanho)
        exibir_contagem -= 1

    estado = (mat, mat_exib, tamanho, primeiro_clique, segundo_clique, acertos, total_pares, exibir_contagem)
    return estado


# Função para desenhar botões de dificuldade
def desenhar_botoes():
    turtle.clear()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.tracer(0, 0)

    botao_posicoes = [(-75, 50, "Fácil"), (-75, 0, "Médio"), (-75, -50, "Difícil")]

    for x, y, label in botao_posicoes:
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.color('black', 'lightgrey')
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(150)
            turtle.right(90)
            turtle.forward(40)
            turtle.right(90)
        turtle.end_fill()
        turtle.penup()
        turtle.goto(x + 75, y - 25)
        turtle.color('black')
        turtle.write(label, align="center", font=("Arial", 16, "bold"))

    turtle.update()


# Função para exibir a mensagem de vitória
def exibir_vitoria():
    turtle.clear()
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color('black')
    turtle.write('Parabéns, você ganhou!', align="center", font=("Arial", 24, "bold"))
    turtle.hideturtle()
    turtle.update()
    time.sleep(5)  # Espera 5 segundos antes de fechar
    turtle.bye()


# Função para lidar com o clique nos botões de dificuldade
def clique_botao(x, y):
    if -75 <= x <= 75:
        if 30 <= y <= 70:
            jogar(1)
        elif -20 <= y <= 20:
            jogar(2)
        elif -70 <= y <= -30:
            jogar(3)


# Função principal do jogo
def jogar(dificuldade):
    mat, mat_exib, tamanho = criar_matriz(dificuldade)
    total_pares = (tamanho * tamanho) // 2
    acertos = 0
    primeiro_clique = None
    segundo_clique = None
    exibir_contagem = 2

    estado = (mat, mat_exib, tamanho, primeiro_clique, segundo_clique, acertos, total_pares, exibir_contagem)

    desenhar_matriz(mat_exib, tamanho)

    def clique_wrapper(x, y):
        nonlocal estado
        estado = clique(x, y, estado)

    def exibir_respostas_wrapper():
        nonlocal estado
        estado = exibir_respostas(estado)

    turtle.onscreenclick(clique_wrapper)
    turtle.onkey(exibir_respostas_wrapper, "v")
    turtle.listen()
    turtle.mainloop()


# Função para inicializar o jogo com a tela de seleção de dificuldade
def iniciar_jogo():
    turtle.setup(width=700, height=700)
    desenhar_botoes()
    turtle.onscreenclick(clique_botao)
    turtle.listen()
    turtle.mainloop()


if __name__ == "__main__":
    iniciar_jogo()
    turtle.done()