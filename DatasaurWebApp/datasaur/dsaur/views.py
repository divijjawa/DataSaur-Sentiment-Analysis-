from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import tweepy
import numpy as np
import json
import pandas as pd
import geocoder
from textblob import TextBlob
import json
from havenondemand.hodclient import *
from urllib.parse import unquote


import indicoio
indicoio.config.api_key = '99baa0441481dacdbb785ecd9c34f473'

# Initiate Haven OnDemand client
client = HODClient('53e8d89e-8b9d-4bd5-8ece-6a67fba081b7', version="v2")


#################twitter api
consumer_key = 'Tj1FDBq2tjo0b42oVDLkaPKhP'
consumer_secret = 'PSxSkisrZ1IhXu14ZMg0H2tLHWvek4aim5WbWP2xGAWLQShLLX'
access_token = '195347491-sSQ7QahfVDGuzVNH7qKy3n0ApECbo0HlBC0hqp2E'
access_token_secret = 'Tbd9aRVXQ6DMnyQjkUQTGyXOA32d7VFyKedcfpjTW6Hkf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
###########


def home(request):
    return render(request,'home.html')


def search(request,query):
    print("search")
    tweets = fetchtweets(query)

    return render(request, 'search.html',{'tweets':tweets,'query':query})

def heatsearch(request,query):
    print("search")
    tweets = fetchtweets(query)

    return render(request, 'heatmap.html',{'tweets':tweets,'query':query})


def trending(request):
    result = api.trends_place(23424775)         #canada 	23424775 , india 	23424848, usa 23424775
    data = result[0]['trends']
    return render(request,'trending.html', {'trends': data})


def trendDetail(request,query):
    print("query")
    print(query)
    return render(request,'trendDetail.html',{'query':query})


def trendtweets(request,query):
    print(query)
    tweets = []
    text = []
    for tweet in tweepy.Cursor(api.search, q=query + ' -RT', lang="en").items(100):
        jtweet = {}
        jtweet['created_at'] = tweet._json['created_at']
        jtweet['text'] = tweet._json['text']
        text.append(jtweet['text'])

        #params = {'text': jtweet['text']}

        #try:
            #analysis = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
            #sentiment = analysis['aggregate']['score']
        #except:
            #continue
        jtweet['location'] = tweet._json['user']['location']
        tweets.append(jtweet)

    print(len(tweets))
    analyze = indicoio.analyze_text(text, apis=[ 'people', 'places', 'organizations'], threshold=0.7)

    places = analyze['places']
    people = analyze['people']
    org = analyze['organizations']

    print(org)
    pl=[]
    ppl = []
    og = []

    for place in places:
        if len(place) != 0:
            pl.append(place[0]['text'])
    for p in people:
        if len(p) != 0:
            ppl.append(p[0]['text'])
    for o in org:
        if len(o) != 0:
            og.append(o[0]['text'])
    pl = list(set(pl))
    ppl = list(set(ppl))
    og = list(set(og))
    print(pl)
    print(ppl)
    print(og)

    return JsonResponse({'tweets':tweets,'people':ppl,'places':pl,'org':og})

def trendtone(request,query):
    print(query)
    print("trendtone")
    tweets = []
    emotion = {'fear':0,'sadness':0,'joy':0,'anger':0,'surprise':0}
    for tweet in tweepy.Cursor(api.search, q=query + ' -RT', lang="en").items(100):

        jtweet = {}
        jtweet['created_at'] = tweet._json['created_at']
        jtweet['text'] = tweet._json['text']
        #params = {'text': jtweet['text']}

        #try:
            #analysis = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
            #sentiment = analysis['aggregate']['score']
        #except:
            #continue
        ctweet = clean_tweet(jtweet['text'])
        if len(ctweet)!=0:
            emotions = indicoio.emotion(ctweet)

        emotion['fear'] += emotions['fear']
        emotion['surprise'] += emotions['surprise']
        emotion['sadness'] += emotions['sadness']
        emotion['anger'] += emotions['anger']
        emotion['joy'] += emotions['joy']

        jtweet['location'] = tweet._json['user']['location']

        tweets.append(jtweet)

    print(len(tweets))
    return JsonResponse({'tweets':tweets,'emotion':emotion})


def fetchtweets(query):
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=query + ' -RT', lang="en").items(150):
        location = tweet._json['user']['location']
        if len(location) != 0:
            jtweet = {}
            jtweet['created_at'] = tweet._json['created_at']
            jtweet['text'] = tweet._json['text']
            analysis = TextBlob((clean_tweet(jtweet['text'])))
            jtweet['sentiment'] = round(analysis.sentiment.polarity,1)
            jtweet['location'] = tweet._json['user']['location']
            tweets.append(jtweet)

    for tweet in tweets:
        g = geocoder.arcgis(tweet['location'])
        try:
            tweet['latitude'] = g.json['lat']
            tweet['longitude'] = g.json['lng']
        except:
            pass
    print(len(tweets))
    return tweets



import re

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
