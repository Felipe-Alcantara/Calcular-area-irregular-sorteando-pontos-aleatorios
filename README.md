# Calculando a Área de Formas Irregulares com Pontos Aleatórios

Este repositório contém um projeto em Python que permite ao usuário desenhar formas geométricas irregulares em uma interface gráfica e calcular suas áreas usando o método de Monte Carlo com pontos aleatórios. O projeto evoluiu através de três versões distintas:

1. **Versão Inicial (com Bugs)**
2. **Versão Corrigida**
3. **Versão Refatorada com Classes**

A seguir, detalhamos cada versão, explicando suas características, problemas identificados e melhorias implementadas.

---

## Índice

- [Introdução](#introdução)
- [Versão Inicial (com Bugs)](#versão-inicial-com-bugs)
  - [Descrição](#descrição)
  - [Problemas Identificados](#problemas-identificados)
- [Versão Corrigida](#versão-corrigida)
  - [Melhorias Implementadas](#melhorias-implementadas)
  - [Como os Problemas Foram Corrigidos](#como-os-problemas-foram-corrigidos)
- [Versão Refatorada com Classes](#versão-refatorada-com-classes)
  - [Refatoração Usando Programação Orientada a Objetos](#refatoração-usando-programação-orientada-a-objetos)
  - [Benefícios da Nova Estrutura](#benefícios-da-nova-estrutura)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Conclusão](#conclusão)

---

## Introdução

Este projeto tem como objetivo demonstrar como calcular a área de formas geométricas irregulares desenhadas pelo usuário, utilizando pontos aleatórios (método de Monte Carlo). O usuário pode desenhar uma forma na interface gráfica, e o programa estima a área dessa forma gerando pontos aleatórios dentro de um retângulo envolvente e verificando quais pontos estão dentro da forma.

O projeto passou por três versões, cada uma aprimorando a anterior em termos de funcionalidade, organização do código e usabilidade.

---

## Versão Inicial (com Bugs)

### Descrição

A primeira versão do projeto foi uma prova de conceito inicial, implementando a funcionalidade básica de desenho e cálculo de área. O usuário podia desenhar uma forma na metade inferior da janela, e o programa gerava pontos aleatórios para estimar a área.

**Características Principais:**

- Desenho de formas livres usando o mouse.
- Geração de pontos aleatórios dentro do retângulo envolvente.
- Cálculo da área baseado na proporção de pontos dentro da forma.

### Problemas Identificados

Apesar de funcional em certos aspectos, a versão inicial apresentava vários problemas que afetavam a execução e a usabilidade:

1. **Variáveis Globais Não Declaradas Adequadamente:**

   - Variáveis globais eram modificadas dentro de funções sem a declaração `global`, causando comportamentos inesperados.

2. **Loops Bloqueantes que Congelavam a Interface Gráfica:**

   - Uso de loops `while` bloqueantes na geração de pontos, impedindo que a interface respondesse a eventos do usuário.

3. **Condições de Parada Impraticáveis:**

   - A condição de parada da geração de pontos dependia de um evento improvável (geração de nenhum ponto fora da forma), resultando em loops infinitos.

4. **Atualização Inadequada da Estimativa de Área:**

   - A estimativa da área não era atualizada continuamente, deixando o usuário sem feedback sobre o cálculo.

5. **Inicialização e Reset de Variáveis Inconsistente:**

   - Variáveis não eram inicializadas corretamente ou redefinidas ao limpar o desenho, causando erros e estados inconsistentes.

6. **Estruturação Geral do Código:**

   - Código desorganizado, com funções e variáveis espalhadas, dificultando a leitura, manutenção e depuração.

---

## Versão Corrigida

### Melhorias Implementadas

A segunda versão do projeto abordou os problemas identificados na versão inicial, resultando em um código mais funcional e usável.

**Principais Melhorias:**

1. **Declaração Adequada de Variáveis Globais:**

   - Todas as variáveis globais foram declaradas explicitamente dentro das funções que as modificam, garantindo consistência no estado do programa.

2. **Uso do Método `after()` do Tkinter:**

   - Substituição dos loops bloqueantes pela função `after()`, permitindo que a interface gráfica permaneça responsiva durante a geração de pontos.

3. **Controle de Geração de Pontos pelo Usuário:**

   - Introdução de botões "Pausar" e "Retomar", permitindo que o usuário controle a geração de pontos.

4. **Atualização Contínua da Estimativa de Área:**

   - A estimativa da área do polígono é atualizada após cada lote de pontos gerados, proporcionando feedback imediato ao usuário.

5. **Inicialização e Reset Correto de Variáveis:**

   - Todas as variáveis são inicializadas e redefinidas adequadamente, especialmente ao limpar o desenho.

6. **Organização e Comentários no Código:**

   - O código foi reorganizado com funções bem definidas e comentários explicativos, melhorando a legibilidade e manutenção.

### Como os Problemas Foram Corrigidos

- **Variáveis Globais:**

  As variáveis globais foram declaradas dentro das funções usando a palavra-chave `global`, evitando conflitos e garantindo que o estado global fosse atualizado corretamente.

- **Loops Bloqueantes:**

  O uso do método `after()` do Tkinter permitiu agendar a geração de pontos sem bloquear o loop de eventos da interface gráfica.

- **Condições de Parada:**

  A condição de parada impraticável foi removida, e o controle de geração de pontos foi delegado ao usuário através dos botões de "Pausar" e "Retomar".

- **Atualização da Estimativa de Área:**

  A função de cálculo da área do polígono foi chamada após cada geração de pontos, atualizando a estimativa continuamente.

- **Inicialização de Variáveis:**

  Variáveis como `num_points` foram inicializadas corretamente, e todas as variáveis relevantes foram redefinidas na função de limpeza.

- **Estruturação do Código:**

  O código foi reorganizado, com funções agrupadas logicamente e nomes claros para variáveis e funções.

---

## Versão Refatorada com Classes

### Refatoração Usando Programação Orientada a Objetos

A terceira versão do projeto refatorou o código usando programação orientada a objetos (POO), encapsulando toda a funcionalidade dentro de uma classe.

**Características Principais:**

- **Criação da Classe `AreaCalculatorApp`:**

  - Todos os atributos (dados) e métodos (funções) foram encapsulados dentro da classe.

- **Eliminação de Variáveis Globais:**

  - Variáveis globais foram substituídas por atributos de instância, acessados via `self`.

- **Organização Modular:**

  - Métodos organizados por funcionalidade (eventos do mouse, geração de pontos, cálculo de áreas, atualização da interface).

- **Melhoria na Manutenção e Extensibilidade:**

  - O código orientado a objetos facilita a manutenção e expansão futura, permitindo adicionar novas funcionalidades com facilidade.

### Benefícios da Nova Estrutura

1. **Encapsulamento de Dados e Funções:**

   - Agrupamento lógico de dados e comportamentos relacionados, melhorando a organização do código.

2. **Redução de Erros:**

   - O uso de atributos de instância reduz o risco de conflitos e comportamentos inesperados associados a variáveis globais.

3. **Melhor Legibilidade e Manutenção:**

   - O código está mais limpo e fácil de entender, com responsabilidades bem definidas para cada método.

4. **Facilidade de Expansão:**

   - Novas funcionalidades podem ser adicionadas como métodos ou subclasses, sem impactar negativamente o restante do código.

5. **Uso de Boas Práticas de Programação:**

   - A adoção de POO segue padrões amplamente aceitos na engenharia de software, resultando em um código mais profissional.

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado em seu sistema.
- Biblioteca Tkinter (geralmente já incluída com a instalação padrão do Python).

### Passos para Execução

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/Felipe-Alcantara/Calcular-area-irregular-sorteando-pontos-aleatorios
   cd nome-do-repositorio
   ```

2. **Escolha a Versão:**

   - **Versão Inicial (com Bugs):** Arquivo `versao_inicial.py`
   - **Versão Corrigida:** Arquivo `versao_corrigida.py`
   - **Versão com Classes:** Arquivo `area_calculator_app.py`

3. **Execute o Arquivo Desejado:**

   ```bash
   python area_calculator_app.py
   ```

   *Substitua `area_calculator_app.py` pelo nome do arquivo da versão que deseja executar.*

### Utilização do Programa

1. **Desenhar a Forma:**

   - Clique e arraste o mouse na metade inferior da janela para desenhar o polígono.
   - Solte o botão do mouse para finalizar o desenho. O polígono será fechado automaticamente.

2. **Geração de Pontos:**

   - Após finalizar o desenho, o programa começará a gerar pontos aleatórios dentro do retângulo envolvente.
   - Pontos dentro do polígono são marcados em verde; pontos fora, em vermelho.

3. **Estimativa da Área:**

   - A área do retângulo envolvente e a estimativa da área do polígono são exibidas na tela em centímetros quadrados.

4. **Controles Adicionais:**

   - **Atualizar `num_points`:** Insira um novo valor no campo de entrada e clique em "Atualizar num_points" para alterar o número de pontos gerados por lote.
   - **Pausar/Retomar:** Use os botões "Pausar" e "Retomar" para controlar a geração de pontos.
   - **Limpar:** Clique no botão "Limpar" para resetar o desenho e começar novamente.

5. **Log de Eventos:**

   - As ações realizadas são registradas em um log exibido na interface, permitindo acompanhar o histórico de eventos.

---

## Conclusão

Este projeto demonstra a evolução de um aplicativo simples de cálculo de área, destacando a importância de práticas adequadas de programação e organização do código. A transição da versão inicial com bugs para uma versão corrigida e, posteriormente, para uma versão orientada a objetos, evidencia como melhorias estruturais podem impactar positivamente a funcionalidade, usabilidade e manutenção de um software.

**Aprendizados Chave:**

- **Gestão Adequada de Variáveis e Estados:**

  - A importância de declarar variáveis globais e gerenciar estados corretamente para evitar comportamentos inesperados.

- **Interface Gráfica Responsiva:**

  - Uso de métodos assíncronos, como `after()` no Tkinter, para manter a interface responsiva durante operações contínuas.

- **Programação Orientada a Objetos:**

  - Encapsulamento de funcionalidades em classes melhora a organização e facilita a expansão futura do código.

- **Feedback Contínuo ao Usuário:**

  - Atualização regular de informações, como a estimativa de área, melhora a experiência do usuário.

Esperamos que este projeto seja útil como referência para desenvolvedores interessados em interfaces gráficas, cálculos geométricos e boas práticas de programação em Python.

---

**Autor:** Felipe Alcântara Martins (melhorias com ChatGPT)

**Licença:** [MIT](LICENSE)