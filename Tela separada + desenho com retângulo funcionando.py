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

# Inicializa a janela
root = tk.Tk()

# Inicializa o canvas
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Adiciona um texto acima do canvas e muda sua posição
texto = canvas.create_text(10, 10, text="Pontos sorteados: ", font=("Arial", 20), anchor="nw")

# Após a conclusão do desenho e antes da geração dos pontos aleatórios, você pode adicionar mais texto ao canvas
canvas.create_text(10, 80, text="Outro texto que você deseja exibir", font=("Arial", 14), anchor="nw")

# Certifique-se de que o texto esteja acima de tudo no canvas
canvas.tag_raise(texto)

# Configurações iniciais
half_width = root.winfo_screenwidth() / 2
half_height = root.winfo_screenheight() / 2
is_drawing = False
drawing_completed = False
points = []

# Desenha a linha horizontal central
stroke_line(0, half_height, root.winfo_screenwidth(), half_height)

# Cria um texto vazio para as coordenadas do mouse
mouse_coords = canvas.create_text(half_width, half_height - 20, text="", fill="black")

# Função chamada quando o botão do mouse é pressionado
def on_mouse_down(event):
    global is_drawing, drawing_completed
    if event.y < half_height or drawing_completed:
        return
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
    global is_drawing, drawing_completed, points
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

    # Gera pontos aleatórios dentro do retângulo
    num_points = 50
    random_points = [(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) for _ in range(num_points)]

    # Verifica se cada ponto está dentro ou fora da forma
    for point in random_points:
        x, y = point
        is_inside = is_point_inside_polygon(x, y, points)
        if is_inside:
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="green")  # Ponto dentro do polígono
        else:
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")    # Ponto fora do polígono

    points = []
    drawing_completed = True

# Associa os eventos do mouse às funções correspondentes
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Motion>", on_mouse_move)

# Inicia o loop principal da interface gráfica
root.mainloop()
