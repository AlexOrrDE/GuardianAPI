import json
import boto3
from unittest.mock import patch, Mock
from moto import mock_aws
from mock_request import mocked_requests_get
from src.handler import lambda_handler


@mock_aws
@patch("requests.get", side_effect=mocked_requests_get)
def test_handler_success(mock_requests_get):
    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    stream_name = "test_stream"
    client = boto3.client("kinesis", region_name="eu-west-2")
    client.create_stream(StreamName=stream_name, ShardCount=1)

    event = {
        "query": "machine learning",
        "date_from": "2023-01-01",
        "broker_id": stream_name,
    }
    context = {}

    response = lambda_handler(event, context)
    response_body = " ".join(response["body"].split())

    assert response["statusCode"] == 200
    assert "Successfully published 2 articles to Kinesis" in response_body
    mock_requests_get.assert_called_once()


@mock_aws
@patch("requests.get", side_effect=mocked_requests_get)
def test_no_query_provided(mock_requests_get):
    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    stream_name = "test_stream"
    client = boto3.client("kinesis", region_name="eu-west-2")
    client.create_stream(StreamName=stream_name, ShardCount=1)

    event = {
        "date_from": "2023-01-01",
        "broker_id": stream_name,
    }
    context = {}

    response = lambda_handler(event, context)
    response_body = " ".join(response["body"].split())

    assert response["statusCode"] == 400
    assert "Missing required query parameter" in response_body


@mock_aws
@patch("requests.get", side_effect=mocked_requests_get)
def test_no_stream_provided(mock_requests_get):
    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    stream_name = "test_stream"
    client = boto3.client("kinesis", region_name="eu-west-2")
    client.create_stream(StreamName=stream_name, ShardCount=1)

    event = {
        "query": "machine learning",
        "date_from": "2023-01-01",
    }
    context = {}

    response = lambda_handler(event, context)
    response_body = " ".join(response["body"].split())

    assert response["statusCode"] == 400
    assert "Missing required broker_id parameter" in response_body


@mock_aws
def test_handler_secret_error():
    event = {
        "query": "machine learning",
        "date_from": "2023-01-01",
        "broker_id": "test_stream",
    }
    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Error retrieving secrets" in response["body"]


@mock_aws
@patch("handler.fetch_guardian_articles")
def test_handler_fetch_articles_error(mock_fetch_guardian_articles):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("Test exception")
    mock_fetch_guardian_articles.return_value = mock_response

    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    event = {
        "query": "machine learning",
        "date_from": "2023-01-01",
        "broker_id": "test_stream",
    }
    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Error fetching articles" in response["body"]


@mock_aws
@patch("requests.get", side_effect=mocked_requests_get)
@patch("handler.publish_to_kinesis")
def test_handler_publish_to_kinesis_error(
    mock_requests_get,
    mock_publish_to_kinesis,
):
    mock_publish_to_kinesis.side_effect = Exception(
        "Error publishing to Kinesis",
    )

    secret_name = "guardian_secrets"
    secret_value = json.dumps({"GUARDIAN_API_KEY": "test_key"})

    client = boto3.client("secretsmanager", region_name="eu-west-2")
    client.create_secret(Name=secret_name, SecretString=secret_value)

    event = {
        "query": "machine learning",
        "date_from": "2023-01-01",
        "broker_id": "test_stream",
    }
    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert "Error publishing to Kinesis" in response["body"]
