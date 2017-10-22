from django.apps import AppConfig
import gmplot
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from random import uniform
import json
from twitter import OAuth, TwitterStream


class FetchTweetConfig(AppConfig):
    name = 'fetch_tweet'

    # def ready(self):
    #     ACCESS_TOKEN = ''
    #     ACCESS_SECRET = ''
    #     CONSUMER_KEY = ''
    #     CONSUMER_SECRET = ''
    #     oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    #
    #     twitter_stream = TwitterStream(auth=oauth)
    #
    #     iterator = twitter_stream.statuses.filter(track="pollution,LGBTQ,vegan,North Korea,Modi")
    #
    #     awsauth = AWS4Auth('', '', 'us-east-1', 'es')
    #
    #     host = 'search-tweet-store-gsxdukg3yfbejw5oabidx4wf5y.us-east-1.es.amazonaws.com'
    #
    #     es = Elasticsearch(
    #         hosts=[{'host': host, 'port': 443}],
    #         http_auth=awsauth,
    #         use_ssl=True,
    #         verify_certs=True,
    #         connection_class=RequestsHttpConnection,
    #         timeout=30
    #     )
    #
    #     if es.indices.exists(index="tweets"):
    #         print ("index tweets exists")
    #     else:
    #         es.indices.delete(index="tweets")
    #         request_body = {
    #             "settings": {
    #                 "index.mapping.total_fields.limit": 2000
    #             }
    #         }
    #         es.indices.create(index="tweets", body=request_body)
    #
    #     for tweet in iterator:
    #         document = json.dumps(tweet)
    #         try:
    #             es.index(index="tweets", doc_type="tweet", body=document)
    #         except Exception as e:
    #             print(e)


