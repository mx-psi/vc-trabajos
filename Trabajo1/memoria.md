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
header-includes:
- \usepackage{graphicx}
toc: true
citation-style: estilo.csl
---

*****

Para cada ejercicio he definido dos funciones: `apNX` y `ejemploNX`.
La función `apNX` implementa el ejercicio y la función `ejemploNX` prueba con distintos ejemplos.

Para cada ejercicio bonus he definido dos funciones `bonusN` y `ejemploBN`.
Hay dos ejercicios bonus 3 que llamo "3" y "3 bis" respectivamente según el orden en el que aparecen en el pdf.

\newpage

# Ejercicio 1

## A) Cálculo de convolución de una imagen con máscara Gaussiana 2D


\begin{figure}[h!]
\centering
\includegraphics[height=4cm]{src/ej1A-1.png}
\caption{Original, $\sigma = 3$, $\sigma = 15$}
\label{fig:im0}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[height=4cm]{src/ej1A-2.png}
\caption{Original, $\sigma_X \neq \sigma_Y$}
\label{fig:im1}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[height=4cm]{src/ej1A-3.png}
\caption{Original vs mismo $\sigma$ y distinto kernel}
\label{fig:im2}
\end{figure}

Para calcular la convolución con una máscara gaussiana utilizamos la función `GaussianBlur`.
Por defecto, salvo que se especifique otro argumento fijo $\sigma_Y := \sigma_X$ y dejo que la función calcule automáticamente el tamaño de kernel.

En los ejemplos podemos ver 5 convoluciones fijando distintos parámetros:

#. Con $\sigma_X = \sigma_Y = 3$ (\ref{fig:im0}) se aprecia pérdida de nitidez y los colores se difuminan uniformemente en todas las direcciones
#. Con $\sigma_X = \sigma_Y = 15$ (\ref{fig:im0}) la pérdida de nitidez es mayor (aumenta en función del sigma). La difuminación sigue siendo uniforme en todas las direcciones.
#. Con $\sigma_X = 3, \sigma_Y = 15$ (\ref{fig:im1}) la imagen pierde nitidez y además se ve deformada en el eje Y debido a que el ratio $\frac{\sigma_Y}{\sigma_X} >> 1$. Análogamente pero en la otra dirección si intercambiamos los argumentos.
#. Con $\sigma_X = \sigma_Y = 10$ (\ref{fig:im2}) pero fijando el tamaño del kernel a 3 se aprecia poca pérdida de nitidez. Esto se debe a que sólo una pequeña parte de la masa de probabilidad de la gaussiana entra dentro del kernel.
#. Con $\sigma_X = \sigma_Y = 10$ (\ref{fig:im2}) pero fijando el tamaño del kernel a 21 se aprecia una mayor pérdida de nitidez ya que, en comparación con el caso anterior, la mayor parte de la masa de probabilidad de la gaussiana ha entrado dentro del kernel.

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
: En este caso aproximamos $$\lim_{\varepsilon \to 0} \frac{f(x+\varepsilon)- f(x-\varepsilon)}{\varepsilon} \approx f(x+1) - f(x-1)$$ Esto nos muestra los bordes porque aproxima la derivada que nos indica el ratio de cambio.

`dx = 2`
: Aproximamos la segunda derivada haciendo una aproximación de la primera derivada $$\lim_{\varepsilon \to 0} \frac{f'(x +\varepsilon) - f'(x-\varepsilon)}{\varepsilon} \approx (f(x+1) - f(x)) - (f(x) - f(x-1))=$$ $$f(x+1) - 2f(x) + f(x-1)$$ La segunda derivada será negativa antes de un cambio y positiva después de este

Para tamaño 5 utilizamos las fórmulas de tamaño 3 ponderando:

`dx = 0`
: Hacemos $$f(x-2) + 4f(x-1) + 6f(x) + 4f(x+1) + f(x+2)$$. De nuevo es un filtro de alisamiento; es simétrico y da más peso a los píxeles centrales.

`dx = 1`
: Calcula $$f(x+2) + 2(f(x+1) - f(x-1)) - f(x-2)=$$  $$(f(x+2) - f(x)) + 2(f(x+1) - f(x-1)) + (f(x) - f(x-2))$$ que aproxima la primera derivada haciendo una media ponderada de las aproximaciones de primera derivada de tamaño 3.

`dx = 2`
: Calcula $$f(x+2) - 2f(x) + f(x-2)=$$ $$(f(x+2) - f(x)) - (f(x) - f(x-2))$$, que aproxima la segunda derivada a partir de las aproximaciones de la primera derivada de tamaño 3.

\newpage

## C) Cálculo de convolución 2D con una máscara de laplaciana de tamaño variable

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej1C.png}
\caption{Laplaciana con distintos tamaños}
\label{fig:im3}
\end{figure}

La función `Laplacian` calcula la laplaciana de gaussiana de una imagen a partir de diferencias finitas. En concreto aproxima el operador $$\Delta(f) = f_{xx} + f_{yy}$$
Añadimos un filtro de alisamiento gaussiano inicialmente para eliminar ruido y mejorar la visualización de la imagen.
Podemos ver el resultado en (\ref{fig:im3}).

Este operador permite detectar algunos bordes: en los puntos donde no hay cambio de intensidad la salida es 0, y en los que haya un gran cambio en la intensidad de los píxeles en una dirección tendremos que el operador es positivo a un lado y negativo al otro, por lo que podemos detectar los bordes. El tamaño del kernel modifica el grosor de los bordes: en el ejemplo uso tamaños 3 y 5 en los que podemos ver la diferencia de grosor.

Además, el tipo de borde afecta en los bordes de la imagen: puede apreciarse como, en el caso de borde constante, la salida en los bordes tiene un borde negro que no aparece al replicar los bordes.

# Ejercicio 2

## A) Convolución 2D con máscara separable

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej2A.png}
\caption{Ejemplos de convolución con filtro gaussiano y de caja de unos}
\label{fig:im4}
\end{figure}

Utilizamos la función `sepFilter2D` para aplicar una máscara separable a partir de sus vectores de máscara en las componentes X e Y. `sepfilter2D` calcula la correlación así que tenemos que invertir los vectores.
El parámetro de profundidad lo ponemos a `-1` para tomar la profundidad de la imagen original.

Como ejemplos de ejecución paso una gaussiana a partir de su máscara 1D utilizando la función `getGaussianKernel` y un filtro de caja del mismo tamaño que tiene todos sus valores iguales normalizados a 1 (ver \ref{fig:im4}).
En el caso de la gaussiana podemos observar que el resultado coincide con el del apartado 1A.

## B) Convolución 2D de 1ª derivada

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej2B-1.png}
\caption{Convolución 2D de 1ª derivada}
\label{fig:im5}
\end{figure}

Utilizamos la función `getDerivKernels` para obtener las máscaras 1D que pasamos a la función del apartado A.

En concreto hacemos una 1ª derivada respecto de X y respecto de Y, variando el tamaño del kernel. Como vemos en la imagen la derivada en X detecta los bordes verticales mientras que la derivada en Y detecta los bordes horizontales. Esto es especialmente notable en los extremos de la imagen (ver \ref{fig:im5}) ya que estamos usando bordes a cero y por tanto la derivada en X (Y) destaca el borde izquierdo (superior) de la imagen.

Si aumentamos el tamaño de la máscara aumentamos el tamaño de los bordes que se muestran, pero esto hace también que el ruido afecte más. El tamaño del kernel por tanto debe ajustarse al tamaño de la imagen.

\newpage

## C) Convolución 2D de 2ª derivada

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej2C-1.png}
\caption{Convolución 2D de 2ª derivada}
\label{fig:im6}
\end{figure}


Utilizamos la función `getDerivKernels` para obtener las máscaras 1D que pasamos a la función del apartado A.
Como vemos en los ejemplos (\ref{fig:im6}) en este caso también apreciamos los bordes en una u otra dirección ya que en la segunda derivada 

## D) Pirámide Gaussiana

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej2D.png}
\caption{Pirámide gaussiana}
\label{fig:im7}
\end{figure}

Creamos una pirámide gaussiana ayudándonos de la función `pyrDown`, que genera un nivel de la pirámide a partir del anterior. Utilizamos bordes reflejados y replicados, que, en este caso, no generan un efecto apreciable en la imagen.

El cuerpo de la función es:

```python
piramide = [im]
for n in range(niveles-1):
  piramide.append(cv.pyrDown(piramide[-1], borderType = tipoBorde))
```

Creamos el siguiente nivel de la pirámide aplicando `pyrDown` al último nivel existente.
Como vemos en (\ref{fig:im7}) cada imagen tiene la mitad de tamaño que la anterior y se le aplica un filtro gaussiano para evitar *aliasing*. Los distintos niveles de la pirámide nos muestran cómo veríamos la imagen a distancia.
En el ejercicio de bonus podemos ver como esto hace que veamos las frecuencias altas o bajas.

## E) Pirámide Laplaciana

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej2E.png}
\caption{Pirámide laplaciana}
\label{fig:im8}
\end{figure}

Creamos una pirámide laplaciana a partir de la pirámide gaussiana de apartado anterior. Sumamos una constante a las imágenes de la pirámide laplaciana para poder apreciar mejor los niveles de la pirámide. Los distintos niveles nos muestran los bordes de la imagen en cada paso, ya que nos quedamos con las frecuencias altas.
Podemos ver el resultado en (\ref{fig:im8}).

El cuerpo de la función es:

```python
p_gauss = ap2D(im, tipoBorde, niveles = niveles+1)
pir_lap   = []

for n in range(niveles):
  pir_lap.append(
    cv.subtract(p_gauss[n], # Resta al nivel n
        cv.pyrUp(p_gauss[n+1], 
                 dstsize = (p_gauss[n].shape[1], p_gauss[n].shape[0])) # el nivel n+1
                  ) + 50) # Suma una constante para visualizarlo
```

Restamos al nivel n de la pirámide laplaciana el nivel $n+1$ aumentado. Para aumentarlo tenemos que fijar el parámetro `dstsize`.

La pirámide laplaciana se crea a partir de la gaussiana.
Cada nivel de la laplaciana se forma al restar un nivel de la gaussiana el nivel siguiente aumentado. Para aumentar la imagen utilizamos `pyrUp`. Es importante indicar el tamaño al que queremos redimensionar la imagen, lo que hacemos a partir de `.shape`.

# Ejercicio 3

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ej3-3.png}
\caption{Ejemplo de pareja de imágenes híbridas}
\label{fig:im9}
\end{figure}

En este ejercicio construimos imágenes híbridas en blanco y negro a partir de parejas de imágenes.
En primer lugar definimos en `ap3` la imagen híbrida y posteriormente mostramos ejemplos en `ejemplo3`.

Para obtener las frecuencias bajas utilizamos un filtro gaussiano con el parámetro $\sigma_1$.
Para obtener las frecuencias altas restamos a una imagen sus frecuencias bajas (que obtenemos con un filtro gaussiano con parámetro $\sigma_2$).
Es importante para este segundo caso que utilicemos la función `subtract` de OpenCV; si no habrá píxeles en los que tendremos overflow por estar las imágenes guardadas como enteros sin signo.

Los ejemplos en `ejemplo3` los hacemos con las 3 parejas avión y pájaro, bicicleta y moto, gato y perro.
Ajustamos individualmente los parámetros $\sigma_1, \sigma_2$ para cada pareja de imágenes de tal manera que se vea correctamente. Los valores elegidos son:

- 3 y 5 para las parejas avión-pájaro y bicicleta-moto
- 9 y 9 para la pareja gato-perro (en \ref{fig:im9})

En el ejercicio bonus 3 bis veremos como en función de la distancia a la que veamos las imágenes podemos ver un elemento de la pareja u otro (simulando esta vista a distancia con la pirámide gaussiana).

\newpage

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

En este ejercicio calculamos la convolución 1D de una señal con una máscara, con condiciones de contorno reflejadas en la función `bonus2(mascara, orig)`. Para ello, por comodidad, primero definimos una función de correlación a la que después le pasamos el vector máscara invertido.

En primer lugar debemos distinguir si estamos en el caso multibanda o unibanda. Si estamos en el caso multibanda (`len(orig.shape) == 2`) entonces separamos cada canal y aplicamos la función en cada canal. Finalmente unimos con `np.stack`:

```python
NCH = orig.shape[1]
return np.stack((bonus2(mascara, orig[::,j]) for j in range(NCH)), axis = 1)
```

He utilizado la función `stack` en este caso porque tiene la misma funcionalidad que `merge` de OpenCV pero funciona para vectores 1D.

En el caso unibanda reservamos en `nueva` la nueva señal y calculamos la mitad del vector máscara en `M`.
Para optimizar la función utilizo funciones de NumPy.
En concreto, extiendo en `extended` el vector señal para tener los bordes adecuados (reflejando la señal) y a continuación calculo la correlación con el producto escalar.

El cuerpo principal de la función es:

```python
extended = np.concatenate((orig[::-1], orig, orig[::-1]))

for i in range(N):
  nueva[i] = np.dot(mascara, extended[i-M+N:i+M+N+1])
```

El bucle recorre los elementos del vector señal y se calcula la correlación en cada punto como el producto escalar de la máscara por el trozo de señal centrado en el elemento actual.

Finalmente, para hacer la convolución llamamos a la función de correlación con el vector máscara invertido.
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

En otro caso hacemos una copia de la imagen en `nueva` y aplicamos por columnas y filas la correlación 1D del apartado anterior con los vectores máscara invertidos (que llamamos `rVX` y `rVY`).

En este caso `N` y `M` son las dimensiones de la imagen.
Tomamos una fila/columna de la imagen y se la pasamos a la función del ejercicio bonus 2 para convolucionarla, y hacemos lo mismo con el otro ejercicio.


```python
for j in range(M):
  nueva[::,j] = correl(rVX, nueva[::, j])
for i in range(N):
  nueva[i,::] = correl(rVY, nueva[i, ::])
```

\newpage

## Ejercicio 3 bis Bonus

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ejB3b.png}
\caption{Pirámide gaussiana de imagen híbrida}
\label{fig:im10}
\end{figure}

*(Este es el segundo ejercicio 3 bonus que aparece en el pdf)*

En este ejercicio calculamos la pirámide gaussiana de imágenes híbridas del ejercicio 3.
El código es idéntico al del apartado 2D, excepto que utilizamos la implementación propia de la función `cv.pyrDown`.

La implementación completa de esta función es:

```python
vGauss = bonus1(1)
im_bor = bonus3(vGauss, vGauss, im)
forma = (im.shape[0]//2, im.shape[1]//2)
nueva_im = np.zeros(forma, np.uint8)

for i in range(forma[0]):
  for j in range(forma[1]):
    nueva_im[i,j] = im_bor[2*i, 2*j]
return nueva_im
```

En primer lugar aplicamos un filtro gaussiano a la imagen utilizando el ejercicio 3 bonus (no bis).
Calculamos la forma del siguiente nivel de la gaussiana haciendo la división entera de las dimensiones de la imagen original.

Finalmente rellenamos la nueva imagen tomando uno de cada dos píxeles (es decir, eliminamos una de cada dos filas y una de cada dos columnas).

Como vemos en los resultados (\ref{fig:im10}) cuanto más pequeña es la imagen más destacan las frecuencias bajas y más vemos por tanto la primera imagen del par. En el caso del par gato-perro podemos ver ese efecto de forma notable.

## Ejercicio 4 Bonus

\begin{figure}[h!]
\includegraphics[width=\textwidth]{src/ejB4.png}
\caption{Ejemplo de imagen híbrida a color}
\label{fig:im11}
\end{figure}

En este ejercicio reproducimos el ejercicio 3 no bonus con las mismas parejas pero a color. (\ref{fig:im11}) nos muestra el resultado.

Como vemos el resultado es similar al de las imágenes híbridas en blanco y negro. El procedimiento es análogo al de las imágenes híbridas en blanco y negro pero utilizando funciones propias, que separan en las 3 bandas y aplican el algoritmo de imágenes híbridas en cada banda. 
Es importante pasar las imágenes a un tipo con signo para hacer la resta y luego pasar a 0 los valores negativos (`vG2` es el vector máscara gaussiano):

```python
hi_pass = im2.astype(float) - bonus3(vG2, vG2, im2).astype(float)
hi_pass[hi_pass < 0] = 0
hi_pass = hi_pass.astype('uint8') # Frecuencias altas de im2
```

Los parámetros utilizados son los mismos que los de las imágenes híbridas en blanco y negro.
