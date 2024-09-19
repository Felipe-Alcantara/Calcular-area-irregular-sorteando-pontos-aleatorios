import tkinter as tk
import random

# Definindo a escala de conversão
pixels_per_cm = 100  # Ajuste este valor conforme necessário

# Lista para armazenar as mensagens de log
log_messages = []

# Função para adicionar mensagens ao log
def add_log_message(message):
    log_messages.append(message)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)  # Rolagem automática para o fim

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
                        xinters = (y - p1y)*(p2x - p1x)/(p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Função para pausar a geração de pontos
def pausar():
    global pausar_geracao
    pausar_geracao = True
    add_log_message("Pausa solicitada.")

# Função para retomar a geração de pontos
def retomar():
    global pausar_geracao
    pausar_geracao = False
    add_log_message("Retomando a geração de pontos.")
    generate_points()

# Função chamada quando o botão do mouse é pressionado
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
    global is_drawing, drawing_completed, points, drawing_started
    global min_x, max_x, min_y, max_y, area_retangulo
    is_drawing = False

    if drawing_completed or not points:
        return

    # Fecha o polígono
    stroke_line(points[-1][0], points[-1][1], points[0][0], points[0][1])

    # Calcula o retângulo envolvente
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]

    canvas.create_rectangle(min_x, min_y, max_x, max_y, width=2)

    # Calcula a área do retângulo e exibe
    area_retangulo = calcular_area_retangulo(points)
    exibir_area_retangulo()

    # Inicia a geração de pontos
    add_log_message("Desenho criado.")
    generate_points()

def calcular_area_retangulo(pontos):
    largura = max_x - min_x
    altura = max_y - min_y
    # Converte largura e altura em centímetros
    largura_cm = largura / pixels_per_cm
    altura_cm = altura / pixels_per_cm
    return largura_cm * altura_cm  # Área em cm²

def exibir_area_retangulo():
    canvas.itemconfig(area_retangulo_text, text=f"Área do retângulo: {area_retangulo:.2f} cm²")

def exibir_area_poligono():
    if total_points_counter == 0:
        return
    proporcao = inside_points_counter / total_points_counter
    area_poligono = proporcao * area_retangulo
    canvas.itemconfig(area_poligono_text, text=f"Área do polígono: {area_poligono:.2f} cm²")

def generate_points():
    global total_points_counter, inside_points_counter

    if not points or drawing_completed or pausar_geracao:
        return

    # Gera pontos aleatórios
    random_points = [(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) for _ in range(num_points)]

    for x, y in random_points:
        total_points_counter += 1
        is_inside = is_point_inside_polygon(x, y, points)
        if is_inside:
            canvas.create_oval(x-1, y-1, x+1, y+1, fill="green", outline="")
            inside_points_counter += 1
        else:
            canvas.create_oval(x-1, y-1, x+1, y+1, fill="red", outline="")

    # Atualiza contadores e exibição
    canvas.itemconfig(num_pontos_texto, text=f"Pontos sorteados: {total_points_counter}")
    canvas.itemconfig(green_points_text, text=f"Pontos dentro: {inside_points_counter}")
    canvas.itemconfig(red_points_text, text=f"Pontos fora: {total_points_counter - inside_points_counter}")

    # Atualiza estimativa de área
    exibir_area_poligono()

    # Agenda a próxima geração de pontos
    if not pausar_geracao:
        canvas.after(100, generate_points)  # Ajuste o delay conforme necessário

# Função para atualizar num_points
def update_num_points():
    global num_points
    try:
        num_points = int(num_points_entry.get())
        add_log_message(f"Atualizado num_points para {num_points}.")
        print(f"num_points atualizado para {num_points}")
    except ValueError:
        print("Por favor, insira um número inteiro válido.")

# Função para limpar o desenho
def clear_drawing():
    global points, drawing_completed, total_points_counter, inside_points_counter
    global is_drawing, drawing_started, pausar_geracao

    # Limpa o canvas
    canvas.delete("all")

    # Redesenha a linha horizontal
    stroke_line(0, half_height, root.winfo_screenwidth(), half_height)

    # Recria os itens de texto
    create_text_items()

    # Redefine variáveis
    points.clear()
    drawing_completed = False
    total_points_counter = 0
    inside_points_counter = 0
    is_drawing = False
    drawing_started = False
    pausar_geracao = False

    add_log_message("Desenho limpo.")

def create_text_items():
    global num_pontos_texto, red_points_text, green_points_text, area_retangulo_text, area_poligono_text, mouse_coords

    num_pontos_texto = canvas.create_text(10, 10, text="Pontos sorteados: 0", font=("Arial", 16), anchor="nw")
    red_points_text = canvas.create_text(10, 30, text="Pontos fora: 0", font=("Arial", 16), anchor="nw")
    green_points_text = canvas.create_text(10, 50, text="Pontos dentro: 0", font=("Arial", 16), anchor="nw")
    area_retangulo_text = canvas.create_text(10, 70, text="Área do retângulo: 0 cm²", font=("Arial", 16), anchor="nw")
    area_poligono_text = canvas.create_text(10, 90, text="Área do polígono: 0 cm²", font=("Arial", 16), anchor="nw")
    mouse_coords = canvas.create_text(half_width, half_height - 20, text="", fill="black")

# Inicializa a janela
root = tk.Tk()
root.title("Calcular a área com pontos aleatórios")
root.geometry("1000x600")

# Configurações iniciais
half_width = root.winfo_screenwidth() / 2
half_height = root.winfo_screenheight() / 2
is_drawing = False
drawing_started = False
drawing_completed = False
points = []
pausar_geracao = False
num_points = 100  # Número padrão de pontos por lote
total_points_counter = 0
inside_points_counter = 0

# Variáveis para o retângulo envolvente
min_x = max_x = min_y = max_y = area_retangulo = 0

# Frame principal
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame para o canvas e o log
canvas_frame = tk.Frame(main_frame)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Inicializa o canvas
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Frame para os controles
controls_frame = tk.Frame(main_frame)
controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Desenha a linha horizontal central
stroke_line(0, half_height, root.winfo_screenwidth(), half_height)

# Cria os textos iniciais
create_text_items()

# Associa os eventos do mouse às funções correspondentes
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Motion>", on_mouse_move)

# Adiciona um botão para atualizar num_points
update_button = tk.Button(controls_frame, text="Atualizar num_points", command=update_num_points)
update_button.pack(padx=10, pady=5)

# Adiciona um campo de entrada para num_points
num_points_entry = tk.Entry(controls_frame)
num_points_entry.insert(0, str(num_points))  # Valor padrão
num_points_entry.pack(padx=10, pady=5)

# Adiciona botões de pausar e retomar
botao_pausar = tk.Button(controls_frame, text="Pausar", command=pausar)
botao_pausar.pack(padx=10, pady=5)

botao_retomar = tk.Button(controls_frame, text="Retomar", command=retomar)
botao_retomar.pack(padx=10, pady=5)

# Adiciona um botão para limpar o desenho
botao_limpar = tk.Button(controls_frame, text="Limpar", command=clear_drawing)
botao_limpar.pack(padx=10, pady=5)

# Widget de texto para exibir o log
log_label = tk.Label(controls_frame, text="Log de Eventos:")
log_label.pack(padx=10, pady=(20, 5))

log_text = tk.Text(controls_frame, height=15, width=30)
log_text.pack(padx=10, pady=5)
log_text.config(state=tk.NORMAL)  # Permite inserção de texto

# Inicia o loop principal da interface gráfica
root.mainloop()
