import json
import uuid

from .gig_model import GigModel


def create(event, context):
    data = json.loads(event["body"])
    response = {}

    gig = GigModel(
        gig_id=str(uuid.uuid1()),
        title=data["title"],
        music_starts=data["music_starts"],
        doors_open=data["doors_open"],
        performance_date=data["performance_date"],
        price=data["price"],
        description=data["description"],
        url=data["url"],
        image_url=data["image_url"],
    )

    try:
        gig.save()
        response["status"] = 201
        response["body"] = gig
    except:
        response["status"] = 500
        response["body"]["error"] = "Error saving gig"

    response["body"] = json.dumps(response["body"])
    return response
