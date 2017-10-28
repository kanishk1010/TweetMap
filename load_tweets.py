import json
from twitter import OAuth, TwitterStream
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import time

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
iterator = twitter_stream.statuses.filter(track="pollution,LGBTQ,vegan,North Korea, Modi")
awsauth = AWS4Auth('', '', 'us-east-1', 'es')
host = 'search-tweet-store-gsxdukg3yfbejw5oabidx4wf5y.us-east-1.es.amazonaws.com'
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)

index_exists = None
while index_exists is None:
    try:
        index_exists = es.indices.exists(index="tweets")
    except Exception:
        time.sleep(30)

if index_exists:
    print("index tweets exists")
else:
    request_body = {
        "settings": {
            "index.mapping.total_fields.limit": 2000
        }
    }
    index_response = None

    while index_response is None:
        try:
            index_response = es.indices.create(index="test", body=request_body)
        except Exception:
            time.sleep(30)

for tweet in iterator:
    document = json.dumps(tweet)
    try:
        es.index(index="tweets", doc_type="tweet", body=document)
    except Exception as e:
        print(e)
        time.sleep(30)
