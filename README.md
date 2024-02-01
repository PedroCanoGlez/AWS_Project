## Proyecto AWS Lambda Workflow

Este proyecto en AWS proporciona un flujo de trabajo eficiente para el análisis y mejora de código, utilizando tres funciones Lambda almacenadas en el bucket 'lambda-bucket'. A continuación, se detalla el flujo de trabajo:

![thumbnail_image](https://github.com/PedroCanoGlez/AWS_Project/assets/90764191/179b557f-4532-4a1d-9b65-0ecdc0cc9662)

## Estructura del Proyecto
Codigo Entreno --> Archivos para entrenar modelo predictivo.
Initializer.py --> Este código inicializa todo nuestro entorno AWS en localstack.
lambda1, lambda2 y lambda3 --> lambdas llamadas bucket-viewer, code-metrics y word-suggester para realizar las acciones que ahora detallaremos.
language_model.keras --> modelo entrenado para predicción de palabras.
main.py --> Graphical User Interface(GUI) sencilla, para que sea más fácil y más simple la ejecución de las lambdas, así como la búsqueda de archivos y la introducción de texto.
model.py --> Archivo que entrena y genera el modelo predictivo.
prueba_modelo.py --> Pequeño código que prueba la precisión del modelo entrenado.
