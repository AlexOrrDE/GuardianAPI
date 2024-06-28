import requests

GUARDIAN_API_URL = "https://content.guardianapis.com/search"


def mocked_requests_get(*args, **kwargs):
    """Mock request from Guardian API for use in testing"""

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"{self.status_code} Client Error")

    if args[0] == "https://content.guardianapis.com/search":
        return MockResponse(
            {
                "response": {
                    "results": [
                        {
                            "webPublicationDate": "2023-01-01T00:00:00Z",
                            "webTitle": "Test Article 1",
                            "webUrl": "https://example.com/article1",
                        },
                        {
                            "webPublicationDate": "2023-01-02T00:00:00Z",
                            "webTitle": "Test Article 2",
                            "webUrl": "https://example.com/article2",
                        },
                    ]
                }
            },
            200,
        )
    return MockResponse(None, 404)
