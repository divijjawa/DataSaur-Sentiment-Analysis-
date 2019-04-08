
import geocoder
# Create your tests here.



from textblob import TextBlob
import tweepy

consumer_key = 'Tj1FDBq2tjo0b42oVDLkaPKhP'
consumer_secret = 'PSxSkisrZ1IhXu14ZMg0H2tLHWvek4aim5WbWP2xGAWLQShLLX'
access_token = '195347491-sSQ7QahfVDGuzVNH7qKy3n0ApECbo0HlBC0hqp2E'
access_token_secret = 'Tbd9aRVXQ6DMnyQjkUQTGyXOA32d7VFyKedcfpjTW6Hkf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)




# 45.797095;15.982453;hr;Europe/Belgrade

tweets = []
locations = []
for tweet in tweepy.Cursor(api.search, q='trump' + ' -RT', lang="en").items(200):
    location = tweet._json['user']['location']
    if len(location) != 0:
        jtweet = {}
        jtweet['created_at'] = tweet._json['created_at']
        jtweet['text'] = tweet._json['text']
        analysis = TextBlob((jtweet['text']))
        jtweet['sentiment'] = round(analysis.sentiment.polarity,1)
        jtweet['location'] = tweet._json['user']['location']
        locations.append(jtweet['location'])
        tweets.append(jtweet)
print(len(tweets))

#for location in locations:
    #print(type(location))

g = geocoder.mapquest(locations,method='batch')
print(g)





