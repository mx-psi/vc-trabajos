---
title: Trabajo 3
subtitle: Visión por Computador
author: Pablo Baeyens Fernández
date: Curso 2018-2019
documentclass: scrartcl
classoption: egregdoesnotlikesansseriftitles
lang: es
colorlinks: true
bibliography: citas.bib
biblio-style: plain
link-citations: true
header-includes:
- \usepackage{graphicx}
toc: true
toc-depth: 2
citation-style: estilo.csl
---

***

Nombro a los descriptores e imágenes por el orden en el que aparecen en los archivos.
Cada apartado indica en qué función está implementado.

\newpage


# Ejercicio 1

Este ejercicio está implementado en las funciones `ap1Fixed`, `ap1Interactive` 
y pueden verse ejemplos en `ejemplo1` y `ejemplo1Interactivo`.

Para facilitar la corrección en la ejecución se ejecuta el código con regiones fijas seleccionadas.
Si se quiere seleccionar manualmente una región con la ayuda de `extractRegion` basta descomentar 
las lineas correspondientes en la función `main`.

## Seleccionar región común en dos imágenes

Este apartado está implementado en `ap1Interactive` y `ap1Fixed`.

La función `ap1Interactive` toma dos imágenes a comparar. 
Con la ayuda de la función auxiliar `extractRegion` obtenemos los puntos que definen el polígono que define la región de interés y convertimos su salida a un array NumPy:
```python
points = np.array(auxFunc.extractRegion(im1))
```
A continuación llamamos a la función `ap1Fixed` con estos puntos.

***

La función `ap1Fixed` toma dos imágenes `im1` e `im2` a comparar y un array NumPy de puntos `points` que define un polígono convexo en coordenadas de la imagen `im1`.

Para generar la máscara, en primer lugar declaramos una máscara de ceros unibanda con las dimensiones de `im1` con:
```python
mask = cv.cvtColor(np.zeros(im1.shape, np.uint8), cv.COLOR_BGR2GRAY)
```

A continuación rellenamos con unos la región definida por `points` con la función `fillConvexPoly`.
Lo relleno de color blanco:
```python
cv.fillConvexPoly(mask, points, (256, 256, 256))
```

## Extraer puntos SIFT y calcular correspondencias

Continuando en el código de `ap1Fixed` tenemos ahora que tomar los puntos SIFT de la región de la primera imagen y de toda la segunda. 

Nos ayudamos del objeto `SIFT` que defino con los parámetros por defecto y que gestiono en la función `getDescriptors`. Esta función extrae los descriptores y los normaliza según la ayuda (dividiendo por la norma sobre el eje 1).
```python
ps, ds = SIFT.detectAndCompute(im,mask)
normalized_ds = ds/np.linalg.norm(ds, axis = 1).reshape((ds.shape[0],1))
```

A continuación obtenemos los puntos y descriptores.

```python
p1, d1  = getDescriptors(im1, mask)
p2, d2  = getDescriptors(im2)
```
`pN` y `dN` son respectivamente los puntos y descriptores de la imagen `N`. 
En el caso de `im1` utilizamos la máscara `mask` que definimos anteriormente para restringirnos a la región de interés.

Utilizando la función `ap2A_LA2NN` que hice en la práctica 2 hallamos las correspondencias con el método *LoweAverage+2NN*
```python
matches = ap2A_LA2NN(d1, d2)
```

## Mostrar correspondencias

Mostramos las correspondencias utilizando la función `drawMatches` que utilizamos en la práctica 2:
```python
   pintaI(cv.drawMatches(im1, p1, im2, p2,
           matches, None, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS))
```

Mostramos además la imagen `im1` y la máscara para poder valorar los resultados.

## Valoración de resultados

![Región elegida de imagen 0](src/mascara1.png)

He elegido dos parejas de imágenes `0.png` y `2.png` y `24.png` y `25.png` para la valoración de resultados.

![Correspondencias entre imágenes 0 y 2](src/corr1.png)

Para ambas imágenes he preseleccionado la región, que se muestra adyacente a la imagen.
Puede descomentarse la línea posterior para poder ejecutarlo haciendo uso de `extractRegion`.

![Región elegida de imagen 0](src/mascara2.png)

![Correspondencias entre imágenes 24 y 25](src/corr2.png)

En ambas parejas de imágenes podemos apreciar que esta técnica produce buenos resultados, consiguiendo hallar las correspondencias adecuadas entre las imágenes. En la segunda pareja tenemos algunas falsas correspondencias que no siguen la dirección general del resto de correspondencias pero mayoritariamente son correctas.

Esto nos indica que esta técnica puede ser adecuada en algunas situaciones para hallar la localización de regiones u objetos de interés en una escena, aunque debemos notar que hemos tenido que seleccionar manualmente la región de interés en una de las imágenes.


# Ejercicio 2

## Implementación de modelo de índice invertido + bolsa de palabras

Este ejercicio está implementado en la función `ap2A`.
Un ejemplo (junto con la ejecución de la segunda parte) puede verse en la función `ejemplo2`, que se discute en el apartado B.

Tomamos la lista de imágenes `ims` ya cargadas. 
A partir de estas calculamos dos listas: `inv_index` que tiene el índice invertido de tamaño igual al tamaño del diccionario y `bags` que inicialmente es una lista vacía.

Para cada imagen obtenemos sus descriptores y buscamos para cada descriptor el descriptor del diccionario de centroides que esté más cercano de acuerdo a su distancia euclídea. Hemos normalizado el diccionario de forma similar a la normalización de los descriptores en `getDescriptors`.
```python
ds = getDescriptors(im)
matches = matcher.match(ds, KMEANS_DICT)
```

A continuación creamos el histograma utilizando un objeto `Counter` del módulo `collections` (un diccionario con valor 0 por defecto) y añadimos para cada correspondencia hallada por el matcher el centroide correspondiente:

```python
bag_dict = collections.Counter()
for match in matches:
  bag_dict[match.trainIdx] += 1
```

Finalmente construimos a partir de este diccionario el vector de histograma y el índice invertido.
Habitualmente es más eficiente trabajar con una representación como vector disperso del histograma ya que el número de entradas no nulas en cada histograma es reducido pero para esta práctica lo pasamos a un vector NumPy por conveniencia al ser el diccionario que utilizamos de tamaño reducido.

```python
bag = np.zeros(len(KMEANS_DICT))
for word, cnt in bag_dict.items():
  bag[word] = cnt
  inv_index[word].append(n)
bags.append(bag/np.linalg.norm(bag))
```

Para cada centroide `word` añadimos el número de ocurrencias al histograma y añadimos la imagen (`n`) al índice invertido. Finalmente añadimos el vector de histograma normalizado a la lista de histogramas.

Lo ponemos normalizado ya que de esta forma nos ahorramos la normalización en el cálculo de la similitud.

## Hallar imágenes más cercanas a una imagen pregunta

Este ejercicio está implementado en el apartado `ap2B` y la función `similitud`.

La función `similitud` calcula el producto escalar de dos vectores. 
No lo normalizamos porque los vectores que le pasamos ya están normalizados en el apartado anterior.

Recibimos como argumentos `im_index`, el índice de la imagen de la que queremos hallar las 5 más cercanas, `bolsas`, la lista de bolsas de palabras calculadas en el apartado anterior e `ims`, la lista de imágenes.

Ordenamos los índices del iterable `range(len(ims))` según la similitud, estando en las primeras posiciones aquellas imágenes con mayor similitud (para lo que ponemos un signo menos):
```python
matches = sorted(range(len(ims)),
                 key = lambda i: - similitud(bolsas[i], bolsas[im_index]))
```
El parámetro `key` nos permite dar una función con la que ordenar.

A continuación añadimos las imágenes asociadas a los 6 primeros elementos de esta lista a una lista que devolvemos:
```python
closest = []
for i in matches[:6]:
  closest.append(ims[i])
return closest
```
Cogemos 6 porque la primera imagen, de similitud máxima, será la imagen original.

## Ejemplos de funcionamiento. Conclusiones


![Imágenes más similares a la imagen nº 19. La imagen 19 está en la esquina superior izquierda.](src/im19.png)

Los ejemplos de funcionamiento están implementados en la función `ejemplo2`.
Esta función calcula el índice invertido y modelo de bolsa de palabras y muestra las 5 imágenes-pregunta más similares a una imagen dada, ayudándose de la función `muestraMI`.
```python
inv_index, bags = ap2A(ims)

for n in seleccionadas:
  muestraMI(ap2B(n, bags, ims),
            titulo = "Imágenes más similares a imagen nº {n}".format(n = n),
            rows = 2)
```

He implementado un parámetro `rows` que permita visualizar las imágenes en varias filas para este apartado y el siguiente de tal forma que no ocupen demasiado espacio en pantalla.

![Imágenes más similares a la imagen nº 100. La imagen 100 está en la esquina superior izquierda.](src/im100.png)

Como ejemplos de buen funcionamiento del modelo he elegido las imágenes 19 y 100.
En ambas podemos observar que todas las imágenes que se observan pertenecen a la misma escena y se ignoran características que no son relevantes para determinar la escena.

En la imagen 19 se detectan con independencia de las expresiones faciales o posiciones de los brazos, y en la imagen 100 tenemos que objetos visuales como los créditos no impiden el reconocimiento de la similitud entre las imágenes.

![Imágenes más similares a la imagen nº 345. La imagen 345 está en la esquina superior izquierda.](src/im345.png)

Como ejemplo erróneo he elegido la imagen 345.
Para esta imagen podemos observar que las imágenes obtenidas no tienen en general casi similitud con la imagen original, mostrando escenas diferentes con luminosidad, personajes y ambientes diferentes, lo que nos muestra que el modelo puede fallar.

Como conclusión vemos que el modelo de bolsa de palabras parece ser efectivo en la mayoría de los casos para resumir el contenido visual de las imágenes y nos puede servir por ejemplo para reconocer imágenes que pertenecen a la misma escena, pero en algunos casos el modelo es incapaz de resumir este contenido de forma eficaz.
Además, hay algunos parámetros para la formación del vocabulario que no hemos ajustado manualmente pero que podrían tener efectos notables en el rendimiento de esta técnica.

# Ejercicio 3

Este ejercicio está implementado en la función `ap3`.
Un ejemplo de funcionamiento está disponible en la función `ejemplo3`.

## Visualizar regiones cercanas a cada palabra visual

La función `ap3` toma un índice de palabra visual `word` y muestra los 10 parches más cercanos a esta palabra.

Utilizamos un `BFMatcher` para buscar los parches más cercanos a cada palabra visual.
En primer lugar creamos el matcher `matcher = cv.BFMatcher_create(crossCheck = False)`.

A continuación haciendo uso del método `knnMatch` buscamos los `k = 10` descriptores de parches más cercanos de la lista de descriptores (`PT_DESC`) al descriptor de la palabra, `KMEANS_DICT[word]`.
Tenemos que crear una lista de un sólo elemento para el descriptor. La salida tendrá un solo match en la posición 0:

```python
matches = matcher.knnMatch(
   np.array([KMEANS_DICT[word]]), # Lista de un sólo element0
   PT_DESC, # descriptores de parches
   k = 10)[0]
```

Por último, para cada match de la lista lo pasamos a blanco y negro y redimensionamos la imagen para que tenga tamaño $96\times96$ con `cvtColor` y `resize` respectivamente:
```python
chosen = [] # Lista de parches
for m in matches:
  chosen.append(
    cv.resize(
      cv.cvtColor(PATCHES[m.trainIdx], cv.COLOR_RGB2GRAY), # parche en BN
      (96,96))) # tamaño a redimensionar
```

Mostramos esos parches en dos filas.

## Explicar resultados

![Parches visuales más cercanos a la palabra 32](src/parches32.png)

![Parches visuales más cercanos a la palabra 206](src/parches206.png)

He elegido 3 ejemplos de palabras visuales para mostrar el comportamiento con distintas palabras visuales.

En los primeros dos ejemplos, correspondientes a las palabras visuales 32 y 206, vemos que se aprecia el mismo patrón en todos los parches visuales elegidos, lo que nos indica que estas palabras se corresponden claramente con un cierto patrón visual.

![Parches visuales más cercanos a la palabra 154](src/parches154.png)

En cambio, en el caso de palabras visuales como la 154 podemos ver que no hay concordancia entre las regiones visualizadas en términos de cercanía visual. Esto nos muestra que, en general, no tenemos asegurada la cercanía visual entre los parches asociados a una palabra.

No obstante en general sí que se aprecia cercanía visual entre los parches lo que nos muestra que el modelo de bolsa de palabras funciona razonablemente bien en la situación de esta práctica.
