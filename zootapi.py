import boto3
import json
import yaml

from gigmanagement import GigManagement
gm = GigManagement()


def lambda_handler(event, context):

    # Identify request intent
    verb = event['context']['http-method']
    method = event['context']['resource-path']

    # Pass to the appropriate function
    if verb=="GET" and method = "/gigmanagement/getgigs":

        if event['params']['querystring']:
            query_params = event['params']['querystring']
            venue = query_params['venue'] if 'venue' in query_params else None
            # date = query_params['date'] if 'date' in query_params else None

        gigs = gm.get_gigs('bbb')

        return gigs

    elif verb=="POST" and method = "/gigmanagement/addgigs":

        venue = event['body-json']['venue']
        title = event['body-json']['title']
        music_starts = event['body-json']['music_starts']
        doors_open = event['body-json']['doors_open']
        performance_date = event['body-json']['performance_date']
        price = event['body-json']['price']
        description = event['body-json']['description']
        url = event['body-json']['url']
        image_url = event['body-json']['image_url']

        gm.add_gig(venue = venue,
                    title = title,
                    music_starts = music_starts,
                    doors_open = doors_open,
                    performance_date = performance_date,
                    price = price, 
                    description = description,
                    url = url,
                    image_url = image_url)

        return {
            "status": "Success!"
        }

    else:
        # Return some error....

        return {
            "status": "incorrect method &/or verb combo"
        }

