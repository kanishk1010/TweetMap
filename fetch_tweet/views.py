from random import uniform
from django.shortcuts import render
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAlZCLQckOd17qOFDVyFJk9TN8mIvH4zMs')
awsauth = AWS4Auth('AKIAIW4WGIXUESC3K4SQ', 'kiX8y+gNAHeduKXd8tURF1H3w1hRQ99bUIFw4axy', 'us-east-1', 'es')
host = 'search-tweet-store-gsxdukg3yfbejw5oabidx4wf5y.us-east-1.es.amazonaws.com'
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)
es.indices.refresh(index="tweets")


def generate_plot(keyword, s=1000, geocode=False, random=False):
    res = es.search(index="tweets", doc_type="tweet", size=s, body={"query": {"match": {"text": keyword}}})
    print("Got %d Hits:" % res['hits']['total'])
    tweet_list = []
    for hit in res['hits']['hits']:
        tweet = hit["_source"]["text"][:100].replace('\n', ' ').replace('\r', '')
        if hit["_source"]["coordinates"] is None:
            if hit["_source"]["user"]["location"] and geocode:
                try:
                    geocode_result = gmaps.geocode(hit["_source"]["user"]["location"])
                    lat = geocode_result[0]['geometry']['location']['lat']
                    long = geocode_result[0]['geometry']['location']['lng']
                except Exception as e:
                    print(e)
                    if random:
                        lat, long = uniform(-90,90), uniform(-180,180)
                    else:
                        continue
            elif random:
                lat, long = uniform(-90, 90), uniform(-180, 180)
            else:
                continue
        else:
            long, lat = hit["_source"]["coordinates"]["coordinates"]
        tweet_list.append({"latlng": {"lat": lat, "lng": long}, "tweet": tweet})
    return {'tweets': tweet_list}


def index(request):
    return render(request, 'fetch_tweet/index.html', {'coordinates': []})


def search(request, keyword, size, geocode, random):
    parse_geocode = {0: False, 1: True}
    parse_random = {0: False, 1: True}
    print(size, geocode, random)
    context = generate_plot(keyword, s=int(size), geocode=parse_geocode[int(geocode)], random=parse_random[int(random)])
    print(len(context['tweets']))
    return render(request, 'fetch_tweet/index.html', context)
