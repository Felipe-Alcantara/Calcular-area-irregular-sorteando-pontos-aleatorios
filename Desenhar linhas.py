import tkinter as tk

def iniciar_desenho(event):
    global x_inicial, y_inicial
    x_inicial, y_inicial = event.x, event.y
    desenhar()

def atualizar_posicao(event):
    global x_atual, y_atual, linha
    x_atual, y_atual = event.x, event.y
    canvas.delete(linha)
    desenhar()

def desenhar():
    global linha, x_atual, y_atual, linha_anterior
    linha = canvas.create_line(x_inicial, y_inicial, x_atual, y_atual)
    canvas.delete(linha_anterior)
    linha_anterior = linha

# def terminar_desenho(event):
#     canvas.delete(linha)

janela = tk.Tk()
janela.title("Desenho")
janela.geometry("800x600")

canvas = tk.Canvas(janela, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", iniciar_desenho)
canvas.bind("<B1-Motion>", atualizar_posicao)
# canvas.bind("<ButtonRelease-1>", terminar_desenho)

janela.mainloop()
