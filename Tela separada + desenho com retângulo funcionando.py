import tkinter as tk

# Função para desenhar uma linha
def stroke_line(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, width=2, capstyle=tk.ROUND)

# Inicializa a janela e o canvas
root = tk.Tk()
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Configurações iniciais
half_width = root.winfo_screenwidth() / 2
half_height = root.winfo_screenheight() / 2
is_drawing = False
drawing_completed = False # Adicionado para controlar se o desenho já foi concluído
points = []

# Desenha a linha horizontal central
stroke_line(0, half_height, root.winfo_screenwidth(), half_height)

# Cria um texto vazio para as coordenadas do mouse
mouse_coords = canvas.create_text(half_width, half_height - 20, text="", fill="black")

# Cria um texto acima da linha
texto = tk.Label(root, text="Pontos sorteados: ", bg="White", font=("Arial", 40))
texto.place(x=half_width - 740, y=half_height - 500, anchor="center")

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
    global is_drawing, drawing_completed, points # Adicionar points como global
    is_drawing = False

    if drawing_completed or not points:
        return

    stroke_line(points[-1][0], points[-1][1], points[0][0], points[0][1])

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for x, y in points:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    print(min_x, min_y, max_x, max_y)
    canvas.create_rectangle(min_x, min_y, max_x, max_y, width=2)

    points = []
    drawing_completed = True

# Associa os eventos do mouse às funções correspondentes
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Motion>", on_mouse_move)

# Inicia o loop principal da interface gráfica
root.mainloop()
