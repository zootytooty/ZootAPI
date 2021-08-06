"""Entry point for Zoot API."""

import json
import os
from typing import List

from venuemanagement import VenueManagement


vm = VenueManagement(
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
    connection_string=os.getenv("MONGO_CONNECTION_STRING"),
    database="zootdb",
)


def get_venues(event: dict, context: object) -> List[dict]:
    """Entry point for GET-venues API, retrieving all venue details.

    Args:
        event (dict): API request including gateway information
        context (object): Methods and properties that provide information about the invocation,
                          function, and execution environment

    Returns:
        List[dict]: All known venues based on the request parameters
    """

    try:
        venues = vm.get_venues()
        response = {"statusCode": 200, "body": json.dumps(venues)}

        return response

    except Exception as ex:

        response = {"statusCode": 500, "error": json.dumps(str(ex))}
        return response


def add_venue(event: dict, context: object) -> dict:
    """Entry point for POST-venues API, inserting the provided venue.

    Args:
        event (dict): API request including gateway information
        context (object): Methods and properties that provide information about the invocation,
                          function, and execution environment

    Returns:
        dict: Number of records successfully added.
    """
    try:
        venue_to_add = json.loads(event["body"])

        response = vm.add_venue(venue_to_add)
        response = {"statusCode": 200, "body": json.dumps(response)}

        return response

    except Exception as ex:

        response = {"statusCode": 500, "error": json.dumps(str(ex))}
        return response
