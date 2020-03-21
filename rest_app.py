from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
import time
import urllib.request
from bs4 import BeautifulSoup
from web_scrapping import get_photo_links, get_summary, get_spec, get_name, get_product_id, get_product_links
from mongoengine import *
from db_objects import *



# Setup Flask Application
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

PUBLICATION_PORT = 9876

# Setup Connection to MongoDB
connect('ReeceCatalogueApp_test', host='localhost', port=27017)


##############################################################################################################################
##############################################################################################################################
# All POST Methods
##############################################################################################################################
##############################################################################################################################


@app.route('/database', methods=['POST'])
def create_database():
    # Web scrap Reece website to get all info for all products


    #       get_warranty(soup)

    return 'Hello, World!'


@app.route('/database/toilet_suites', methods=['POST'])
def replace_toilet_suites_in_db():
    # Get all page links for all Toilet Suites
    link = 'https://www.reece.com.au/search/toilets-c469/toilet-suites-c705'

    # Get all individual page links
    links = get_product_links(link)
    count=0

    # Loop through all links
    for link_tail in links:
        time.sleep(1)
        page = requests.get('https://www.reece.com.au'+link_tail)

        soup = BeautifulSoup(page.content, 'html.parser')

        product_id = get_product_id(soup)
        name = get_name(soup)

        # Create Toilet Suite object to add to DB

        toilet_suite_object = Product(Name=name, id=product_id, Product='toilet_suite')

        photo_links = get_photo_links(soup)
        for i in range(len(photo_links)):
            #pl = PhotoLink(Photo=i+1, Link=photo_links[i])
            toilet_suite_object.Photos.append(photo_links[i])

        # for link in photo_links:
        # get_photo(link)

        summary = get_summary(soup)
        toilet_suite_object.Summary = summary

        specs = get_spec(soup)
        for spec in specs:
            spec_object = Specification(Spec=spec[0], Value=spec[1])
            toilet_suite_object.Specifications.append(spec_object)

        #print(ts.Specifications[0])

        toilet_suite_object.save()
        count += 1
        print(count)

    return 'Toilet Suites updated in database', 200


##############################################################################################################################
##############################################################################################################################
# All GET Methods
##############################################################################################################################
##############################################################################################################################


@app.route('/database/toilet_suites', methods=['GET'])
@cross_origin()
def get_toilet_suites_in_db():
    # Get all Toilet Suites from Database
    toilet_suites = []

    for toilet in Product.objects:
        toilet_suites.append(toilet.to_json())

    results = {'results': toilet_suites}

    return results, 200


@app.route('/database/toilet_suites/<id>', methods=['GET'])
@cross_origin()
def get_toilet_suites_in_db_with_id(id):
    # Get Toilet Suite with this id from Database
    toilet = Product.objects(id=id)
    print(toilet.to_json())
    return toilet.to_json(), 200


if __name__ == '__main__':
    app.run(debug=True,port=PUBLICATION_PORT)