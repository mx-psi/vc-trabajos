#! /usr/bin/python3
# Autor: Pablo Baeyens
# Uso: ./main.py

import cv2 as cv
import numpy as np
import math

#########################
# PARÁMETROS AJUSTABLES #
#########################

PATH = "imagenes/" # Carpeta de imágenes
IM_PATH = PATH + "plane.bmp" # Path de la imagen que uso como ejemplo
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

def ap1A(im, sX, sY = 0, tam = 0):
  """Aplica una máscara Gaussiana 2D.

  Argumentos posicionales:
   - im: la imagen
   - sX: sigma en la dirección X (y la Y si no se especifica sY)

  Argumentos opcionales:
   - tam: tamaño del kernel. Por defecto lo calcula GaussianBlur.
   - sY: sigma en la dirección Y. Por defecto igual a sX
  """

  return cv.GaussianBlur(im, (tam,tam), sX, sigmaY = sY)

def ejemplo1A(im):
  """Ejemplos de apartado 1A con σ pequeño, grande,
  distinto en ambas direcciones y con tamaño fijado explícitamente."""

  pintaMI((im, "Original"),
           (ap1A(im, 3),  "σ = 3"),
           (ap1A(im, 15), "σ = 15"))

  pintaMI((im, "Original"),
          (ap1A(im, 3, sY = 15), "σx = 3, σy = 15"),
          (ap1A(im, 15, sY = 3), "σx = 15, σy = 3"))

  pintaMI((im, "Original"),
           (ap1A(im, 10, tam = 5), "σ = 10, tam = 3"),
           (ap1A(im, 10, tam = 21), "σ = 10, tam = 21"))


## 1 B)

def ap1B(dx,dy,tam):
  """Obtiene máscaras 1D de máscaras derivadas.

  Argumentos posicionales:
  - dx: orden de derivación respecto de x
  - dy: orden de derivación respecto de y
  - tam: tamaño del kernel
  """

  return cv.getDerivKernels(dx,dy,tam)

def ejemplo1B():
  """Ejemplos de apartado 1B con distintos tamaños de kernel y derivadas."""

  # Derivadas y tamaños de kernel a probar
  ders = [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
  tams = [3, 5]

  for tam in tams:
    print("tam = {}".format(tam))
    for dx, dy in ders:
      print("  dx = {}, dy = {}".format(dx, dy), end = ": ")
      # Imprimo como vectores fila para ahorrar espacio
      print("{}, {}".format(*map(np.transpose,
                                 ap1B(dx, dy, tam) )))


## 1 C)

def ap1C(im, tam, tipoBorde):
  """Aplica máscara laplaciana a imagen
  Argumentos posicionales:
  - im: Imagen a la que aplicar la máscara
  - tam: Tamaño de la máscara
  - tipoBorde: Tipo de borde"""
  im_blur = ap1A(im, 5)
  return cv.Laplacian(im, -1, ksize = tam, borderType = tipoBorde, delta = 50)

def ejemplo1C(im):
  """Ejemplo de apartado 1C con distintos tamaños"""

  bordes  = [cv.BORDER_REPLICATE, cv.BORDER_CONSTANT]
  tams    = [3, 5]
  nombres = {cv.BORDER_REPLICATE: "replica", cv.BORDER_CONSTANT: "constante"}

  ims = [(im, "Original")]
  for tam in tams:
    for borde in bordes:
      ims.append((ap1C(im, tam, borde),
             "tam = {}, {}".format(tam, nombres[borde])))
  pintaMI(*ims)


###############
# EJERCICIO 2 #
###############

## 2 A)

def ap2A(im, vX, vY, tipoBorde = cv.BORDER_REPLICATE):
  """Aplica una convolución con máscara separable a una imagen.
  Argumentos posicionales:
  - im: La imagen a convolucionar
  - vX: El kernel de convolución en X
  - vY: El kernel de convolución en Y

  Argumentos opcionales:
  - tipoBorde: El tipo de borde. Por defecto reflejado.
  """

  return cv.sepFilter2D(im,-1,vX[::-1], vY[::-1], borderType = tipoBorde)


def ejemplo2A(im):
  """Ejemplo apartado 2A con distintos tamaños"""

  # Filtro gaussiano 1D
  g5 = cv.getGaussianKernel(5,-1)
  g10 = cv.getGaussianKernel(10,-1)

  # Filtro de alisado
  alisado = lambda n: np.array([1]*n)/n

  pintaMI((im, "original"),
          (ap2A(im, g5, g5), "Gaussiano tam = 5"),
          (ap2A(im, alisado(5), alisado(5)), "Matriz de unos tam = 5"))

  pintaMI((im, "original"),
          (ap2A(im, g10, g10), "Gaussiano tam = 10"),
          (ap2A(im, alisado(10), alisado(10)), "Matriz de unos tam = 10"))


## 2 B)

def ap2B(im, tam, var):
  """Aplica una máscara de primera derivada.
  Argumentos posicionales:
  - im: La imagen a convolucionar
  - tam: Tamaño del kernel
  - var: Variable por la que derivar ('x' o 'y')"""

  # Obtenemos los kernels 1D a partir del apartado 1B
  if var == 'x':
    vX, vY = ap1B(1,0,tam)
  elif var == 'y':
    vX, vY = ap1B(0,1,tam)

  return ap2A(im, vX, vY, tipoBorde = cv.BORDER_CONSTANT)

def ejemplo2B(im):
  """Ejemplos apartado 2B con distintos tamaños"""

  pintaMI((im, "Original"),
         (ap2B(im, 3, 'x'), "dx, tam = 3"),
         (ap2B(im, 3, 'y'), "dy, tam = 3"),
         (ap2B(im, 5, 'x'), "dx, tam = 5"))


## 2 C)

def ap2C(im, tam, var):
  """Aplica una máscara de segunda derivada
  Argumentos posicionales:
  - im: La imagen a convolucionar
  - tam: Tamaño del kernel
  - var: Variable por la que derivar ('x' o 'y')"""

  # Obtenemos los kernels 1D a partir del apartado 1B
  if var == 'x':
    vX, vY = ap1B(2,0,tam)
  elif var == 'y':
    vX, vY = ap1B(0,2,tam)

  return ap2A(im, vX, vY, tipoBorde = cv.BORDER_CONSTANT)

def ejemplo2C(im):
  """Ejemplos apartado 2C con distintos tamaños"""


  pintaMI((im, "Original"),
         (ap2C(im, 3, 'x'), "dx, tam = 3"),
         (ap2C(im, 3, 'y'), "dy, tam = 3"),
         (ap2C(im, 5, 'x'), "dx, tam = 5"))

## 2 D)

def ap2D(im, tipoBorde, niveles = 4):
  """Genera representación de pirámide gaussiana
  Argumentos posicionales:
  - im: La imagen a la que generar la pirámide gaussiana
  - tipoBorde: Tipo de borde a utilizar
  Argumentos opcionales:
  - niveles: Número de niveles de la pirámide gaussiana (4 por defecto)"""

  piramide = [im]
  for n in range(niveles-1):
    piramide.append(
      cv.pyrDown(piramide[-1], borderType = tipoBorde))

  return piramide

def ejemplo2D(im):
  """Ejemplos apartado 2D"""

  piramide = ap2D(im, cv.BORDER_REPLICATE)
  muestraMI(piramide, "Pirámide gaussiana")



## 2 E)

def ap2E(im, tipoBorde, niveles = 4):
  """Genera representación de pirámide laplaciana
  Argumentos posicionales:
  - im: La imagen a la que generar la pirámide laplaciana
  Argumentos opcionales:
  - niveles: Número de niveles de la pirámide laplaciana (4 por defecto)
  """
  p_gauss = ap2D(im, tipoBorde, niveles = niveles)
  pir_lap   = []

  for n in range(niveles-1):
    pir_lap.append(
      cv.subtract(p_gauss[n],
                  cv.pyrUp(p_gauss[n+1], dstsize = (p_gauss[n].shape[1], p_gauss[n].shape[0])
                  )) + 50)
  pir_lap.append(p_gauss[-1])
  return pir_lap

def ejemplo2E(im):
  """Ejemplos apartado 2E"""

  piramide = ap2E(im, cv.BORDER_REPLICATE)
  muestraMI(piramide, "Pirámide laplaciana")


###############
# EJERCICIO 3 #
###############

def ap3(im1, im2, sigma1, sigma2):
  """Construye una imagen híbrida a partir de dos imágenes con las mismas dimensiones"""
  lo_pass = ap1A(im1, sigma1)
  hi_pass = cv.subtract(im2, ap1A(im2, sigma2))
  return [lo_pass, hi_pass, cv.addWeighted(lo_pass, 0.5, hi_pass, 0.5, 0)]

def ejemplo3():
  """Ejemplo ejercicio 3"""
  im_a1, im_a2 = leeimagen(PATH + "bird.bmp", GRIS), leeimagen(PATH + "plane.bmp", GRIS)
  im_b1, im_b2 = leeimagen(PATH + "bicycle.bmp", GRIS), leeimagen(PATH + "motorcycle.bmp", GRIS)
  im_c1, im_c2 = leeimagen(PATH + "dog.bmp", GRIS), leeimagen(PATH + "cat.bmp", GRIS)

  muestraMI(ap3(im_a1, im_a2, 3, 5), "Avión - Pájaro")
  muestraMI(ap3(im_b1, im_b2, 3, 5), "Bicicleta - Moto")
  muestraMI(ap3(im_c1, im_c2, 9, 9), "Gato - Perro")


#########
# BONUS #
#########

## 1

def bonus1(sigma):
  """Calcula el vector máscara gaussiano
  Argumentos posicionales:
  - sigma: Parámetro σ de la función de densidad de la gaussiana"""

  longitud = 1 + 2*int(3*sigma)
  mid = int(3*sigma)

  f = lambda x: math.exp(-0.5*x*x/(sigma*sigma))
  mascara = np.zeros(longitud)

  for n in range(longitud):
    x = n - mid
    mascara[n] = f(x)

  return mascara/np.sum(mascara)

def ejemploB1():
  print("  Máscara gaussiana con σ = 0.5: {v}".format(v = bonus1(0.5)))

## 2


def bonus2(mascara, orig):
  """Calcula convolución 1D de vector con señal.
  Argumentos posicionales:
  - mascara: vector-máscara
  - orig: Señal original
  """

  if len(orig.shape) == 2: # si es multibanda
    NCH = orig.shape[1]
    return np.stack((bonus2(mascara, orig[::,j]) for j in range(NCH)), axis = 1)

  nueva = np.zeros(orig.shape)
  N, M = len(orig), (len(mascara)-1)//2

  for i in range(N):
    for j in range(-M, M+1):
      k = i-j
      if k < 0 or k >= N:
        k = N - 1 - (k % N)
      nueva[i] += mascara[j+M]*orig[k]
    nueva[i] = max(min(nueva[i], 255), 0)
  return nueva

def ejemploB2():
  """Ejemplo 2 BONUS (convolución 1D)"""
  v = np.array([1,2,3,4,5])
  mascara = [0,0,1]
  print("  Original: {v}".format(v = v))
  print("  Desplazado una unidad: {v}".format(v = bonus2(mascara, v)))

## 3

def bonus3(vX, vY, im):
  """Convolución 2D usando máscaras separables
  Argumentos posicionales:
  - vX: Vector-máscara en dirección X
  - vY: Vector-máscara en dirección Y
  - im: Imagen a convolucionar
  """
  if not isBW(im): # Si tiene 3 canales
    canales  = cv.split(im)
    return cv.merge([bonus3(vX, vY, canal) for canal in canales])

  nueva = im.copy()
  N, M = im.shape
  for j in range(M):
    nueva[::,j] = bonus2(vX, nueva[::, j])
  for i in range(N):
    nueva[i,::] = bonus2(vY, nueva[i, ::])

  return nueva

def ejemploB123(im):
  """Combina ejemplos para mostrar funcionalidad en ejercicios bonus 1, 2 y 3"""
  vGauss = bonus1(1)
  gauss  = bonus3(vGauss, vGauss, im)

  pintaMI((im, "Original"),
          (gauss, "Gaussiana propia sigma = 3"))


## 3 (bis)

def pirAbajo(im):
  """Versión propia de cv.pyrDown para ejercicio bonus 3 bis"""

  vGauss = bonus1(1)
  im_bor = bonus3(vGauss, vGauss, im)
  forma = (im.shape[0]//2, im.shape[1]//2)
  nueva_im = np.zeros(forma, np.uint8)

  for i in range(forma[0]):
    for j in range(forma[1]):
      nueva_im[i,j] = im_bor[2*i, 2*j]

  return nueva_im


def bonus3b(im, niveles):
  """Pirámide Gaussiana de 5 niveles con imágenes híbridas"""
  piramide = [im]
  for n in range(niveles-1):
    piramide.append(pirAbajo(piramide[-1]))
  return piramide

def ejemploB3b(im):
  """Ejemplo 3 bis BONUS"""
  piramide = bonus3b(im, 5)
  muestraMI(piramide, "Pirámide gaussiana")

## 4

def bonus4(im1, im2, sigma1, sigma2):
  """Construye una imagen híbrida a color a partir de dos imágenes con las mismas dimensiones"""
  vG1, vG2 = bonus1(sigma1), bonus1(sigma2)
  lo_pass = bonus3(vG1, vG1, im)
  hi_pass = cv.subtract(im2, bonus3(vG2, vG2, im2))
  return [lo_pass, hi_pass, cv.addWeighted(lo_pass, 0.5, hi_pass, 0.5, 0)]

def ejemploB4():
  im_a1, im_a2 = leeimagen(PATH + "plane.bmp", COLOR), leeimagen(PATH + "bird.bmp", COLOR)
  im_b1, im_b2 = leeimagen(PATH + "bicycle.bmp", COLOR), leeimagen(PATH + "motorcycle.bmp", COLOR)
  im_c1, im_c2 = leeimagen(PATH + "cat.bmp", COLOR), leeimagen(PATH + "dog.bmp", COLOR)

  muestraMI(bonus4(im_a1, im_a2, 3, 5), "Avión - Pájaro")
  muestraMI(bonus4(im_b1, im_b2, 3, 5), "Bicicleta - Moto")
  muestraMI(bonus4(im_c1, im_c2, 10, 10), "Gato - Perro")


def main():
  """Llama de forma secuencial a la función de cada apartado."""

  im = leeimagen(IM_PATH, COLOR)
  # Usar imágenes de un sólo canal para 2
  im_bn = leeimagen(IM_PATH, GRIS)

  #pintaI(im)

  # print("Ejemplo 1A: (en visor de imágenes)")
  # ejemplo1A(im)
  # print("Ejemplo 1B:")
  # ejemplo1B()
  # espera()
  print("Ejemplo 1C: (en visor de imágenes)")
  ejemplo1C(im_bn)
  print("Ejemplo 2A: (en visor de imágenes)")
  ejemplo2A(im_bn)
  # print("Ejemplo 2B: (en visor de imágenes)")
  # ejemplo2B(im_bn)
  # print("Ejemplo 2C: (en visor de imágenes)")
  # ejemplo2C(im_bn)
  # print("Ejemplo 2D: (en visor de imágenes)")
  # ejemplo2D(im_bn)
  #print("Ejemplo 2E: (en visor de imágenes)")
  #ejemplo2E(im_bn)
  print("Ejemplo 3: (en visor de imágenes)")
  ejemplo3()
  # print("Ejemplo 1 BONUS")
  # ejemploB1()
  # espera()
  # print("Ejemplo 2 BONUS")
  # ejemploB2()
  # espera()
  # print("Ejemplo 1,2 y 3 BONUS (en visor de imágenes)")
  # print("Tarda unos 4 segundos en aparecer en mi ordenador")
  # ejemploB123(im)
  # print("Ejemplo 3 bis BONUS (en visor de imágenes)")
  # ejemploB3b(im_bn)
  # print("Ejemplo 4 BONUS (en visor de imágenes)")
  # ejemplo4()



if __name__ == "__main__":
  main()
