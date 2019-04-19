# ZootAPI

Basic API to manage database interactions. 

## Functionality

### Add Gigs
Insert process to add new shows. Requires the following inputs:
- venue    
- title    
- music_starts    
- doors_open    
- performance_date    
- price    
- description    
- url    
- image_url 

A JSON payload containing a list of gigs can be posted to the `addgigs` endpoint.
```
{
    "gigs": [
    {
        "venue": ,
        "title": ,
        "music_starts": ,
        "doors_open": ,
        "performance_date": ,
        "price": ,
        "description": ,
        "url": ,
        "image_url": 
    }]
}
```


### Get Gigs
**Currently Poorly Implemented**



## Requirements
- AWS Lambda funciton called "Get-Gigs"
- RDS Instance with connection details in a conf.yaml


## Deployment

```shell
deploy.sh
```