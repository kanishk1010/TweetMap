from random import uniform
from django.shortcuts import render
from elasticsearch import Elasticsearch, RequestsHttpConnection
from gmplot import gmplot
from requests_aws4auth import AWS4Auth
from bs4 import BeautifulSoup

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

def putkey(htmltxt, apikey, apistring=None):
    """put the apikey in the htmltxt and return soup"""
    if not apistring:
        apistring = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initialize&libraries=visualization&sensor=true_or_false"
    soup = BeautifulSoup(htmltxt, 'html.parser')
    soup.script.decompose() #remove the existing script tag
    body = soup.body
    src = apistring % (apikey,)
    tscript = soup.new_tag("script", src=src, async="defer")
    body.insert(-1, tscript)
    return soup

def generate_plot(keyword):
    gmap = gmplot.GoogleMapPlotter(0, 0, 1)
    res = es.search(index="tweets", doc_type="tweet", body={"query": {"match": {"text": keyword}}})
    print("Got %d Hits:" % res['hits']['total'])
    latitudes = []
    longitudes = []
    for hit in res['hits']['hits']:
        if hit["_source"]["coordinates"] is None:
            if hit["_source"]["user"]["location"] is not None:
                try:
                    lat, long = gmap.geocode(hit["_source"]["user"]["location"])
                except Exception:
                    lat, long = uniform(-90,90), uniform(-180,180)
            else:
                lat, long = uniform(-90,90), uniform(-180,180)
        else:
            lat, long = hit["_source"]["coordinates"]
        latitudes.append(lat)
        longitudes.append(long)
    gmap.scatter(latitudes, longitudes, 'k', marker=True)
    gmap.draw("./fetch_tweet/templates/map.html")
    htmltxt = open("./fetch_tweet/templates/map.html", 'r').read()
    soup = putkey(htmltxt, "AIzaSyAlZCLQckOd17qOFDVyFJk9TN8mIvH4zMs")
    newtxt = soup.prettify()
    open("./fetch_tweet/templates/map.html", 'w').write(newtxt)
    print('\nKey Insertion Completed!!')


def index(request):
    return render(request, 'index.html', {})


def pollution(request):
    generate_plot("pollution")
    return render(request, 'map.html', {})


def vegan(request):
    generate_plot("vegan")
    return render(request, 'map.html', {})


def nk(request):
    generate_plot("North Korea")
    return render(request, 'map.html', {})


def modi(request):
    generate_plot("Modi")
    return render(request, 'map.html', {})


def lgbtq(request):
    generate_plot("lgbtq")
    return render(request, 'map.html', {})

