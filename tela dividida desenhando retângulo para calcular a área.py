import tkinter as tk

def iniciar_desenho(event):
    global coordenadas
    coordenadas = [(event.x, event.y)]

def desenhar_rastro(event):
    global coordenadas
    if event.widget == canvas_cima:  return
    coordenadas.append((event.x, event.y))
    if len(coordenadas) > 1:
        x1, y1 = coordenadas[-2]
        x2, y2 = coordenadas[-1]
        canvas.create_line(x1, y1, x2, y2)

def limpar_rastro(event):
    global coordenadas
    if len(coordenadas) > 1:
        x_coords, y_coords = zip(*coordenadas)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        canvas.create_rectangle(x_min, y_min, x_max, y_max)
        x1, y1 = coordenadas[-1]
        x2, y2 = coordenadas[0]
        canvas.create_line(x1, y1, x2, y2)
    coordenadas.clear()

def mostrar_coordenadas(event):
    coordenadas_label.config(text=f'Coordenadas do mouse: ({event.x}, {event.y})')

janela = tk.Tk()
janela.title("Desenho")
janela.geometry("800x600")

canvas = tk.Canvas(janela, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas_baixo = tk.Canvas(janela, bg="White", width=800, height=600)
canvas_baixo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas_cima = tk.Canvas(janela, bg="white", width=400, height=600)
canvas_cima.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

coordenadas_label = tk.Label(janela, text="Coordenadas do mouse: (0, 0)")
coordenadas_label.pack()

coordenadas = []

canvas.bind("<Button-1>", iniciar_desenho)
canvas.bind("<B1-Motion>", desenhar_rastro)
canvas.bind("<ButtonRelease-1>", limpar_rastro)
canvas.bind("<Motion>", mostrar_coordenadas)

janela.mainloop()