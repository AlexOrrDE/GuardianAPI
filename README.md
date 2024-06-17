# Guardian API Streaming Project using AWS Kinesis #

Project link: 
____
This application is designed to retrieve relevant articles from the Guardian API based on a given search term and a date (optional), and then publish these articles to a specified message broker. The fetched articles can be utilized by marketing and careers teams for analysis and many other various purposes.

The code is fully tested, secure, and PEP8 compliant.

**An AWS account is required to use this code.**

## Overview

The application comprises four functions:
- **access_secret()** which retrieves the value of the Guardian API key stored in AWS Secrets Manager.
- **fetch_guardian_articles()** which contacts the Guardian API and gets the ten most recent results pertaining to the specified query.
- **publish_to_kinesis()** which sends the retrieved articles in JSON format to the specified message broker.
- **lambda_handler()** which manages the execution of the other functions, as well as logging as error-handling.

These are packaged into a "function.zip" file ready to be uploaded to AWS.

The repository also includes tests for these functions, a requirements.txt file, and a Makefile to assist with the set up of the code.

## Functionality

The application accepts the following inputs in JSON format:
- A **search term** 
- An optional **"date_from"** field
- A reference to a **message broker** (AWS Kinesis stream)

Given these inputs, the application performs the following steps:
1. **Fetch Articles**: Retrieves up to ten articles from the Guardian API based on the search term and date.
2. **Publish to Kinesis**: Publishes the retrieved articles in JSON format to the specified AWS Kinesis stream.

### Example Input

The input will take the following JSON format:

```json
{
    "query": "machine learning",
    "date_from": "2023-01-01",
    "broker_id": "guardian_content"
}
```

In this case, the application retrieves the ten most recent articles returned by the Guardian API pertaining to "machine learning" (so long as they are from after 2023-01-01) and posts them in JSON format to the Kinesis stream with ID "guardian_content".


### Example Output

The published data to the Kinesis stream will have the following JSON format:

```json
{
    "webPublicationDate": "2023-11-21T11:11:31Z",
    "webTitle": "Who said what: using machine learning to correctly attribute quotes",
    "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes"
}
```


## Setup

To set up the code, simply follow these steps:

- Clone the repository and install dependencies:

        git clone LINK
        cd GuardianAPI
        make requirements

- Get a free key from the [Guardian API](https://open-platform.theguardian.com/).

- Configure AWS Resources:

    - Create a secret in the Secrets Manager called "guardian_secrets" and assign your Guardian API key as its value.

    - Create an S3 bucket, and upload "function.zip" from this repository to it.

    - Create a lambda function:
        - In the AWS console, create a new Lambda function.
        - In "Code source", choose to upload "function.zip" from the S3 location created in the previous step.
        - Ensure that the handler is set to "handler.lambda_handler"
        - Make sure that the Lambda function has permissions to access S3, Secrets Manager, CloudWatch, and Kinesis.

    - Create a Kinesis stream with a name which matches the desired "broker_id" value you will use as an input for the Lambda function.

You can now trigger the lambda using the AWS CLI, or set up an API Gateway to do this. The output can be viewed and/or saved by streaming it through a data hose (eg: Amazon Data  Firehose).

## Testing

The code is fully tested and secure. It is also PEP8 compliant. To set up the testing environment, you can follow these steps:

- In the terminal in your virtual environment, run:

        make dev-setup
        make run-checks

This will check that the code is secure and PEP8 compliant, as well as test that the code functions correctly and is covered to a strong degree by the tests.