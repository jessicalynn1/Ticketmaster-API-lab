from flask import Flask, render_template, request

from pprint import pformat, pprint
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

# https://developer-acct.ticketmaster.com/user/register
# Do this in your venv, and then you should be able to use it.
# export TICKETMASTER_KEY="Jess' secret!"

"""
events = data['_embedded']['events']
data = {'_embedded': {'events': [list o'events.....]}}
events = [list o'events.....]
events[0] = {the_first_event dict with keys like 'name', 'type', 'id', 'test', 'url', 'locale', 'images', 'sales', 'dates', 'classifications', 'outlets', 'seatmap', '_links', '_embedded'}
"""






API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}

    payload['keyword'] = keyword
    # payload = {'apikey': '8uh4r8uhrf8yruh', 'keyword': "ABBA"}
    payload['postalcode'] = postalcode
    payload['radius'] = radius
    payload['unit'] = unit
    payload['sort'] = sort

    # Another way to fill our dictionary:
    # payload = {'apikey': API_KEY, 'keyword': keyword, 'postalcode': postalcode, 'radius': radius, 'unit': unit, 'sort': sort}

    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # + Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    # https://fellowship.hackbrightacademy.com/materials/serpt5/exercises/apis/
    # Section: Get Familiar with Requests

    res = requests.get(url, params=payload)
    # res comes back as a json string.
    # print(res)  # <Response [200]>
    

    data =  res.json()
    pprint(data)
    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function

    # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#event-details-v2

    # /discovery/v2/events/{id}
    
    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}
    payload['id'] = id

    res = requests.get(url, params=payload)

    data =  res.json()
    pprint(data)
    eventname = data['_embedded']['events'][0]['name']
    description = data['_embedded']['events'][0].get('info', "No description found.")

    # eventname = "Jess is awesome party"
    return render_template('event-details.html',
                            EVENTNAME=eventname,
                            description=description)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
