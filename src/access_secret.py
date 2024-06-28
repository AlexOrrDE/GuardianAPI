import boto3
import json
from botocore.exceptions import ClientError


def access_secret():
    """Fetches secret API key saved in AWS secretsmanager"""

    secret_name = "guardian_secrets"
    region = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        raise Exception("Error retrieving secret: {}".format(e))

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)
