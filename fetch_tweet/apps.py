from django.apps import AppConfig
import gmplot
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from random import uniform
import json
from twitter import OAuth, TwitterStream


class FetchTweetConfig(AppConfig):
    name = 'fetch_tweet'

