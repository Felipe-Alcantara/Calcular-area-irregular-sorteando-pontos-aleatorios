import tkinter as tk
from tkinter import messagebox

def mostrar_mensagem():
    messagebox.showinfo("Mensagem", "Você clicou no botão!")

janela = tk.Tk()
janela.title("Minha janela")
janela.geometry("1350x455")

def iniciar_desenho(event):
    # Declaração de variáveis globais para armazenar as coordenadas iniciais do mouse
    global x_inicial, y_inicial
    
    # Atribuição das coordenadas x e y do evento ao x_inicial e y_inicial
    x_inicial, y_inicial = event.x, event.y
    
    # Chamada da função desenhar() para iniciar o desenho da linha
    desenhar()

def atualizar_posicao(event):
    global x_atual, y_atual
    x_atual, y_atual = event.x, event.y  # Correção aqui
    canvas.delete(linha)
    desenhar()


def desenhar():
    # Declaração de variável global para a linha desenhada
    global linha, x_atual, y_atual
    
    # Criação da linha no canvas com base nas coordenadas inicial e atual do mouse
    linha = canvas.create_line(x_inicial, y_inicial, x_atual, y_atual)
    canvas.delete(linha_anterior)
    linha_anterior = linha

def terminar_desenho(event):
    canvas.delete(linha)

canvas = tk.Canvas(janela, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", iniciar_desenho)
canvas.bind("<Motion>", atualizar_posicao)  # Correção aqui
canvas.bind("ButtonRelease-1", terminar_desenho)

janela.mainloop()