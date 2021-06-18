import boto3
import json

from gigmanagement import GigManagement
gm = GigManagement()


def manager(event, context):

    # Identify request intent
    verb = event['context']['http-method']
    method = event['context']['resource-path']

    # Pass to the appropriate function
    if verb == "GET" and method == "/gigmanagement/getgigs":

        filters = event['params']['querystring']
        gigs = gm.get_gigs(filters)
        return gigs

    elif verb == "POST" and method == "/gigmanagement/addgigs":

        gigs_to_add = event['body-json']

        if isinstance(gigs_to_add, dict):
            gigs_to_add = [gigs_to_add]

        response = gm.add_gigs(gigs_to_add)
        return response
        

    else:
        # Return some error....

        return {
            "status": "incorrect method &/or verb combo"
        }

