import feedparser
import csv
import pandas as pd
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def extragere(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
#creare rss feed pentru fiecare an/luna incepand cu 2012-2021
    an = 2012
    luna = 1
    datiDeParcurs = []
    for i in range(2012, 2021):
        for j in range(1,13):
            if j < 10:
                datiDeParcurs.append(str(i)+"0"+str(j))
            else:
                datiDeParcurs.append(str(i)+str(j)) 

#creez csv-ul in care scriu categoriile de care am nevoie

    with open('/tmp/new2.csv','w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Titlu","Descriere",'Categorie'])

    for i in datiDeParcurs:
        url = 'http://avizier.upt.ro/?m=' + str(i) + '&feed=rss2'
        d = feedparser.parse(url)
        if d.status == 200:
            for post in d.entries:
                with open('/tmp/new2.csv', 'a', encoding="utf-8", newline='') as csvfile:
                    print("TITLU:", post.title, ", ", "DESCRIERE: ", post.description, ",", "CATEGORIE: ", post.category)
                    writer = csv.writer(csvfile)
                    writer.writerow([post.title, post.description, post.category])
    
    upload_blob('rss-avizier-upt', '/tmp/new2.csv', 'RSS-data.csv')

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Success!'
