#! /usr/bin/python3
# Autor: Pablo Baeyens
# Uso: ./main.py

import cv2 as cv
import numpy as np
import math
import collections
import random

#########################
# PARÁMETROS AJUSTABLES #
#   Y CONSTANTES        #
#########################

PATH = "imagenes/" # Carpeta de imágenes
COLOR, GRIS = cv.IMREAD_COLOR, cv.IMREAD_GRAYSCALE

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

###############
# EJERCICIO 1 #
###############

## 1 A)

def ap1A(im, tipo,  **kwargs):
  """Detecta puntos SIFT o SURF sobre una imagen.
  Argumentos posicionales:
  - im: Imagen
  - tipo: El tipo de detector ("SIFT" o "SURF")
  Argumentos opcionales:
  - Cualquiera que podamos pasarle a la función `cv.xfeatures2d.SIFT_create` (o `cv.xfeatures2d.SURF_create`)
  Devuelve:
  - Los puntos detectados
  """
  if tipo == "SIFT":
    sift   = cv.xfeatures2d.SIFT_create(**kwargs)
    return sift.detect(im)
  elif tipo == "SURF":
    surf   = cv.xfeatures2d.SURF_create(**kwargs)
    return surf.detect(im)

def ej1A(im):
  """Ejemplo de prueba del apartado 1A."""
  pass


## 1 B)

def getOctave(kp):
  """ Obtiene octava de un keypoint de SIFT
  Argumentos posicionales:
  - kp: punto detectado por SIFT
  Devuelve:
  - Octava

  Nota: Esta función reimplementa la función `unpackOctave` de OpenCV
  https://github.com/opencv/opencv_contrib/blob/master/modules/xfeatures2d/src/sift.cpp#L214
  """
  octave = kp.octave & 255
  octave = octave if octave < 128 else (-128 | octave)
  return octave


def getLayer(kp):
  """ Obtiene capa de un keypoint de SIFT
  Argumentos posicionales:
  - kp: punto detectado por SIFT
  Devuelve:
  - capa

  Nota: Esta función reimplementa la función `unpackOctave` de OpenCV
  https://github.com/opencv/opencv_contrib/blob/master/modules/xfeatures2d/src/sift.cpp#L214
  """
  layer = (kp.octave >> 8) & 255
  return layer


def ap1B_octave(keypoints, tipo):
  """Identifica puntos en cada octava.
  Argumentos posicionales:
  - keypoints: Puntos
  - tipo: El tipo de puntos ("SIFT" o "SURF")
  Devuelve:
  - Lista de pares (octava, cantidad)
  """
  # cnt es un contador: diccionario con valor 0 por defecto.
  cnt = collections.Counter()

  if tipo == "SIFT":
    for kp in keypoints:
      cnt[getOctave(kp)] += 1
  elif tipo == "SURF":
    for kp in keypoints:
      cnt[kp.octave] += 1

  return sorted(cnt.items())


def ap1B_layer(keypoints):
  """Identifica puntos en cada capa (sólo SIFT).
  Argumentos posicionales:
  - keypoints: Puntos
  Devuelve:
  - Lista de pares (capa, cantidad)
  """
  # cnt es un contador: diccionario con valor 0 por defecto.
  cnt = collections.Counter()
  for kp in keypoints:
    cnt[getLayer(kp)] += 1

  return sorted(cnt.items())


def ap1B_draw_circles(im, keypoints, tipo):
  """Dibuja keypoints sobre una imagen dando un color distinto a cada octava.
  Argumentos posicionales:
  - im: Imagen de la que son los puntos.
  - keypoints: Puntos de `im`.
  - tipo: El tipo de los puntos ("SIFT" o "SURF")
  Devuelve:
  - Imagen original con un círculo centrado en cada punto con color dependiente de su octava."""

  im_puntos = im.copy()

  # Colores para los círculos de cada octava
  OCTAVE_COLORS = {
    -1: (244, 66, 66), # rojo
    0: (244, 140, 66), # naranja
    1: (244, 226, 66), # amarilla
    2: (122, 244, 66), # verde
    3: (65, 113, 244), # azul
    4: (143, 65, 244), # morado
    5: (244, 65, 172)} # rosa

  if tipo == 'SIFT':
    for kp in keypoints:
      color = OCTAVE_COLORS[getOctave(kp)]
      center = (round(kp.pt[0]), round(kp.pt[1])) # Aproxima el centro a un píxel
      im_puntos = cv.circle(im_puntos, center, int(kp.size), color)
  elif tipo == 'SURF':
    for kp in keypoints:
      color = OCTAVE_COLORS[kp.octave]
      center = (round(kp.pt[0]), round(kp.pt[1])) # Aproxima el centro a un píxel
      im_puntos = cv.circle(im_puntos, center, int(0.2*kp.size), color)
  return im_puntos


## 1 C)

def ap1C(im, keypoints, tipo, **kwargs):
  """Obtiene descriptores SIFT y SURF de cada punto
  Argumentos posicionales:
  - im: La imagen
  - keypoints: Puntos
  - tipo: El tipo de detector ("SIFT" o "SURF")
  Argumentos opcionales:
  - Cualquiera que podamos pasarle a la función `cv.xfeatures2d.SIFT_create` (o `cv.xfeatures2d.SURF_create`)
  Devuelve: Descriptores de cada punto"""
  if tipo == "SIFT":
    sift   = cv.xfeatures2d.SIFT_create(**kwargs)
    _, descriptors = sift.compute(im, keypoints)
    return descriptors
  elif tipo == "SURF":
    surf   = cv.xfeatures2d.SURF_create(**kwargs)
    _, descriptors = surf.compute(im, keypoints)
    return descriptors


def ej1ABC(ims):
  """Ejemplo de funcionamiento de la detección de puntos SIFT y SURF en yosemite.
  Argumentos posicionales:
  - ims: Lista de imágenes de ejemplo"""

  for im, title in ims:
    print("Imagen: {title}".format(title = title))
    print(" SIFT")
    puntos_sift = ap1A(im, "SIFT")
    print("  Nº de puntos detectados: {sift}".format(sift = len(puntos_sift)))
    print("  Nº por octava: {num_octave}".format(num_octave = ap1B_octave(puntos_sift, "SIFT")))
    print("  Nº por capa: {num_layer}".format(num_layer = ap1B_layer(puntos_sift)))
    print("  Forma de descriptores: {descriptor}".format(descriptor = ap1C(im, puntos_sift, "SIFT").shape))

    print(" SURF")
    puntos_surf = ap1A(im, "SURF")
    print("  Nº de puntos detectados: {surf}".format(surf = len(puntos_surf)))
    print("  Nº por octava: {num_octave}".format(num_octave = ap1B_octave(puntos_surf, "SURF")))
    print("  Forma de descriptores: {descriptor}".format(descriptor = ap1C(im, puntos_surf, "SURF").shape))

    im_sift = ap1B_draw_circles(im, puntos_sift, 'SIFT')
    im_surf = ap1B_draw_circles(im, puntos_surf, 'SURF')
    pintaMI((im, "Original"), (im_sift,  "SIFT"), (im_surf, "SURF"))


###############
# EJERCICIO 2 #
###############

def ap2A_BFCC(d_im1, d_im2):
  """Obtiene correspondencias entre descriptores.
  Usa el método 'BruteForce+crossCheck'.
  Argumentos posicionales:
  - d_im1, d_im2: Descriptores de cada imagen
  Devuelve: Correspondencias"""

  # Declara el matcher con crossCheck y obten correspondencias
  matcher = cv.BFMatcher_create(crossCheck = True)
  matches = matcher.match(d_im1, d_im2)

  return matches



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

# Los ejercicios 2 B y 2 C no tienen código asociado.

def ej2(im1, im2):
  """Ejemplo de correspondencias entre puntos
  Argumentos posicionales:
  - im1, im2: Imágenes a comparar"""

  # Obten keypoints y descriptores de SIFT
  p_im1, p_im2  = ap1A(im1, "SIFT"), ap1A(im2, "SIFT")
  d_im1, d_im2  = ap1C(im1, p_im1, "SIFT"), ap1C(im2, p_im2, "SIFT")

  possible_matches = [(ap2A_BFCC(d_im1, d_im2), "BruteForce+crossCheck"),
                      (ap2A_LA2NN(d_im1, d_im2, ratio = 0.6), "Lowe-Average-2NN ratio = 0.5"),
                      (ap2A_LA2NN(d_im1, d_im2), "Lowe-Average-2NN"),
                      (ap2A_LA2NN(d_im1, d_im2, ratio = 0.9), "Lowe-Average-2NN ratio = 0.9")]

  for matches, title in possible_matches:
    chosen_matches = random.sample(matches, 100)
    pintaI(cv.drawMatches(im1, p_im1, im2, p_im2,
           chosen_matches, None, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS),
           title)


###################
# EJERCICIO 3 Y 4 #
###################

# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

def ap3A(ims, canvas_height, canvas_width, dx = 0, dy = 0):
  """Define imagen en la que se pintará el mosaico
  Argumentos posicionales:
  - canvas_height, canvas_width: Dimensiones del mosaico
  Argumentos opcionales:
  - dx,dy: Desplazamiento opcional para la homografía
  Devuelve:
  - Imagen en la que se pintará el mosaico y
  - Homografía que traslada una imagen al centro del mosaico"""

  # Define el canvas
  canvas = np.zeros((canvas_height, canvas_width, 3), np.uint8)

  # Define la homografía como una traslación
  height, width, _ = ims[len(ims)//2].shape
  tx = (canvas_width - width)/2 + dx
  ty = (canvas_height - height)/2 + dy
  M = np.array([[1,0,tx],[0,1,ty],[0,0,1]])

  return canvas, M


def ap3B_direct_homographies(ims):
  """Define homografías entre las imágenes.
  Argumentos posicionales:
  - ims: Imágenes
  Devuelve:
  - Lista del mismo número de elementos que `ims`.
  En las posiciones inferiores a la posición central, define una homografía de una imagen a su siguiente.
  En las posiciones superiores a la posición centralm definie una homografía de una imagen a su anterior.
  El contenido de la lista en la posición central no está definido."""

  mid = len(ims)//2

  homs = []
  for n in range(len(ims)):
    if n != mid: # Si no estamos en la posición central
      m = n+1 if n < mid else n-1 # Define homografía a la imagen siguiente (anterior)

      # Calcula puntos, descriptores y correspondencias de cada imagen
      p1, p2 = ap1A(ims[n], "SIFT"), ap1A(ims[m], "SIFT")
      d1, d2 = ap1C(ims[n], p1, "SIFT"), ap1C(ims[m], p2, "SIFT")
      matches = ap2A_LA2NN(d1, d2) # matches

      # Divide correspondencias en fuentes y destinos
      sources = np.array([p1[match.queryIdx].pt for match in matches])
      dests   = np.array([p2[match.trainIdx].pt for match in matches])

      # Calcula la homografía
      homs.append(cv.findHomography(sources, dests, cv.RANSAC, 1)[0])
    else:
      homs.append(None) # Añade la posición central (no usada)
  return homs


def ap3B(M,ims):
  """Calcula homografías de cada imagen al mosaico.
  Argumentos posicionales:
  - M: Homografía que lleva la imagen central al canvas
  - ims: Imágenes
  Devuelve:
  - Lista con tantos elementos como `ims` que tiene en la posición `n` la homografía
  que lleva `ims[n]` al mosaico."""

  homs = ap3B_direct_homographies(ims)
  mosaic_homs = []
  mid = len(ims)//2

  for n in range(len(ims)):
    homography = M
    for m in range(n, mid, 1 if n < mid else -1):
      homography = homography @ homs[m]
    mosaic_homs.append(homography)

  return mosaic_homs


def ap3C(canvas, M, ims):
  """Trasladar imágenes al mosaico"""

  H, W, _ = canvas.shape
  homographies = ap3B(M,ims)

  for im, hom in zip(ims, homographies):
    canvas = cv.warpPerspective(im, hom, (W, H), dst = canvas, borderMode = cv.BORDER_TRANSPARENT)

  return canvas


def ej3(ims, dx = 0, dy = 0):
  """Genera y muestra un mosaico a partir de N = 3 imágenes
  Asumo que las imágenes están ordenadas conforme al mosaico.
  """
  canvas, M = ap3A(ims, 600, 1600, dx = dx, dy = dy)
  pintaI(ap3C(canvas, M, ims), "Canvas")


def ej4(ims):
  """Genera y muestra un mosaico a partir de N = 3 imágenes
  Asumo que las imágenes están ordenadas conforme al mosaico.
  """
  canvas, M = ap3A(ims, 530, 1100)
  pintaI(ap3C(canvas, M, ims), "mosaico")


def main():
  """Llama de forma secuencial a la función de cada apartado."""

  yosemite = []
  for n in range(1,8):
    yosemite.append(leeimagen(PATH + "yosemite{n}.jpg".format(n = n), COLOR))

  mosaico = []
  for n in range(2,12):
    mosaico.append(leeimagen(PATH + "mosaico{n:03d}.jpg".format(n = n), COLOR))

  # print("Ejemplo Ejercicio 1:")
  ej1ABC([(yosemite[0], "Yosemite 0"), (yosemite[1], "Yosemite 1")])

  # print("Ejemplo Ejercicio 2:")
  #ej2(yosemite[0], yosemite[1])

  # print("Ejemplo Ejercicio 3:")
  #ej3(yosemite[:4])
  #ej3(yosemite[4:], dx = 200, dy = 50)

  #print("Ejemplo Ejercicio 4:")
  #ej4(mosaico)

if __name__ == "__main__":
  main()
