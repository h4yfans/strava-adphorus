from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.SegmentsApi()
bounds = "123"  # array[Float] | The latitude and longitude for two points describing a rectangular boundary for the search: [southwest corner latitutde, southwest corner longitude, northeast corner latitude, northeast corner longitude]
activityType = activityType_example  # String | Desired activity type. (optional)
minCat = 56  # Integer | The minimum climbing category. (optional)
maxCat = 56  # Integer | The maximum climbing category. (optional)

try:
    # Explore segments
    api_response = api_instance.exploreSegments(bounds, activityType=activityType, minCat=minCat, maxCat=maxCat)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SegmentsApi->exploreSegments: %s\n" % e)
