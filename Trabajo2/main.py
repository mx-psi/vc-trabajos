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

###############
# EJERCICIO 1 #
###############

## 1 A)

def ap1A(im, tipo):
  """Detecta puntos SIFT o SURF sobre una imagen.
  Argumentos posicionales:
  - im: Imagen
  - tipo: El tipo de detector ("SIFT" o "SURF")
  Devuelve:
  - Los puntos detectados
  """
  if tipo == "SIFT":
    return SIFT.detect(im)
  elif tipo == "SURF":
    return SURF.detect(im)


def ej1A(im):
  """Ejemplo de prueba del apartado 1A.
  Argumentos posicionales:
  - im: La imagen sobre la que probamos los distintos detectores"""
  detectors_SIFT =  [
    (cv.xfeatures2d.SIFT_create(contrastThreshold = 0.06, edgeThreshold = 8),
     "SIFT umbrales contraste: 0.06, bordes: 8"),
    (SIFT,
     "SIFT umbrales contraste: 0.04, bordes: 5"),
    (cv.xfeatures2d.SIFT_create(contrastThreshold = 0.02, edgeThreshold = 8),
     "SIFT umbrales contraste: 0.02, bordes: 8"),]

  ims = []
  for detector, titulo in detectors_SIFT:
    keypoints = detector.detect(im)
    print(titulo, "- Nº de puntos: ", len(keypoints))
    ims.append((ap1B_draw_circles(im, keypoints, "SIFT"), titulo))
  pintaMI(*ims)

  detectors_SURF = [
    (cv.xfeatures2d.SURF_create(hessianThreshold = 50), "SURF umbral hessiana: 50"),
    (SURF, "SURF umbral hessiana: 200"),
    (cv.xfeatures2d.SURF_create(hessianThreshold = 400), "SURF umbral hessiana: 400")]

  ims = []
  for detector, titulo in detectors_SURF:
    keypoints = detector.detect(im)
    print(titulo, "- Nº de puntos: ", len(keypoints))
    ims.append((ap1B_draw_circles(im, keypoints, "SURF"), titulo))
  pintaMI(*ims)



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
    cnt[(getOctave(kp), getLayer(kp))] += 1

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

def ap1C(im, keypoints, tipo):
  """Obtiene descriptores SIFT y SURF de cada punto
  Argumentos posicionales:
  - im: La imagen
  - keypoints: Puntos
  - tipo: El tipo de detector ("SIFT" o "SURF")
  Devuelve: Descriptores de cada punto"""
  if tipo == "SIFT":
    detector = SIFT
  elif tipo == "SURF":
    detector = SURF

  return detector.compute(im, keypoints)


def ej1ABC(ims):
  """Ejemplo de funcionamiento de la detección de puntos SIFT y SURF en yosemite.
  Argumentos posicionales:
  - ims: Lista de imágenes de ejemplo"""

  for im, title in ims:
    print("Imagen: {title}".format(title = title))
    print(" SIFT")
    puntos_sift = ap1A(im, "SIFT")
    puntos_sift, descriptores = ap1C(im, puntos_sift, "SIFT")
    print("  Nº de puntos detectados: {sift}".format(sift = len(puntos_sift)))

    num_octave = ap1B_octave(puntos_sift, "SIFT")
    print("  Nº por octava: {num_octave}".format(num_octave = num_octave))

    print("  Nº por capa:")
    layers = ap1B_layer(puntos_sift)
    for octave, _ in num_octave:
      print("  ", list(filter(lambda x: x[0][0] == octave, layers)))

    print("  Forma de descriptores: {descriptor}".format(descriptor = descriptores.shape))

    print(" SURF")
    puntos_surf = ap1A(im, "SURF")
    puntos_surf, descriptores = ap1C(im, puntos_surf, "SURF")
    print("  Nº de puntos detectados: {surf}".format(surf = len(puntos_surf)))
    print("  Nº por octava: {num_octave}".format(num_octave = ap1B_octave(puntos_surf, "SURF")))
    print("  Forma de descriptores: {descriptor}".format(descriptor = descriptores.shape))

    espera()
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
  p1, d1  = ap1C(im1, ap1A(im1, "SIFT"), "SIFT")
  p2, d2  = ap1C(im2, ap1A(im2, "SIFT"), "SIFT")

  possible_matches = [(ap2A_BFCC(d1, d2), "BruteForce+crossCheck"),
                      (ap2A_LA2NN(d1, d2, ratio = 0.6), "Lowe-Average-2NN ratio = 0.5"),
                      (ap2A_LA2NN(d1, d2), "Lowe-Average-2NN"),
                      (ap2A_LA2NN(d1, d2, ratio = 0.9), "Lowe-Average-2NN ratio = 0.9")]

  for matches, title in possible_matches:
    chosen_matches = random.sample(matches, 100)
    pintaI(cv.drawMatches(im1, p1, im2, p2,
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
      p1, d1 = ap1C(ims[n], ap1A(ims[n], "SIFT"), "SIFT")
      p2, d2 = ap1C(ims[m], ap1A(ims[m], "SIFT"), "SIFT")
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
    a = ""
    for m in range(n, mid, 1 if n < mid else -1):
      a += str(m)
      homography = homography @ homs[m]
    print(a)
    mosaic_homs.append(homography)

  return mosaic_homs


def ap3C(canvas, M, ims):
  """Trasladar imágenes al mosaico
  Argumentos posicionales:
  - canvas: Canvas en el que pintar
  - M: Homografía que lleva la imagen central al canvas
  - ims: Imágenes con las que hacer la homografía
  Devuelve:
  El canvas con las imágenes trasladadas"""

  H, W, _ = canvas.shape
  homographies = ap3B(M,ims)

  for im, hom in zip(ims, homographies):
    canvas = cv.warpPerspective(im, hom, (W, H), dst = canvas, borderMode = cv.BORDER_TRANSPARENT)

  return canvas


def ej3(ims, dx = 0, dy = 0):
  """Genera y muestra un mosaico a partir de N = 3 imágenes
  Asumo que las imágenes están ordenadas conforme al mosaico
  (esto es, dos imágenes adyacentes tienen alguna región común)
  Argumentos posicionales:
  - ims: Imágenes del mosaico (yosemiteN.jpg)
  """
  canvas, M = ap3A(ims, 600, 1600, dx = dx, dy = dy)
  pintaI(ap3C(canvas, M, ims), "yosemite")


###############
# EJERCICIO 4 #
###############

def ej4(ims):
  """Genera y muestra un mosaico a partir de N = 3 imágenes
  Asumo que las imágenes están ordenadas conforme al mosaico.
  Argumentos posicionales:
  - ims: Imágenes del mosaico (mosaico0N.jpg)
  """
  canvas, M = ap3A(ims, 530, 1100)
  pintaI(ap3C(canvas, M, ims), "mosaico")


#########
# BONUS #
#########

# Ejercicio 3 Bonus

def ap3Bonus_hom(srcs, dsts):
  """Calcula la homografía dadas 4 correspondencias.
  Argumentos posicionales:
  - srcs: Coordenadas de las fuentes (4)
  - dsts: Coordenadas de los destinos (4)
  Devuelve: Homografía que lleva srcs[i] en dsts[i]"""
  v = np.zeros(3)
  A = None

  # Para cada correspondencia añade las 2 filas del sistema
  for src, dst in zip(srcs, dsts):
    src_h = np.append(src, 1)
    f1 = np.concatenate((src_h, v, -dst[0]*src_h))
    f2 = np.concatenate((v, src_h, -dst[1]*src_h))
    if A is None:
      A = np.vstack((f1, f2))
    else:
      A = np.vstack((A, f1, f2))

  # Halla SVD
  U, s, V = np.linalg.svd(A)
  sv = np.argmin(s)

  # Toma el vector con menor valor singular asociado
  return V[sv, :].reshape((3,3))


def ap3Bonus(srcs, dsts, max_iters = 1000, p = 0.99):
  """Implementa de forma eficiente la estimación de una homografía usando RANSAC.
  Argumentos posicionales:
  - srcs: Coordenadas de las fuentes
  - dsts: Coordenadas de los destinos de tal forma que dsts[i] es la correspondencia de srcs[i]
  Devuelve: La homografía estimada"""

  N = len(srcs)
  new_srcs = np.array([srcs])

  # Calcula número de inliers inicial
  idx = np.random.choice(N, 4, replace = False) # Coge 4 índices aleatorios
  best_H   = ap3Bonus_hom(srcs[idx], dsts[idx]) # Calcula homografía
  hom_dsts = cv.perspectiveTransform(new_srcs, best_H)[0] # Calcula imágenes de homografía
  best_inliers = np.sum(np.linalg.norm(dsts-hom_dsts, 2, axis = 1) <= 3) # Cantidad de puntos a dist <= 3

  # Calcula número de iteraciones
  err = 1 - float(best_inliers)/N
  if err == 0: # Si encaja con todos los puntos devuelve
    return best_H
  elif err == 1: # Si todos los puntos fallan usa el máximo
    N_reps = max_iters
  else:
    N_reps = math.ceil(math.log(1 - p)/math.log(1 - (1 - err)**4.0))

  for _ in range(min(N_reps, max_iters)):
    idx = np.random.choice(N, 4, replace = False) # Coge 4 índices aleatorios
    H   = ap3Bonus_hom(srcs[idx], dsts[idx]) # Calcula homografía
    hom_dsts = cv.perspectiveTransform(new_srcs, H)[0] # Calcula imágenes de homografía
    inliers = np.sum(np.linalg.norm(dsts-hom_dsts, 2, axis = 1) <= 3) # Cantidad de puntos a dist <= 3

    if inliers > best_inliers: # Si es mejor
      best_inliers = inliers
      best_H       = H

  return best_H


def ej3Bonus(ims):
  """Ejemplo de estimación de homografía para RANSAC"""
  p1, d1 = ap1C(ims[0], ap1A(ims[0], "SIFT"), "SIFT")
  p2, d2 = ap1C(ims[1], ap1A(ims[1], "SIFT"), "SIFT")
  matches = ap2A_LA2NN(d1, d2) # matches

  # Divide correspondencias en fuentes y destinos
  sources = np.array([p1[match.queryIdx].pt for match in matches], dtype = 'float32')
  dests   = np.array([p2[match.trainIdx].pt for match in matches], dtype = 'float32')
  H = ap3Bonus(sources, dests) # Calcula la homografía

  # Pinta el resultado
  width, height = 1200, 700
  canvas, M  = ap3A(ims[1:], height, width, dx = 200)
  canvas = cv.warpPerspective(ims[1], M, (width, height), dst = canvas, borderMode = cv.BORDER_TRANSPARENT)
  canvas = cv.warpPerspective(ims[0], M @ H, (width, height), dst = canvas, borderMode = cv.BORDER_TRANSPARENT)
  pintaI(canvas, "RANSAC")



def main():
  """Llama de forma secuencial a la función de cada apartado."""

  yosemite = []
  for n in range(1,4):
    yosemite.append(leeimagen(PATH + "yosemite{n}.jpg".format(n = n), COLOR))

  print("Ejemplo Ejercicio 1:")
  ej1A(yosemite[0])
  ej1ABC([(yosemite[0], "Yosemite 0"), (yosemite[1], "Yosemite 1")])

  print("Ejemplo Ejercicio 2: (en visor de imágenes)")
  ej2(yosemite[0], yosemite[1])

  print("Ejemplo Ejercicio 3: (en visor de imágenes)")
  ej3(yosemite)

  mosaico = []
  for n in range(2,12):
    mosaico.append(leeimagen(PATH + "mosaico{n:03d}.jpg".format(n = n), COLOR))

  print("Ejemplo Ejercicio 4: (en visor de imágenes)")
  ej4(mosaico)

  print("Ejemplo Ejercicio 3 BONUS: (en visor de imágenes)")
  ej3Bonus([yosemite[1], yosemite[2]])

if __name__ == "__main__":
  main()
