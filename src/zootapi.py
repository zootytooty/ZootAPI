"""Entry point for Zoot API."""

import json
import os
from typing import List

from gigmanagement import GigManagement


gm = GigManagement(
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
    connection_string=os.getenv("MONGO_CONNECTION_STRING"),
)


def get_gigs(event: dict, context: object) -> List[dict]:
    """Entry point for GET-gigs API, retrieving gigs based on the requst details.

    Args:
        event (dict): API request including gateway information
        context (object): Methods and properties that provide information about the invocation,
                          function, and execution environment

    Returns:
        List[dict]: All known gigs based on the request parameters
    """
    try:
        filters = event["params"]["querystring"]
        gigs = gm.get_gigs(filters)
        return gigs

    except Exception as ex:

        response = {"statusCode": 500, "error": json.dumps(str(ex))}
        return response


def add_gigs(event: dict, context: object) -> dict:
    """Entry point for POST-gigs API, inserting the provided gig/s.

    Args:
        event (dict): API request including gateway information
        context (object): Methods and properties that provide information about the invocation,
                          function, and execution environment

    Returns:
        dict: Number of records successfully added.
    """
    try:
        gigs_to_add = event["body-json"]

        # If only a single gig is provided, then turn it into a pseudo batch request of length 1
        if isinstance(gigs_to_add, dict):
            gigs_to_add = [gigs_to_add]

        response = gm.add_gigs(gigs_to_add)
        return response

    except Exception as ex:

        response = {"statusCode": 500, "error": json.dumps(str(ex))}
        return response
