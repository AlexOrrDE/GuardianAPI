import boto3
import json

kinesis_client = boto3.client("kinesis")


def publish_to_kinesis(data, stream_name):
    """Sends the data retrieved from the Guardian API
    to the AWS Kinesis stream specified in the input"""

    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey="partitionKey")
    return response
