import boto3
import json
import os

def initialize_localstack():
    # Configuración de LocalStack
    print("Configurando LocalStack...")
    localstack_endpoint = "http://localhost:4566"
    aws_region = "us-east-1"  
    # Tiempo de inicio deseado (en segundos)
    startup_timeout_seconds = 120


    # Configuración de las variables de entorno
    environment_variables = {"LAMBDA_RUNTIME_ENVIRONMENT_TIMEOUT": str(startup_timeout_seconds)}

    s3_client = boto3.client("s3", endpoint_url=localstack_endpoint, region_name=aws_region)
    lambda_client = boto3.client("lambda", endpoint_url=localstack_endpoint)
    iam_client = boto3.client("iam", endpoint_url=localstack_endpoint)
    sqs_client = boto3.client("sqs", endpoint_url=localstack_endpoint, region_name=aws_region)
    eventbridge_client = boto3.client("events", endpoint_url=localstack_endpoint, region_name=aws_region)

    #Buckets

    buckets = ["lambdas-bucket","code-bucket"]
    for bucket_name in buckets:
        print(f"Creando el bucket {bucket_name}...")
        s3_client.create_bucket(Bucket=bucket_name)

    # Folder path to your local code directory
    code_folder_path = "CodigoEntreno"

    # S3 bucket name
    s3_bucket_name = "code-bucket"

    # Function to upload files from a local directory to an S3 bucket
    def upload_files_to_s3(local_path, s3_bucket):
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)

                # Use the filename as the S3 object key (without any subdirectories)
                s3_object_key = os.path.basename(local_file_path)

                print(f"Uploading {local_file_path} to S3 bucket {s3_bucket} with key {s3_object_key}")
                s3_client.upload_file(local_file_path, s3_bucket, s3_object_key)

    # Upload files from the local code directory to the root of the S3 bucket
    upload_files_to_s3(code_folder_path, s3_bucket_name)

    #Roles
    print("Creando el rol de IAM...")
    # Nombre del rol y archivo de política de confianza
    rol_nombre = "MiNuevoRol"
    trust_policy_file = "trust-policy.json"

    # Cargar la política de confianza desde el archivo JSON
    with open(trust_policy_file, "r") as file:
        trust_policy = json.load(file)

    # Crear el rol de IAM
    response = iam_client.create_role(
        RoleName=rol_nombre,
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )

    #SQS
    print("Creando la cola SQS...")
    queue_name = "sqs-request"

    queue_url = sqs_client.create_queue(QueueName=queue_name)["QueueUrl"]
    
    #Lambdas
    
    lambda_arns = [] 
    lambdas_bucket_name = "lambdas-bucket"
    zip_file_paths = ["lambda1.zip", "lambda2.zip","lambda3.zip"]

    for zip_file_path in zip_file_paths:
        zip_file_name = os.path.basename(zip_file_path)
        s3_key = zip_file_name

        print(f"Subiendo {zip_file_name} a {lambdas_bucket_name}...")
        with open(zip_file_path, "rb") as data:
            s3_client.upload_fileobj(data, lambdas_bucket_name, s3_key)

    zip_file_name = os.path.basename("my_lambda_layer.zip")
    s3_key = zip_file_name

    print(f"Subiendo {zip_file_name} a {lambdas_bucket_name}...")
    with open(zip_file_path, "rb") as data:
        s3_client.upload_fileobj(data, lambdas_bucket_name, s3_key)
        
    layer_name = 'layer1'
    zip_file_path = 'my_lambda_layer.zip'
    
    # Upload the ZIP archive as a Lambda Layer
    response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Content={
            'S3Bucket': 'lambdas-bucket',  
            'S3Key': zip_file_path,
        },
        CompatibleRuntimes=['python3.10'],
        Description='TensorFlow Lambda Layer',
        LicenseInfo='MIT',
    )

    layer_arn = response['LayerVersionArn']
    print(f'Lambda Layer ARN: {layer_arn}')
    
    lambdas = ["lambda1", "lambda2", "lambda3"]
    i = 0
    for zip_file_path in zip_file_paths:
        if i < 2:
            response = lambda_client.create_function(
                FunctionName=lambdas[i],
                Runtime="python3.11",
                Role="arn:aws:iam::123456789012:role/execution_role",
                Handler= lambdas[i] + ".lambda_handler",
                Code={
                    "S3Bucket": lambdas_bucket_name,
                    "S3Key": zip_file_path,
                },
                Environment={"Variables": environment_variables}

            )
        else:
            response = lambda_client.create_function(
                FunctionName=lambdas[i],
                Layers=[layer_arn],
                Runtime="python3.10",
                Role="arn:aws:iam::123456789012:role/execution_role",
                Handler= lambdas[i] + ".lambda_handler",
                Code={
                    "S3Bucket": lambdas_bucket_name,
                    "S3Key": zip_file_path,
                },
                Environment={"Variables": environment_variables}

            )
        lambda_arn = response['FunctionArn']  # Extract Lambda ARN from the response
        lambda_arns.append(lambda_arn)  # Add Lambda ARN to the list
        print(f"Lambda {lambdas[i]} created with ARN: {lambda_arn}")
        i += 1
    
    print("Creando las reglas de EventBridge...")
    
    #EventBrige
    event_pattern_sqs_1 = {
        "source": ["aws.sqs"],
        "detail-type": ["SQS Message Published"],
        "resources": [queue_url],
        "detail": {
            "messageAttributes": {
                "eventType": [{"value": ["type_1"]}]
            }
        }
    }

    # Event Pattern for SQS Message Type 2
    event_pattern_sqs_2 = {
        "source": ["aws.sqs"],
        "detail-type": ["SQS Message Published"],
        "resources": [queue_url],
        "detail": {
            "messageAttributes": {
                "eventType": [{"value": ["type_2"]}]
            }
        }
    }

    # Event Pattern for SQS Message Type 3
    event_pattern_sqs_3 = {
        "source": ["aws.sqs"],
        "detail-type": ["SQS Message Published"],
        "resources": [queue_url],
        "detail": {
            "messageAttributes": {
                "eventType": [{"value": ["type_3"]}]
            }
        }
    }

    # Lambda Function ARNs
    lambda_function_arn_1 = lambda_arns[0]  # Replace with the actual Lambda function ARN for type_1
    lambda_function_arn_2 = lambda_arns[1]  # Replace with the actual Lambda function ARN for type_2
    lambda_function_arn_3 = lambda_arns[2]  # Replace with the actual Lambda function ARN for type_3

    # Create EventBridge rules for each event type
    rule_name_1 = "event_rule_type_1"
    response = eventbridge_client.put_rule(
        Name=rule_name_1,
        EventPattern=json.dumps(event_pattern_sqs_1),
        State="ENABLED",
    )

    rule_name_2 = "event_rule_type_2"
    response = eventbridge_client.put_rule(
        Name=rule_name_2,
        EventPattern=json.dumps(event_pattern_sqs_2),
        State="ENABLED",
    )

    rule_name_3 = "event_rule_type_3"
    response = eventbridge_client.put_rule(
        Name=rule_name_3,
        EventPattern=json.dumps(event_pattern_sqs_3),
        State="ENABLED",
    )

    # Add targets for each rule
    response = eventbridge_client.put_targets(
        Rule=rule_name_1,
        Targets=[
            {
                "Id": "lambda_target_1",
                "Arn": lambda_function_arn_1,
            }
        ],
    )

    response = eventbridge_client.put_targets(
        Rule=rule_name_2,
        Targets=[
            {
                "Id": "lambda_target_2",
                "Arn": lambda_function_arn_2,
            }
        ],
    )

    response = eventbridge_client.put_targets(
        Rule=rule_name_3,
        Targets=[
            {
                "Id": "lambda_target_3",
                "Arn": lambda_function_arn_3,
            }
        ],
    )

    