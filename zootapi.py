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
    if verb == "GET" and method == "/gigmanagement/getgigs":
        
        filters = event['params']['querystring']
        gigs = gm.get_gigs(filters)
        return gigs

    elif verb == "POST" and method == "/gigmanagement/addgigs":

        body = event['body-json']
        gig_ids = []

        for gig in body['gigs']:

            venue = gig['venue']
            title = gig['title']
            music_starts = gig['music_starts']
            doors_open = gig['doors_open']
            performance_date = gig['performance_date']
            price = gig['price']
            description = gig['description']
            url = gig['url']
            image_url = gig['image_url']

            gig_ids.append(gm.add_gig(venue = venue,
                                    title = title,
                                    music_starts = music_starts,
                                    doors_open = doors_open,
                                    performance_date = performance_date,
                                    price = price, 
                                    description = description,
                                    url = url,
                                    image_url = image_url))

        return {
            "gig_ids": gig_ids
        }

    else:
        # Return some error....

        return {
            "status": "incorrect method &/or verb combo"
        }

