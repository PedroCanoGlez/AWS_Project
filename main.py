import PySimpleGUI as sg
import os
import boto3
from initializer import initialize_localstack
import json
from first_lambda import first_lambda

localstack_endpoint = "http://localhost:4566"
aws_region = "us-east-1"

def crear_ventana(titulo, layout, icon_path=None, size=(450, 150)):
    return sg.Window(titulo, layout, icon=icon_path, size=size)

def mensaje_error(mensaje):
    sg.popup_error(mensaje)

def main():
    
    
    initialize_localstack()
    
    sg.theme("Default1")

    # Establecer la ruta del archivo de icono (.ico)
    icon_path = "aws_logo_smile_1200x630.ico"

    while True:
        layout_inicio = [
            [sg.Text("Seleccione una opción:")],
            [sg.Button("Subir archivo", key="opcion1"),
             sg.Button("Ver métricas de código", key="opcion2"),
             sg.Button("Sugerir palabras", key="opcion3")]
        ]

        window_inicio = crear_ventana("AWS Service", layout_inicio, icon_path)

        event_inicio, _ = window_inicio.read()

        if event_inicio == sg.WIN_CLOSED:
            break

        window_inicio.close()

        if event_inicio in ("opcion1"):
            archivo_ruta = pedir_ruta_archivo(icon_path)
            if archivo_ruta:
                ejecutar_opcion(event_inicio, archivo_ruta)
        elif event_inicio == "opcion2" or event_inicio == "opcion3":
            ejecutar_opcion(event_inicio, None)

def pedir_ruta_archivo(icon_path):
    layout_archivo = [
        [sg.Text("Seleccione un archivo:")],
        [sg.InputText(key="archivo_ruta", enable_events=True), sg.FileBrowse()],
        [sg.Button("Aceptar"), sg.Button("Cancelar")]
    ]

    window_archivo = crear_ventana("Seleccione un archivo", layout_archivo, icon_path)

    while True:
        event_archivo, values_archivo = window_archivo.read()

        if event_archivo == sg.WIN_CLOSED or event_archivo == "Cancelar":
            window_archivo.close()
            return None

        archivo_ruta = values_archivo["archivo_ruta"]

        if os.path.isfile(archivo_ruta):
            window_archivo.close()
            return archivo_ruta

    window_archivo.close()

def ver_metricas_codigo():
    layout_metricas = [
        [sg.Text("Nombre del archivo:"), sg.InputText(key="nombre_archivo")],
        [sg.Text("Seleccione la extensión:"), sg.Combo([".java", ".py", ".c", ".js"], key="extension")],
        [sg.Button("Ver contenido del Bucket")],
        [sg.Button("Aceptar"), sg.Button("Cancelar")]
    ]

    window_metricas = crear_ventana("Ver Métricas de Código", layout_metricas)

    while True:
        event_metricas, values_metricas = window_metricas.read()

        if event_metricas == sg.WIN_CLOSED or event_metricas == "Cancelar":
            window_metricas.close()
            break
        
        if event_metricas == "Ver contenido del Bucket":
            x=1
            lambda_client = boto3.client("lambda", endpoint_url=localstack_endpoint, region_name=aws_region)

            print("Invocando Lambda4...")
            response = lambda_client.invoke(
                FunctionName="lambda1",
                InvocationType="RequestResponse"
            )
            response = response["Payload"].read().decode("utf-8")

            sg.popup(response)

            ver_metricas_codigo()
        
        nombre_archivo = values_metricas["nombre_archivo"]
        extension = values_metricas["extension"]
        nombre = nombre_archivo + extension
        if nombre_archivo and extension:
            lambda_client = boto3.client("lambda", endpoint_url=localstack_endpoint, region_name=aws_region)

            # Construir el payload con los parámetros
            payload = {
                "nombre_archivo": nombre_archivo,
                "extension": extension
            }

            # Convertir el payload a una cadena JSON
            payload_json = json.dumps(payload)

            print(f"Payload: {payload_json}")
            print("Invocando Lambda2...")

            # Invocar la función Lambda con el payloadS
            response = lambda_client.invoke(
                FunctionName="lambda2",
                InvocationType="RequestResponse",
                Payload=payload_json
            )

            # Leer y decodificar la respuesta
            metrics = response["Payload"].read().decode("utf-8")

            sg.popup(metrics)

            # Cerrar la ventana
            window_metricas.close()
            break

    window_metricas.close()
    return nombre_archivo, extension


def ask_for_sentence():
    layout_input = [
        [sg.Text("Ingrese una oración:")],
        [sg.InputText(key="user_input")],
        [sg.Button("Aceptar"), sg.Button("Cancelar")]
    ]

    window_input = crear_ventana("Ingrese una oración", layout_input)

    while True:
        event_input, values_input = window_input.read()

        if event_input == sg.WIN_CLOSED or event_input == "Cancelar":
            window_input.close()
            return None

        user_input = values_input["user_input"]

        if user_input.strip():
            window_input.close()
            return user_input

    window_input.close()



def ejecutar_opcion(opcion, archivo_ruta):


    # Configuración del cliente de Lambda para LocalStack
    lambda_client = boto3.client("lambda", endpoint_url=localstack_endpoint, region_name=aws_region)

    if opcion == "opcion1":
        first_lambda(archivo_ruta)

        sg.popup("Archivo subido correctamente")
    elif opcion == "opcion2":
        # Llamada a la función Lambda de métricas de código con parámetros
        ver_metricas_codigo()
    elif opcion == "opcion3":
        
        user_input = ask_for_sentence()
        print(f"Invoking lambda3 with input: {user_input}")
        response = lambda_client.invoke(
            FunctionName="lambda3",
            InvocationType="RequestResponse",
            Payload=json.dumps({"input": user_input})
        )
        result = response["Payload"].read().decode("utf-8")
        sg.popup(result)
if __name__ == "__main__":
    main()
