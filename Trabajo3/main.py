#! /usr/bin/python3
# Autor: Pablo Baeyens
# Uso: ./main.py

import cv2 as cv
import numpy as np
import math
import collections
import random
import auxFunc

#########################
# PARÁMETROS AJUSTABLES #
#   Y CONSTANTES        #
#########################

PATH = "imagenes/" # Carpeta de imágenes
COLOR, GRIS = cv.IMREAD_COLOR, cv.IMREAD_GRAYSCALE

# Objetos SIFT y SURF con parámetros elegidos
SIFT = cv.xfeatures2d.SIFT_create(contrastThreshold = 0.04, edgeThreshold = 5)
SURF = cv.xfeatures2d.SURF_create(hessianThreshold = 200)

########################
# FUNCIONES AUXILIARES #
########################

def espera():
  """Función para introducir una espera"""
  input("[Enter para continuar]")

# Del trabajo 0

def leeimagen(filename, flagColor):
  """Lee una imagen y la muestra (tanto en grises como en color)
    - filename: nombre del fichero
    - flagColor: flag que indica si tiene color o no"""

  return cv.imread(filename, flagColor)

def pintaI(im, titulo = "Imagen"):
  """Visualiza una matriz de números reales cualquiera
     - im: Imagen a visualizar"""
  cv.imshow(titulo, im)
  cv.waitKey(0)
  cv.destroyAllWindows()

def isBW(im):
  """Indica si una imagen está en blanco y negro"""
  return len(im.shape) == 2

def muestraMI(vim, titulo = "Imágenes"):
  """Visualiza varias imágenes a la vez
  - vim: Secuencia de imágenes"""

  altura = max(im.shape[0] for im in vim)

  for i,im in enumerate(vim):
    if isBW(im): # Pasar a color
      vim[i] = cv.cvtColor(vim[i], cv.COLOR_GRAY2BGR)

    if im.shape[0] < altura: # Redimensionar imágenes
      borde = int((altura - vim[i].shape[0])/2)
      vim[i] = cv.copyMakeBorder(
        vim[i], borde, borde + (altura - vim[i].shape[0]) % 2,
        0, 0, cv.BORDER_CONSTANT, value = (0,0,0))

  imMulti = cv.hconcat(vim)
  pintaI(imMulti, titulo)


def pintaMI(*parejas):
  """Representa varias imágenes con sus títulos en una ventana
  - parejas: lista de pares (imagen, título)
  """

  vim, titulos = zip(*parejas)
  muestraMI(list(vim), titulo = " | ".join(titulos))


###########################
# FUNCIONES DEL TRABAJO 2 #
###########################

def ap2A_LA2NN(d_im1, d_im2, ratio = 0.8):
  """Obtiene correspondencias entre descriptores.
  Usa el método 'Lowe-Average-2NN'.
  Argumentos posicionales:
  - d_im1, d_im2: Descriptores de cada imagen
  Argumentos opcionales:
  - ratio: El ratio usado para descartar correspondencias ambiguas. Por defecto 0.8
  Devuelve: Correspondencias"""

  # Declara el matcher
  matcher = cv.FlannBasedMatcher_create()

  # Obten las dos mejores correspondencias de cada punto
  matches = matcher.knnMatch(d_im1, d_im2, k = 2)

  # Toma las correspondencias que no sean ambiguas de acuerdo al test dado por Lowe
  clear_matches = []
  for best, second in matches:
    if best.distance/second.distance < ratio:
      clear_matches.append(best)

  return clear_matches


##############
# EJERCICIOS #
##############

## Ejercicio 1

def ej1(im1, im2):
  """Selecciona región de una imagen y pinta sus correspondencias con otra imagen."""
  print("Extrae la región de la corbata")
  points = np.array(auxFunc.extractRegion(im1))
  mask = np.zeros(im1.shape)
  cv.fillConvexPoly(mask, points, (256, 256, 256))
  pintaI(mask)

def ejemplo1(parejas):
  """Selecciona región """
  for im1, im2 in parejas:
    ej1(im1, im2)

def main():
  """Llama de forma secuencial a la función de cada apartado."""
  friends = []
  N = 5 #441
  for n in range(N):
     friends.append(leeimagen(PATH + "{n}.png".format(n = n), COLOR))

  ejemplo1([(friends[0], friends[2])])

if __name__ == "__main__":
  main()
