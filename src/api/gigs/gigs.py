import json
import uuid

from datetime import datetime
from .gig_model import GigModel


def create(event, context):
    response = {}
    try:
        data = json.loads(event["body"])
    except json.decoder.JSONDecodeError:
        response["status"] = 400
        response["body"] = json.dumps({"error": "Invalid JSON"})
        return response

    try:
        gig = GigModel(
            gig_id=str(uuid.uuid1()),
            title=data["title"],
            music_starts=data["music_starts"],
            doors_open=data["doors_open"],
            performance_date=datetime.fromisoformat(data["performance_date"]),
            price=data["price"],
            description=data["description"],
            url=data["url"],
            image_url=data["image_url"],
        )
    except KeyError as err:
        response["status"] = 400
        response["body"] = json.dumps({"error": f"{err} is required"})
        return response

    try:
        gig.save()
        response["status"] = 201
        response["body"] = gig.as_dict()
    except:
        response["status"] = 500
        response["body"] = {"error": "Error saving gig"}

    response["body"] = json.dumps(response['body'])
    return response
