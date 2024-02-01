## Proyecto AWS Lambda Workflow

Este proyecto en AWS proporciona un flujo de trabajo eficiente para el análisis y mejora de código, utilizando tres funciones Lambda almacenadas en el bucket 'lambda-bucket'. A continuación, se detalla el flujo de trabajo:

![thumbnail_image](https://github.com/PedroCanoGlez/AWS_Project/assets/90764191/179b557f-4532-4a1d-9b65-0ecdc0cc9662)

## Estructura del Proyecto  
Codigo Entreno --> Archivos para entrenar modelo predictivo.  
Initializer.py --> Este código inicializa todo nuestro entorno AWS en localstack.  
lambda1, lambda2 y lambda3 --> Lambdas llamadas bucket-viewer, code-metrics y word-suggester para realizar las acciones que ahora detallaremos.  
language_model.keras --> Modelo entrenado para predicción de palabras.  
main.py --> Graphical User Interface(GUI) sencilla, para que sea más fácil y más simple la ejecución de las lambdas, así como la búsqueda de archivos y la introducción de texto.  
model.py --> Archivo que entrena y genera el modelo predictivo.  
prueba_modelo.py --> Pequeño código que prueba la precisión del modelo entrenado.


## Pasos del Flujo de Trabajo  

1- Importación del Código al Datalake  
El usuario introduce su código en el **datalake**, que sirve como el repositorio central para el almacenamiento de códigos.  
  
2- Visualización del Contenido del Bucket  
El usuario lanza la primera lambda (**bucket_viewer**) para obtener una vista previa del contenido del bucket **datalake**. Esta función Lambda proporciona una manera rápida y eficiente de explorar los archivos y estructuras dentro del bucket.  

3- Métricas Generales del Código  
Para obtener métricas generales sobre un código específico en **datalake**, el usuario lanza la segunda lambda(**code_metrics**). Esta función Lambda realiza análisis y proporciona información valiosa sobre el código.  
  
4- Sugerencias de Palabras  
El usuario pasa una oración y lanza la tercera lambda(**word_suggester**) para obtener sugerencias de palabras adicionales. Esta función Lambda utiliza algoritmos de procesamiento de lenguaje natural para sugerir palabras que podrían seguir en la oración dada


## Configuración del Proyecto  
Asegúrese de tener configurado LocalStack con las credenciales adecuadas.  
- Si no lo tienes puedes obtener más información en https://www.localstack.cloud/  
- Asegúrese de que su instancia de LocalStack apunta al puerto 4566  
- Ejecute main.py para inicializr su entorno de LocalStack  
  
## Conclusión  
Este proyecto proporciona una solución completa para el análisis de código y sugerencias de palabras, permitiendo a los usuarios mejorar la calidad y eficiencia de su código de manera efectiva.
