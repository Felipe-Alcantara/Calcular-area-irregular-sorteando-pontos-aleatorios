# Calcular Área Irregular Sorteando Pontos Aleatórios

Este repositório contém códigos que fazem parte de um programa de desenho interativo. Ele permite ao usuário criar formas na tela usando o mouse e calcular a área desses desenhos. Os códigos demonstram como a biblioteca `tkinter` do Python pode ser usada para criar programas de desenho interativos e como os eventos do mouse podem ser usados para controlar o desenho.

## Desenhar Linhas

Este código permite ao usuário desenhar linhas na tela arrastando o mouse. As linhas são desenhadas entre o ponto onde o botão do mouse foi pressionado e o ponto onde o botão do mouse foi solto.

### Como Funciona

1. **Importação e Definição de Variáveis**: Primeiro, o código importa a biblioteca `tkinter` e define algumas variáveis globais que serão usadas para armazenar as coordenadas do mouse e a linha atualmente sendo desenhada.

2. **Iniciar Desenho**: A função `iniciar_desenho(event)` é chamada quando o botão esquerdo do mouse é pressionado. Ela armazena as coordenadas atuais do mouse nas variáveis `x_inicial` e `y_inicial` e chama a função `desenhar()`.

3. **Atualizar Posição**: A função `atualizar_posicao(event)` é chamada quando o mouse é movido enquanto o botão esquerdo está pressionado. Ela atualiza as coordenadas atuais do mouse e deleta a linha anteriormente desenhada antes de chamar a função `desenhar()` novamente.

4. **Desenhar**: A função `desenhar()` desenha uma linha da posição inicial do mouse para a posição atual e deleta a linha anteriormente desenhada.

5. **Criação de Janela e Canvas**: O código então cria uma janela `tkinter` e um `canvas` onde as linhas serão desenhadas.

6. **Vinculação de Eventos**: O código vincula os eventos do mouse às funções apropriadas, para que quando o usuário pressione o botão esquerdo do mouse, mova o mouse enquanto o botão está pressionado, ou solte o botão do mouse, as funções correspondentes sejam chamadas.

7. **Loop Principal**: Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa simples de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar linhas na tela arrastando o mouse. Cada parte do código tem uma função específica para garantir o funcionamento correto do programa.

## Desenhar Retas Usando o Mesmo Ponto

Este código é uma extensão do primeiro, permitindo ao usuário desenhar múltiplas linhas a partir de um único ponto de partida. As linhas são desenhadas entre o ponto onde o botão do mouse foi pressionado pela primeira vez e o ponto onde o mouse está atualmente.

### Como Funciona

1. **Mostrar Mensagem**: Ele define uma função `mostrar_mensagem()` que exibe uma caixa de mensagem quando chamada. No entanto, esta função não é usada no restante do código.

2. **Criação de Janela**: Ele cria uma janela `tkinter` com um título e um tamanho específico.

3. **Criação de Canvas**: Ele cria um `canvas` onde as linhas serão desenhadas. O `canvas` é configurado para preencher toda a janela e se expandir conforme a janela é redimensionada.

4. **Vinculação de Eventos**: Ele vincula os eventos do mouse às funções apropriadas. Quando o usuário pressiona o botão esquerdo do mouse, a função `iniciar_desenho(event)` é chamada. Quando o mouse é movido, a função `atualizar_posicao(event)` é chamada. Quando o botão esquerdo do mouse é solto, a função `terminar_desenho(event)` é chamada.

5. **Iniciar Desenho**: A função `iniciar_desenho(event)` armazena as coordenadas iniciais do mouse e chama a função `desenhar()`.

6. **Atualizar Posição**: A função `atualizar_posicao(event)` atualiza as coordenadas atuais do mouse, deleta a linha anteriormente desenhada e chama a função `desenhar()` novamente.

7. **Desenhar**: A função `desenhar()` desenha uma linha da posição inicial do mouse para a posição atual e deleta a linha anteriormente desenhada.

8. **Terminar Desenho**: A função `terminar_desenho(event)` deleta a linha que está sendo desenhada quando o botão esquerdo do mouse é solto.

9. **Loop Principal**: Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é uma extensão do primeiro código. Ele também é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. No entanto, este código tem algumas funcionalidades adicionais.

## Tela Dividida Desenhando Retângulo para Calcular a Área

Este código divide a tela em duas partes e permite ao usuário desenhar retângulos na parte inferior da tela. Ele calcula e desenha um retângulo delimitador ao redor das linhas desenhadas quando o botão do mouse é solto.

### Como Funciona

1. **Importação**: Primeiro, ele importa a biblioteca `tkinter`.

2. **Iniciar Desenho**: A função `iniciar_desenho(event)` é chamada quando o botão esquerdo do mouse é pressionado. Ela armazena as coordenadas atuais do mouse em uma lista chamada `coordenadas`.

3. **Desenhar Rastro**: A função `desenhar_rastro(event)` é chamada quando o mouse é movido enquanto o botão esquerdo está pressionado. Ela adiciona as coordenadas atuais do mouse à lista `coordenadas` e desenha uma linha entre as duas últimas coordenadas na lista.

4. **Limpar Rastro**: A função `limpar_rastro(event)` é chamada quando o botão esquerdo do mouse é solto. Ela cria um retângulo que envolve todas as linhas desenhadas e, em seguida, limpa a lista `coordenadas`.

5. **Mostrar Coordenadas**: A função `mostrar_coordenadas(event)` é chamada sempre que o mouse é movido. Ela atualiza um rótulo na janela para mostrar as coordenadas atuais do mouse.

6. **Criação de Janela e Canvas**: O código então cria uma janela `tkinter` e três `canvas` onde as linhas serão desenhadas. Dois dos `canvas` são empacotados à esquerda e à direita, respectivamente, e o terceiro `canvas` é empacotado para preencher o restante do espaço na janela.

7. **Vinculação de Eventos**: O código vincula os eventos do mouse às funções apropriadas, para que quando o usuário pressione o botão esquerdo do mouse, mova o mouse enquanto o botão está pressionado, ou solte o botão do mouse, as funções correspondentes sejam chamadas.

8. **Loop Principal**: Finalmente, o código entra no loop principal do `tkinter` com `janela.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar retângulos na tela arrastando o mouse.

## Tela Separada + Desenho com Retângulo Funcionando

Este código é uma extensão do terceiro, adicionando a funcionalidade de desenhar retângulos na tela. Ele também exibe as coordenadas atuais do mouse na tela.

### Como Funciona

1. **Importação**: Primeiro, ele importa a biblioteca `tkinter`.

2. **Função Stroke Line**: A função `stroke_line(x1, y1, x2, y2)` é definida para desenhar uma linha no canvas.

3. **Inicialização de Janela e Canvas**: Ele inicializa a janela e o canvas.

4. **Configurações Iniciais**: Ele define algumas configurações iniciais, como a metade da largura e altura da tela, uma variável `is_drawing` para rastrear se o usuário está atualmente desenhando, e uma lista `points` para armazenar as coordenadas dos pontos desenhados.

5. **Desenho de Linha Horizontal**: Ele desenha uma linha horizontal no meio da tela.

6. **Criação de Texto Vazio**: Ele cria um texto vazio no canvas para mostrar as coordenadas do mouse.

7. **Funções de Eventos do Mouse**: Ele define várias funções para lidar com eventos do mouse:
    - `on_mouse_down(event)`: Esta função é chamada quando o botão esquerdo do mouse é pressionado. Ela verifica se o mouse está na metade inferior da tela e, em caso afirmativo, define `is_drawing` como True e adiciona as coordenadas do mouse à lista `points`.
    - `on_mouse_move(event)`: Esta função é chamada quando o mouse se move. Ela atualiza o texto das coordenadas do mouse e, se o mouse estiver na metade inferior da tela e `is_drawing` for True, adiciona as coordenadas do mouse à lista `points` e desenha uma linha entre o último e o penúltimo ponto.
    - `on_mouse_up(event)`: Esta função é chamada quando o botão esquerdo do mouse é solto. Ela define `is_drawing` como False, desenha uma linha do último ponto para o primeiro ponto na lista `points`, calcula o retângulo delimitador que envolve todos os pontos na lista `points`, desenha esse retângulo e limpa a lista `points`.

8. **Associação de Eventos**: Ele associa os eventos do mouse às funções correspondentes.

9. **Loop Principal**: Finalmente, ele entra no loop principal do `tkinter` com `root.mainloop()`, que mantém a janela aberta e responde aos eventos do mouse.

Este código é um programa de desenho que usa a biblioteca `tkinter` do Python para criar uma interface gráfica. Ele permite ao usuário desenhar retângulos na tela arrastando o mouse. Estes códigos demonstram como a biblioteca `tkinter` do Python pode ser usada para criar programas de desenho interativos e como os eventos do mouse podem ser usados para controlar o desenho.