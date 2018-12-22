---
title: Cuestionario Teoría 3
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
---

# Pregunta 1

>  ¿Cuáles son las propiedades esenciales que permiten que los
> modelos de recuperación de instancias de objetos de una gran
> base de datos a partir de descriptores sean útiles?

Los modelos de recuperación de instancias de objetos de una gran base de datos hacen uso de algún tipo de resumen de la imagen a partir de descriptores asociados a puntos de interés la imagen.

La propiedad esencial para el buen funcionamiento de estas técnicas es que los descriptores son regiones afines locales que son *invariantes a cambios suficientemente pequeños de la geometría, punto de vista, iluminación*, lo que hace que sean un buen resumen de un objeto rígido.

Esto hace que su uso para reconocimiento de objetos sea muy útil, ya que si un mismo objeto aparece en dos imágenes es muy probable que esta regiones aparezcan en ambas imágenes. Es por esto que el uso de estas técnicas es útil en el caso de la recuperación de instancias de objetos y no normalmente en el caso más complejo de reconocimiento de categorías en el que no podemos asegurar la existencia de estas regiones que aparezcan en varias imágenes.

# Pregunta 2

> ¿Justifique el uso del modelo de bolsa de palabras en el
> proceso de detección y reconocimiento de instancias de
> objetos? ¿Qué ganamos?, ¿Qué perdemos?

El modelo de bolsa de palabras resume el contenido de una imagen a partir de los descriptores de puntos de interés, que se clasifican en *palabras visuales* a partir de un algoritmo de clustering. Sus principales ventajas son:

- su flexibilidad a los cambios de punto de vista, geometría o ciertas deformaciones debido a que tenemos la localización, escala y orientación de cada descriptor,
- su capacidad para resumir de forma vectorial el contenido de la imagen de forma compacta (mediante la bolsa de palabras: un histograma de las palabras visuales presentes en la imagen) y
- sus buenos resultados en la práctica

Entre lo que perdemos están las siguientes características:

- Si los puntos de interés no se localizan exclusivamente dentro de la zona del objeto perdemos la capacidad de distinguir el fondo de los objetos,
- La creación del vocabulario (el conjunto de palabras visuales) no tiene un método claro, por ejemplo no sabemos cuál es el tamaño de vocabulario óptimo o cuál es el algoritmo de clustering más adecuado y
- se ignora la geometría de la imagen, esto es, la localización relativa de los distintos puntos de interés no queda codificada dentro del modelo de bolsa de palabras y por tanto debe verificarse a posteriori con técnicas como RANSAC o la transformada de Hough.

# Pregunta 3

> Describa la diferencia esencial entre los problemas de
> reconocimiento de instancias y reconocimiento de categorías
> ¿Qué deformaciones se presentan en uno y otro?

El reconocimiento de instancias consiste en reconocer la localización en una imagen un objeto rígido desde algún punto de vista y posiblemente con alguna parte oculta. Por ejemplo, es el caso del problema de reconocer una lata de Coca-Cola en una imagen. Las deformaciones que se presentan son cambios en la geometría, el punto de vista, la iluminación o las partes del objeto que son visibles.

En cambio, el reconocimiento de categorías intenta reconocer clases generales como categoría funcionales o ad-hoc o clases de animales. Un ejemplo sería el reconocimiento de sillas o perros, un problema mucho más complejo ya que estas clases no tienen una definición clara y no están formadas por objetos rígidos, luego las deformaciones que se presentan son mucho más generales.

La diferencia esencial se halla en la ambigüedad de la definición en el caso de las categorías, lo que lo hacen un problema mucho más complejo en el que las técnicas aplicadas para el reconocimiento de objetos tienen un rendimiento mucho peor.

# Pregunta 4

> ¿Es posible usar el modelo de bolsa de palabras para el reconocimiento de categorías de objetos?

En general **no** es recomendable el uso del modelo de bolsa de palabras para el reconocimiento de categorías ya que no podemos obtener un conjunto de palabras visuales representativo con facilidad.

El modelo de bolsas de palabras es una técnica basada en la obtención de descriptores de puntos de interés de las imágenes, clasificarlos en palabras visuales y asociar a cada imagen un histograma (*bolsa de palabras*) que resume las palabras visuales contenidas en la imagen.

En el caso de reconocimiento de instancias esta técnica da buenos resultados ya que los objetos son rígidos y tendrán descriptores similares en distintas imágenes. 

En el caso del reconocimiento de categorías, como se comenta en la respuesta a la [Pregunta 3] las deformaciones que se presentan entre las distintas imágenes son mucho mayores, ya que desconocemos qué propiedades comunes tienen los objetos cada categoría. 
Por esta razón que los descriptores **no tienen suficiente uniformidad** como para conseguir un conjunto representativo de palabras visuales que nos permitan utilizar este modelo con facilidad.


# Pregunta 5

> Suponga que desea detectar, en una imagen, una instancia de un objeto a partir de una foto del mismo tomada desde el mismo punto de vista del que aparece en la imagen y en un entorno de iluminación similar. Analice la situación en el contexto de las técnicas de reconocimiento de objetos e identifique que algoritmo concreto aplicaría que fuese útil para cualquier objeto. Argumente porqué funcionaría y especifique los detalles necesarios que permitan entender su funcionamiento.

Este es un problema de reconocimiento de instancias. 
Es una situación muy restrictiva en la que no hay cambios importantes en la geometría o la iluminación, lo que simplifica enormemente el problema. Si está tomado desde el mismo punto de vista el objeto se verá de forma similar salvo escala y si la iluminación es similar también lo serán los píxeles concretos.

En este caso podríamos utilizar simplemente la técnica de ventana deslizante, esto es, calcular la correlación en para cada píxel de la imagen en la que queremos buscar la instancia del objeto con la foto del mismo que tenemos como base en diferentes escalas. Esto nos daría una nueva imagen en la que cada píxel tendría asociada una magnitud. Si tomamos el punto donde se alcance la máxima correlación tendremos con alta probabilidad, si se cumplen las condiciones del enunciado, el lugar donde se encuentra el objeto.

Este algoritmo sería útil para cualquier objeto que consideremos ya que la técnica de ventana deslizante no depende del objeto que tengamos en la imagen. La desventaja principal del algoritmo es su tiempo de ejecución, que puede ser prohibitivo si tenemos que probar en muchas escalas.


# Pregunta 6

> Suponga de nuevo el problema del ejercicio anterior pero la foto que le dan está tomada con un  punto de vista  del objeto distinto respecto del objeto en la imagen. Analice que repercusiones introduce esta modificación en su solución anterior y que cambios debería de hacer para volver a tener un nuevo algoritmo exitoso. Justificar la respuesta.

Continua siendo un problema de instancia de objetos, pero en este caso, dado que no tenemos las restricciones del apartado anterior, no podemos aplicar una técnica tan simple y necesitamos utilizar técnicas más complejas.

En este caso podemos extraer puntos de interés e intentar alinearlas con el objeto.
Haciendo uso de SIFT u otro descriptor podemos encontrar puntos de interés en las imágenes modelo y la imagen en la que queremos encontrar el objeto (a partir de aquí imagen objetivo) e intentar buscar correspondencias entre las imágenes haciendo uso de alguno de los algoritmos que vimos en el cuestionario 2.

Por último, podremos verificar que estas correspondencias se deben realmente a que el objeto está en esa posición mediante el uso de técnicas de verificación geométrica mediante el alineamiento de la imagen modelo y la imagen objetivo.

Para esta última parte podemos utilizar (entre otras técnicas como RANSAC) la transformada de Hough para verificar que los descriptores hallados tienen la orientación y disposición adecuada.
Tras calcular la alineación del objeto podemos encontrar una ventana en la que se localice el objeto.


# Pregunta 7

>  Suponga que una empresa de Granada le pide implementar un modelo de recuperación de información de edificios históricos de la ciudad a partir de fotos de los mismos. Explique de forma breve y clara que enfoque le daría al problema. Que solución les propondría. Y como puede garantizar que la solución podrá ser usada de forma eficiente a través de dispositivos móviles.

El reconocimiento en imágenes de los edificios históricos se encuadraría dentro del contexto de reconocimiento de instancias: los objetos son rígidos, y las imágenes cambiarían el punto de vista, oclusión o geometría.

Una posible solución sería el uso de redes neuronales convolucionales: podemos obtener imágenes clasificadas de Internet (por ejemplo de redes sociales o lugares como Flickr) para crear un conjunto de datos representativo de los edificios históricos y entrenar una red neuronal convolucional con estos datos que nos permita reconocer a qué edificio se corresponde cada imagen.

Esta solución tendría un coste computacional inicial elevado pero en el dispositivo final podría ser usado de forma eficiente una vez construido el clasificador. Es una solución preferible a otros métodos más tradicionales como el uso del modelo de bolsas de palabras ya que estos tienen un coste computacional más elevado en el dispositivo final debido a que no hay verificación de la geometría de la imagen, lo que dificultaría el uso eficiente en dispositivos móviles.


# Pregunta 8

>  Suponga que desea detectar la presencia/ausencia de señales de tráfico en imágenes tomadas desde una cámara situada en la parte frontal de un coche que viaja por una carretera. Diga que aproximación usaría y porqué. Identifique las principales dificultades y diga como las resolvería.

El reconocimiento de señales sería una categorización de instancias porque son objetos rígidos que estarían sujetos a deformaciones geométricas o de punto de vista.
Su simbología está estandarizada y consta de alto contraste entre las distintas partes de la figura.

Por tanto, creo que el modelo de bolsa de palabras seguido de una posterior verificación geométrica sería adecuado para resolver este problema. Inicialmente necesitaremos una base de datos de imágenes de señales con la que crear el vocabulario, cuyo número de palabras podría ser reducido ya que las señales tienen una simbología común.
Debemos eliminar palabras visuales que se correspondan a elementos habitualmente presentes en una carretera que no sean señales y no nos sean útiles. Además, puede ser útil utilizar un ponderado *tf-idf* debido a esta simbología común entre imágenes.

Posteriormente, en el momento del reconocimiento tendríamos que hacer verificación espacial.
Para ello creo que es adecuado el uso de la transformada de Hough generalizada ya que nos permitiría alinear la imagen tomada por la cámara del coche con el modelo.
Para acelerar el proceso de reconocimiento podemos usar un índice invertido que descarte aquellas imágenes que no tengan palabras visuales en común.

Una última dificultad a tener en cuenta es el hecho de que puede haber imágenes tomadas por la cámara con más de una señal, pero este modelo nos permite realizar esta detección sin problemas.

# Pregunta 9

> ¿Qué han aportado los modelos CNN respecto de los modelos de reconocimiento de objetos empleados hasta 2012? Enumerar las propiedades comunes entre ellos y aquellas claramente distintas que hayan permitido una mejora en la solución del problema por parte de las CNN. Dar una opinión razonada de por qué significan realmente una mejora.

Los modelos existentes antes de las redes neuronales convolucionales para el reconocimiento de objetos podían clasificarse en métodos con enfoque discriminativo o generativo.

Los métodos con enfoque discriminativo definen un cierto descriptor basado en un histograma de características de tipo local e intentan clasificar los objetos con técnicas de aprendizaje automático como SVM o Adaboot [TODO], mientras que los métodos de tipo generativo se basan en definir una distribución de probabilidad sobre un cierto modelo de los objetos y utilizar un estimador a partir de esta distribución.

Estos modelos son demasiado específicos para ser capaces de aprender toda la variabilidad de las imágenes: el modelo discriminativo fija el descriptor, mientras que el generativo fija el modelo probabilístico. 

La arquitectura de los modelos CNN es similar al de ambos enfoques desde un punto de vista abstracto: se basan en la extracción de características de bajo nivel y la construcción a partir de estas de modelos de más alto nivel que son posteriormente clasificados. Su diferencia clave es que las redes convolucionales no fijan los descriptores o el modelo probabilístico, lo que les da más generalidad. 

Esta mayor generalidad supone que las redes neuronales sean capaces de detectar nuevas características locales de mayor complejidad que son difíciles de definir manualmente.
Esto supone una mejora real en la precisión del reconocimiento a cambio de un mayor coste computacional, ya que la especifidad de los modelos anteriores limitaba la capacidad de estos para manejar estas características complejas.


# Pregunta 10

>  Razone y argumente a favor y en contra de usar modelos de redes CNN ya entrenados, y que se conocen han sido efectivos en otras tareas distintas de la que tiene que resolver, como modelos para aplicar directamente o como modelos a refinar para la tarea que tiene entre manos. Dar argumentos que no sean genéricos o triviales y que fundamenten su postura.

Entre las razones a favor podemos destacar que:

1. Son la familia de técnicas que tiene mejor rendimiento en la práctica, superando en rendimiento a cualquier otra técnica conocida,
2. dado un modelo de red CNN ya entrenado para una tarea similar podemos refinarlo de forma sencilla si tenemos un conjunto de datos clasificado y los recursos computacionales adecuados y
3. la estructura interna que crea la red neuronal es jerárquica, yendo de características más sencillas a más complejas, lo que nos permite tener cierto conocimiento de su estructura.

Sus desventajas principales son:

1. Su estructura interna es comparativamente más compleja a la de otros modelos lo que hace que, aunque podamos conocer parte de su estructura, nuestra capacidad de hacer modificaciones de la misma se ve mucho más limitada,
2. La cantidad de recursos computacionales que necesitamos para entrenarla es bastante elevada, así como los datos necesarios para entrenarla, que deben haber sido previamente clasificados manualmente. Esto limita su aplicabilidad en situaciones complejas.


# Bibliografía

- Diapositivas de clase
- Szeliski, R. (2010). *Computer vision: algorithms and applications*. Springer Science & Business Media.
