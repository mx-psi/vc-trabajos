---
title: Trabajo 1
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
toc: true
citation-style: estilo.csl
---

*****

Para cada ejercicio he definido dos funciones: `apNX` y `ejemploNX`.
La función `apNX` implementa el ejercicio y la función `ejemploNX` prueba con distintos ejemplos.

Para cada ejercicio bonus he definido dos funciones `bonusN` y `ejemploBN`.
Hay dos ejercicios bonus 3 que llamo "3" y "3 bis" respectivamente según el orden en el que aparecen en el pdf.

En todos los ejercicios llamo $f$ a la función de dos variables asociada a una imagen si es necesario mencionarla.

\newpage

# Ejercicio 1

## A) Cálculo de convolución de una imagen con una máscara Gaussiana 2D

Para calcular la convolución con una máscara gaussiana utilizamos la función `GaussianBlur`.
Por defecto, salvo que se especifique otro argumento fijo el parámetro $\sigma_Y$ igual a $\sigma_X$ y dejo que la función calcule automáticamente el tamaño de kernel.

En los ejemplos podemos ver 5 convoluciones fijando distintos parámetros:

#. Con $\sigma_X = \sigma_Y = 3$ se aprecia pérdida de nitidez y los colores se difuminan uniformemente en todas las direcciones
#. Con $\sigma_X = \sigma_Y = 15$ la pérdida de nitidez es mayor (aumenta en función del sigma). La difuminación sigue siendo uniforme en todas las direcciones.
#. Con $\sigma_X = 3, \sigma_Y = 15$ la imagen pierde nitidez y además se ve deformada en el eje Y debido a que el ratio $\frac{\sigma_Y}{\sigma_X} >> 1$. Análogamente pero en la otra dirección si intercambiamos los argumentos.
#. Con $\sigma_X = \sigma_Y = 10$ pero fijando el tamaño del kernel a 3 se aprecia poca pérdida de nitidez. Esto se debe a que sólo una pequeña parte de la masa de probabilidad de la gaussiana entra dentro del kernel.
#. Con $\sigma_X = \sigma_Y = 10$ pero fijando el tamaño del kernel a 21 se aprecia una mayor pérdida de nitidez ya que, en comparación con el caso anterior, la mayor parte de la masa de probabilidad de la gaussiana ha entrado dentro del kernel.

Los resultados nos indican que:

- La pérdida de nitidez (y mitigación de ruido) aumentan en función del tamaño de $\sigma$
- Si los $\sigma$ no son iguales en ambas direcciones se aprecia cierta deformación hacia la dirección en la que $\sigma$ sea mayor
- Si el tamaño de kernel es demasiado pequeño esto reducirá el efecto del filtro. En particular si $\sigma$ es muy grande tendremos que el filtro es aproximadamente equivalente al dado por una matriz de unos.


## B) Obtener máscaras 1D que permitan calcular la convolución 2D con máscaras de derivadas

Los filtros que obtiene `getDerivKernels` aproximan la derivada de la imagen vista como función de dos variables mediante diferencias finitas. Muestro e interpreto los resultados para $\texttt{dx} = 0,\dots,2$, $\texttt{dy} = 0,\dots,2$ descartando $\texttt{dx} = \texttt{dy} = 0$. Lo hago para tamaños 3 y 5.

A la hora de la interpretación basta restringirnos a las parciales en una de las variables: $\displaystyle \frac{\partial^{n+m} f}{\partial x^n \partial y^m}$ y $\displaystyle \frac{\partial^{n+m} f}{\partial x^m \partial y^n}$ varían sólo en el orden en el que aparecen las máscaras (ya que son la misma operación en distinta dirección).

Además, ajustar `dx` (respectivamente `dy`) sólo varía el primer (segundo) elemento del resultado, luego sólo considero los casos `dx` $= 0, \dots, 2$. Los interpreto sobre una señal 1D que llamo también $f$.
Para tamaño 3:

`dx = 0`
: Si no derivamos en una de las variables en esta variable se hace un filtro de alisamiento 1D. En el caso de tamaño 3 hacemos $f(x-1) + 2f(x) + f(x+1)$. Es un filtro simétrico en el que un píxel tiene más valor cuando más cercano esté a $x$.

`dx = 1`
: En este caso aproximamos $$\lim_{\varepsilon \to 0} \frac{f(x+\varepsilon)- f(x-\varepsilon)}{\varepsilon} \approx \frac{f(x+1) - f(x-1)}{1}$$

`dx = 2`
: Aproximamos la segunda derivada haciendo una aproximación de la primera derivada $$\lim_{\varepsilon \to 0} \frac{f'(x +\varepsilon) - f'(x-\varepsilon)}{\varepsilon} \approx (f(x+1) - f(x)) - (f(x) - f(x-1))=$$ $$f(x+1) - 2f(x) + f(x-1)$$

Para tamaño 5 utilizamos las fórmulas de tamaño 3 ponderando:

`dx = 0`
: Hacemos $$f(x-2) + 4f(x-1) + 6f(x) + 4f(x+1) + f(x+2)$$. De nuevo es un filtro de alisamiento; es simétrico y da más peso a los píxeles centrales.

`dx = 1`
: Calcula $$f(x+2) + 2(f(x+1) - f(x-1)) - f(x-2)=$$  $$(f(x+2) - f(x)) + 2(f(x+1) - f(x-1)) + (f(x) - f(x-2))$$ que aproxima la primera derivada haciendo una media ponderada de las aproximaciones de primera derivada de tamaño 3.

`dx = 2`
: Calcula $$f(x+2) - 2f(x) + f(x-2)=$$ $$(f(x+2) - f(x)) - (f(x) - f(x-2))$$, que aproxima la segunda derivada a partir de las aproximaciones de la primera derivada de tamaño 3.

## C) Cálculo de convolución 2D con una máscara de laplaciana de tamaño variable

La función `Laplacian` calcula la laplaciana de gaussiana de una imagen a partir de diferencias finitas. En concreto aproxima el operador $$\Delta(f) = f_{xx} + f_{yy}$$
Añadimos un filtro de alisamiento gaussiano inicialmente para eliminar ruido y mejorar la visualización de la imagen.

Este operador permite detectar algunos bordes: en los puntos donde no hay cambio de intensidad la salida es 0, y en los que haya un gran cambio en la intensidad de los píxeles en una dirección tendremos que el operador es positivo a un lado y negativo al otro, por lo que podemos detectar los bordes. El tamaño del kernel modifica el grosor de los bordes: en el ejemplo uso tamaños 3 y 31 en los que podemos ver la diferencia de grosor.

Además, el tipo de borde afecta en los bordes de la imagen: puede apreciarse como, en el caso de borde constante, la salida en los bordes tiene un borde negro que no aparece al replicar los bordes.

# Ejercicio 2

## A) Convolución 2D con máscara separable

Utilizamos la función `sepFilter2D` para aplicar una máscara separable a partir de sus vectores de máscara en las componentes X e Y. `sepfilter2D` calcula la correlación así que tenemos que invertir los vectores.
El parámetro de profundidad lo ponemos a `-1` para tomar la profundidad de la imagen original.

Como ejemplos de ejecución paso una gaussiana a partir de su máscara 1D utilizando la función `getGaussianKernel` y un filtro de caja del mismo tamaño que tiene todos sus valores iguales normalizados a 1.
En el caso de la gaussiana podemos observar que el resultado coincide con el del apartado 1A.

## B) Convolución 2D de 1ª derivada

Utilizamos la función `getDerivKernels` para obtener las máscaras 1D que pasamos a la función del apartado A.

En concreto hacemos una 1ª derivada respecto de X y respecto de Y, variando el tamaño del kernel. Como vemos en la imagen la derivada en X detecta los bordes verticales mientras que la derivada en Y detecta los bordes horizontales. Esto es especialmente notable en los extremos de la imagen ya que estamos usando bordes a cero y por tanto la derivada en X (Y) destaca el borde izquierdo (superior) de la imagen.

Si aumentamos el tamaño de la máscara aumentamos el tamaño de los bordes que se muestran, pero esto hace también que el ruido afecte más. El tamaño del kernel por tanto debe ajustarse al tamaño de la imagen.

## C) Convolución 2D de 2ª derivada

Utilizamos la función `getDerivKernels` para obtener las máscaras 1D que pasamos a la función del apartado A.
Como vemos en los ejemplos en este caso también apreciamos los bordes en una u otra dirección ya que en la segunda derivada 

## D) Pirámide Gaussiana

Creamos una pirámide gaussiana ayudándonos de la función `pyrDown`, que genera un nivel de la pirámide a partir del anterior. Utilizamos bordes reflejados.

Como vemos cada imagen tiene la mitad de tamaño que la anterior y se le aplica un filtro gaussiano para evitar *aliasing*.

## E) Pirámide Laplaciana

Creamos una pirámide laplaciana a partir de la pirámide gaussiana de apartado anterior. Sumamos una constante a las imágenes de la pirámide laplaciana para poder apreciar mejor los niveles de la pirámide. Los distintos niveles nos muestran los bordes de la imagen en cada paso, ya que nos quedamos con las frecuencias altas.

La pirámide laplaciana se crea a partir de la gaussiana.
Cada nivel de la laplaciana se forma al restar un nivel de la gaussiana el nivel siguiente aumentado. Para aumentar la imagen utilizamos `pyrUp`. Es importante indicar el tamaño al que queremos redimensionar la imagen, lo que hacemos a partir de `.shape`.

La última imagen es la última de la pirámide gaussiana.

# Ejercicio 3

En este ejercicio construimos imágenes híbridas en blanco y negro a partir de parejas de imágenes.
En primer lugar definimos en `ap3` la imagen híbrida y posteriormente mostramos ejemplos en `ejemplo3`.

Utilizando el ejercicio 1A aplicamos un filtro gaussiano

# Bonus

## Ejercicio 1 Bonus

Definimos una función que dado $\sigma$ devuelve un vector que muestrea a intervalos de 1 unidad la función de densidad de la distribución $\mathcal{N}(0,\sigma)$ y normaliza.

El número de puntos a muestrear lo calculamos como $N = 1 + 2\lfloor3\sigma \rfloor$ de acuerdo a la fórmula que vimos en clase.
Así nos aseguramos tener aproximadamente el ~99.7% de la densidad, ya que en el caso continuo la integral en $[-3\sigma,3\sigma]$ de la función de densidad es aproximadamente $0.997$.

A continuación definimos la mitad de la máscara como `mid`, reservamos memoria para la máscara en `mascara` y definimos la función de densidad de la distribución normal (salvo constante de normalización) en `f`.

Calculamos la máscara muestreando en el punto `n-mid`, de tal forma que si $N = 2n+1$ muestreamos en $\{-n, \dots, 0, \dots, n\}$:

```python
for n in range(longitud):
  x = n - mid
  mascara[n] = f(x)
  
return mascara/np.sum(mascara)
```

Devolvemos la máscara normalizada.
Probamos esta máscara como filtro gaussiano en el ejercicio 3 bonus.

## Ejercicio 2 Bonus

En este ejercicio calculamos la convolución 1D de una señal con una máscara, con condiciones de contorno reflejadas en la función `bonus2(mascara, orig)`.

En primer lugar debemos distinguir si estamos en el caso multibanda o unibanda. Si estamos en el caso multibanda (`len(orig.shape) == 2`) entonces separamos cada canal y aplicamos la función en cada canal. Finalmente unimos con `np.stack`:

```python
NCH = orig.shape[1]
return np.stack((bonus2(mascara, orig[::,j]) for j in range(NCH)), axis = 1)
```

He utilizado la función `stack` en este caso porque tiene la misma funcionalidad que `merge` de OpenCV pero funciona para vectores 1D.

En el caso unibanda reservamos en `nueva` la nueva señal y calculamos la mitad del vector máscara en `M`.
El cuerpo principal de la función es:

```python
for i in range(N):
  for j in range(-M, M+1):
    k = i-j
    if k < 0 or k >= N:
      k = N - 1 - (k % N)
    nueva[i] += mascara[j+M]*orig[k]
  nueva[i] = max(min(nueva[i], 255), 0)
```

El bucle exterior recorre los elementos del vector señal, mientras que el bucle interno calcula la suma que da la convolución en cada punto.

Recorremos de $-M$ a $M$ con `j`. 
En el caso de que no estemos en los bordes hacemos:
`nueva[i] += mascara[j+M]*orig[i-j]`.

Si estamos en los bordes calculamos el índice del pixel que se refleja en ese punto que se calcula con $N - 1 - (k \mod N)$ en ambos sentidos (la fórmula es válida ya que $M < N$).
Finalmente hacemos que la suma quede en $[0,255]$.

En el programa vemos un ejemplo con un filtro que desplaza en una unidad una señal.

## Ejercicio 3 Bonus

*(Este es el primer ejercicio 3 bonus que aparece en el pdf)*

Implementamos, apoyándonos en el ejercicio anterior, la convolución 2D con máscaras separables.
Los argumentos son los vectores de convolución `vX` y `vY` y la imagen `im`.

De nuevo distinguimos el caso unibanda y multibanda. En el segundo caso utilizamos `split` y `merge` para aplicar la convolución a cada canal:
```
canales  = cv.split(im)
return cv.merge([bonus3(vX, vY, canal) for canal in canales])
```

En otro caso hacemos una copia de la imagen en `nueva` y aplicamos por columnas y filas la convolución 1D del apartado anterior.

En este caso `N` y `M` son las dimensiones de la imagen.
Tomamos una fila/columna de la imagen y se la pasamos a la función del ejercicio bonus 2 para convolucionarla, y hacemos lo mismo con el otro ejercicio.


```python
for j in range(M):
  nueva[::,j] = bonus2(vX, nueva[::, j])
for i in range(N):
  nueva[i,::] = bonus2(vY, nueva[i, ::])
```

## Ejercicio 3 bis Bonus

*(Este es el segundo ejercicio 3 bonus que aparece en el pdf)*


## Ejercicio 4 Bonus
