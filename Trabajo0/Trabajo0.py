#! /usr/bin/python3
# Autor: Pablo Baeyens Fernández
# Asignatura: Visión por Computador
# Uso: ./trabajo0.py [nombre imagen de ejemplo]

import cv2
import sys, os.path
import numpy as np

# Ejercicio 1

def leeimagen(filename, flagColor):
  """Lee una imagen y la muestra (tanto en grises como en color)
    - filename: nombre del fichero
    - flagColor: flag que indica si tiene color o no"""

  return cv2.imread(filename, flagColor)


# Ejercicio 2

def pintaI(im, titulo = "Imagen"):
  """Visualiza una matriz de números reales cualquiera
     - im: Imagen a visualizar"""

  cv2.imshow(titulo, im)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


# Ejercicio 3

## ¿Qué pasa si las imágenes no son todas del mismo tipo?
## Respuesta: Si no hacemos un procesamiento previo de las imágenes falla.
## Tenemos que convertir las imágenes en blanco y negro a color

def isBW(im):
  """Indica si una imagen está en blanco y negro"""
  return len(im.shape) == 2

def pintaMI(vim, titulo = "Imágenes"):
  """Visualiza varias imágenes a la vez
  - vim: Secuencia de imágenes"""

  altura = max(im.shape[0] for im in vim)

  for i,im in enumerate(vim):
    if isBW(im): # Pasar a color
      vim[i] = cv2.cvtColor(vim[i], cv2.COLOR_GRAY2BGR)

    if im.shape[0] < altura: # Redimensionar imágenes
      vim[i] = cv2.copyMakeBorder(
        vim[i], 0, altura - vim[i].shape[0],
        0, 0, cv2.BORDER_CONSTANT, value = (0,0,0))

  imMulti = cv2.hconcat(vim)
  pintaI(imMulti, titulo)


# Ejercicio 4

def modPixeles(im, pixels):
  """Modifica el color de cada elemento de una lista de coordenadas
  - im: Imagen
  - pixels: lista de coordenadas
  """
  negro = (0,0,0)

  if isBW(im):
    negro = 0

  for pixel in pixels:
    im[pixel] = negro

# Ejercicio 5

def representaIm(vim, titulos):
  """Representa varias imágenes con sus títulos en una ventana"""
  pintaMI(vim, titulo = " | ".join(titulos))



if __name__ == "__main__":
  """Tests de ejemplo"""

  if len(sys.argv) < 2:
    print("Uso: {0} [fichero imagen ejemplo]".format(sys.argv[0]))
    exit()

  fim = sys.argv[1]
  if(not os.path.isfile(fim)):
    print("No existe el fichero {0}".format(fim))
    exit()

  print("Leyendo imágenes (Ejercicio 1)")
  imColor = leeimagen(fim, cv2.IMREAD_COLOR)
  imBN    = leeimagen(fim, cv2.IMREAD_GRAYSCALE)

  vim = [imColor, imBN]
  tit = ["Imagen en color", "Imagen en B/N"]

  print("Muestra imagen   (Ejercicio 2)")
  pintaI(vim[0], titulo = "Ejercicio 2 color")
  pintaI(vim[1], titulo = "Ejercicio 2 BN")

  print("Muestra imágenes (Ejercicio 3)")
  pintaMI(vim, titulo = "Ejercicio 3")

  print("Modifica píxeles (Ejercicio 4). Resultado mostrado en ejercicio 5")
  # Modifico los píxeles de la mitad superior de la imagen
  modificada = np.copy(imColor)
  altura, anchura, _ = modificada.shape
  modPixeles(modificada,
             [(x,y) for x in range(int(altura/2)) for y in range(anchura)])

  print("Representa imágenes con títulos en una ventana (Ejercicio 5)")
  representaIm(vim + [modificada], tit + ["Imagen modificada"])
