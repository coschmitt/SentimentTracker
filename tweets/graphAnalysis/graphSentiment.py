from datetime import datetime, timedelta
from keras.preprocessing.sequence import pad_sequences
from io import BytesIO
import base64

import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from env import model, tokenizer, BEARER_TOKEN


auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
api = tweepy.API(auth)


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image = buffer.getvalue()
    graph = base64.b64encode(image)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def make_plot(x, y, search):
    plt.switch_backend("AGG")
    plt.figure(figsize=(10, 5))
    plt.title(search + ' Sentiment Analysis!')
    plt.plot(x, y)
    plt.axhline(y=50, color="r", alpha=.5)
    plt.xticks(rotation=45)
    plt.ylim([0, 100])
    plt.xlabel('Day of the Week')
    plt.ylabel('Percent positivity')
    plt.tight_layout()
    
    return get_graph()


def generate_graph(search, region, result_type):
    numTweets = 10
    numDays = 7
    end_date = datetime.utcnow()
    dataf = []  # For storing dataframe of valuable information
    for i in range(0, numDays):
        toDate = (end_date-timedelta(days=i)).strftime('%Y-%m-%d')
        keyword_tweets = api.search_tweets(q=search, count=numTweets, lang="en", until=toDate,
                                           result_type=result_type)

        # gathering info about timeline

        tweets = [status._json["text"] for status in keyword_tweets]
        days = [datetime.strptime(status._json["created_at"], '%a %b %d %H:%M:%S +0000 %Y').date() for status in
                keyword_tweets]
        token_tweets = tokenizer.texts_to_sequences(tweets)
        pad_tweets = pad_sequences(token_tweets, maxlen=300)
        pred = model.predict(pad_tweets).reshape(1, -1)[0]
        dataf.extend(list(zip(days, pred, 1 - pred)))

    dataf.reverse()
    df = pd.DataFrame(dataf, columns=['Day', 'positive', 'negative'])
    df["positive"] = 100 * df["positive"]
    df["negative"] = 100 * df["negative"]
    dfDay = df.groupby(['Day']).mean().sort_values("Day")
    dfDay = dfDay.fillna(0)
    fig = make_plot(list(dfDay.index.astype(str)), dfDay["positive"], search)

    return fig, round(df["positive"].mean(), 2)
