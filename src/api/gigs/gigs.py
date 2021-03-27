import json
import uuid

from datetime import datetime, timedelta
from functools import reduce
from pynamodb.expressions.condition import And

from .gig_model import GigModel


def create(event, context):
    response = {}
    try:
        data = json.loads(event["body"])
    except json.decoder.JSONDecodeError:
        response["statusCode"] = 400
        response["body"] = json.dumps({"error": "Invalid JSON"})
        return response

    try:
        gig = GigModel(
            gig_id=str(uuid.uuid1()),
            venue=data["venue"],
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
        response["statusCode"] = 400
        response["body"] = json.dumps({"error": f"{err} is required"})
        return response

    try:
        gig.save()
        response["statusCode"] = 201
        response["body"] = gig.as_dict()
    except:
        response["statusCode"] = 500
        response["body"] = {"error": "Error saving gig"}

    response["body"] = json.dumps(response["body"], default=str)
    return response


def list(event, context):
    limit = None
    filters = []
    response = {}
    results = []

    params = event["queryStringParameters"]
    
    if params:
        for key, value in params.items():
            if key == "date":
                try:
                    date = datetime.strptime(value, "%Y-%m-%d")
                    filters.append(GigModel.performance_date.between(date, date + timedelta(days=1)))
                except ValueError:
                    response["statusCode"] = 400
                    response["body"] = json.dumps({"error": f"Date must be fomratted YYYY-MM-DD. Received '{value}'"})
                    return response
            if key == "venue":
                filters.append(GigModel.venue == value)
            if key == "limit":
                try:
                    limit = int(value)
                except ValueError:
                    response["statusCode"] = 400
                    response["body"] = json.dumps({"error": f"Limit must be a number. Received '{value}'"})
                    return response

    if len(filters) == 0:
        filters = None
    else:
        filters = reduce(And, filters)
    try:
        for gig in GigModel.scan(filter_condition=filters, limit=limit):
            results.append(gig.as_dict())
        response["statusCode"] = 200
        response["body"] = json.dumps(results, default=str)
        return response
    except:
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "Error fetching gigs from database"})
        return response

def get(event, context):
    response = {}
    gig_id = event["pathParameters"]["id"]

    try:
        gig = GigModel.get(gig_id)

        response["statusCode"] = 200
        response["body"] = json.dumps(gig.as_dict(), default=str)
        return response
    except:
        response["statusCode"] = 404
        response["body"] = json.dumps({"error": f"Gig with id '{gig_id}' not found"})
        return response