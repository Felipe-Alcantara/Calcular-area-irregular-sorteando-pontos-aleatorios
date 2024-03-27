# Calcular-area-irregular-sorteando-pontos-aleatorios
 Esses códigos são parte de um programa de desenho interativo que permite ao usuário criar formas na tela usando o mouse e calcular a área desse desenho.  Esses códigos demonstram como a biblioteca tkinter do Python pode ser usada para criar programas de desenho interativos. Eles também mostram como os eventos do mouse podem ser usados para controlar o desenho.

1. **Desenhar linhas**: Este código permite ao usuário desenhar linhas na tela arrastando o mouse. As linhas são desenhadas entre o ponto onde o botão do mouse foi pressionado e o ponto onde o botão do mouse foi solto.

1. Primeiro, ele importa a biblioteca `tkinter` e define algumas variáveis globais que serão usadas para armazenar as coordenadas do mouse e a linha atualmente sendo desenhada.

2. A função `iniciar_desenho(event)` é chamada quando o botão esquerdo do mouse é pressionado. Ela armazena as coordenadas atuais do mouse nas variáveis `x_inicial` e `y_inicial` e chama a função `desenhar()`.

3. A função `atualizar_posicao(event)` é chamada quando o mouse é movido enquanto o botão esquerdo está pressionado. Ela atualiza as coordenadas atuais do mouse e deleta a linha anteriormente desenhada antes de chamar a função `desenhar()` novamente.

4. A função `desenhar()` desenha uma linha da posição inicial do mouse para a posição atual e deleta a linha anteriormente desenhada.

5. O código então cria uma janela `tkinter` e um `canvas` onde as linhas serão desenhadas.

6. O código vincula os eventos do mouse às funções apropriadas, para que quando o usuário pressione o botão esquerdo do mouse, mova o mouse enquanto o botão está pressionado, ou solte o botão do mouse, as funções correspondentes sejam chamadas.

7. Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa simples de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar linhas na tela arrastando o mouse. Aqui está o que cada parte do código faz:


2. **Desenhar retas usando o mesmo ponto**: Este código é uma extensão do primeiro, permitindo ao usuário desenhar múltiplas linhas a partir de um único ponto de partida. As linhas são desenhadas entre o ponto onde o botão do mouse foi pressionado pela primeira vez e o ponto onde o mouse está atualmente.

1. Ele define uma função `mostrar_mensagem()` que exibe uma caixa de mensagem quando chamada. No entanto, esta função não é usada no restante do código.

2. Ele cria uma janela `tkinter` com um título e um tamanho específico.

3. Ele cria um `canvas` onde as linhas serão desenhadas. O `canvas` é configurado para preencher toda a janela e se expandir conforme a janela é redimensionada.

4. Ele vincula os eventos do mouse às funções apropriadas. Quando o usuário pressiona o botão esquerdo do mouse, a função `iniciar_desenho(event)` é chamada. Quando o mouse é movido, a função `atualizar_posicao(event)` é chamada. Quando o botão esquerdo do mouse é solto, a função `terminar_desenho(event)` é chamada.

5. A função `iniciar_desenho(event)` armazena as coordenadas iniciais do mouse e chama a função `desenhar()`.

6. A função `atualizar_posicao(event)` atualiza as coordenadas atuais do mouse, deleta a linha anteriormente desenhada e chama a função `desenhar()` novamente.

7. A função `desenhar()` desenha uma linha da posição inicial do mouse para a posição atual e deleta a linha anteriormente desenhada.

8. A função `terminar_desenho(event)` deleta a linha que está sendo desenhada quando o botão esquerdo do mouse é solto.

9. Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é uma extensão do primeiro código. Ele também é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. No entanto, este código tem algumas funcionalidades adicionais:

3. **Tela dividida desenhando retângulo para calcular a área**: Este código divide a tela em duas partes e permite ao usuário desenhar retângulos na parte inferior da tela. Ele calcula e desenha um retângulo delimitador ao redor das linhas desenhadas quando o botão do mouse é solto.

1. Primeiro, ele importa a biblioteca `tkinter`.

2. A função `iniciar_desenho(event)` é chamada quando o botão esquerdo do mouse é pressionado. Ela armazena as coordenadas atuais do mouse em uma lista chamada `coordenadas`.

3. A função `desenhar_rastro(event)` é chamada quando o mouse é movido enquanto o botão esquerdo está pressionado. Ela adiciona as coordenadas atuais do mouse à lista `coordenadas` e desenha uma linha entre as duas últimas coordenadas na lista.

4. A função `limpar_rastro(event)` é chamada quando o botão esquerdo do mouse é solto. Ela cria um retângulo que envolve todas as linhas desenhadas e, em seguida, limpa a lista `coordenadas`.

5. A função `mostrar_coordenadas(event)` é chamada sempre que o mouse é movido. Ela atualiza um rótulo na janela para mostrar as coordenadas atuais do mouse.

6. O código então cria uma janela `tkinter` e três `canvas` onde as linhas serão desenhadas. Dois dos `canvas` são empacotados à esquerda e à direita, respectivamente, e o terceiro `canvas` é empacotado para preencher o restante do espaço na janela.

7. O código vincula os eventos do mouse às funções apropriadas, para que quando o usuário pressione o botão esquerdo do mouse, mova o mouse enquanto o botão está pressionado, ou solte o botão do mouse, as funções correspondentes sejam chamadas.

8. Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar retângulos na tela arrastando o mouse.

4. **Tela separada + desenho com retângulo funcionando**: Este código é uma extensão do terceiro, adicionando a funcionalidade de desenhar retângulos na tela. Ele também exibe as coordenadas atuais do mouse na tela.

1. Primeiro, ele importa a biblioteca `tkinter`.

2. A função `stroke_line(x1, y1, x2, y2)` é definida para desenhar uma linha no canvas.

3. Ele inicializa a janela e o canvas.

4. Ele define algumas configurações iniciais, como a metade da largura e altura da tela, uma variável `is_drawing` para rastrear se o usuário está atualmente desenhando, e uma lista `points` para armazenar as coordenadas dos pontos desenhados.

5. Ele desenha uma linha horizontal no meio da tela.

6. Ele cria um texto vazio no canvas para mostrar as coordenadas do mouse.

7. Ele define várias funções para lidar com eventos do mouse:
    - `on_mouse_down(event)`: Esta função é chamada quando o botão esquerdo do mouse é pressionado. Ela verifica se o mouse está na metade inferior da tela e, em caso afirmativo, define `is_drawing` como True e adiciona as coordenadas do mouse à lista `points`.
    - `on_mouse_move(event)`: Esta função é chamada quando o mouse se move. Ela atualiza o texto das coordenadas do mouse e, se o mouse estiver na metade inferior da tela e `is_drawing` for True, adiciona as coordenadas do mouse à lista `points` e desenha uma linha entre o último e o penúltimo ponto.
    - `on_mouse_up(event)`: Esta função é chamada quando o botão esquerdo do mouse é solto. Ela define `is_drawing` como False, desenha uma linha do último ponto para o primeiro ponto na lista `points`, calcula o retângulo delimitador que envolve todos os pontos na lista `points`, desenha esse retângulo e limpa a lista `points`.

8. Ele associa os eventos do mouse às funções correspondentes.

9. Finalmente, ele entra no loop principal do `tkinter` com `root.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar retângulos na tela arrastando o mouse.

Esses códigos demonstram como a biblioteca `tkinter` do Python pode ser usada para criar programas de desenho interativos. Eles também mostram como os eventos do mouse podem ser usados para controlar o desenho.