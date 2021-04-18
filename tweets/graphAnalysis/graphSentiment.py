import tweepy
import boto3
import json
import matplotlib.pyplot as plt
import pandas as pd

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


def byteCalc(s):
    return len(s.encode('utf-8'))


def twitter_aws_connection():
    Username = input("Enter a twitter User: ")
    numTweets = input("How many tweets would you like to analyze? ")

    user_tweets = api.user_timeline(screen_name=Username, count=numTweets, include_rts=False)

    # gathering info about timeline
    text = ""  # String to store users tweets
    day = ""  # String to check what day of the week this tweet was posted

    dataf = []  # For storing dataframe of valuable information
    for status in user_tweets:
        if status._json["created_at"][0:3] != day and day != "":
            day = status._json["created_at"][0:3]
            continue
        day = status._json["created_at"][0:3]
        text = status._json["text"]
        data = json.loads(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
        overallSentiment = data["Sentiment"] * 100
        positive = data["SentimentScore"]["Positive"] * 100
        negative = data["SentimentScore"]["Negative"] * -100
        dataf.append([day, positive, negative])

    print("overallSentiment:", overallSentiment)
    print("Negative:", negative, "%")
    print("Positive:", positive, "%")

    df = pd.DataFrame(dataf, columns=['Day', 'postive%', 'negative%'])

    # Bar graph for day of the week
    dfDay = df.groupby(['Day']).mean()['postive%'].plot.bar(legend=True)
    plt.xlabel('Day of the Week')
    # naming the y axis
    plt.ylabel('Percent positivity')
    plt.title(Username + ' Sentiment Analysis!')
    plt.show()

    # Line graph for more days
    ax = df.plot(x='Day', y='postive%', rot=0)
    plt.xlabel('Day of the Week')
    # naming the y axis
    plt.ylabel('Percent positivity')
    plt.title(Username + ' Sentiment Analysis!')
    plt.show()

