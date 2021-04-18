# SentimentTracker
run pip install requirements.txt.

AWS and Twitter API required for project!

## Inspiration
We wanted to make a place for people to see real time analysis of public opinion on various topics.

## What it does
Using AWS NLP and the twitter API, we use sentiment analysis to show public opinion via line and bar graphs.

## How we built it
We built this project using the Django Framework for python.

## Challenges we ran into
Our biggest challenge was not having enough access to the twitter and AWS APIs in order to run fast, sentiment analysis on large amounts of data.

## Accomplishments that we're proud of
We are very proud about how we were able to create a 'trends' page based by region where a user can click on a topic and be displayed a sentiment dashboard.

## What we learned
We learned that we can never underestimate a task! No matter how trivial it may seem, you never know what obstacles you may run into.

## What's next for Public Sentiment Tracker
We would like to polish out the frontend, make requests faster and add a loading page after the search form is submitted. In addition, we would like to beef up the dashboards to include keywords and top tweets on the topic 

**In order to use the project, you must have tweepy access tokens AND AWS access tokens. Twitter tokens should be located in a 'env.py' file at the project level, while AWS tokens should be in credentials file at ~/.aws**

