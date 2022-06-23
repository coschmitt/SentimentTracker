import tweepy
from env import TWEEPY_CONSUMER_SECRET, TWEEPY_CONSUMER_KEY, TWEEPY_ACCESS_TOKEN_SECRET, TWEEPY_ACCESS_TOKEN, BEARER_TOKEN


# twitter API keys
auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
api = tweepy.API(auth)


# function used for accessing trending on twitter
def get_trending(woeid=1):
    return api.get_place_trends(woeid)


# used to get the WOEID of any location string passed to the function
def get_woeid(locations):
    twitter_world = api.available_trends()
    places = {loc['name'].lower() : loc['woeid'] for loc in twitter_world}
    woeids = []
    for location in locations:
        if location in places:
            woeids.append(places[location])
        else:
            print("err: ",location," woeid does not exist in trending topics")
    return woeids


def get_filter_choices():
    twitter_world = api.available_trends()
    places = []
    for loc in twitter_world:
        places.append((loc['woeid'], loc['name']))  # append the country/city name and ID number

    places = sorted(places, key=lambda x: x[1])     # sort alphabetically
    return tuple(places)                            # turn the list into a tuple for the forms choice
