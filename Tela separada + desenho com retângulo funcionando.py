import tkinter as tk
import random

# Função para desenhar uma linha
def stroke_line(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, width=2, capstyle=tk.ROUND)

# Função para verificar se um ponto está dentro de um polígono
def is_point_inside_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Função para pausar a geração de pontos
def pausar():
    global pausar_geracao
    pausar_geracao = True

# Função para retomar a geração de pontos
def retomar():
    global pausar_geracao
    pausar_geracao = False
    generate_points_until_filled()

# Função chamada quando o botão do mouse é pressionado
drawing_started = False

def on_mouse_down(event):
    global is_drawing, drawing_completed, drawing_started
    if drawing_completed or drawing_started:
        return
    if event.y < half_height:
        return
    drawing_started = True
    is_drawing = True
    points.append((event.x, event.y))


# Função chamada quando o mouse se move
def on_mouse_move(event):
    # Atualiza o texto das coordenadas do mouse
    canvas.itemconfig(mouse_coords, text=f"({event.x}, {event.y})")
    
    if event.y < half_height or not is_drawing:
        return
    points.append((event.x, event.y))
    stroke_line(points[-2][0], points[-2][1], event.x, event.y)

# Função chamada quando o botão do mouse é solto
def on_mouse_up(event):
    global is_drawing, drawing_completed, points, num_pontos
    is_drawing = False

    if drawing_completed or not points:
        return

    stroke_line(points[-1][0], points[-1][1], points[0][0], points[0][1])

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for x, y in points:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    canvas.create_rectangle(min_x, min_y, max_x, max_y, width=2)

    # Chama a função para gerar pontos até que toda a área seja preenchida
    generate_points_until_filled()
red_points_counter = 0
green_points_counter = 0
# Função para gerar pontos até que toda a área seja preenchida
def generate_points_until_filled():
    global points, drawing_completed, num_pontos, pausar_geracao, started, red_points_counter, green_points_counter
    num_points = 1000
    point_counter = 0

    while not drawing_completed:
        if pausar_geracao:
            return  # Retorna se a geração de pontos deve ser pausada

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for x, y in points:
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)

        random_points = [(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) for _ in range(num_points)]

        for point in random_points:
            x, y = point
            is_inside = is_point_inside_polygon(x, y, points)
            point_counter += 1
            if is_inside:
                canvas.create_oval(x-2, y-2, x+2, y+2, fill="green")  # Ponto dentro do polígono
                green_points_counter += 1
            else:
                canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")    # Ponto fora do polígono
                red_points_counter += 1

        if red_points_counter > 0:
            canvas.itemconfig(red_points_text, text=f"Pontos vermelhos: {red_points_counter}")
        if green_points_counter > 0:
            canvas.itemconfig(green_points_text, text=f"Pontos verdes: {green_points_counter}")

        red_points = [point for point in random_points if not is_point_inside_polygon(point[0], point[1], points)]
        if not red_points:
            drawing_completed = True

        canvas.update()

        num_pontos += num_points
        canvas.itemconfig(num_pontos_texto, text=f"Pontos sorteados: {num_pontos}")

# Inicializa a janela
root = tk.Tk()
root.title("Calcular a área com pontos aleatórios")
root.geometry("1920x1080")

# Inicializa o canvas
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Adiciona um texto para mostrar o número de pontos sorteados na tela
num_pontos_texto = canvas.create_text(10, 10, text="Pontos sorteados: 0", font=("Arial", 16), anchor="nw")

# Adiciona texto para mostrar o número de pontos vermelhos
red_points_text = canvas.create_text(10, 30, text="Pontos vermelhos: 0", font=("Arial", 16), anchor="nw")

# Adiciona texto para mostrar o número de pontos verdes
green_points_text = canvas.create_text(10, 50, text="Pontos verdes: 0", font=("Arial", 16), anchor="nw")

# Adiciona botões de pausar e retomar
botao_pausar = tk.Button(root, text="Pausar", command=pausar)
botao_pausar.pack(side=tk.LEFT, padx=10, pady=10)

botao_retomar = tk.Button(root, text="Retomar", command=retomar)
botao_retomar.pack(side=tk.LEFT, padx=10, pady=10)

# Configurações iniciais
half_width = root.winfo_screenwidth() / 2
half_height = root.winfo_screenheight() / 2
is_drawing = False
drawing_completed = False
points = []
num_pontos = 0
pausar_geracao = False

# Desenha a linha horizontal central
stroke_line(0, half_height, root.winfo_screenwidth(), half_height)

# Cria um texto vazio para as coordenadas do mouse
mouse_coords = canvas.create_text(half_width, half_height - 20, text="", fill="black")

# Associa os eventos do mouse às funções correspondentes
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Motion>", on_mouse_move)

# Inicia o loop principal da interface gráfica
root.mainloop()