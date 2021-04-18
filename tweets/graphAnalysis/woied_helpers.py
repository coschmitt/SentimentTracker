import tweepy


# twitter API keys
auth = tweepy.OAuthHandler("KdE45VAZRJYDcjaqHz1NYuRSb", "IqeYxJgRHr4FDdz5lktEYcNtQsQwvELMWbGIb2EAjyVQXEDgoz")
auth.set_access_token("1252352172085383168-Rz2h4E6riMibKxFeS4xfzGgvNHy0TL",
                      "aCLAFYRNgq6zZ0laJS9Q2gbkKa1x2VPlJrvzVCe4dQ9zT")

api = tweepy.API(auth)


# function used for accessing trending on twitter
def get_trending(woeid=1):
    return api.trends_place(woeid)


# used to get the WOEID of any location string passed to the function
def get_woeid(locations):
    twitter_world = api.trends_available()
    places = {loc['name'].lower() : loc['woeid'] for loc in twitter_world}
    woeids = []
    for location in locations:
        if location in places:
            woeids.append(places[location])
        else:
            print("err: ",location," woeid does not exist in trending topics")
    return woeids


def get_filter_choices():
    twitter_world = api.trends_available()
    places = []
    for loc in twitter_world:
        places.append((loc['woeid'], loc['name']))  # append the country/city name and ID number

    places = sorted(places, key=lambda x: x[1])     # sort alphabetically
    return tuple(places)                            # turn the list into a tuple for the forms choice





