---
title: Cuestionario Teoría 2
subtitle: Visión por Computador
author: Pablo Baeyens Fernández
date: Curso 2018-2019
documentclass: scrartcl
classoption: egregdoesnotlikesansseriftitles
lang: es
colorlinks: true
header-includes:
- \usepackage{graphicx}
- \usepackage{csquotes}
- \AtBeginEnvironment{quote}{\itshape}
- \usepackage{xcolor}
toc: false
colorlinks: true
bibliography: citas.bib
biblio-style: plain
link-citations: true
citation-style: estilo.csl
---


# Pregunta 1

> Identificar las diferencias esenciales entre el plano afín y el plano proyectivo.

El plano afín es el espacio afín de dos dimensiones $\mathbb{R}^2$.
El plano proyectivo se construye como un espacio cociente sobre $\mathbb{R}^3-\{0\}$ en el que identificamos dos vectores si son proporcionales, esto es $u \sim v \iff \exists \lambda \in \mathbb{R}: u = \lambda v$.

Podemos ver el plano afín como un subespacio del plano proyectivo mediante la aplicación $i : \mathbb{R}^2 \to \mathbb{P}^2$, dada por $i(x,y) = (x,y,1)$ (coordenadas homogéneas).

Sus diferencias esenciales más importantes son que el plano proyectivo incluye **puntos del infinito** que no pertenecen al plano afín y que las transformaciones inyectivas en el plano proyectivo incluyen transformaciones en perspectiva.

> ¿Cuáles son sus consecuencias?

Las consecuencias más importantes son que el plano proyectivo tiene una geometría con mejores propiedades: todo par de rectas se corta en exactamente un punto (las paralelas lo hacen en puntos del infinito) y podemos permite trabajar de forma más sencilla con transformaciones en perspectiva y representar matricialmente aplicaciones proyectivas que no sean afines.

# Pregunta 2

> Demuestre que los puntos de la recta del infinito del plano proyectivo son vectores del tipo $(a,b,0)$ con $a,b \in \mathbb{R}$

Los puntos de la recta del infinito $R_\infty$ son aquellos que no tienen preimagen respecto de la aplicación $i$ definida en la [Pregunta 1] (esto es, que no pertenecen al espacio afín). Dado un punto $(a,b,c)$ estará relacionado con un punto de la forma $(x,y,1)$ mediante $\sim$ si existe $\lambda \in \mathbb{R}$ tal que $\lambda(a,b,c) = (x,y,1)$.

La tercera coordenada nos da la igualdad $\lambda c = 1$, luego $\lambda$ y, $c$ son no nulos y $\lambda = c^{-1}$.
Es decir, la inversa de $i$, si existe es $i^{-1}(a, b, c) = (a/c, b/c)$. Esta aplicación está definida para puntos con $c \neq 0$, es decir, que los puntos que no pertenecen al espacio afín (esto es, $R_\infty$) son los puntos de la forma $(a,b,0)$.

Alternativamente, podemos definir $R_\infty$ como la recta dada por el vector  $l = (0, 0, 1)^T$. 
Dado un punto $(a,b,c)^T \in \mathbb{P}^2$ estará en la recta del infinito si y sólo si $(a,b,c)(0,0,1)^T = c = 0$, luego los puntos de $R_\infty$ serán aquellos con tercera coordenada nula.

# Pregunta 3

> En coordenadas homogéneas los puntos y rectas del plano se representan por vectores de tres coordenadas (notados $x$ y $l$ respectivamente), de manera que si una recta contiene a un punto se verifica la ecuación $x^Tl=0$.

> Puede verificar que en coordenadas homogéneas el vector de la recta definida por dos puntos afines puede calcularse como el producto vectorial de los vectores de ambos puntos ($l = x \times x'$). 

<!-- $$x \times x' := \left(\left|\begin{matrix}x_2 & x_3 \\ x'_2 & x'_3 \end{matrix}\right|, - \left|\begin{matrix}x_1 & x_3 \\ x'_1 & x'_3 \end{matrix}\right|, \left|\begin{matrix}x_1 & x_2 \\ x'_1 & x'_2 \end{matrix}\right|\right)$$ -->

En efecto, sean $x = (x_1, x_2, x_3)^T, x' = (x'_1, x'_2, x'_3)^T$ dos puntos en coordenadas homogéneas,
Si tomamos $l = x \times x'$ podemos comprobar que $x$ y $x'$ pertenecen a la recta:
\begin{align*}
x^Tl  & = x_1\left|\begin{matrix}x_2 & x_3 \\ x'_2 & x'_3 \end{matrix}\right| - x_2\left|\begin{matrix}x_1 & x_3 \\ x'_1 & x'_3 \end{matrix}\right| + x_3\left|\begin{matrix}x_1 & x_2 \\ x'_1 & x'_2 \end{matrix}\right| \\
& = (x_2x'_3 - x'_2x_3)x_1 - (x_1x'_3 - x'_1x_3)x_2 + (x_1x'_2 -x'_1x_2)x_3 \\
& = \textcolor{blue}{x_2x'_3x_1} - \textcolor{teal}{x'_2x_3x_1} - \textcolor{blue}{x_1x'_3x_2} + \textcolor{purple}{x'_1x_3x_2} + \textcolor{teal}{x_1x'_2x_3} - \textcolor{purple}{x'_1x_2x_3} \\
& = 0
\end{align*}
donde los términos del mismo color se cancelan entre sí.

Para $x'$ aplicamos que el producto vectorial es anticonmutativo y por simetría $$x'^Tl = x'^T( - (x' \times x)) = - (x'^T(x' \times x)) = 0$$
donde hemos aplicado el cálculo anterior invirtiendo los roles de $x$ y $x'$.

> De igual modo el punto intersección de dos rectas $l$ y $l'$ está dado por $x = l \times l'$

Apoyándonos en el apartado anterior podemos verificar también este hecho, ya que si $x,y \in \mathbb{R}^3$ sabemos que $x^T y = x y^T$ (el producto escalar que es conmutativo). De esta forma
$$(l \times l')^Tl = l^T(l \times l') = 0, \qquad (l \times l')^Tl' = l'^T(l \times l') = 0$$
donde hemos aplicado las igualdades obtenidas en el apartado anterior (que son válidas para vectores de $\mathbb{R}^3$ independientemente de si los interpretamos como puntos o rectas).

> ¿Considera de interés las anteriores propiedades de cara a construir un algoritmo que calcule la intersección de dos rectas cualesquiera del plano? 

**Sí**, dadas dos rectas definidas por los vectores $l$ y $l'$ podemos calcular su intersección en el espacio proyectivo como $x = l \times l' = (x_1, x_2, x_3)$. 

Apoyándonos en la [Pregunta 2] vemos que $x$ se corresponderá a un punto del espacio afín si $x_3 \neq 0$.
En tal caso tenemos que el punto del espacio afín es $(x_1/x_3, x_2/x_3)$.
En otro caso las rectas serán paralelas y no tendrán intersección en el plano afín.

Si las rectas vienen dadas por pares de puntos también podremos aplicar la primera propiedad para calcular en primer lugar los vectores que definen las rectas.


# Pregunta 4

> Defina una homografía entre planos proyectivos que haga que el punto (2,0,3) del plano proyectivo se transforme en un punto de la recta del infinito del plano proyectivo

Por la [Pregunta 2] sabemos que los puntos de $R_\infty$  son de la forma $(a,b,0)$, por lo que tenemos que llevar el punto $x = (2,0,3)$ mediante una homografía $H$ a un punto $x' = Hx$ con $x'_3 = 0$.

Si expresamos $H = (H_{ij})_{i,j = 1,2,3}$ tenemos que $x'_3 = 2H_{31} + 3H_{33} = 0$.
Podemos tomar $H_{31} = -3, H_{33} = 2$ para que se de tal igualdad, y rellenar con la matriz identidad el resto de coordenadas. Por tanto la expresión matricial de la homografía vendrá dada por
$$H = \left(\begin{matrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ -3 & 0 & 2 \end{matrix}\right) $$
y podemos verificar que $x' = Hx = (2,0,0)^T \in R_\infty$.

Por último tenemos que verificar que $H$ es invertible, lo que podemos ver sin más que calcular su determinante, $\operatorname{det}(H) = 2 \neq 0$.


# Pregunta 5

> Descomponer en composición de movimientos elementales (traslación, giro, escala, cizalla, proyectivo) cada una de las matrices de las siguientes homografías $H_1$, $H_2$ y $H_3$:

Dos coordenadas homogéneas representan el mismo punto si son proporcionales, lo que se traslada a homografías: dos matrices de homografía son equivalentes si son proporcionales.

Los movimientos elementales afines son de la forma:
$$T_{v} =   \left(\begin{matrix} 1 & 0 & v_1 \\ 0 & 1 & v_2 \\ 0 & 0 & 1 \end{matrix}\right),
  G_{\theta} =   \left(\begin{matrix} \cos(\theta) & \sin(\theta) & 0 \\ -\sin(\theta) & \cos(\theta) & 0 \\ 0 & 0 & 1 \end{matrix}\right), 
  S_{r} =   \left(\begin{matrix} r_1 & 0 & 0 \\ 0 & r_2 & 0 \\ 0 & 0 & 1 \end{matrix}\right), 
  C_{s} =   \left(\begin{matrix} 1 & s_1 & 0 \\ s_2 & 1 & 0 \\ 0 & 0 & 1 \end{matrix}\right)$$
respectivamente son traslación, giro, escala y cizalla y $v, r, s$ son vectores y $\theta$ está en radianes.
Todo movimiento no afín es una aplicación de tipo proyectivo que no descompongo más.


Para obtener la descomposición he usado estas reglas:

1. Si la última fila es de la forma $(0,0,\lambda), \lambda \neq 0$, multiplico por $\lambda^{-1}$ para obtener una aplicación afín,
2. descompongo cualquier aplicación afín en traslación y parte lineal usando
$$\left(\begin{matrix} a & b & v_1 \\ c & d & v_2 \\ 0 & 0 & 1 \end{matrix}\right) = 
    T_{v} \left(\begin{matrix} a & b & 0 \\ c & d & 0 \\ 0 & 0 & 1 \end{matrix}\right) \text{ y}$$
3. descompongo la parte afín según casos discutidos en cada apartado.

Indico los vectores de traslación o escalado en coordenadas afines.

\vspace*{0.7cm}

> Descomposición de $H_1 = \left(\begin{matrix} 1 & 3 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{matrix}\right) 
    \left(\begin{matrix} 0,2 & 0 & 0 \\ 0 & 0,4 & 0 \\ 0 & 0 & 0,2 \end{matrix}\right)
    \left(\begin{matrix} 1,5 & 0 & 3 \\ 0 & 0,8 & 5 \\ 0 & 0 & 2 \end{matrix}\right)$
    
$H_1$ puede descomponerse en 4 movimientos elementales:
\begin{align*}
H_1 & = 0,4\left(\begin{matrix} 1 & 3 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{matrix}\right) 
    \left(\begin{matrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{matrix}\right)
    \left(\begin{matrix} 1 & 0 & 1,5 \\ 0 & 1 & 2,5 \\ 0 & 0 & 1 \end{matrix}\right)
    \left(\begin{matrix} 0,75 & 0 & 0 \\ 0 & 0,4 & 0 \\ 0 & 0 & 1 \end{matrix}\right) \\
    & = C_s S_r T_v S_{r'},
\end{align*}
donde $s = (3,0)^T, r = (1, 2)^T, v = (1,5; 2,5)^T, r' = (0,75; 0,4)^T$.
La descomposición se obtiene sin más que aplicar las reglas dadas anteriormente.

\vspace*{0.7cm}

> Descomposición de $H_2 = \left(\begin{matrix} 0 & 0,5 & -3 \\ -0,5 & 0 & 2 \\ 0 & 0 & 1 \end{matrix}\right) 
    \left(\begin{matrix} 2 & 0 & 0 \\ 2 & 2 & 0 \\ 0 & 0 & 1 \end{matrix}\right)$
    
Podemos reexpresarlo como el siguiente producto:
\begin{align*}
H_2 & = \left(\begin{matrix} 1 & 0 & -3 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{matrix}\right) 
        \left(\begin{matrix} 0,5 & 0 & 0 \\ 0 & 0,5 & 0 \\ 0 & 0 & 1 \end{matrix}\right)
        \left(\begin{matrix} 0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & 1 \end{matrix}\right)
        \left(\begin{matrix} 2 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{matrix}\right)
        \left(\begin{matrix} 1 & 0 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1 \end{matrix}\right) \\
    & = T_{v} S_{r} G_{\pi/2} S_{r'} C_{s},
\end{align*}
donde $v = (-3,2)^T, r = (\frac12, \frac12)^T, r' = (2,2)^T, s = (0,1)^T$.

Para obtener la descomposición de la primera matriz primero he descompuesto en traslación y parte lineal.
La parte lineal no se correspondía con ninguno de los tipos básicos lo que nos indica que es composición de dos movimientos elementales. En este caso eran un escalado y un giro. Obtengo el escalado teniendo en cuenta que el giro debe cumplir que la suma de $h_{11}^2 + h_{12}^2 = 1$.


\vspace*{0.7cm}
    
> Descomposición de $H_3 = \left(\begin{matrix} 2 & 0 & 3 \\ 0 & 2 & -1 \\ 0 & 1 & 2 \end{matrix}\right) 
    \left(\begin{matrix} 1 & 0,5 & 0 \\ 0,5 & 2 & 0 \\ 0 & 0 & 1 \end{matrix}\right)$
    
La última fila de la primera matriz no es de la forma $(0, 0, \lambda)$, por lo que es una aplicación afín, sino proyectiva, por lo que no la descomponemos más[^desc].
La segunda matriz puede descomponerse en un escalado seguido de una cizalla.
Por tanto la descomposición queda:
\begin{align*}
H_3 & = \left(\begin{matrix} 2 & 0 & 3 \\ 0 & 2 & -1 \\ 0 & 1 & 2 \end{matrix}\right) 
\left(\begin{matrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{matrix}\right) 
\left(\begin{matrix} 1 & 0,5 & 0 \\ 0,25 & 1 & 0 \\ 0 & 0 & 1 \end{matrix}\right)\\
    & = H S_r C_s
\end{align*}
donde $H$ es una aplicación proyectiva, $r = (1,2)^T, s = (0,5; 0,25)^T$.
    
Para obtener la descomposición he hallado el escalado que hacía que los elementos de la diagonal quedaran todos a 1.


# Pregunta 6

> ¿Cuáles son las propiedades necesarias y suficientes para que una matriz defina una homografía entre planos?

Una matriz $H \in \mathcal{M}_{3 \times 3}(\mathbb{R})$ define una homografía entre planos proyectivos si y sólo si es invertible: si no lo fuera habría algún vector que iría al $(0,0,0)$ que no son las coordenadas homogéneas de ningún punto.

Una matriz $H \in \mathcal{M}_{3 \times 3}(\mathbb{R})$ define una homografía que lleva el plano afín en el plano afín si y sólo si su última fila es proporcional a $(0, 0, 1)$.
Esta propiedad es claramente suficiente ya que esto define una aplicación afín.

Para ver que es necesaria, si queremos que sea una aplicación entre planos afines tendremos que 
llevar puntos afines en puntos afines. Por la [Pregunta 2], los puntos afines en coordenadas homogéneas son 
aquellos cuya última coordenada es no nula. Por tanto necesitamos que, si $x = (x_1, x_2, x_3)^T$ con $x_3 \neq 0$ su imagen $Hx = x' = (x'_1, x'_2, x'_3)^T$ verifique $x'_3 \neq 0$. 

Si $H = (H_{ij})_{i, j = 1,2,3}$ y desarrollamos el producto tenemos que 
$$x'_3 = H_{31}x_1 + H_{32}x_2 + H_{33}x_3 = H_{31}x_1 + H_{32}x_2 + H_{33}$$
que se anula en algún punto sólo si la recta dada por $l = (H_{31}, H_{32}, H_{33})^T$ tiene algún punto afín.
Por tanto no tendrá puntos afines sólo si es $R_\infty$, es decir $l$ es proporcional a $(0,0,1)^T$, lo que prueba la equivalencia.


# Pregunta 7

> ¿Qué propiedades de la geometría de un plano quedan invariantes si se aplica una homografía general sobre él?

Sólo podemos asumir que se respeta la **colinealidad**, esto es, una homografía lleva siempre rectas en rectas y puntos no alineados en puntos no alineados.

Si $H$ es una homografía y $l$ es el vector de una recta sabemos que todo punto de la recta cumple $x^Tl = 0$.
Como $H$ es homografía es invertible (y también lo es su traspuesta) luego tenemos que
$$0 = x^T l = x^T(H^T (H^T)^{-1}) l = (x^T H^T) ((H^T)^{-1} l) = (Hx)^T ((H^T)^{-1} l)$$

Es decir $x$ pertenece a la recta dada por $l$ si y sólo si $Hx$ pertenece a la recta dada por $(H^T)^{-1} l$,
luego las homografías llevan rectas en rectas y puntos no alineados en puntos no alineados.

Una homografía general **no** respeta otras propiedades geométricas como la orientación, longitudes o ángulos porque toda transformación afín es una homografía y existen transformaciones afines que no respetan estos aspectos.

Por último, aunque las transformaciones afines sí respetan el paralelismo **no** lo hacen en general las homografías.
Por ejemplo, si consideramos la homografía $H$ dada por 
$$H =  \left(\begin{matrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -1 & 1 \end{matrix}\right) \qquad H' = (H^T)^{-1} =  \left(\begin{matrix} 1 & 0 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{matrix}\right)$$
Por el resultado anterior sabemos que las rectas se transforman de acuerdo $H'$.

Sean $l = (1,0,0)^T, l' = (1,0,1)^T$. Estas rectas se cortan en $l \times l' = (0,-1,0)^T \in R_\infty$, luego en el plano afín son paralelas. Sus imágenes son $H'l = (1,0,0)^T, H'l' = (1,1,1)^T$, que se cortan en $(H'l) \times (H'l') = (0,-1,1)^T$ que es un punto afín, luego las imágenes de estas rectas no son paralelas.

\newpage

# Pregunta 8

> ¿Cuál es la deformación geométrica más fuerte que se puede producir sobre la imagen de un plano por el cambio del punto de vista de la cámara?

Si no trasladamos el punto de vista de la cámara sino que sólo rotamos la cámara o modificamos la distancia focal sabemos que la deformación entre dos imágenes se corresponde con una **homografía**[@HartleyMultipleViewGeometry2004], que es el tipo de deformación geométrica más general en el espacio proyectivo. La deformación será mayor cuanto mayor sea el ángulo de rotación.

Si trasladamos el punto de vista de la cámara entonces la deformación que se produce no tiene por qué ser necesariamente una homografía y será mayor cuanto mayor sea la traslación del punto de vista.

# Pregunta 9

> ¿Qué información de la imagen usa el detector de Harris para seleccionar puntos?

El detector de Harris utiliza información sobre el gradiente de la imagen para detectar esquinas en la imagen.
Utilizando el gradiente calcula una forma cuadrática $H$ que estima la curvatura de la imagen.
Esta forma cuadrática es diagonalizable y sus valores propios corresponden con las curvaturas principales de la imagen vista como superficie, que se calculan como los valores propios de la forma cuadrática. Distinguimos casos:

1. si ambas curvaturas principales son pequeñas entonces estamos en una región plana,
2. si una curvatura es pequeña y la otra no entonces habrá una variación fuerte sólo en un sentido y estaremos ante un borde y
3. si ninguna curvatura es pequeña entonces habrá una variación fuerte en dos sentidos y estaremos en una esquinas.

Es decir, para detectar una esquina el detector Harris necesita saber si el mínimo de los valores propios no es pequeña, en concreto si es un máximo local mayor que un cierto umbral.
Para ello aproxima el mínimo de los valores propios con la función
$$f(x,y) = \frac{\operatorname{det}(H)}{\operatorname{traza}(H)}$$

Es decir, la información que utiliza el detector Harris es la existencia de esquinas a partir de una aproximación de la mínima curvatura principal en cada punto.

> ¿El detector de Harris detecta patrones geométricos o fotométricos?

El detector Harris detecta **patrones geométricos** (esquinas) a partir de el gradiente de la imagen, mediante el procedimiento descrito en la parte anterior.

Es invariante a traslaciones de la intensidad de la forma $I \mapsto I + t$ ya que sólo depende de las derivadas, por lo que es parcialmente invariante a transformaciones en plano fotométrico pero no podemos decir que lo sea totalmente debido al uso del umbral. De este modo en cierto sentido no podemos decir que no haga uso de la información fotométrica.

# Pregunta 10

> ¿Sería adecuado usar como descriptor de un punto Harris los valores de los píxeles de su región de soporte?
> En caso positivo identificar cuando y justificar la respuesta

En general **no** sería adecuado, ya que los valores de los píxeles en la región de soporte son un descriptor que no es invariante a transformaciones geométricas como escalados, rotaciones y otras transformaciones afines ni a cambios en la intensidad como cambios uniformes en la iluminación.

En cambio otros descriptores como SIFT descrito en la [Pregunta 11] sí que poseen una invarianza parcial a este tipo de transformaciones, por lo que un descriptor de este tipo no sería útil en la gran mayoría de los casos.

El único caso en el que sería adecuado es cuando las únicas transformaciones entre las imágenes que queremos relacionar son traslaciones, ya que estas preservan la orientación y tamaño y preservarían los valores de los píxeles (salvo posible ruido de la cámara).

# Pregunta 11

> ¿Qué información de la imagen se codifica en el descriptor de SIFT?

El descriptor de SIFT asigna a cada punto de interés un vector de 128 dimensiones que contiene información sobre las orientaciones del gradiente en el entorno cercano al punto. En concreto el descriptor se calcula a partir de los siguientes pasos, descritos en [@LoweDistinctiveImageFeatures2004a, sección 6.1], para los que asumo que tenemos asignada una orientación del punto:

1. calcula el gradiente en cada punto de la imagen utilizando filtros de derivadas; la capa en la que se ha detectado el punto se utiliza para elegir el nivel de alisado gaussiano. Nos quedamos con la magnitud y orientación (ángulo) en cada punto del gradiente. La orientación se corrige con respecto a la orientación del punto para que el descriptor sea invariante a rotaciones.
3. toma una ventana de dimensiones $16 \times 16$ alrededor del punto que divide en celdas $4 \times 4$ y
4. calcula un histograma de las orientaciones agrupándolo en 8 partes.

El descriptor por tanto codifica en este vector los histogramas dando un total de $128 = 4 \times 4 \times 8$.
La información codificada en el descriptor corresponde con las orientaciones en un entorno del punto corregidas respecto de la orientación principal del punto, información que es invariante a rotaciones y a una gran cantidad de deformaciones geométricas y fotométricas a la imagen, lo que explica su robustez.

# Pregunta 12

> Describa un par de criterios que sirvan para seleccionar parejas de correspondencias (“matching”) entre descriptores de regiones extraídos de dos imágenes. Justificar la idoneidad de los mismos

Dados dos conjuntos de descriptores $D = \{d_i\}_{i = 1, \dots, N}, D' = \{d'_j\}_{j = 1, \dots, M}$ de dos imágenes debemos elegir entre estos aquellas parejas $(d_k, d'_l)$ cuyos puntos asociados sean una correspondencia real.
Para ello describo dos métodos. Asumo que tenemos una función $\operatorname{dist}$ que nos da la distancia entre dos correspondencias.

Fuerza bruta con *crossCheck*
: Para cada $d \in D$ elegimos $d' \in D'$ como el descriptor más cercano a $d$ en $D'$.
  A continuación comprobamos que $d$ sea el descriptor más cercano a $d'$ en $D$.
  En tal caso añadimos la correspondencia $(d,d')$. Si falla alguno de los dos sentidos la descartamos.
  
Lowe-Average-2NN
: Es el método de elección de correspondencias descrito en el paper original que presentó el detector y descriptor SIFT [@LoweDistinctiveImageFeatures2004a].
  Para cada $d \in D$ tomamos los dos descriptores más cercanos a $d$ en $D'$, que llamamos $d'_1, d'_2$.
  A continuación calculamos el ratio $$r = \frac{\operatorname{dist}(d,d'_1)}{\operatorname{dist}(d,d'_2)}.$$
  Si $r$ es mayor que un cierto umbral entonces lo descartamos, ya que consideramos que la distancia entre la mejor 
  correspondencia y la segunda mejor es demasiado pequeña y por tanto hay ambigüedad sobre la correspondencia.
  En otro caso añadimos la correspondencia $(d, d'_1)$.
  El valor del ratio óptimo se estima empíricamente en el paper de SIFT como 0.8.
  
En general el segundo método da empíricamente mejores resultados por lo que es más idóneo en la mayoría de las situaciones.

# Pregunta 13

> ¿Cuál es el objetivo principal en el uso de la técnica RANSAC en el cálculo de una homografía?

RANSAC es un algoritmo que se utiliza en el cálculo de homografías.
Su objetivo principal es **encontrar un conjunto de correspondencias de puntos entre dos imágenes para estimar una homografía de forma robusta** cuando tenemos un conjunto de correspondencias con posibles *outliers*.
En general es aplicable a la estimación de parámetros de forma robusta a partir de un conjunto de datos con posibles *outliers*.

Como entrada recibe un conjunto de correspondencias entre dos imágenes: parejas de puntos $p \to p'$ cada uno de una imagen que previamente hemos detectado como posible coincidencia.

Para conseguir su objetivo toma conjuntos aleatorios de 4 correspondencias (el mínimo para calcular una homografía), calcula una homografía $H$ e intenta maximizar el número de correspondencias que no son outliers, esto es, correspondencias $p \to p'$ tal que la distancia entre $H(p)$ y $p'$ sea menor que un cierto error (fijado normalmente a 3 píxeles de distancia).

Repite este proceso un número de veces que depende de la probabilidad de error que consideremos aceptable y de la proporción inicial de outliers.
De esta forma consigue una homografía con un funcionamiento robusto que descarta correspondencias que no lo son realmente.


# Pregunta 14

> Si tengo 4 imágenes de una escena de manera que se solapan la 1-2, 2-3 y 3-4. ¿Cuál es el número mínimo de parejas de puntos en correspondencias necesarios para montar un mosaico? 

El número mínimo es $12 = 3\cdot 4$ parejas de puntos.

Para calcular una homografía $H$ entre dos imágenes necesitamos un mínimo de 4 parejas de puntos para poder calcular la matriz de la homografía; de esta forma tendríamos un sistema de ecuaciones determinado (añadiendo la condición $\lVert H \rVert = 1$).

Para montar un mosaico nos basta con calcular la homografía que lleva cada imagen a una imagen mosaico y aplicarlas adecuadamente. Sea $M$ una homografía prefijada que lleva la imagen $3$ al mosaico. 

Notamos con $H_{ij}$ la homografía que lleva la imagen $i$ en la imagen $j$.
Calculamos las siguientes homografías: $H_{12}$, $H_{32}, H_{43}$. 
Para cada homografía necesitamos 4 parejas de 4 puntos tales que 3 a 3 no estén alineados, ya que cada punto nos da dos ecuaciones (un total de 8 ecuaciones a las que sumamos una condición de normalización).
No podemos utilizar menos puntos porque tenemos un total de 9 incógnitas en cada homografía. 
Esto nos da un total de 12 puntos.

A partir de estas homografías podemos calcular las homografías al mosaico de cada imagen:

1. para la imagen 1 calculamos $M \cdot H_{12}$,
2. para la imagen 2 calculamos $M$,
3. para la imagen 3 calculamos $M \cdot H_{32}$ y
3. para la imagen 4 calculamos $M \cdot H_{43} \cdot H_{32}$.

De esta forma podemos montar el mosaico, luego 12 puntos son suficientes.
No podemos calcular menos homografías para sacar todas luego este es el mínimo número.


# Pregunta 15

> En la confección de un mosaico con proyección rectangular es esperable que aparezcan deformaciones de la escena real. ¿Cuáles y por qué? 

Podemos esperar deformaciones dadas por el cambio del punto de vista de la cámara: si por algún motivo trasladamos el punto de vista de la cámara la deformación entre ambos puntos no es necesariamente una homografía, ya que podrían verse nuevas partes de los objetos. En este caso los métodos que utilizamos podrían producir deformaciones.

Además pueden darse por errores en la estimación de las homografías por fallos en la detección de los puntos o las correspondencias o porque la imagen no está en un plano. Estos errores pueden ser suficientemente pequeños en una sola homografía para ser imperceptibles, pero la composición de homografías puede dar lugar a la acumulación de errores.

> ¿Bajo qué condiciones esas deformaciones podrían desaparecer?

El tamaño de las deformaciones producidas por el movimiento del punto de vista de la cámara es inversamente proporcional a la distancia a la que están los objetos. De esta forma, si intentamos hacer un mosaico con proyección rectangular las deformaciones podrían desaparecer si el mosaico se compone de imágenes de objetos suficientemente lejanos.

Las deformaciones producidas por errores en homografías pueden reducirse ajustando adecuadamente los parámetros de los detectores. Además podemos reducir la acumulación de error utilizando la composición dada en la [Pregunta 14] en lugar de componer directamente de la primera a la última imagen. Por último para este problema en algunos casos podríamos calcular una homografía circular en la que podemos reducir de forma global el error y después pasar a una proyección rectangular.

# Bibliografía
