import cv2
import numpy as np
import time

img = cv2.imread('templo.jpg')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

blur = np.array([[1, 1, 1],
                 [1, 1, 1],
                 [1, 1, 1]])

sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])

emboss = np.array([[-2, -1, 0],
                   [-1, 1, 1],
                   [0, 1, 2]])

boost = np.array([[0, -1, 0],
                  [-1, 5, -1],
                  [0, -1, 0]])

bordas = np.array([[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]])

def aplicar_kernel(img, kernel):
    return cv2.filter2D(img, -1, kernel)

start_time = time.time()
r_blur = aplicar_kernel(img, blur)
print(f"{(time.time() - start_time)} segundos blur")

start_time = time.time()
r_sharpen = aplicar_kernel(img, sharpen)
print(f"{(time.time() - start_time)} segundos sharpen")

start_time = time.time()
r_emboss = aplicar_kernel(img, emboss)
print(f"{(time.time() - start_time)} segundos emboss")

start_time = time.time()
r_boost = aplicar_kernel(img, boost)
print(f"{(time.time() - start_time)} segundos boost")

start_time = time.time()
r_bordas = aplicar_kernel(img, bordas)
print(f"{(time.time() - start_time)} segundos bordas")



cv2.imshow('Imagem Original', img)
cv2.imshow('Blur', r_blur)
cv2.imshow('Sharpen', r_sharpen)
cv2.imshow('Emboss', r_emboss)
cv2.imshow('Boost', r_boost)
cv2.imshow('Bordas', r_bordas)


cv2.waitKey(0)
cv2.destroyAllWindows()
