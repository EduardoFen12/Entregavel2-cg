import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
from PIL import Image

LARGURA_JANELA, ALTURA_JANELA = 800, 600
CAMINHO_IMAGEM = r"./../templo.jpg"


id_textura = None
local_tamanho_texel = None
local_kernel = None
local_indice_kernel = None
local_modo_cinza = None

indice_kernel = 0
modo_cinza = False

def carregar_textura(caminho):
    imagem = Image.open(caminho).convert("RGB")
    largura, altura = imagem.size
    dados = imagem.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, dados)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura, largura, altura, dados

def teclado_callback(janela, tecla, scancode, acao, mods):
    global indice_kernel
    if acao == glfw.PRESS:
        if tecla == glfw.KEY_1: indice_kernel = 1
        elif tecla == glfw.KEY_2: indice_kernel = 2
        elif tecla == glfw.KEY_3: indice_kernel = 3
        elif tecla == glfw.KEY_4: indice_kernel = 4
        elif tecla == glfw.KEY_5: indice_kernel = 5
        elif tecla == glfw.KEY_0: indice_kernel = 0

def mouse_callback(janela, botao, acao, mods):
    global modo_cinza, id_textura
    if botao == glfw.MOUSE_BUTTON_LEFT and acao == glfw.PRESS:
        modo_cinza = not modo_cinza
    if botao == glfw.MOUSE_BUTTON_RIGHT and acao == glfw.PRESS:
        global indice_kernel
        indice_kernel = 0


def compilar_shader(codigo, tipo_shader):
    shader = glCreateShader(tipo_shader)
    glShaderSource(shader, codigo)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def ligar_programa(shader_vertices, shader_fragmento):
    programa = glCreateProgram()
    glAttachShader(programa, shader_vertices)
    glAttachShader(programa, shader_fragmento)
    glLinkProgram(programa)
    if not glGetProgramiv(programa, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(programa).decode())
    return programa

def main():
    global programa_shader, VAO_quadrado, VBO_quadrado, id_textura, local_tamanho_texel, local_kernel, local_indice_kernel, local_modo_cinza, largura_textura, altura_textura

    if not glfw.init():
        raise SystemExit("Falha ao iniciar GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 0)

    janela = glfw.create_window(LARGURA_JANELA, ALTURA_JANELA, "Kernels - Templo", None, None)
    if not janela:
        glfw.terminate()
        raise SystemExit("Falha ao criar janela")
    glfw.make_context_current(janela)
    glfw.swap_interval(0)

    glfw.set_key_callback(janela, teclado_callback)
    glfw.set_mouse_button_callback(janela, mouse_callback)

    vertices_quadrado = np.array([
        -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
        -1.0, -1.0, 0.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
        -1.0,  1.0, 0.0, 1.0,
    ], dtype=np.float32)

    VAO_quadrado = glGenVertexArrays(1)
    VBO_quadrado = glGenBuffers(1)
    glBindVertexArray(VAO_quadrado)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_quadrado)
    glBufferData(GL_ARRAY_BUFFER, vertices_quadrado.nbytes, vertices_quadrado, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(2*4))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    with open("vertex_shader.glsl", "r") as f:
        codigo_vs = f.read()
    with open("fragment_shader.glsl", "r") as f:
        codigo_fs = f.read()
    shader_vs = compilar_shader(codigo_vs, GL_VERTEX_SHADER)
    shader_fs = compilar_shader(codigo_fs, GL_FRAGMENT_SHADER)
    programa_shader = ligar_programa(shader_vs, shader_fs)
    glDeleteShader(shader_vs)
    glDeleteShader(shader_fs)

    glUseProgram(programa_shader)
    local_tamanho_texel = glGetUniformLocation(programa_shader, "texelSize")
    local_kernel = glGetUniformLocation(programa_shader, "kernel")
    local_indice_kernel = glGetUniformLocation(programa_shader, "kernelIndex")
    local_modo_cinza = glGetUniformLocation(programa_shader, "grayMode")

    global imagem_original
    id_textura, largura_textura, altura_textura, imagem_original = carregar_textura(CAMINHO_IMAGEM)

    glUniform2f(local_tamanho_texel, 1.0/largura_textura, 1.0/altura_textura)
    glUniform1i(local_indice_kernel, 0)
    glUniform1i(local_modo_cinza, 0)
    glUseProgram(0)

    glActiveTexture(GL_TEXTURE0)

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(programa_shader)

        if indice_kernel == 0:
            matriz_kernel = np.array([0,0,0,
                                      0,1,0,
                                      0,0,0], dtype=np.float32)
        elif indice_kernel == 1:
            matriz_kernel = np.array([1,1,1,
                                      1,1,1,
                                      1,1,1], dtype=np.float32)/9.0
        elif indice_kernel == 2:
            matriz_kernel = np.array([0,-1,0,
                                      -1,5,-1,
                                      0,-1,0], dtype=np.float32)
        elif indice_kernel == 3:
            matriz_kernel = np.array([-2,-1,0,
                                      -1,1,1,
                                      0,1,2], dtype=np.float32)
        elif indice_kernel == 4:
            matriz_kernel = np.array([-1,-1,-1,
                                      0,0,0,
                                      1,1,1], dtype=np.float32)
        elif indice_kernel == 5:
            matriz_kernel = np.array([1,0,-1,
                                      1,0,-1,
                                      1,0,-1], dtype=np.float32)
        else:
            matriz_kernel = np.array([0,0,0,
                                      0,1,0,
                                      0,0,0], dtype=np.float32)

        glUniform1fv(local_kernel, 9, matriz_kernel)
        glUniform1i(local_indice_kernel, indice_kernel)
        glUniform1i(local_modo_cinza, int(modo_cinza))

        glBindVertexArray(VAO_quadrado)
        glBindTexture(GL_TEXTURE_2D, id_textura)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

        glUseProgram(0)
        glfw.swap_buffers(janela)

    glDeleteVertexArrays(1, [VAO_quadrado])
    glDeleteBuffers(1, [VBO_quadrado])
    glDeleteTextures(1, [id_textura])
    glDeleteProgram(programa_shader)

    glfw.destroy_window(janela)
    glfw.terminate()

if __name__ == "__main__":
    main()