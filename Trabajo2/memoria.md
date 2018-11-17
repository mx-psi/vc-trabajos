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

# Ejercicio 1

Un ejemplo de la ejecución de todas las partes de este ejercicio está en la función `ej1ABC`.

## A) Cálculo de puntos con SIFT y SURF

Este ejercicio está implementado en la función `ap1A`.
Un ejemplo está en la función `ej1A`.

### Variar valores de umbral hasta obtener un conjunto numeroso (> 1000) de puntos SIFT y SURF representativo de la imagen.

### Justificar la elección de los parámetros en relación a la representatividad de los puntos obtenidos.

> Probar con distintos parámetros para la justificación

## B) Identificar localización de puntos

Este ejercicio está implementado en las funciones `getOctave`, `getLayer`, `ap1B_octave`, `ap1B_layer` y `ap1B_draw_circles`. 

Las funciones `getOctave` y `getLayer` son reimplementaciones en Python del código fuente en C de la función `unpackOctave` del módulo `xfeatures2d.SIFT` [@RepositoryOpenCVextra2018].
Estas funciones permiten obtener respectivamente la octava y la capa de un punto obtenido con SIFT.

### Identificar cuántos puntos se han detectado dentro de cada octava.

Para obtener la octava:

- En el caso de SURF sólo tenemos que obtener la octava a partir del atributo `.octave` de cada punto.
- En el caso de SIFT la octava está guardada en el byte superior del atributo `.octave`. 
  Utilizamos la función `getOctave` obtenida del código fuente de opencv_contrib.

La octava se indica con un entero. 
La imagen original se corresponde al entero $-1$ y los enteros sucesivos ($0,1,\dots$) corresponden a las octavas sucesivas en orden.


### En el caso de SIFT, identificar también los puntos detectados en cada capa.

> ¡Hay que mirar el código fuente directamente!
> Hay que identificar de qué octava y de qué capa ha salido.

## C) Cálculo de descriptores

> Mostrar cómo con el vector de keyPoint extraídos se pueden calcular los descriptores SIFT y SURF asociados a cada punto usando OpenCV.

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

La obtención de los puntos clave y sus descriptores se hacen a partir de las funciones `ap1A` y `ap1C` del ejercicio 1. 
Los puntos se guardan en variables del tipo `p_imN` y los descriptores en variables del tipo `d_imN`.
El cálculo de las correspondencias se hace con la función correspondiente al método (descritas antes de este apartado).

Para dibujarlas utilizamos la función `random.sample` para escoger 100 correspondencias aleatorias sin repetición.
A continuación, con la función `cv.drawMatches` mostramos en un mismo canvas ambas imágenes con las correspondencias elegidas uniendo los puntos. 
La flag `cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS` indica que no dibujamos los puntos que no tienen correspondencia.

## B) Valorar la calidad de los resultados obtenidos

## C) Comparar ambas técnicas en términos de calidad

# Ejercicio 3

> Escribir una función que genere un mosaico de calidad a
> partir de N = 3 imágenes relacionadas por homografías, sus listas de
> keyPoints calculados de acuerdo al punto anterior y las correspondencias
> encontradas entre dichas listas. Estimar las homografías entre ellas usando
> la función cv2.findHomography(p1,p2, CV RANSAC,1). Para el mosaico
> será necesario.

NO DEFINIR CADA HOMOGRAFÍA DE CADA IMAGEN AL MOSAICO
Sacar los keypoints de todas e ir componiendo desde el centro.

## A) Definir imagen de mosaico.
## B) Definir homografía de imágenes a mosaico.
## C) Trasladar imágenes al mosaico

# Ejercicio 4

# Bonus
## Ejercicio 1 Bonus
Implementar de forma eficiente el detector propuesto en el paper de Brown & Szeliski & Winder.

## Ejercicio 2 Bonus
Implementar de forma eficiente el descriptor propuesto en el paper de Brown & Szeliski & Winder.

## Ejercicio 3 Bonus
Implementar de forma eficiente la estimación de una homografía usando RANSAC.


\newpage

# Bibliografía
