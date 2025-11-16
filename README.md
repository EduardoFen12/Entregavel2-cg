# Entregavel2-cg

## Integrantes: 
* Eduardo Garcia Fensterseifer 
* Guilherme Beno kemmer Dalmoro
* Livia Souza da Silva

## Elevator Pitch:
O Entregável 2 é uma aplicação de Computação Gráfica que demonstra o poder do processamento paralelo de imagens utilizando a pipeline programável da GPU (OpenGL/GLSL). Ele permite aplicar filtros de convolução 3x3 (como Blur, Sharpen, Emboss e Detecção de Bordas) em uma textura 3D em tempo real. O sistema é controlado pelo teclado e mouse, permitindo a navegação no espaço 3D (matrizes MVP) e a alternância instantânea entre diferentes kernels para uma visualização imediata e eficiente do efeito na imagem.

## Como Rodar o Projeto:
Para executar a aplicação, você precisará de uma máquina com suporte a OpenGL 3.3+ e as seguintes dependências em Python.

### Requisitos
O projeto utiliza bibliotecas comuns para gráficos e visão computacional, como:

* numpy
* PyOpenGL (módulos OpenGL.GL e ctypes)
* glfw
* Pillow (PIL.Image)
* opencv-python (cv2) (Opcional: usado apenas para o arquivo de comparação conv_opencv_G2.py)

> pip install numpy PyOpenGL glfw Pillow

### Instruções de Execução
1. Organização: Certifique-se de que todos os arquivos do repositório (main.py, Fragment_shader.glsl, vertex_shader.glsl, fps_counter.py e a imagem templo.jpg) estão no mesmo diretório.
2. Execução: Execute o arquivo principal a partir do seu terminal:
> python main.py

## Descrição das Funcionalidades
O projeto combina navegação 3D com a aplicação de filtros de imagem via Fragment Shader (convolução).

### Funcionalidades de Processamento de Imagem

### Controles de Navegação e Câmera
