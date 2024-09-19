import tkinter as tk
import random

class AreaCalculatorApp:
    def __init__(self):
        # Configurações iniciais
        self.pixels_per_cm = 100  # Ajuste este valor conforme necessário
        self.num_points = 100  # Número padrão de pontos por lote

        # Variáveis de estado
        self.is_drawing = False
        self.drawing_started = False
        self.drawing_completed = False
        self.pausar_geracao = False

        # Listas e contadores
        self.points = []
        self.log_messages = []
        self.total_points_counter = 0
        self.inside_points_counter = 0

        # Variáveis para o retângulo envolvente
        self.min_x = self.max_x = self.min_y = self.max_y = self.area_retangulo = 0

        # Inicialização da janela
        self.root = tk.Tk()
        self.root.title("Calcular a área com pontos aleatórios")
        self.root.geometry("1000x600")

        self.half_width = self.root.winfo_screenwidth() / 2
        self.half_height = self.root.winfo_screenheight() / 2

        # Configuração da interface
        self.setup_interface()

        # Inicia o loop principal
        self.root.mainloop()

    def setup_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para o canvas e o log
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inicializa o canvas
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame para os controles
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Desenha a linha horizontal central
        self.stroke_line(0, self.half_height, self.root.winfo_screenwidth(), self.half_height)

        # Cria os textos iniciais
        self.create_text_items()

        # Associa os eventos do mouse às funções correspondentes
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Adiciona controles
        self.add_controls(controls_frame)

    def add_controls(self, frame):
        # Adiciona um botão para atualizar num_points
        update_button = tk.Button(frame, text="Atualizar num_points", command=self.update_num_points)
        update_button.pack(padx=10, pady=5)

        # Adiciona um campo de entrada para num_points
        self.num_points_entry = tk.Entry(frame)
        self.num_points_entry.insert(0, str(self.num_points))  # Valor padrão
        self.num_points_entry.pack(padx=10, pady=5)

        # Adiciona botões de pausar e retomar
        botao_pausar = tk.Button(frame, text="Pausar", command=self.pausar)
        botao_pausar.pack(padx=10, pady=5)

        botao_retomar = tk.Button(frame, text="Retomar", command=self.retomar)
        botao_retomar.pack(padx=10, pady=5)

        # Adiciona um botão para limpar o desenho
        botao_limpar = tk.Button(frame, text="Limpar", command=self.clear_drawing)
        botao_limpar.pack(padx=10, pady=5)

        # Widget de texto para exibir o log
        log_label = tk.Label(frame, text="Log de Eventos:")
        log_label.pack(padx=10, pady=(20, 5))

        self.log_text = tk.Text(frame, height=15, width=30)
        self.log_text.pack(padx=10, pady=5)
        self.log_text.config(state=tk.NORMAL)  # Permite inserção de texto

    def stroke_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=2, capstyle=tk.ROUND)

    def add_log_message(self, message):
        self.log_messages.append(message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Rolagem automática para o fim

    def on_mouse_down(self, event):
        if self.drawing_completed or self.drawing_started:
            return
        if event.y < self.half_height:
            return
        self.drawing_started = True
        self.is_drawing = True
        self.points.append((event.x, event.y))

    def on_mouse_move(self, event):
        # Atualiza o texto das coordenadas do mouse
        self.canvas.itemconfig(self.mouse_coords, text=f"({event.x}, {event.y})")
        
        if event.y < self.half_height or not self.is_drawing:
            return
        self.points.append((event.x, event.y))
        self.stroke_line(self.points[-2][0], self.points[-2][1], event.x, event.y)

    def on_mouse_up(self, event):
        self.is_drawing = False

        if self.drawing_completed or not self.points:
            return

        # Fecha o polígono
        self.stroke_line(self.points[-1][0], self.points[-1][1], self.points[0][0], self.points[0][1])

        # Calcula o retângulo envolvente
        self.min_x = min(self.points, key=lambda p: p[0])[0]
        self.max_x = max(self.points, key=lambda p: p[0])[0]
        self.min_y = min(self.points, key=lambda p: p[1])[1]
        self.max_y = max(self.points, key=lambda p: p[1])[1]

        self.canvas.create_rectangle(self.min_x, self.min_y, self.max_x, self.max_y, width=2)

        # Calcula a área do retângulo e exibe
        self.area_retangulo = self.calcular_area_retangulo()
        self.exibir_area_retangulo()

        # Inicia a geração de pontos
        self.add_log_message("Desenho criado.")
        self.generate_points()

    def calcular_area_retangulo(self):
        largura = self.max_x - self.min_x
        altura = self.max_y - self.min_y
        # Converte largura e altura em centímetros
        largura_cm = largura / self.pixels_per_cm
        altura_cm = altura / self.pixels_per_cm
        return largura_cm * altura_cm  # Área em cm²

    def exibir_area_retangulo(self):
        self.canvas.itemconfig(self.area_retangulo_text, text=f"Área do retângulo: {self.area_retangulo:.2f} cm²")

    def exibir_area_poligono(self):
        if self.total_points_counter == 0:
            return
        proporcao = self.inside_points_counter / self.total_points_counter
        area_poligono = proporcao * self.area_retangulo
        self.canvas.itemconfig(self.area_poligono_text, text=f"Área do polígono: {area_poligono:.2f} cm²")

    def is_point_inside_polygon(self, x, y):
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0]
        for i in range(n+1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y)*(p2x - p1x)/(p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def generate_points(self):
        if not self.points or self.drawing_completed or self.pausar_geracao:
            return

        # Gera pontos aleatórios
        random_points = [(random.uniform(self.min_x, self.max_x), random.uniform(self.min_y, self.max_y)) for _ in range(self.num_points)]

        for x, y in random_points:
            self.total_points_counter += 1
            is_inside = self.is_point_inside_polygon(x, y)
            if is_inside:
                self.canvas.create_oval(x-1, y-1, x+1, y+1, fill="green", outline="")
                self.inside_points_counter += 1
            else:
                self.canvas.create_oval(x-1, y-1, x+1, y+1, fill="red", outline="")

        # Atualiza contadores e exibição
        self.canvas.itemconfig(self.num_pontos_texto, text=f"Pontos sorteados: {self.total_points_counter}")
        self.canvas.itemconfig(self.green_points_text, text=f"Pontos dentro: {self.inside_points_counter}")
        self.canvas.itemconfig(self.red_points_text, text=f"Pontos fora: {self.total_points_counter - self.inside_points_counter}")

        # Atualiza estimativa de área
        self.exibir_area_poligono()

        # Agenda a próxima geração de pontos
        if not self.pausar_geracao:
            self.canvas.after(100, self.generate_points)  # Ajuste o delay conforme necessário

    def update_num_points(self):
        try:
            self.num_points = int(self.num_points_entry.get())
            self.add_log_message(f"Atualizado num_points para {self.num_points}.")
        except ValueError:
            self.add_log_message("Valor inválido para num_points.")

    def pausar(self):
        self.pausar_geracao = True
        self.add_log_message("Pausa solicitada.")

    def retomar(self):
        self.pausar_geracao = False
        self.add_log_message("Retomando a geração de pontos.")
        self.generate_points()

    def clear_drawing(self):
        # Limpa o canvas
        self.canvas.delete("all")

        # Redesenha a linha horizontal
        self.stroke_line(0, self.half_height, self.root.winfo_screenwidth(), self.half_height)

        # Recria os itens de texto
        self.create_text_items()

        # Redefine variáveis
        self.points.clear()
        self.drawing_completed = False
        self.total_points_counter = 0
        self.inside_points_counter = 0
        self.is_drawing = False
        self.drawing_started = False
        self.pausar_geracao = False

        self.add_log_message("Desenho limpo.")

    def create_text_items(self):
        self.num_pontos_texto = self.canvas.create_text(10, 10, text="Pontos sorteados: 0", font=("Arial", 16), anchor="nw")
        self.red_points_text = self.canvas.create_text(10, 30, text="Pontos fora: 0", font=("Arial", 16), anchor="nw")
        self.green_points_text = self.canvas.create_text(10, 50, text="Pontos dentro: 0", font=("Arial", 16), anchor="nw")
        self.area_retangulo_text = self.canvas.create_text(10, 70, text="Área do retângulo: 0 cm²", font=("Arial", 16), anchor="nw")
        self.area_poligono_text = self.canvas.create_text(10, 90, text="Área do polígono: 0 cm²", font=("Arial", 16), anchor="nw")
        self.mouse_coords = self.canvas.create_text(self.half_width, self.half_height - 20, text="", fill="black")

# Inicializa a aplicação
if __name__ == "__main__":
    AreaCalculatorApp()
