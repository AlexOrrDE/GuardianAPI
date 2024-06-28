import logging
from get import fetch_guardian_articles
from kinesis import publish_to_kinesis
from access_secret import access_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Manages the execution of the other functions and error handling"""

    logger.info("Received event: %s", event)

    try:
        secrets = access_secret()
        guardian_api_key = secrets["GUARDIAN_API_KEY"]
    except Exception as e:
        logger.error("Error retrieving secrets: %s", e)
        return {
            "statusCode": 500,
            "body": f"Error retrieving secrets: {str(e)}"}

    query = event.get("query")
    date_from = event.get("date_from", None)
    broker_id = event.get("broker_id")

    if not query:
        logger.error("Missing required query parameter")
        return {"statusCode": 400, "body": "Missing required query parameter"}
    if not broker_id:
        logger.error("Missing required broker_id parameter")
        return {
            "statusCode": 400,
            "body": "Missing required broker_id parameter"}

    logger.info(
        "Fetching articles with query: %s and date_from: %s",
        query,
        date_from)

    try:
        articles = fetch_guardian_articles(
            guardian_api_key, query, date_from)
        logger.info("Fetched %d articles", len(articles))
    except Exception as e:
        logger.error("Error fetching articles: %s", e)
        return {
            "statusCode": 500,
            "body": f"Error fetching articles: {str(e)}"}

    published_articles = []
    for article in articles:
        try:
            publish_to_kinesis(article, broker_id)
            published_articles.append(article)
            logger.info(
                "Published article to Kinesis: %s",
                article["webTitle"])
        except Exception as e:
            logger.error("Error publishing to Kinesis: %s", e)
            return {
                "statusCode": 500,
                "body": f"Error publishing to Kinesis: {str(e)}"}

    logger.info(
        "Successfully published %d articles to Kinesis",
        len(published_articles))
    return {
        "statusCode": 200,
        "body": f"""Successfully published {len(published_articles)}
         articles to Kinesis""",
    }
