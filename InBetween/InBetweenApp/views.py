from django.shortcuts import render

from InBetweenApp.forms import LocationAForm, LocationBForm, KeywordForm
import requests
import math


API_KEY = 'AIzaSyCDV8b-Ht-AF1LWYjydiKmdWL9KQbygYkc'
# Create your views here.
def index(request):
    if request.method == 'POST':
        formA = LocationAForm(request.POST)
        formB = LocationBForm(request.POST)
        formKey = KeywordForm(request.POST)


        if formA.is_valid() and formB.is_valid() and formKey.is_valid():
            loc_a = formA.cleaned_data['loc_a']
            loc_b = formB.cleaned_data['loc_b']
            keyword = formKey.cleaned_data['keyword']


            locationA = loc_a
            locationB = loc_b

             # create RESTful URL from two locations
            payload = {'origin':locationA, 'destination':locationB, 'key':API_KEY}
            url = 'https://maps.googleapis.com/maps/api/directions/json?'

            # get response from Google Maps Directions API
            search_res = requests.get(url, params=payload)
            search_res.raise_for_status()


            # convert Google response to JSON
            json_result = search_res.json()

            total_distance = json_result['routes'][0]['legs'][0]['distance']['value']
            half_distance = total_distance/2

            steps = get_steps(json_result)
            middle = get_midpoint(half_distance, steps)

            data = get_data(keyword, middle)
            places = get_places(data)


            return render(request, 'mapped.html', {
            'formA': formA,
            'formB': formB,
            'formKey': formKey,
            'loc_a': loc_a,
            'loc_b': loc_b,
            'middle': middle,
            'keyword': keyword,
            'places': places
        })
    else:
        formA = LocationAForm()
        formB = LocationBForm()
        formKey = KeywordForm()
        return render(request, 'index.html',{
            'formA': formA,
            'formB': formB,
            'formKey': formKey,
            'places': (10,30)
        })





def get_steps(jsonr):
    """Get the steps (distance in meters, startpoint lat&lng, endpoint lat&lng) along route"""
    steps = []
    for step in jsonr['routes'][0]['legs'][0]['steps']:
        steps.append([step['distance']['value'], step['start_location'], step['end_location']])
    return steps

def get_midpoint(half_distance: int, steps: [(int, str, str)]) -> (str, str):
    """Get the latitude and longitude of best approximating midpoint between two locations"""
    cur_distance = 0
    cur_step = 0
    while(cur_distance + steps[cur_step][0] <= half_distance):
        cur_distance += steps[cur_step][0]
        cur_step += 1

    left_over_distance = half_distance - cur_distance

    # lat, lng
    startpos = (steps[cur_step][1]['lat'],steps[cur_step][1]['lng'])
    endpos = (steps[cur_step][2]['lat'],steps[cur_step][2]['lng'])
    lat_length = endpos[0] - startpos[0]
    lng_length = endpos[1] - startpos[1]

    angle = math.atan(lng_length/lat_length)

    if (endpos[0] > startpos[0] and endpos[1] > startpos[1]) or \
       (endpos[0] < startpos[0] and endpos[1] > startpos[1]):
        return (startpos[0]+left_over_distance*math.cos(angle)/111000, startpos[1]+left_over_distance*math.sin(angle)/111000)
    return (startpos[0]-left_over_distance*math.cos(angle)/111000, startpos[1]-left_over_distance*math.sin(angle)/111000)


def get_data(search, midpoint):
    url = 'https://api.foursquare.com/v2/venues/explore'

    query = search
    cur_location = str(midpoint)[1:-1]

    params = dict(
        client_id='G15NBKKGLQULJQJ40W2IIW4KNK2YYO23ULFTQI5QSW1DDISP',
        client_secret='OOPKKSDWURQS0R1E5RY3C34OE0DJVTEUSQTRWO1MJDLS0IYF',
        v='20180331',
        ll=cur_location,
        query=query,
        limit=5
    )

    resp = requests.get(url=url, params=params)
    data = resp.json()

    return data


def get_places(data):
    places = []
    for item in data['response']['groups'][0]['items']:
        address = ' '.join(item['venue']['location']['formattedAddress'])
        places.append(address)
    return places
