"""
Calculadora de Área com Pontos Aleatórios
Aplicação para calcular área de polígonos irregulares usando o método de Monte Carlo.

Autor: Felipe Alcantara
Repositório: Calcular-area-irregular-sorteando-pontos-aleatorios
"""

import tkinter as tk
from tkinter import ttk
import random


class AreaCalculatorApp:
    """
    Aplicação para calcular áreas de polígonos irregulares desenhados pelo usuário
    utilizando o método de Monte Carlo (pontos aleatórios).
    """

    def __init__(self):
        # Configurações iniciais
        self.pixels_per_cm = 100  # Escala de conversão pixels para centímetros
        self.num_points = 100  # Número padrão de pontos por lote

        # Variáveis de estado
        self.is_drawing = False
        self.drawing_started = False
        self.drawing_completed = False
        self.pausar_geracao = False
        self.ctrl_pressed = False  # Rastreia se o Ctrl está pressionado
        self.locked_axis = None  # Eixo travado ('x' ou 'y')
        self.locked_coord = None  # Coordenada travada
        self.axis_locked = False  # Controla se o eixo está travado

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
        """Configura toda a interface gráfica da aplicação."""
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

        # Frame para os resultados (labels)
        results_frame = ttk.Frame(drawing_frame)
        results_frame.pack(fill=tk.X, padx=5, pady=5)

        # Widgets de labels para os resultados
        self.num_pontos_label = ttk.Label(results_frame, text="Pontos sorteados: 0")
        self.num_pontos_label.pack(anchor='w')

        self.red_points_label = ttk.Label(results_frame, text="Pontos fora: 0")
        self.red_points_label.pack(anchor='w')

        self.green_points_label = ttk.Label(results_frame, text="Pontos dentro: 0")
        self.green_points_label.pack(anchor='w')

        self.area_retangulo_label = ttk.Label(results_frame, text="Área do retângulo: 0 cm²")
        self.area_retangulo_label.pack(anchor='w')

        self.area_poligono_label = ttk.Label(results_frame, text="Área do polígono: 0 cm²")
        self.area_poligono_label.pack(anchor='w')

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

        # Ajusta a posição inicial do separador
        paned_window.sashpos(0, 200)

        # Associa os eventos do mouse e teclado às funções correspondentes
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.root.bind("<KeyPress-Control_L>", self.on_ctrl_press)
        self.root.bind("<KeyRelease-Control_L>", self.on_ctrl_release)
        self.root.bind("<KeyPress-Control_R>", self.on_ctrl_press)
        self.root.bind("<KeyRelease-Control_R>", self.on_ctrl_release)

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
        """Adiciona os botões de controle à interface."""
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
        """Desenha uma linha no canvas."""
        self.canvas.create_line(x1, y1, x2, y2, width=2, capstyle=tk.ROUND)

    def add_log_message(self, message):
        """Adiciona uma mensagem ao log."""
        self.log_messages.append(message)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Rolagem automática para o fim
        self.log_text.config(state=tk.DISABLED)

    def on_ctrl_press(self, event):
        """Handler para quando a tecla Ctrl é pressionada."""
        if not self.ctrl_pressed:
            self.ctrl_pressed = True
            self.add_log_message("Tecla Ctrl pressionada.")

    def on_ctrl_release(self, event):
        """Handler para quando a tecla Ctrl é solta."""
        self.ctrl_pressed = False
        self.locked_axis = None
        self.locked_coord = None
        if self.axis_locked:
            self.add_log_message("Eixo destravado.")
            self.axis_locked = False
        self.add_log_message("Tecla Ctrl liberada.")

    def on_mouse_down(self, event):
        """Handler para quando o botão do mouse é pressionado."""
        if self.drawing_completed:
            return
        if event.y < self.get_drawing_area_top():
            return
        self.drawing_started = True
        self.is_drawing = True
        self.points.append((event.x, event.y))

    def on_mouse_move(self, event):
        """Handler para quando o mouse se move enquanto está desenhando."""
        if event.y < self.get_drawing_area_top() or not self.is_drawing:
            return

        if len(self.points) == 0:
            return

        prev_x, prev_y = self.points[-1]

        if self.ctrl_pressed:
            if self.locked_axis is None:
                # Determina o eixo a ser travado com base no movimento
                delta_x = event.x - prev_x
                delta_y = event.y - prev_y
                if abs(delta_x) > abs(delta_y):
                    self.locked_axis = 'y'
                    self.locked_coord = prev_y
                    axis_name = 'Horizontal'
                else:
                    self.locked_axis = 'x'
                    self.locked_coord = prev_x
                    axis_name = 'Vertical'
                if not self.axis_locked:
                    self.add_log_message(f"Eixo travado: {axis_name}")
                    self.axis_locked = True

            if self.locked_axis == 'x':
                event_x = self.locked_coord
                event_y = event.y
            elif self.locked_axis == 'y':
                event_x = event.x
                event_y = self.locked_coord
        else:
            if self.axis_locked:
                self.add_log_message("Eixo destravado.")
                self.axis_locked = False
            self.locked_axis = None
            self.locked_coord = None
            event_x = event.x
            event_y = event.y

        # Evita adicionar pontos duplicados
        if (event_x, event_y) != (prev_x, prev_y):
            self.points.append((event_x, event_y))
            self.stroke_line(prev_x, prev_y, event_x, event_y)

    def on_mouse_up(self, event):
        """Handler para quando o botão do mouse é solto."""
        if not self.is_drawing:
            return

        self.is_drawing = False

        if not self.points:
            return

        # Fecha o polígono
        self.stroke_line(self.points[-1][0], self.points[-1][1], self.points[0][0], self.points[0][1])

        # Marca o desenho como concluído
        self.drawing_completed = True
        self.drawing_started = False

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
        """Obtém a posição vertical da área de desenho (abaixo do separador)."""
        sash_coords = self.canvas.winfo_rooty() - self.root.winfo_rooty()
        return sash_coords

    def calcular_area_retangulo(self):
        """Calcula a área do retângulo envolvente em cm²."""
        largura = self.max_x - self.min_x
        altura = self.max_y - self.min_y
        # Converte largura e altura em centímetros
        largura_cm = largura / self.pixels_per_cm
        altura_cm = altura / self.pixels_per_cm
        return largura_cm * altura_cm  # Área em cm²

    def exibir_area_retangulo(self):
        """Exibe a área do retângulo na interface."""
        self.area_retangulo_label.config(text=f"Área do retângulo: {self.area_retangulo:.2f} cm²")

    def exibir_area_poligono(self):
        """Calcula e exibe a área estimada do polígono usando o método de Monte Carlo."""
        if self.total_points_counter == 0:
            return
        proporcao = self.inside_points_counter / self.total_points_counter
        area_poligono = proporcao * self.area_retangulo
        self.area_poligono_label.config(text=f"Área do polígono: {area_poligono:.2f} cm²")

    def is_point_inside_polygon(self, x, y):
        """
        Verifica se um ponto está dentro do polígono usando o algoritmo Ray Casting.
        
        Args:
            x: Coordenada x do ponto
            y: Coordenada y do ponto
            
        Returns:
            bool: True se o ponto está dentro do polígono, False caso contrário
        """
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
        """Gera pontos aleatórios e verifica se estão dentro do polígono."""
        if not self.points or self.pausar_geracao or not self.drawing_completed:
            return

        # Gera pontos aleatórios
        random_points = [(random.uniform(self.min_x, self.max_x), random.uniform(self.min_y, self.max_y)) 
                        for _ in range(self.num_points)]

        for x, y in random_points:
            self.total_points_counter += 1
            is_inside = self.is_point_inside_polygon(x, y)
            if is_inside:
                self.canvas.create_oval(x-1, y-1, x+1, y+1, fill="green", outline="")
                self.inside_points_counter += 1
            else:
                self.canvas.create_oval(x-1, y-1, x+1, y+1, fill="red", outline="")

        # Atualiza contadores e exibição
        self.num_pontos_label.config(text=f"Pontos sorteados: {self.total_points_counter}")
        self.green_points_label.config(text=f"Pontos dentro: {self.inside_points_counter}")
        self.red_points_label.config(text=f"Pontos fora: {self.total_points_counter - self.inside_points_counter}")

        # Atualiza estimativa de área
        self.exibir_area_poligono()

        # Agenda a próxima geração de pontos
        if not self.pausar_geracao:
            self.canvas.after(100, self.generate_points)

    def update_num_points(self):
        """Atualiza o número de pontos a serem gerados por lote."""
        try:
            self.num_points = int(self.num_points_entry.get())
            self.add_log_message(f"Atualizado num_points para {self.num_points}.")
        except ValueError:
            self.add_log_message("Valor inválido para num_points.")

    def pausar(self):
        """Pausa a geração de pontos aleatórios."""
        self.pausar_geracao = True
        self.add_log_message("Pausa solicitada.")

    def retomar(self):
        """Retoma a geração de pontos aleatórios."""
        self.pausar_geracao = False
        self.add_log_message("Retomando a geração de pontos.")
        self.generate_points()

    def clear_drawing(self):
        """Limpa o desenho atual e salva os cálculos."""
        # Salva os cálculos atuais antes de limpar
        if self.drawing_started or self.drawing_completed:
            self.save_current_calculation()

        # Limpa o canvas
        self.canvas.delete("all")

        # Redefine variáveis
        self.points.clear()
        self.drawing_completed = False
        self.drawing_started = False
        self.total_points_counter = 0
        self.inside_points_counter = 0
        self.is_drawing = False
        self.pausar_geracao = False
        self.locked_axis = None
        self.locked_coord = None
        self.axis_locked = False

        # Reset labels
        self.num_pontos_label.config(text="Pontos sorteados: 0")
        self.green_points_label.config(text="Pontos dentro: 0")
        self.red_points_label.config(text="Pontos fora: 0")
        self.area_retangulo_label.config(text="Área do retângulo: 0 cm²")
        self.area_poligono_label.config(text="Área do polígono: 0 cm²")

        self.add_log_message("Desenho limpo.")

    def save_current_calculation(self):
        """Salva os cálculos do desenho atual no histórico."""
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
        """Atualiza a exibição dos cálculos anteriores."""
        self.annotations_text.config(state=tk.NORMAL)
        self.annotations_text.delete(1.0, tk.END)
        for idx, calc in enumerate(self.previous_calculations, 1):
            self.annotations_text.insert(tk.END, f"Desenho {idx}:\n")
            for key, value in calc.items():
                self.annotations_text.insert(tk.END, f"  {key}: {value}\n")
            self.annotations_text.insert(tk.END, "\n")
        self.annotations_text.config(state=tk.DISABLED)


# Inicializa a aplicação
if __name__ == "__main__":
    AreaCalculatorApp()
