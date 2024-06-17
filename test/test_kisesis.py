import boto3
from moto import mock_aws
from src.kinesis import publish_to_kinesis


@mock_aws
def test_publish_to_kinesis():
    stream_name = "test_stream"
    data = {"id": "1", "value": "test_value"}

    client = boto3.client("kinesis", region_name="eu-west-2")
    client.create_stream(StreamName=stream_name, ShardCount=1)

    response = publish_to_kinesis(data, stream_name)

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
