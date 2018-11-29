---
title: Trabajo 2
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

*****

Cada apartado indica qué funciones lo implementan en el caso de que haya que programar.
Si el argumento `tipo` no es `"SIFT"` o `"SURF"` el comportamiento es indeterminado.
Las funciones de un mismo ejercicio están separadas en el fichero `main.py` con comentarios.

\newpage

# Ejercicio 1

Un ejemplo de la ejecución de todas las partes de este ejercicio está en la función `ej1ABC`.

## A) Cálculo de puntos con SIFT y SURF

Este ejercicio está implementado en la función `ap1A`.
Un ejemplo con distintos parámetros está en la función `ej1A`.

### Variar valores de umbral hasta obtener un conjunto numeroso (> 1000) de puntos SIFT y SURF representativo de la imagen.

Para encontrar puntos clave SIFT crea una pirámide a partir de la imagen, que se divide en octavas (con la imagen a a distintas escalas) y estas a su vez se dividen en capas que tienen una aproximación de la pirámide laplaciana a partir de diferencias de gaussianas. 

A continuación detecta puntos que sean extremos locales en cada capa y descarta aquellos en el que este extremo tengan un valor menor que un cierto umbral.
Además, descarta los puntos que pertenezcan a bordes (los puntos clave necesitan ser esquinas) viendo si el ratio de las curvaturas principales (calculado mediante el ratio de los valores propios de la hessiana) es mayor que un umbral (si el ratio es "grande" nos indicaría que probablemente hay un borde).

La interfaz de OpenCV nos permite ajustar algunos parámetros para SIFT:

- `nfeatures`, que limita el número de características y que no modificamos para tener tantas como SIFT encuentre,
- `nOctaveLayers`, que ajusta el número de capas por octava. De nuevo no lo modificamos ya que el valor por defecto (que es el dado en el paper original) funciona correctamente y no es un umbral,
- `sigma`, que indica el sigma de la gaussiana para la primera octava.
- `contrastThreshold`, que ajusta el umbral para descartar extremos locales demasiado débiles y 
- `edgeThreshold` que ajusta el umbral para descartar bordes.

En el ejemplo podemos ver que el número de puntos detectados incrementa conforme se reduce el umbral de contraste y conforme incrementa el umbral de bordes.

****

SURF es una versión que optimiza más agresivamente su algoritmo para ser más rápido a cambio de una pequeña pérdida de rendimiento. Aproxima la pirámide laplaciana con un filtro de caja, lo que puede ser calculado de forma más rápida. A continuación toma como puntos de interés aquellos en los que el determinante de la hessiana sea un extremo.

La interfaz de OpenCV nos permite ajustar algunos parámetros para SURF:

- `hessianThreshold`, que indica el umbral con el cuál descartamos extremos detectados con la hessiana,
- `nOctaves` y `nOctaveLayers` ajustan el número de octavas y el número de capas por octava, que dejamos en sus valores por defecto y 
- `extended` y `upright` que permiten activar versiones alternativas del algoritmo.

En el ejemplo podemos ver que el número de puntos detectados se reduce conforme aumenta el umbral de la hessiana.

### Justificar la elección de los parámetros en relación a la representatividad de los puntos obtenidos.

He decidido utilizar en ambos casos parámetros cercanos a los parámetros por defecto que describo a continuación para cada caso.
Ambos obtienen una cantidad numerosa de puntos (en torno a los 2000 puntos) y son representativas en las imágenes que he utilizado para probar. 

En SIFT, si aumentamos demasiado el umbral de contraste o reducimos el umbral de bordes algunas regiones como la zona de bosque de la esquina inferior derecha no está bien representada. Si los modificamos en la dirección contraria obtenemos algunos puntos en la región oscura de la esquina inferior izquierda que probablemente se deban a ruido. He decidido utilizar un umbral de contraste de 0.04 (el valor por defecto) y un umbral de bordes de 5 (que he reducido para reducir el número de puntos en bordes).

En SURF, si el valor de la hessiana es demasiado alto tenemos un problema similar a SIFT en términos de representatividad de los puntos ya que algunas regiones que potencialmente tienen características de interés no son reflejadas en los puntos clave, mientras que si el valor de la hessiana es demasiado bajo obtenemos puntos que probablemente se deban a ruido. El valor 200 parece dar buenos resultados.

En los ejercicios siguientes utilizo los parámetros encontrados en este apartado; defino dos objetos `SIFT` y `SURF` con esos parámetros.

## B) Identificar localización de puntos

Este apartado está implementado en las funciones `getOctave`, `getLayer`, `ap1B_octave`, `ap1B_layer` y `ap1B_draw_circles`. 

Las funciones `getOctave` y `getLayer` son reimplementaciones en Python del código fuente en C de la función `unpackOctave` del módulo `xfeatures2d.SIFT` [@RepositoryOpenCVextra2018].
Estas funciones permiten obtener respectivamente la octava y la capa de un punto obtenido con SIFT.

### Identificar cuántos puntos se han detectado dentro de cada octava.

Esta parte está implementado en la función `ap1B_octave`.
Utilizo un contador (del módulo `collections`) para contar los puntos en cada capa.
Un contador es un diccionario con valor cero por defecto. 
La función `items` nos devuelve una lista con pares $(\operatorname{clave},\operatorname{valor})$ para aquellos con valor distinto de cero.

Para obtener la octava:

- En el caso de SURF sólo tenemos que obtener la octava a partir del atributo `.octave` de cada punto.
- En el caso de SIFT la octava está guardada en el byte superior del atributo `.octave`. 
  Utilizamos la función `getOctave` obtenida del código fuente de `opencv_contrib`.

La octava se indica con un entero. 
La imagen original se corresponde al entero $-1$ y los enteros sucesivos ($0,1,\dots$) corresponden a las octavas sucesivas en orden de mayor a menor.
Como hemos decidido para estos apartados utilizar los valores por defecto tenemos que SIFT tiene 5 octavas (más la imagen original) y SURF tiene 3 octavas (más la imagen original).

Como vemos de la salida de la terminal la gran mayoría de los puntos detectados se obtienen de la imagen original y la primera octava, tanto en SIFT como en SURF. Esto nos indica que la mayoría de las características se obtienen al tamaño original de la imagen y no cuando subimos en la pirámide, porque tienen un entorno pequeño en el que son extremos locales.

### En el caso de SIFT, identificar también los puntos detectados en cada capa.

Esta parte está implementado en la función `ap1B_layer`.
Análogamente a la parte anterior utilizamos también un contador.

Utilizando la función `getLayer` que obtenemos del código de `opencv_contrib`.
La capa está guardada en el byte inferior. 
Como hemos utilizado los valores por defecto el número de capas es 3.
Las capas se indican con un entero, que empieza desde el 1.

Como vemos, en contraste a la distribución por octavas, los puntos detectados se distribuyen de manera más uniforme entre las capas en cada octava, aunque seguimos teniendo una concentración mayor en la primera capa.

### Mostrar el resultado sobre la imagen original

Esta parte está implementada en la función `ap1B_draw_circles`.
La función `cv.circle` toma una imagen, el centro del círculo, su radio y su color y devuelve una nueva imagen con este círculo.

Para este ejercicio definimos un diccionario de colores `OCTAVE_COLORS` para asignar un color a cada capa.
Me restrinjo al número de capas que aparecen en el ejemplo que tomo.

Además, el centro de un punto detectado es un par de flotantes, por lo que redondeo las coordenadas para aproximar al píxel más cercano.

Por último, el otro dato que tenemos que obtener del punto es un valor proporcional al tamaño de sigma.
Mirando el código de `opencv_contrib` vemos que en ambos casos el atributo `.size` guarda un valor proporcional a sigma.
En el caso de SURF reduzco ese valor a un 20% del original para que el resultado sea más claro.
Esta operación mantiene la proporcionalidad del radio al valor de sigma.

Por tanto, el código se reduce a un bucle que actualiza una imagen `im_puntos` en el que vamos pintando los diferentes círculos. Muestro el bucle para el caso de SIFT:
```python
for kp in keypoints:
  color = OCTAVE_COLORS[getOctave(kp)]
  center = (round(kp.pt[0]), round(kp.pt[1]))
  im_puntos = cv.circle(im_puntos, center, int(kp.size), color)
```

## C) Cálculo de descriptores

Este apartado está implementado en la función `ap1C`.
Para obtener los descriptores de un conjunto de puntos utilizamos el método `.compute` del objeto SIFT o SURF.
Le pasamos la imagen y el conjunto de puntos y el método devuelve los puntos actualizados (eliminando aquellos para los que no ha podido obtener un descriptor).
Devolvemos por tanto los puntos actualizados y los descriptores.

Los descriptores son vectores de 128 o 64 elementos en SIFT o SURF (ya que no estamos usando descriptores extendidos en SURF al no haber fijado el parámetro `extended` a `True`).

# Ejercicio 2

Un ejemplo de ejecución del código está en la función `ej2`.

En primer lugar explico la obtención de las correspondencias antes de los apartados.
Esta parte está implementada en las funciones `ap2A_BFCC` y `ap2A_LA2NN`, que implementan la detección de correspondencias con los métodos "BruteForce+crossCheck" y "Lowe-Average-2NN" respectivamente.

Los descriptores de cada imagen se guardan en variables del tipo `d_imN` donde `N` es el número de imagen.
La detección de correspondencias varía en función del método:

Para **"BruteForce+crossCheck"** utilizamos el matcher `BFMatcher` con el parámetro `crossCheck` activado.
Por defecto, este matcher corresponde cada punto con el punto con descriptor más cercano de la otra imagen.
El parámetro `crossCheck` indica que la correspondencia debe ser en ambos sentidos: dos descriptores 
$D_1 \in \mathtt{d}_\mathtt{im1},D_2 \in \mathtt{d}_\mathtt{im2}$ se corresponden entre sí si $D_2$ es el 
descriptor más cercano a $D_1$ de entre los descriptores de $\mathtt{d}_\mathtt{im2}$ y viceversa.
El código es por tanto:
```python
matcher = cv.BFMatcher_create(crossCheck = True)
matches = matcher.match(d_im1, d_im2)
```

Para **"Lowe-Average-2NN"** utilizamos el matcher `FlannBasedMatcher`. `FlannBasedMatcher` busca los dos vecinos más cercanos de forma aproximada utilizando un árbol k-d.
A continuación utilizamos los dos vecinos más cercanos para escoger las correspondencias que tengan menos ambigüedad.
De acuerdo al test dado por Lowe en su paper[@LoweDistinctiveImageFeatures2004a], consideramos que una correspondencia no es ambigua cuando el ratio entre la distancia de esa correspondencia y la segunda no excede un cierto umbral; si la correspondencia es errónea es probable que haya otras correspondencias erróneas cercanas.
Fijamos el umbral a 0.8 de acuerdo al paper.

Es decir, el código de obtención de correspondencias en este caso es:
```python
matcher = cv.FlannBasedMatcher_create()
matches = matcher.knnMatch(d_im1, d_im2, k = 2)

clear_matches = []
for best, second in matches:
  if best.distance/second.distance < ratio:
    clear_matches.append(best)
```

## A) Mostrar correspondencias entre ambas imágenes

Este ejercicio está implementado en la función `ap2A`.
La obtención de los puntos clave y sus descriptores se hacen a partir de las funciones `ap1A` y `ap1C` del ejercicio 1. 
Los puntos se guardan en variables del tipo `p_imN` y los descriptores en variables del tipo `d_imN`.
El cálculo de las correspondencias se hace con la función correspondiente al método (descritas antes de este apartado).

Para dibujarlas utilizamos la función `random.sample` para escoger 100 correspondencias aleatorias sin repetición.
A continuación, con la función `cv.drawMatches` mostramos en un mismo canvas ambas imágenes con las correspondencias elegidas uniendo los puntos. 
La flag `cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS` indica que no dibujamos los puntos que no tienen correspondencia.

## B) Valorar la calidad de los resultados obtenidos

\begin{figure}[h!]
\centering
\includegraphics[height=6cm]{src/ej2BF.png}
\caption{100 correspondencias aleatorias con método "BruteForce+CrossCheck"}
\label{fig:ej2BF}
\end{figure}

Los resultados obtenidos pueden verse en las imágenes \ref{fig:ej2BF} y \ref{fig:ej2LA}.

En el caso del método "BruteForce+CrossCheck" las correspondencias encontradas son mayoritariamente correctas (podemos apreciarlo visualmente viendo que casi todas tienen la misma dirección). Sin embargo hay un porcentaje notable de correspondencias erróneas (por ejemplo, la correspondencia del punto azul más alto es errónea).
La variación del porcentaje de correspondencias correctas en función de las correspondencias aleatorias tomadas es alta.

\begin{figure}[h!]
\centering
\includegraphics[height=6cm]{src/ej2LA.png}
\caption{100 correspondencias aleatorias con método "Lowe-Average-2NN" con ratio 0.8}
\label{fig:ej2LA}
\end{figure}

En el caso del método "Lowe-Average-2NN" con ratio 0.8 la gran mayoría de las correspondencias son correctas: los puntos de origen y fin se corresponden con la región de solapamiento de ambas imágenes y la dirección de la gran mayoría de las rectas es correcta. Hay un porcentaje menor de correspondencias erróneas. La variación del porcentaje de correspondencias correctas en función de las correspondencias aleatorias tomadas es baja.

## C) Comparar ambas técnicas en términos de calidad

La técnica "Lowe-Average-2NN" es sin duda superior a "BruteForce+CrossCheck" cuando ajustamos el ratio correctamente.
Podemos ver en las correspondencias aleatorias mostradas por el programa que consigue de forma muy consistente más correspondencias correctas.

\begin{figure}[h!]
\centering
\includegraphics[height=6cm]{src/ej2LA5.png}
\caption{100 correspondencias aleatorias con método "Lowe-Average-2NN" con ratio 0.5}
\label{fig:ej2LA5}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[height=6cm]{src/ej2LA9.png}
\caption{100 correspondencias aleatorias con método "Lowe-Average-2NN" con ratio 0.9}
\label{fig:ej2LA9}
\end{figure}

Su rendimiento depende esencialmente del ratio elegido; si reducimos el ratio reducimos el número de correspondencias pero aumentamos su calidad (ver imagen \ref{fig:ej2LA5}) mientras que si aumentamos el ratio aumentamos el número de correspondencias pero tenemos más correspondencias erróneas (ver \ref{fig:ej2LA9}).
Con un ratio de 0.9 el comportamiento del algoritmo es visualmente similar al de "BruteForce+CrossCheck".

Utilizaremos por tanto el método "Lowe-Average-2NN" para los ejercicios siguientes, en los que tomamos el ratio 0.8 de acuerdo a lo descrito en el paper, ya que da una cantidad suficiente de correspondencias con un porcentaje muy pequeño de estas que sea errónea.

# Ejercicio 3 y 4

\begin{figure}[h!]
\centering
\includegraphics[height=6cm]{src/ej3-2.jpg}
\caption{Mosaico con $N = 3$ imágenes}
\label{fig:ej3}
\end{figure}

En esta sección describo tanto el ejercicio 3 como el 4 ya que utilizan el mismo código (sólo varían en la definición del canvas).
Ejemplos de ejecución pueden verse en `ej3` y `ej4` (la única diferencia está en la definición del canvas).
Sus resultados pueden verse en las imágenes \ref{fig:ej3} y \ref{fig:ej4} respectivamente.

## A) Definir imagen de mosaico.

Este ejercicio está implementado en la función `ap3A`.
Esta función define la imagen en la que estará el mosaico y la homografía que traslada una imagen al centro del mosaico.

Defino el canvas como un array NumPy de ceros tribanda de `uint8` con suficiente espacio para que quepa el mosaico. Dado que las homografías son transformaciones afines arbitrarias no podemos a priori calcular el tamaño que ocupará el mosaico así que las dimensiones que he tomado están ajustadas manualmente para los ejemplos (con las imágenes yosemite y mosaico). De esta forma la definición del canvas es:
`canvas = np.zeros((canvas_height, canvas_width, 3), np.uint8)`

A continuación definimos la homografía que lleva la imagen central al mosaico.
La homografía en este caso será una traslación, que definimos de tal manera que la imagen del punto medio de la imagen central sea el punto medio del canvas (salvo posible ajuste manual).
Para ello, calculamos la mitad de la diferencia entre la altura (anchura) del mosaico y la altura (anchura) de la imagen central y construimos manualmente la matriz de la homografía:
```python
height, width, _ = ims[N//2].shape
tx = (canvas_width - width)/2 + dx
ty = (canvas_height - height)/2 + dy
M = np.array([[1,0,tx],[0,1,ty],[0,0,1]])
```
Los parámetros `dx` y `dy` nos permiten trasladar manualmente el centro de la imagen para centrar la imagen.

## B) Definir homografía de imágenes a mosaico.

Este ejercicio está implementado en la función `ap3B` y la función `ap3B_direct_homographies`.

### Homografías directas

La función `ap3B_direct_homographies` toma la lista de imágenes y devuelve una lista de las homografías directas entre una imagen y la siguiente o anterior. 
Dada una lista de $N$ imágenes definimos su imagen central como la imagen en la posición $\operatorname{mid} = \lfloor N/2\rfloor$ (empezando a contar desde 0).

La función `ap3B_direct_homographies` entonces calcula una lista `homs` de $N$ elementos que tiene en la posición $n$:

- si $n < \operatorname{mid}$ entonces calcula una homografía de $n$ a $m := n+1$,
- si $n > \operatorname{mid}$ entonces calcula una homografía de $n$ a $m := n-1$ y
- si $n = \operatorname{mid}$ entonces no está definida (en concreto vale `None`)

La función se reduce entonces a un bucle que recorre los $n$ que enumeran las imágenes y calcula la homografía adecuada. Asumiendo que ya hemos fijado el valor de `m` tenemos que el cuerpo del bucle es:
```python
p1, p2 = ap1A(ims[n], "SIFT"), ap1A(ims[m], "SIFT")
d1, d2 = ap1C(ims[n], p1, "SIFT"), ap1C(ims[m], p2, "SIFT")
matches = ap2A_LA2NN(d1, d2) # matches

sources = np.array([p1[match.queryIdx].pt for match in matches])
dests   = np.array([p2[match.trainIdx].pt for match in matches])

homs.append(cv.findHomography(sources, dests, cv.RANSAC, 1)[0])
```

Como vemos, calculamos los puntos usando el ejercicio 1, sus correspondencias usando el ejercicio 2, y finalmente separamos en 2 listas (`sources` y `dests`) los orígenes y destinos de las correspondencias utilizando los campos `queryIdx` y `trainIdx` de cada correspondencia.

Por último, calculamos la homografía con `findHomography` y tomamos su primer valor de retorno (que es la matriz 3x3 que define la homografía).

### Homografías al mosaico

Obtenidas estas homografías y la homografía que lleva la imagen central al mosaico, la función `ap3B` compone estas homografías para obtener una homografía que lleva cada imagen al mosaico.

Definimos `homs` como el resultado de llamar a `ap3B_direct_homographies`, `mid` como en la sección
anterior y `M` como la homografía que lleva la imagen central al canvas. En tal caso sólo tenemos que componer las homografías para obtener la homografía de cada imagen al mosaico.

Para la imagen en la posición `n` calculamos la homografía con el siguiente código:
```python
homography = M
for m in range(n, mid, 1 if n < mid else -1):
  homography = homography @ homs[m]
```

`@` denota el producto matricial.
Para entender el código discuto qué hace el código en función del valor de `n`:

- si $n < \operatorname{mid}$ entonces compone con `M` por la derecha las homografías que llevan cada imagen a su siguiente de `n` a `mid-1`. Esta composición de homografías nos da por tanto una homografía que lleva la imagen `n` en el mosaico.
- si $n > \operatorname{mid}$ entonces compone con `M` por la derecha las homografías que llevan cada imagen a su anterior de `n` a `mid-1` (en este caso recorridas en orden decreciente). Esta composición de homografías nos da por tanto una homografía que lleva la imagen `n` en el mosaico.
- si $n = \operatorname{mid}$ entonces `range(n,mid,...)` es vacío y por tanto la homografía calculada es simplemente la homografía `M`, que por definición lleva la imagen central al mosaico.

Por último devolvemos esta lista de homografías.

## C) Trasladar imágenes al mosaico

\begin{figure}[h!]
\centering
\includegraphics[height=7cm]{src/ej4.jpg}
\caption{Mosaico con $N > 4$ imágenes}
\label{fig:ej4}
\end{figure}

Este ejercicio está implementado en la función `ap3C`.

En primer lugar obtenemos las homografías que nos da el apartado anterior que guardamos en `homographies`.
A continuación sólo tenemos que trasladar cada imagen en el mosaico.
Para ello utilizamos la función `warpPerspective` con el flag `cv.BORDER_TRANSPARENT` que hace los bordes transparentes (este flag no está documentado pero aparece en el guion).
Esta función aplica una homografía a una imagen y la mueve a una nueva imagen dada por el parámetro `dst`.
Tenemos además que pasarle las dimensiones del canvas resultado.
Por tanto el bucle principal queda:
```python
for im, hom in zip(ims, homographies):
  canvas = cv.warpPerspective(im, hom, (W, H), dst = canvas, 
           borderMode = cv.BORDER_TRANSPARENT)
```

El resultado puede verse en las imágenes \ref{fig:ej3} y \ref{fig:ej4}.

# Bonus

## Ejercicio 3 Bonus

Este ejercicio está implementado en las funciones `ap3Bonus` y `ap3Bonus_hom`.
En ambas funciones `srcs` son los puntos de origen y `dsts` los de destino. 
Un ejemplo de ejecución en el que calculamos la homografía entre dos imágenes de Yosemite y las unimos con la homografía está en `ej3Bonus`.

`ap3Bonus_hom` calcula una homografía dadas 4 correspondencias.
Construye en la matriz `A` el sistema de las diapositivas y calcula la descomposición en valores singulares de `A` con la ayuda de la función `np.linalg.svd`. A continuación toma el vector con menor valor singular asociado y lo transforma en una matriz de homografía.

***

`ap3Bonus` implementa el cálculo de la homografía usando RANSAC. En primer luegar calculamos el número de inliers inicial. Para ello hacemos una ejecución del bucle principal (ver debajo) y calculamos el error (proporción de los puntos que son outliers). Si la proporción es 0 hemos encontrado la homografía y la devolvemos. Si la proporción es 1 entonces fijamos un número máximo de iteraciones. En otro caso usamos el número de iteraciones dado por la fórmula que aparece en [@HartleyMultipleViewGeometry2004].

A continuación ejecutamos ese número de iteraciones el algoritmo principal.
En primer lugar cogemos 4 índices aleatorios sin reemplazamiento: `idx = np.random.choice(N, 4, replace = False)`. A continuación aplicamos la función `ap3Bonus_hom` en `srcs[idx], dsts[idx]` y sacamos la homografía `H`.

Utilizando la función `perspectiveTransform` de OpenCV convertimos a coordenadas homogéneas los puntos, los multiplicamos por la homografía y volvemos a las coordenadas usuales. El resultado se guarda en `homs_dsts`

Por último calculamos el número de inliers. Para ello (reescribo ligeramente el código aquí para la explicación):

1. Calculamos la distancia euclídea entre cada punto destino y su imagen por la homografía `v = np.linalg.norm(dsts-hom_dsts, 2, axis = 1)`
2. Comprobamos aquellos que están a distancia menor que 3 `u = v <= 3` (`u` será un array de booleanos)
3. Sumamos `u` (`True` vale 1 y `False` vale 0) con `np.sum`

Por último actualizamos la mejor homografía hasta el momento si el número de inliers es mayor.

En el ejemplo calculamos la homografía a partir de correspondencias SIFT y representamos el resultado.


\newpage

# Bibliografía
