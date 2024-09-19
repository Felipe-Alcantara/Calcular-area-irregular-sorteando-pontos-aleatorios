import tkinter as tk
from tkinter import ttk
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

        # Lista para armazenar as anotações de cálculos anteriores
        self.previous_calculations = []

        # Inicialização da janela
        self.root = tk.Tk()
        self.root.title("Calcular a área com pontos aleatórios")
        self.root.geometry("1200x700")

        # Configuração da interface
        self.setup_interface()

        # Inicia o loop principal
        self.root.mainloop()

    def setup_interface(self):
        # Estilos para os frames
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabelframe', background='white')
        style.configure('TLabelframe.Label', font=('Arial', 12, 'bold'))

        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para o canvas e as anotações
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para o canvas com borda e título
        drawing_frame = ttk.LabelFrame(left_frame, text="Área de Desenho")
        drawing_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Cria um PanedWindow vertical para separar o canvas e permitir redimensionamento
        paned_window = ttk.PanedWindow(drawing_frame, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Frame vazio acima do canvas para permitir o redimensionamento
        self.upper_frame = ttk.Frame(paned_window, height=100)
        paned_window.add(self.upper_frame, weight=1)

        # Frame para o canvas
        canvas_frame = ttk.Frame(paned_window)
        paned_window.add(canvas_frame, weight=4)

        # Inicializa o canvas
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Ajusta o tamanho mínimo do canvas
        self.canvas.update_idletasks()
        # Ajusta a posição inicial do separador
        paned_window.sashpos(0, 200)

        # Cria os textos iniciais no canvas
        self.create_text_items()

        # Associa os eventos do mouse às funções correspondentes
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Frame para as anotações
        annotations_frame = ttk.LabelFrame(left_frame, text="Cálculos Anteriores")
        annotations_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Widget de texto para exibir as anotações
        self.annotations_text = tk.Text(annotations_frame, height=10)
        self.annotations_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.annotations_text.config(state=tk.DISABLED)

        # Frame para os controles e log
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para os controles com borda e título
        controls_frame = ttk.LabelFrame(right_frame, text="Controles")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        # Adiciona controles
        self.add_controls(controls_frame)

        # Frame para o log com borda e título
        log_frame = ttk.LabelFrame(right_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Widget de texto para exibir o log
        self.log_text = tk.Text(log_frame, height=15, width=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)  # Inicia como somente leitura


    def add_controls(self, frame):
        # Frame interno para organizar os botões
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=5)

        # Botão de atualizar num_points
        update_button = ttk.Button(buttons_frame, text="Atualizar num_points", command=self.update_num_points)
        update_button.grid(row=0, column=0, padx=5, pady=5)

        # Campo de entrada para num_points
        self.num_points_entry = ttk.Entry(buttons_frame, width=10)
        self.num_points_entry.insert(0, str(self.num_points))  # Valor padrão
        self.num_points_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botão de pausar
        botao_pausar = ttk.Button(buttons_frame, text="Pausar", command=self.pausar)
        botao_pausar.grid(row=1, column=0, padx=5, pady=5)

        # Botão de retomar
        botao_retomar = ttk.Button(buttons_frame, text="Retomar", command=self.retomar)
        botao_retomar.grid(row=1, column=1, padx=5, pady=5)

        # Botão de limpar
        botao_limpar = ttk.Button(buttons_frame, text="Limpar", command=self.clear_drawing)
        botao_limpar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def stroke_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=2, capstyle=tk.ROUND)

    def add_log_message(self, message):
        self.log_messages.append(message)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Rolagem automática para o fim
        self.log_text.config(state=tk.DISABLED)

    def on_mouse_down(self, event):
        if self.drawing_completed or self.drawing_started:
            return
        if event.y < self.get_drawing_area_top():
            return
        self.drawing_started = True
        self.is_drawing = True
        self.points.append((event.x, event.y))

    def on_mouse_move(self, event):
        # Atualiza o texto das coordenadas do mouse
        self.canvas.itemconfig(self.mouse_coords, text=f"({event.x}, {event.y})")
        
        if event.y < self.get_drawing_area_top() or not self.is_drawing:
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

    def get_drawing_area_top(self):
        # Obtém a posição vertical da área de desenho (abaixo do separador)
        sash_coords = self.canvas.winfo_rooty() - self.root.winfo_rooty()
        return sash_coords

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
        # Salva os cálculos atuais antes de limpar
        if self.drawing_started or self.drawing_completed:
            self.save_current_calculation()

        # Limpa o canvas
        self.canvas.delete("all")

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

    def save_current_calculation(self):
        proporcao = self.inside_points_counter / self.total_points_counter if self.total_points_counter else 0
        area_poligono = proporcao * self.area_retangulo
        calculation = {
            'Pontos sorteados': self.total_points_counter,
            'Pontos dentro': self.inside_points_counter,
            'Pontos fora': self.total_points_counter - self.inside_points_counter,
            'Área do retângulo': f"{self.area_retangulo:.2f} cm²",
            'Área do polígono': f"{area_poligono:.2f} cm²"
        }
        self.previous_calculations.append(calculation)
        self.update_annotations()

    def update_annotations(self):
        self.annotations_text.config(state=tk.NORMAL)
        self.annotations_text.delete(1.0, tk.END)
        for idx, calc in enumerate(self.previous_calculations, 1):
            self.annotations_text.insert(tk.END, f"Desenho {idx}:\n")
            for key, value in calc.items():
                self.annotations_text.insert(tk.END, f"  {key}: {value}\n")
            self.annotations_text.insert(tk.END, "\n")
        self.annotations_text.config(state=tk.DISABLED)

    def create_text_items(self):
        self.num_pontos_texto = self.canvas.create_text(10, 10, text="Pontos sorteados: 0", font=("Arial", 12), anchor="nw")
        self.red_points_text = self.canvas.create_text(10, 30, text="Pontos fora: 0", font=("Arial", 12), anchor="nw")
        self.green_points_text = self.canvas.create_text(10, 50, text="Pontos dentro: 0", font=("Arial", 12), anchor="nw")
        self.area_retangulo_text = self.canvas.create_text(10, 70, text="Área do retângulo: 0 cm²", font=("Arial", 12), anchor="nw")
        self.area_poligono_text = self.canvas.create_text(10, 90, text="Área do polígono: 0 cm²", font=("Arial", 12), anchor="nw")
        self.mouse_coords = self.canvas.create_text(10, 110, text="", fill="black", anchor="nw")

# Inicializa a aplicação
if __name__ == "__main__":
    AreaCalculatorApp()
