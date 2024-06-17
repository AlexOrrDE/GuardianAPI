import boto3
import pytest
import json
from moto import mock_aws
from src.access_secret import access_secret


@mock_aws
def test_access_secret():
    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    secrets = access_secret()

    assert secrets["GUARDIAN_API_KEY"] == "test_key"


@mock_aws
def test_access_secret_client_error():
    with pytest.raises(Exception) as e:
        access_secret()

    assert "Error retrieving secret" in str(e.value)
