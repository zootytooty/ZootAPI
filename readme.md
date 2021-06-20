# ZootAPI       [![Deploy](https://github.com/zootytooty/ZootAPI/actions/workflows/deploy.yml/badge.svg)](https://github.com/zootytooty/ZootAPI/actions/workflows/deploy.yml)


Basic API to manage database interactions. It manages the following datapoints:
- venue    
- title    
- music_starts    
- doors_open    
- performance_date    
- price    
- description    
- url    
- image_url 


## Deployment

The API is managed via the [serverless framework](https://www.serverless.com/), using an AWS backend. To deploy, install the dependencies then run deploy using your desired AWS profile.

```bash
npm install
sls deploy --aws-profile <profile-name>
```


## Functionality

All methods are within `gigmanagement.py`


### Get Gigs

`GET: gigs`

By default returns all shows; shows from the past and future. The API supports querystring filtering by any of the above listed data points, eg:
```http
/gigs?venue=jazzlab
/gigs?venue=paris_cat&date=YYYYMMDD
```

The response is a JSON array containing the shows requested, eg:
```JSON
[
    {
        "title": "Rob Burke presents: Paul Williamson and the Young GUNS",
        "venue": "jazzlab",
        "description": "Paul has built his reputation on the Australian jazz and improvisation scene as an individual voice in trumpet and composition. Tonight he is joined by some of the rising stars of the Australian jazz scene.  ",
        "performance_date": "2019-05-15",
        "doors_open": "8:00 PM",
        "music_starts": "8:30 PM",
        "price": 20,
        "url": "https://jazzlab.club/1089-rob-burke-presents-paul-williamson-and-the-young-guns",
        "image_url": "https://jazzlab.club/media/com_eventbooking/images/PW-Image.jpg"
    },
    {
        "title": "Raymond MacDonald (Scotland) + Rob Burke Quartet",
        "venue": "jazzlab",
        "description": "As a saxophonist and composer Raymond MacDonald's work is informed by a view of improvisation as a social, collaborative and uniquely creative process that provides opportunities to develop new ways of working musically. Raymond will be joined by Rob Burke (saxophone), Paul Grabowsky (piano), Nick Haywood (bass), Tony Floyd (drums)",
        "performance_date": "2019-05-29",
        "doors_open": "8:00 PM",
        "music_starts": "8:30 PM",
        "price": 20,
        "url": "https://jazzlab.club/1091-raymond-macdonald-scotland-rob-burke-quartet",
        "image_url": "https://jazzlab.club/media/com_eventbooking/images/RaymondMacDonald.jpg"
    }
]

```

### Add Gigs

`POST: gigs`

Insert process to add new shows. The API supports both single & batch requests. Both require a gig object to be provided which should resemble:
```json
{
    "venue": "venue",
    "title": "title",
    "music_starts": "HH:MM",
    "doors_open": "HH:MM",
    "performance_date": "YYYY-MM-DD",
    "price": price,
    "description": "description",
    "url": "url",
    "image_url": "image url" 
}
```

For single items, submit just the above object. For batch requests submit an array of them. Eg:
```json
[
    {
    "venue": "venue",
    "title": "title",
    "music_starts": "HH:MM",
    "doors_open": "HH:MM",
    "performance_date": "YYYY-MM-DD",
    "price": price,
    "description": "description",
    "url": "url",
    "image_url": "image url" 
    },
    ...
]
```

The response is a JSON containing the number of records attempted, updated and added, eg:
```JSON
{
    "records_attempted": 3,
    "records_updated": 2,
    "records_added": 1
}
```
