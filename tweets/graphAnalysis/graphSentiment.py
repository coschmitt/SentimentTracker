from datetime import datetime, timedelta

import mpld3
import tweepy
import boto3
import json
import matplotlib.pyplot as plt
import pandas as pd
import pdb
from env import TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET, TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

auth = tweepy.OAuthHandler(TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET)
auth.set_access_token(TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def byteCalc(s):
    return len(s.encode('utf-8'))


# def get_keywords(search, region, end_date, result_type, aws_client, twitter_client):
#     text_batch = []
#     num_days = 7
#     end_date = datetime.strptime(end_date, '%Y-%m-%d')
#
#     for day in range(0, num_days):
#         tweets = twitter_client.search(q=search, rpp=100, count=30, until=end_date-timedelta(days=day),
#                                        result_type=result_type, region=region)
#         composite_tweet_string = ""
#         for tweet in tweets:
#             body = tweet._json.get('text')
#             composite_tweet_string += " " + body
#         text_batch.append(composite_tweet_string)
#
#     codes = []
#     response = aws_client.batch_detect_dominant_language(TextList=text_batch)['ResultList']
#     for r in response:
#         codes.append(r['Languages'][0]['LanguageCode'])
#     dom_language = max(set(codes), key=codes.count)



def generate_graph(search, region, end_date, result_type):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


    numTweets = 5
    numDays = 7
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    dataf = []  # For storing dataframe of valuable information
    for i in range(0,numDays):
        untilDate = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
        keyword_tweets = api.search(q=search, rpp=100, count=numTweets, until=end_date-timedelta(days=i),
                                    result_type=result_type, region=region)

        # gathering info about timeline
        # text = "" #String to store users tweets
        # day  = "" #String to check what day of the week this tweet was posted

        for status in keyword_tweets:
            day = status._json["created_at"][0:3]
            text = status._json["text"]
            data = json.loads(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
            overallSentiment = data["Sentiment"]
            positive = data["SentimentScore"]["Positive"]
            negative = data["SentimentScore"]["Negative"]
            dataf.append([day, positive, negative])


    dataf.reverse()

    df = pd.DataFrame(dataf, columns=['Day', 'positive', 'negative%'])

    df["positive"] = 100 * df["positive"]
    df["negative%"] = 100 * df["negative%"]

    dfDay = df.groupby(['Day']).mean()

    dfDay = dfDay.reindex(["Mon", "Tue", "Wed", "Thu", "Fri","Sat","Sun"])

    dfDay=dfDay.fillna(0)
    dayList = dfDay.index.get_level_values('Day')

    positiveList = dfDay.reset_index()["positive"].tolist()
    negativeList = dfDay.reset_index()["negative%"].tolist()

    # Bar graph

    fig1 = plt.figure()
    plt.bar(dayList, negativeList)
    # naming the y axis
    plt.ylabel('Percent')

    plt.title(search + ' Sentiment Analysis!')

    fig1 = mpld3.fig_to_html(fig1)

    #Line graph
    # Line graph for more days

    fig2 = plt.figure()
    plt.plot(dayList, positiveList)
    plt.xlabel('Day of the Week')
    # naming the y axis
    plt.ylabel('Percent positivity')
    plt.title(search + ' Sentiment Analysis!')
    fig2 = mpld3.fig_to_html(fig2)

    return [fig1,fig2]
