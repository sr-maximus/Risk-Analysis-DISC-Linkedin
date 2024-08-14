# Analysis-DISC

## Objetivo:
El proyecto tiene como objetivo la extracción, análisis y visualización de datos de perfiles de LinkedIn. Utiliza una arquitectura distribuida para manejar solicitudes a la API de LinkedIn de manera eficiente y segura. El sistema proporciona análisis del riesgo de exposición en Internet basado en la sensibilidad de los datos compartidos en los perfiles, así como un análisis DISC de los perfiles.

## Componentes Principales:

### Extracción de Datos:

Celery: Utiliza Celery, una biblioteca de tareas distribuidas en Python, para gestionar la extracción de datos de perfiles de LinkedIn de manera asíncrona y eficiente.
API de LinkedIn: Conecta con la API de LinkedIn para obtener datos de perfiles utilizando tokens de API que se rotan para manejar las limitaciones de tasa.
Caché: Implementa un sistema de caché (utilizando cachetools) para almacenar temporalmente los datos de los perfiles y reducir la cantidad de solicitudes a la API.

### Análisis de Datos:

Riesgo de Exposición: Calcula el riesgo de exposición en Internet para cada perfil basándose en la sensibilidad de la información disponible, como la experiencia profesional, el número de contactos, y la presencia de información de contacto.
Análisis DISC: Evalúa los perfiles según el modelo DISC (Dominancia, Influencia, Estabilidad, Conformidad) utilizando la información del perfil (título profesional y conexiones).

### Visualización:

Mapa de Calor: Genera un mapa de calor que muestra la correlación entre diferentes factores de riesgo de exposición.
Red de Interacciones: Crea una visualización de red utilizando Plotly para mostrar las interacciones entre los perfiles, representando cada perfil como un nodo y las conexiones como bordes.
Gráficos DISC: Produce gráficos de pastel para cada perfil, visualizando la puntuación DISC en diferentes categorías.

### Monitoreo y Escalado:

Flower: Utiliza Flower para monitorear el estado de los trabajadores de Celery, permitiendo observar el progreso de las tareas y el rendimiento del sistema en tiempo real.
Escalado Horizontal: La arquitectura está diseñada para permitir el escalado horizontal distribuyendo los trabajadores de Celery en múltiples máquinas si es necesario.

### Estructura del Código:

celery.py: Configura la aplicación Celery con el broker y el backend de Redis, y define la tasa de solicitudes para las tareas.
tasks.py: Define las tareas de Celery para extraer datos de LinkedIn, con manejo de errores y caché para optimizar el rendimiento.
main.py: Coordina la ejecución de tareas, realiza el análisis de datos, y genera las visualizaciones correspondientes.
requirements.txt: Lista las dependencias necesarias para el proyecto.

## Instrucciones para Ejecutar:

Instalar las dependencias.
Iniciar Redis.
Iniciar los trabajadores de Celery.
(Opcional) Iniciar Flower para monitoreo.
Ejecutar el script principal main.py.

### Consideraciones de Seguridad:
Asegurarse de que los tokens de API estén protegidos y que el manejo de errores sea robusto para evitar la exposición de información sensible.

# Instrucciones para Ejecutar Paso a Paso
### Instalar Dependencias:
Asegúrate de tener un entorno virtual activo y ejecuta:
pip install -r requirements.txt

### Iniciar Redis:
Asegúrate de que el servidor Redis esté en funcionamiento.

### Iniciar los Trabajadores de Celery:
Ejecuta en una terminal:
celery -A celery worker --loglevel=info

### Iniciar Flower (opcional para monitoreo):
En una terminal separada:
celery -A celery flower

Accede a Flower en http://localhost:5555.

### Ejecutar el Script Principal:
Ejecuta main.py para iniciar el procesamiento y la visualización de datos.
