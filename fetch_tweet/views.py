from random import uniform
from django.shortcuts import render
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import googlemaps

gmaps = googlemaps.Client(key='')
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
es.indices.refresh(index="tweets")


def generate_plot(keyword):
    res = es.search(index="tweets", doc_type="tweet", size=100, body={"query": {"match": {"text": keyword}}})
    print("Got %d Hits:" % res['hits']['total'])
    coordinates = []
    for hit in res['hits']['hits']:
        if hit["_source"]["coordinates"] is None:
            if hit["_source"]["user"]["location"]:
                try:
                    geocode_result = gmaps.geocode(hit["_source"]["user"]["location"])
                    lat = geocode_result[0]['geometry']['location']['lat']
                    long = geocode_result[0]['geometry']['location']['lng']
                except Exception:
                    lat, long = uniform(-90,90), uniform(-180,180)
            else:
                lat, long = uniform(-90,90), uniform(-180,180)
        else:
            long, lat = hit["_source"]["coordinates"]["coordinates"]
        coordinates.append({"lat": lat, "lng": long})
        print(lat,long)
    return coordinates


def index(request):
    return render(request, 'fetch_tweet/index.html', {'coordinates': []})


def search(request, keyword):
    context = generate_plot(keyword)
    print(len(context))
    return render(request, 'fetch_tweet/index.html', {'coordinates': context})


