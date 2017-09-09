import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class Twitter_User(object):

	def __init__(self):
		consumer_key='FM3nYXvUHxxxxxxxxxxxxxxxb'
		consumer_secret='8LXbtMybMsEZe0Bz3OoWvIzK4crV9HVZxxxxxxxxxxxxxxx'
		access_token='4834720380xxxxxxxxxxxxxxxxxxxxxxxxxxxxCSACLUtnMlOte1zBxUo8a'
		access_secret='lZd7RiVbY3xxxxxxxxxxxxxxxxxxxxxxxxxwmQGWO'


       # You will need consumer_key, consumer_secret,access_token,access_secret to use twitter API
       # To get the above mentioned details you must sign up for aps.twitter.com        


		try:
			self.auth=OAuthHandler(consumer_key,consumer_secret)
			self.auth.set_access_token(access_token,access_secret)
			self.api=tweepy.API(self.auth)
		except:
			print("Authentication Failed")

    #This function is used to clean the tweet i.e to remove the links, special characters etc...
	def clean_tweet(self,tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)"," ",tweet).split())



    #This function is used to analyze the tweet and calculate its polarity
    #You don't have to do much the textblob library do all the work for you.

	def get_tweet_sentiment(self,tweet):
		analysis=TextBlob(self.clean_tweet(tweet))
		if analysis.sentiment.polarity>0:
			return 'positive'
		elif analysis.sentiment.polarity==0:
			return 'neutral'
		else:
			return 'negative'

    #To fetch the tweets using tweepy API
	def get_tweets(self,query,count=20):
		tweets=[]
		try:
			fetched_tweets=self.api.search(q=query,count=count)
			for tweet in fetched_tweets:
				parsed_current_tweet={}
				parsed_current_tweet['text']=tweet.text
				parsed_current_tweet['sentiment']=self.get_tweet_sentiment(tweet.text)

				if tweet.retweet_count>0:
					if parsed_current_tweet not in tweets:
						tweets.append(parsed_current_tweet)
				else:
					tweets.append(parsed_current_tweet)
			return tweets
		except tweepy.TweepError as e:
			print("Error: " %(e))


def main():
	print("\nEnter the name for sentiment analysis: \n")
	query=input()
	user=Twitter_User()
	tweets=user.get_tweets(query=query,count=10)
	ptweets=[tweet for tweet in tweets if tweet['sentiment']=='positive']
	print("Positive Tweets percentage: {}%".format(100*len(ptweets)/len(tweets)))
	ntweets=[tweet for tweet in tweets if tweet['sentiment']=='negative']
	print("Negative Tweets percentage: {}%".format(100*len(ntweets)/len(tweets)))
	print("Neutral  Tweets percentage: {}%".format(100*len(tweets-ptweets-ntweets)/len(tweets)))
	print("\n\n")
	print("\nPositive Tweets: ")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	print("\n\nNegative Tweets: ")
	for tweet in ntweetss[:10]:
		print(tweet['text'])

if __name__=="__main__":
	main()

