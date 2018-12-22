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
#########################

# Carga y visualización de imágenes
PATH = "imagenes/" # Carpeta de imágenes
COLOR, GRIS = cv.IMREAD_COLOR, cv.IMREAD_GRAYSCALE

# Carga de datos de k medias
KMEANS_FILENAME = "kmeanscenters2000.pkl"
np.seterr(divide='ignore', invalid='ignore') # evitar errores por norma cero
_, _,  kmeans = auxFunc.loadDictionary(KMEANS_FILENAME)
KMEANS_DICT = kmeans/np.linalg.norm(kmeans, axis = 1).reshape((kmeans.shape[0],1))

# Carga de datos de parches
PATCHES_FILENAME = "descriptorsAndpatches2000.pkl"
PT_DESC, PATCHES = auxFunc.loadAux(PATCHES_FILENAME, True)

# Objetos SIFT y SURF con parámetros elegidos
SIFT = cv.xfeatures2d.SIFT_create()


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

N= 0
def pintaI(im, titulo = "Imagen"):
  """Visualiza una matriz de números reales cualquiera
     - im: Imagen a visualizar"""
  global N
  cv.imwrite(titulo + str(N) + ".png", im)
  N += 1
  #cv.imshow(titulo, im)
  #cv.waitKey(0)
  #cv.destroyAllWindows()

def isBW(im):
  """Indica si una imagen está en blanco y negro"""
  return len(im.shape) == 2

def juntaMI(vim, rows):
  """Junta imágenes en varias filas
  PRECONDICIÓN: len(vim) tiene que ser divisible por rows"""
  N = math.ceil(len(vim)/rows)
  output = []

  for i in range(rows): # Crea cada fila
    rim = vim[N*i: N*(i+1)]
    altura = max(im.shape[0] for im in rim)

    for i,im in enumerate(rim):
      if isBW(im): # Pasar a color
        rim[i] = cv.cvtColor(rim[i], cv.COLOR_GRAY2BGR)

        if im.shape[0] < altura: # Redimensionar imágenes
          borde = int((altura - rim[i].shape[0])/2)
          rim[i] = cv.copyMakeBorder(rim[i], borde, borde + (altura - rim[i].shape[0]) % 2,
                                     0, 0, cv.BORDER_CONSTANT, value = (0,0,0))
    output.append(cv.hconcat(rim))

    # Redimensiona filas
    anchura = max(im.shape[1] for im in output)
    for j,im in enumerate(output):
      if im.shape[1] < anchura: # Redimensionar imágenes
        borde = anchura - output[i].shape[1]
        output[i] = cv.copyMakeBorder(output[i], 0,0, 0, borde, cv.BORDER_CONSTANT, value = (0,0,0))
  return cv.vconcat(output)


def muestraMI(vim, titulo = "Imágenes", rows = 1):
  """Visualiza varias imágenes a la vez
  - vim: Secuencia de imágenes"""

  imMulti = juntaMI(vim, rows)
  pintaI(imMulti, titulo)


def pintaMI(*parejas):
  """Representa varias imágenes con sus títulos en una ventana
  - parejas: lista de pares (imagen, título)
  """

  vim, titulos = zip(*parejas)
  muestraMI(list(vim), titulo = " | ".join(titulos))


######################################
# FUNCIONES DEL TRABAJO 2 AUXILIARES #
######################################

def getDescriptors(im, mask = None):
  """Obten descriptores normalizados SIFT de una imagen.
  Argumentos posicionales:
  - im: Imagen
  Argumentos opcionales:
  - mask: Máscara"""
  ps, ds = SIFT.detectAndCompute(im,mask)
  normalized_ds = ds/np.linalg.norm(ds, axis = 1).reshape((ds.shape[0],1))
  return ps, normalized_ds

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

def ap1Fixed(im1, im2, points):
  """Muestra correspondencias entre imágenes dada una región de la primera
  Argumentos posicionales:
  - im1, im2: Imágenes a comparar,
  - points: Puntos que describen un polígono convexo en im1 que tiene el objeto de interés
  """

  mask = cv.cvtColor(np.zeros(im1.shape, np.uint8), cv.COLOR_BGR2GRAY)
  cv.fillConvexPoly(mask, points, (256, 256, 256))

  p1, d1  = getDescriptors(im1, mask)
  p2, d2  = getDescriptors(im2)

  matches = ap2A_LA2NN(d1, d2)
  pintaMI((im1, "Imagen original"), (mask, "Máscara"))
  pintaI(cv.drawMatches(im1, p1, im2, p2,
           matches, None, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS))

def ap1Interactive(im1, im2):
  """Selecciona interactivamente región de una imagen
  y pinta sus correspondencias con otra imagen.
  Argumentos posicionales:
  - im1: Imagen de la que seleccionar interactivamente una región,
  - im2: Imagen en la que encontrar objeto de la región de im1.
  """

  print("Extrae la región de la corbata")
  points = np.array(auxFunc.extractRegion(im1))
  print("Puntos elegidos: ", points)
  ap1Fixed(im1, im2, points)


def ejemplo1(parejas):
  """Ejemplo ejercicio 1
  Argumentos posicionales:
  - parejas: Lista de tripletas im1, im2, points para ejemplo
  """
  for im1, im2, ps in parejas:
    ap1Fixed(im1, im2, ps)

def ejemplo1Interactivo(parejas):
  """Ejemplo ejercicio 1 (interactivo)
  Argumentos posicionales:
  - parejas: Lista de parejas im1, im2 para ejemplo interactivo.
  """
  for im1, im2 in parejas:
    ap1Interactive(im1, im2)



## Ejercicio 2

def similitud(bag1, bag2):
  """Calcula producto escalar normalizado de vectores bolsa de palabras.
  Argumentos posicionales:
  - bag1, bag2: Bolsas de palabras normalizadas
  Devuelve:
  - Producto escalar normalizado"""
  return np.dot(bag1, bag2)

def closestMatch(d):
  """Halla el centroide más cercano a un descriptor."""
  return np.argmin(np.linalg.norm(KMEANS_DICT-d))

def ap2A(ims):
  """Implementa modelo de índice invertido + bolsa de palabras
  Argumentos posicionales:
  - ims: Imágenes
  Devuelve:
  - Índice invertido y bolsa de palabras"""

  inv_index = [[] for _ in range(len(KMEANS_DICT))]
  bags = []
  matcher = cv.BFMatcher_create(crossCheck = False)

  for n, im in enumerate(ims):
    _, ds = getDescriptors(im)
    matches = matcher.match(ds, KMEANS_DICT)

    # Cuenta matches
    bag_dict = collections.Counter()
    for match in matches:
      bag_dict[match.trainIdx] += 1

    # Guarda en histograma e índice invertido
    bag = np.zeros(len(KMEANS_DICT))
    for word, cnt in bag_dict.items():
      bag[word] = cnt
      inv_index[word].append(n)

    # Normalizado
    bags.append(bag/np.linalg.norm(bag))
  return inv_index, bags

def ap2B(im_index, bolsas, ims):
  """Halla 5 imágenes más semejantes a una dado modelo
  de índice invertido + bolsa de palabras.
  Argumentos posicionales:
  - im: Índice de imagen para hallar semejantes,
  - bolsas: vector de bolsas de palabras,
  - ims: Lista de imágenes

  Devuelve:
  - Lista de 5 imágenes más semejantes
  """
  matches = sorted(range(len(ims)),
                   key = lambda i: - similitud(bolsas[i], bolsas[im_index]))

  closest = []
  for i in matches[:6]:
    closest.append(ims[i])
  return closest

def ejemplo2(ims, seleccionadas):
  """Ejemplo del ejercicio 2.
  Argumentos posicionales:
  - ims: Lista de imágenes"""

  print("Creando modelo de bolsa de palabras + índice invertido...", end='', flush=True)
  inv_index, bags = ap2A(ims)
  print(" Creado.")

  for n in seleccionadas:
    muestraMI(ap2B(n, bags, ims),
              titulo = "Imágenes más similares a imagen nº {n}".format(n = n),
              rows = 2)


## Ejercicio 3

def ap3(word):
  """Visualiza las regiones imagen de los 10 parches más cercanos a la palabra
  Argumentos posicionales:
  - word: El índice de la palabra visual"""
  matcher = cv.BFMatcher_create(crossCheck = False)
  matches = matcher.knnMatch(np.array([KMEANS_DICT[word]]), PT_DESC, k = 10)[0]

  chosen = []
  for m in matches:
    chosen.append(cv.resize(cv.cvtColor(PATCHES[m.trainIdx], cv.COLOR_RGB2GRAY), (96,96)))

  muestraMI(chosen, titulo = "Parches asociados a palabra Nº {n}".format(n = word), rows = 2)


def ejemplo3(words):
  """Ejemplo del ejercicio 3
  Argumentos posicionales:
  - words: Iterable de índices de palabras visuales elegidas"""
  for word in words:
    ap3(word)




def main():
  """Llama de forma secuencial a la función de cada apartado."""
  print("Cargando imágenes...",end='', flush=True)
  friends = []
  N = 441
  for n in range(N):
     friends.append(leeimagen(PATH + "{n}.png".format(n = n), COLOR))
  friends = np.array(friends)
  print(" Cargadas.")

  print("Ejemplo ejercicio 1 (descomentar código para versión con detectRegion):")
  ejemplo1([(friends[0], friends[2], np.array([[180,262],[242,256],[248,334],[184,329],[180,262]])),
            (friends[24], friends[25], np.array([[203,330],[349,332],[339,476],[217,480],[203,330]]))])

  #print("Ejemplo ejercicio 1 (interactivo)")
  #ejemplo1Interactivo([(friends[0], friends[2]), (friends[24], friends[25])])

  print("Ejemplo ejercicio 2 (en visualizador de imágenes):")
  ejemplo2(friends, [19, 100, 345])

  print("Ejemplo ejercicio 3 (en visualizador de imágenes):")
  ejemplo3([32, 206, 154])

if __name__ == "__main__":
  main()
