---
title: Cuestionario Teoría -1
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
toc: false
colorlinks: true
bibliography: citas.bib
biblio-style: plain
link-citations: true
citation-style: estilo.csl
---
  
# Pregunta 1

> Diga en una sola frase cuál cree que es el objetivo principal de la Visión por Computador

El objetivo principal de la Visión por Computador es el uso de técnicas matemáticas y algorítmicas para el tratamiento de las imágenes y la obtención de información semántica y geométrica de estas.

> Diga también cuál es la principal propiedad de cara a los algoritmos que está presente en todas las imágenes

La propiedad principal de las imágenes es que la información debe obtenerse mirando en un entorno de cada píxel.
La región cercana a un píxel guarda relación con el valor del mismo, lo que es relevante para la obtención de cualquier tipo de información de la imagen.
La existencia de ambigüedad y ruido también hace necesario el uso de esta propiedad.

# Pregunta 2

> Expresar las diferencias y semejanzas entre las operaciones de correlación y convolución.
> Dar una interpretación de cada una de ellas que en el contexto de uso en visión por computador.

Las operaciones de correlación y convolución son transformaciones locales que agregan información local de la imagen en los píxeles cercanos.
Ambas utilizan una *máscara* $M$ representada mediante una matriz cuadrada de orden impar de números reales que define esta agregación.
Sus fórmulas son:
$$M \otimes F = \sum_{u,v} M[u,v]F(i+u, j+v) \qquad M \star F = \sum_{u,v} M[u,v]F(i-u, j-v)$$
donde $\otimes$ representa la correlación y $\star$ la convolución.
Si $M \in \mathcal{M}_{2n+1}(\mathbb{R})$ entonces $M[u,v] = M_{u-n, v-n}$ de tal forma que $M[0,0]$ es el valor central de la matriz.

Las operaciones coinciden cuando $M$ es una matriz simétrica, y, en general, la correlación con $M$ se corresponde con la convolución con otra máscara $M'$ donde $M'$ se corresponde con la máscara $M$ invertida por filas y por columnas. La convolución tiene mejores propiedades algebraicas; en concreto es asociativa, conmutativa, bilineal y tiene elemento neutro (la máscara nula salvo un uno en el centro).

En el contexto de la visión por computador la correlación puede interpretarse como una operación que busca un patrón dentro de la imagen.
El resultado de hacer una correlación de un patrón con una imagen nos da una nueva imagen con valores más altos en los lugares en los que haya coincidencia.
La convolución suele utilizarse en Visión por Computador para aplicar filtros ya que tiene mejores propiedades.


# Pregunta 3

> ¿Los filtros de convolución definen funciones lineales sobre las imágenes? 

Sí. Si tomamos una máscara $M$, dos constantes $\alpha, \beta$ y $F, G$ dos imágenes tenemos que
\begin{align*}
M \star (\alpha F + \beta G) & = \sum_{u,v} M[u,v] (\alpha F+ \beta G)(i-u, j-v)  \\
& = \sum_{u,v} M[u,v] \alpha F(i-u, j-v) + \sum_{u,v} M[u,v] \beta G(i-u, j-v) \\
& = \alpha \sum_{u,v} M[u,v] F(i-u, j-v) + \beta \sum_{u,v} M[u,v]  G(i-u, j-v) \\
& = \alpha (M \star F) + \beta (M \star G)
\end{align*}

> ¿Y los de mediana?

No, la mediana no es una función lineal sobre las imágenes.
Vemos un contraejemplo sobre señales, que podemos extender fácilmente a un contraejemplo sobre las imágenes repitiendo las señales por filas.

Si tomamos $A = [1,2,3,4,5], B = [1,-1,1,-1,1]$ y aplicamos un filtro de mediana de tamaño 3 con bordes a cero tenemos que
$$f(A) + f(B) = [1,2,3,4,4] + [0,1,-1,1,0] = [2,1,4,3,5]$$
pero
$$f(A+B) = f([2,1,4,3,5]) = [1,2,3,4,3]$$
luego $f(A+B) \neq f(A) + f(B)$ en este caso.

\newpage

# Pregunta 4

> Una operación de máscara que tipo de información usa, ¿local o global?

Una operación de máscara $F$ utiliza información local: dada una imagen $f$, el valor de un pixel $F(f)(i,j)$ tras aplicar la operación de máscara sólo depende de los valores de los píxeles en un entorno de $f(i,j)$ en la imagen original.
En concreto depende de los valores de la submatriz de centro $(i,j)$ y dimensiones iguales al tamaño de la máscara.

Esta propiedad restringe el tipo de operaciones que podemos hacer: no podemos tener en cuenta todos los píxeles para hacer por ejemplo algunas aplicaciones afines.
Sin embargo, tienen gran versatilidad ya que operaciones como la traslación, alisado o aproximación de derivadas por diferencias finitas son operaciones locales implementables por una operación de máscara.

# Pregunta 5

> ¿De qué depende que una máscara de convolución pueda ser implementada de forma separable por filas y columnas?

Depende de la descomposición en valores singulares de la máscara.
Dado un filtro representado por una matriz $M$ podemos hallar una descomposición en valores singulares de la forma $$M = ODQ^T \quad \text{ con } O, Q \text{ ortogonales y } D \text{ diagonal}$$
Por simplicidad descartamos el caso de la matriz nula, que no tiene utilidad práctica.

Podemos reescribir la igualdad de la descomposición en valores singulares: si llamamos $O_i, Q_i$ a las columnas i-ésimas de $O$ y $Q$ respectivamente entonces
$$M = \sum_i D_{i,i} O_iQ_i^T$$
Si sólo tenemos un valor singular, esto es, si sólo hay un $j$ tal que $D_{j,j} \neq 0$ entonces podemos expresar $$M = D_{j,j} O_jQ_j^T$$
y podemos separar por tanto por ejemplo en los vectores $D_{j,j}O_j, Q_j$.

Como $O,Q$ son ortogonales tienen rango máximo y por tanto $\operatorname{rango}(M) = \operatorname{rango}(ODQ^T) = \operatorname{rango}(OD) = \operatorname{rango}(D)$.
El rango de $D$ es el número de elementos no nulos en la diagonal, luego vemos que, para $M$ no nula:
$$M \text{ es separable } \quad \iff \quad \operatorname{rango}(M) = 1$$

# Pregunta 6

> Para implementar una función que calcule la imagen gradiente de una
> imagen cabe plantearse dos alternativas:
>
> a) Primero alisar la imagen y después calcular las derivadas sobre la
> imagen alisada
> 
> b) Primero calcular las imágenes derivadas y después alisar dichas
> imágenes.
>
> Discutir y decir cuál de las estrategias es la más adecuada, si alguna lo
> es, tanto en el plano teórico como en el de la implementación.

<!-- En el caso continuo, esto es, si vemos una imagen como una función $F: [0,N] \times [0,M] \to \mathbb{R}$ suficientemente derivable (análogamente para la máscara) y utilizamos la operación de convolución continua entonces ambas alternativas dan el mismo resultado: $$\frac{\partial}{\partial x^n \partial y^m}(H \ast F) = H \ast \left(\frac{\partial}{\partial x^n \partial y^m} F\right)$$ -->

En el plano teórico (esto es, asumiendo que tratamos realmente con números reales y no con las operaciones del ordenador que provocan errores de redondeo e ignorando los posibles efectos en el borde) ambas estrategias dan el mismo resultado ya que la convolución con una máscara es conmutativa; si $D$ es el filtro de derivada respecto de x/y, $G$ el de alisamiento y $F$ la imagen $$D \star (G \star F) = G \star (D \star F)$$


De cara a la implementación es preferible la opción **a)**; es preferible alisar antes de aproximar las derivadas <!-- por las posibles deformaciones que produce el ruido en la imagen y también es preferible --> ya que si hacemos el alisamiento a posteriori tendremos que hacerlo dos veces: una para la derivada en x y otra para la derivada en y.

# Pregunta 7

> Verificar matemáticamente que las primeras derivadas (respecto de x
> e y) de la Gaussiana 2D se puede expresar como núcleos de convolución
> separables por filas y columnas. Interpretar el papel de dichos núcleos
> en el proceso de convolución.

Dada una máscara $F(x,y)$ será separable si existen funciones $G,H$ tales que $F(x,y) = G(x)H(y)$.
En este caso estamos haciendo muestreo de una función $f$ de variable real, luego en particular nos basta expresar $f(x,y) = g(x)h(y)$ para tener la separabilidad del filtro (los vectores máscara 1D serán el muestreo de $g$ y $h$).

La función densidad de la gaussiana 2D con media 0 y varianzas $\sigma_x,\sigma_y$ es
\begin{align*}
f(x,y) & = \frac{1}{2\pi\sigma_x \sigma_y}\exp\left(-\frac12\left(\frac{x^2}{\sigma_x^2} + \frac{y^2}{\sigma_y^2} \right) \right) \\
& = \frac{1}{\sqrt{2\pi}\sigma_x}\exp\left(-\frac{x^2}{2\sigma_x^2}\right) \frac{1}{\sqrt{2\pi}\sigma_y}\exp\left(-\frac{y^2}{2\sigma_y^2}\right) \\
& = g(x; \sigma_x)g(y; \sigma_y)
\end{align*}
donde $g(\cdot; \sigma)$ es la función de densidad de la gaussiana 1D con media 0 y varianza $\sigma$
$$g(x;\sigma) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{x^2}{2\sigma^2}\right)$$

Si derivamos la función de densidad de la gaussiana 1D utilizando la regla de la cadena
\begin{align*}
g'(x; \sigma) & = \frac{1}{\sqrt{2\pi}\sigma} \frac{\mathrm{d}}{\mathrm{d}x}\left(\exp\left(-\frac{x^2}{2\sigma^2}\right)\right) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{x^2}{2\sigma^2}\right) \frac{-2x}{2\sigma^2} \\
& = \frac{-x}{\sigma^2} \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{x^2}{2\sigma^2}\right) = \frac{-x}{\sigma^2} g(x;\sigma)
\end{align*}

Si derivamos la gaussiana 2D usando esta expresión tenemos que
$$\frac{\partial f}{\partial x}(x,y) =  g'(x; \sigma_x)g(y; \sigma_y) = \left(\frac{-x}{\sigma_x^2} g(x;\sigma_x)\right)g(y;\sigma_y)$$
y análogamente para $y$ 
$$\frac{\partial f}{\partial y}(x,y) = g(x; \sigma_x)g'(y; \sigma_y) = g(x;\sigma_x)\left(\frac{-y}{\sigma_y^2} g(y;\sigma_y)\right)$$
por tanto ambas derivadas pueden expresarse de forma separable.

Los núcleos de convolución por filas y columnas son los mismos salvo orden en el caso de la derivada respecto de x o y (esto es, el núcleo por filas de un caso es el de columnas en el otro).
Uno de los núcleos muestrea la función de densidad gaussiana 1D $g(x;\sigma)$ y realiza por tanto un filtro gaussiano en esa dirección.
El otro filtro se corresponde con la función de densidad de la gaussiana 1D derivada $g'(x;\sigma) = \frac{-x}{\sigma^2}g(x;\sigma^2)$ y por tanto combina un alisado gaussiano con una derivada en esa dirección: nos dará una aproximación de la derivada en esa dirección combinada con un alisado.

\newpage

# Pregunta 8

> Verificar matemáticamente que la Laplaciana de la Gaussiana se puede
> implementar a partir de núcleos de convolución separables por filas y
> columnas. Interpretar el papel de dichos núcleos en el proceso de
> convolución.

Siguiendo la notación de la pregunta anterior y usando $g'(x;\sigma) = \frac{-x}{\sigma^2}g(x;\sigma^2)$

\begin{align*}g''(x; \sigma_x) & = \frac{\mathrm{d}}{\mathrm{d}x}\left(\frac{-x}{\sigma^2} g(x;\sigma)\right) =  \frac{-1}{\sigma^2}g(x;\sigma) + \frac{-x}{\sigma^2} g'(x;\sigma) \\
& = \frac{-1}{\sigma^2}g(x;\sigma) + \left(\frac{-x}{\sigma^2}\right)^2 g(x;\sigma)  = \left(\frac{-1}{\sigma^2} + \frac{x^2}{\sigma^4}\right) g(x;\sigma) = \frac{x^2 - \sigma_x^2}{\sigma_x^4}g(x;\sigma_x) \\
& = \frac{x^2 - \sigma_x^2}{\sigma_x^4}\left(\frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{x^2}{2\sigma^2}\right)\right)
\end{align*}

Debemos en esta ocasión calcular la suma de las segundas derivadas respecto de $x$ e $y$
$$\Delta(f) = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} = g''(x;\sigma_x)g(y;\sigma_y) + g(x;\sigma_x)g''(y;\sigma_y) = \left(\frac{x^2 -\sigma_x^2}{\sigma_x^4} + \frac{y^2 -\sigma_y^2}{\sigma_y^4}\right)f(x,y)$$
Podemos comprobar que esta función **no** es separable; si tomamos $\sigma_x = \sigma_y = 1$ y construimos un filtro $3 \times 3$ muestreando obtenemos un filtro que no es separable de acuerdo a la caracterización dada en la pregunta 5

$$M = \left(\begin{matrix}
0 & -0,096 & 0 \\
-0,096 & -0,318 & -0,096 \\
0 & -0,096 & 0
\end{matrix}\right), \qquad \operatorname{rango}(M) = 2$$

Sin embargo **sí** podemos implementar la laplaciana de la gaussiana a partir de filtros separables: calculamos por separado las segundas derivadas parciales en cada variable y sumamos las imágenes resultantes.
Si la imagen es $m \times m$ y el filtro $n \times n$ el cálculo mediante dos filtros separables nos proporciona un algoritmo con eficiencia asintótica $O(nm^2)$ igual a si el filtro fuera separable (aunque la constante es mayor).

Los núcleos por filas y columnas de cada filtro son de nuevo los mismos salvo orden por ser la gaussiana simétrica respecto de x e y. Uno de los filtros será un filtro de alisado gaussiano muestreando $g(x;\sigma^2)$ mientras que el otro realiza la segunda derivada en la dirección correspondiente mediante el muestreo de la función $g''(x;\sigma^2) = \frac{x^2 - \sigma^2}{\sigma^4}g(x;\sigma)$.

\newpage

# Pregunta 9

> ¿Cuáles son las operaciones básicas en la reducción del tamaño de una
> imagen? Justificar el papel de cada una de ellas.

Para la reducción del tamaño de una imagen se realizan dos operaciones:

Alisado gaussiano
: Elimina las frecuencias altas en la imagen mediante un alisado gaussiano convolucionando con un kernel gaussiano

Submuestreo
: Elimina una de cada dos filas y columnas para obtener una imagen de la mitad de tamaño

El submuestreo nos permite obtener una imagen de menores dimensiones pero utilizado sin un alisado gaussiano previo puede dar lugar a efectos de *aliasing* en los que la frecuencia de muestreo no es suficiente para representar la imagen y se generan patrones que no estaban presentes en la imagen original.

El alisado gaussiano elimina las frecuencias que son demasiado altas para la frecuencia de muestreo que tendremos en la imagen reducida, posibilitando así la reducción del tamaño de la imagen sin la generación de artefactos

# Pregunta 10

> ¿Qué información de la imagen original se conserva cuando vamos
> subiendo niveles en una pirámide Gaussiana?

La pirámide gaussiana de una imagen se forma al aplicar la operación de reducción de la imagen descrita en la pregunta anterior repetidas veces.
El primer nivel de la pirámide es la imagen original; a continuación cada nivel de la pirámide se forma aplicando
el filtro de reducción de la imagen al nivel de la pirámide anterior.

Esta operación usa un alisado gaussiano, que actúa como un filtro que elimina o reduce las frecuencias altas.
Es decir, conforme vamos subiendo niveles la información que se conserva de la imagen original son las frecuencias más bajas.


# Pregunta 11

> ¿Qué información podemos extraer de la pirámide Gaussiana y la
> pirámide Laplaciana de una imagen? ¿Qué nos aporta cada una de ellas?

La pirámide gaussiana crea diferentes representaciones a distintos tamaños de la imagen, en la que nos quedamos cada vez con frecuencias más bajas. Nos permite ver las características de la imagen que corresponden con un mayor o menor grado de detalle, permitiéndonos así centrarnos en el grado de detalle adecuado para reconocer características como texturas o la disposición general de la imagen.

La pirámide laplaciana nos muestra, por definición, las diferencias entre los distintos niveles de la pirámide gaussiana. Estas diferencias nos permiten extraer las distintas frecuencias de la imagen y separarlas en distintos niveles; de esta manera podemos observar de forma separada las frecuencias altas y las frecuencias bajas.
El primer nivel de la pirámide laplaciana se corresponde aproximadamente con extraer las frecuencias altas de la imagen que corresponden con los bordes.
Adicionalmente (ver pregunta 12) la pirámide laplaciana nos aporta toda la información de la imagen original ya que nos permite reconstruirla.


# Pregunta 12

> ¿Podemos garantizar una perfecta reconstrucción de una imagen a
> partir de su pirámide Laplaciana? Dar argumentos y discutir las opciones
> que considere necesario.

De forma teórica **sí** podemos. 
Dada la pirámide laplaciana de una imagen para reconstruir la imagen original aplicamos el algoritmo inverso al de la construcción de la pirámide.
Sea $[G_1, \dots, G_n]$ la pirámide gaussiana que hemos utilizado para construir la laplaciana, $[L_1, \dots, L_n]$ la laplaciana (con $L_n = G_n$ el nivel más pequeño) y $F$ la función que expande la imagen de un nivel superior al tamaño del nivel anterior.

Sabemos que, por definición de pirámide laplaciana $L_k := G_k - F(G_{k+1})$, luego despejando podemos reconstruir su pirámide gaussiana $$G_n = L_n, \qquad G_k = L_k + F(G_{k+1})$$

Finalmente $G_1$ será el primer nivel de la pirámide gaussiana que coincide con la imagen original.
No obstante, en el caso práctico podrían apreciarse errores debido a la precisión limitada de las operaciones de cálculo para flotantes.

# Pregunta 13

> En OpenCV solo se pueden calcular máscaras Sobel de hasta dimensión
> 7x7 ¿Por qué? De una explicación razonable a este hecho y diga cómo
> influye en el cálculo con máscaras de mayor tamaño.

Aunque la documentación especifica lo contrario, en OpenCV sí podemos calcular máscaras de Sobel de dimensión mayor que $7\times 7$ (en concreto podemos llegar a obtener máscaras con tamaños de hasta $31\times 31$). Por ejemplo podemos hacerlo con la función `getDerivkernels` que utilizamos en la práctica inicial.

Sin embargo, el uso de máscaras de Sobel de mayor dimensión no supone una mejora en resultados notable respecto a los resultados obtenidos por una máscara $7\times 7$; como la derivada es una operación local añadir nuevos puntos a mayor distancia no tiene por qué producir un mejor resultado. Estos nuevos puntos además disminuyen el peso de los puntos cercanos (que son los más relevantes para la aproximación de la derivada) y los más lejanos quedan con un valor muy pequeño; si normalizamos el kernel de tamaño 9x9 lo valores en los extremos llegan a ser del orden de $10^{-5}$.

# Pregunta 14

> Cuales son las contribuciones más relevantes del algoritmo de Canny
> al cálculo de los contornos sobre una imagen?. ¿Existe alguna conexión
> entre las máscaras de Sobel y el algoritmo de Canny?

El algoritmo de Canny intenta cumplir con 3 criterios de acuerdo al paper original [@canny1986computational]:

1. buena detección: baja cantidad de falsos positivos y falsos negativos respecto a la detección de contornos,
2. buena localización: localización de los contornos en los puntos más cercanos al centro del contorno real y
3. cada contorno debe dar una única respuesta

Sus contribuciones más relevantes son que consigue cumplir con estos criterios de forma razonable utilizando un algoritmo que no depende de técnicas de aprendizaje automático. Para ello:

1. aplica un filtro gaussiano para alisar la imagen, 
2. halla el gradiente de la imagen (su magnitud y dirección en cada punto),
3. elimina los puntos de los contornos obtenidos en el gradiente de la imagen que, en la dirección del gradiente, no sean máximos locales,
4. define dos umbrales alto y bajo y reconstruye los contornos empezando en los puntos con valor mayor al umbral alto y continuando si tienen un valor superior al umbral bajo.

Existe una conexión entre las máscaras de Sobel y el algoritmo de Canny: en el segundo paso, para la obtención del gradiente, podemos obtener el gradiente con las máscaras de Sobel aproximando las derivadas parciales respecto de x e y con las mismas.
OpenCV en su implementación del algoritmo de Canny utiliza por defecto la máscara de Sobel para obtener el gradiente.


# Pregunta 15

> Suponga que le piden implementar un algoritmo para el cálculo de la
> derivada de primer y segundo orden sobre una imagen usando un filtro
> gaussiano cualesquiera. Enumere y explique los pasos necesarios para
> llevarlo a cabo.

Podemos especificar un filtro gaussiano de dos formas diferentes: podemos dar los parámetros que determinan el filtro (esto es, $\sigma_X, \sigma_Y$) o dar el filtro como matriz directamente (en vector de filas y columnas o como matriz). Discuto ambos casos.

En el caso de tener el filtro a partir de los parámetros podemos utilizar las expresiones obtenidas en la [Pregunta 7] y la [Pregunta 8] y muestrearlas en puntos equiespaciados para obtener un filtro separable que calcula la derivada de primer y segundo orden sobre una imagen respectivamente. Es decir, los pasos serían

1. calcular el tamaño de los filtros de derivada en función de $\sigma_x,\sigma_y$ de tal manera que un ~95% de la densidad de la función gaussiana (o de la derivada en valor absoluto) quede dentro. Para esto podemos tomar un tamaño de $1 + 6 \lceil \sigma \rceil$ ya que a distancia 3$\sigma$ tenemos aproximadamente un 99.7% de la masa de la función de densidad.
1. Calcular los filtros de derivada a partir de la expresión de la primera (segunda) derivada de la función de densidad de la gaussiana (son separables así que obtendremos dos vectores, para filas y columnas). Para ello muestreamos la función en tantos puntos como el tamaño calculado en el paso anterior, haciéndolo de tal manera que el valor central muestree en 0.
2. Normalizar el filtro multiplicando por $\sigma$ en el caso de la primera derivada y por $\sigma^2$ en el caso de la segunda derivada.
2. Aplicar estos filtros por filas y columnas con una convolución con la imagen.

En el caso de tener directamente el filtro como matriz (o como vectores) tendríamos que calcular un nuevo filtro a partir de este para hacer la derivada. Para ello podemos utilizar una máscara Sobel o cualquier otra máscara de derivada para obtener la nueva máscara de derivación. Los pasos serían:

1. convolucionar los filtros de derivada y los filtros gaussianos,
2. Normalizar el filtro multiplicando por $\sigma$ en el caso de la primera derivada y por $\sigma^2$ en el caso de la segunda derivada.
2. aplicar los filtros resultantes por filas y columnas con una convolución con la imagen


\newpage

# Bibliografía
