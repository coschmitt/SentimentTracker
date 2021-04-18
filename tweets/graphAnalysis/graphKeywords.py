import datetime as datetime
import tweepy
import boto3
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta
import math

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

auth = tweepy.OAuthHandler("KdE45VAZRJYDcjaqHz1NYuRSb", "IqeYxJgRHr4FDdz5lktEYcNtQsQwvELMWbGIb2EAjyVQXEDgoz")
auth.set_access_token("1252352172085383168-Rz2h4E6riMibKxFeS4xfzGgvNHy0TL", "aCLAFYRNgq6zZ0laJS9Q2gbkKa1x2VPlJrvzVCe4dQ9zT")

api = tweepy.API(auth)
# user = api.get_user('joebiden')


api = tweepy.API(auth)
search = input("Enter a search query: ")
numTweets = input("How many tweets would you like to analyze? ")
numDays = int(input("How many days would you like to analyze (max 7)? "))

dataf = [] #For storing dataframe of valuable information
for i in range(0,numDays):
    untilDate = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
    keyword_tweets = api.search(q=search, rpp=100, count=numTweets, until = untilDate-timedelta(days = i))

    #gathering info about timeline
    text = "" #String to store users tweets
    day  = "" #String to check what day of the week this tweet was posted

    print(len(keyword_tweets))
    for status in keyword_tweets:
        day = status._json["created_at"][0:3]
        text = status._json["text"]
        data = json.loads(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
        overallSentiment = data["Sentiment"]
        positive = data["SentimentScore"]["Positive"]
        negative = data["SentimentScore"]["Negative"]
        dataf.append([day, positive, negative])
        print(status)


dataf.reverse()
print(dataf)
print("Negative:", negative)
print("Positive:", positive)

df = pd.DataFrame(dataf, columns=['Day', 'positive', 'negative%'])

df["positive"] = 100 * df["positive"]
df["negative%"] = 100 * df["negative%"]

correct_order = ["Mon", "Tue", "Wed", "Thu", "Fri","Sat","Sun"]
dfDay = df.groupby(['Day']).mean()

dfDay = dfDay.reindex(["Mon", "Tue", "Wed", "Thu", "Fri","Sat","Sun"])

dfDay=dfDay.fillna(0)
print(dfDay)


dfDayBar = dfDay.plot.bar(legend=True)

#Bar graph

# naming the y axis
plt.ylabel('Percent')
plt.title(search + ' Sentiment Analysis!')
plt.show()

#Line graph
# Line graph for more days
dayList = dfDay.index.get_level_values('Day')
positiveList = dfDay.reset_index()["positive"].tolist()
print(dayList)

dfDayLine = plt.plot(dayList, positiveList)


plt.xlabel('Day of the Week')
# naming the y axis
plt.ylabel('Percent positivity')
plt.title(search + ' Sentiment Analysis!')
plt.show()

