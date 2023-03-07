from pymongo import MongoClient
import pymongo
import json
import os.path
import subprocess

client =None
db = None
collection = None

def connect_server(port):
    global client, db, collection

    ''' connect to port on lovalhost for the mongodb server'''
    client_str = 'mongodb://localhost:'+port
    client = MongoClient(client_str)

def construct_db():
    global client, db, collection

    ''' open or create the 291db database on server'''
    db = client["291db"]
  
def create_collection(json_file,port):
    global client, db, collection

    collist = db.list_collection_names()
    if "dblp" in collist:
        db["dblp"].drop()
    # if "venue_with_ref" in collist:
    #     db["venue_with_ref"].drop()

    collection = db["dblp"]

    # load json
    #  mongoimport --port 27045 --db 291db --collection dblp --drop --batchSize 10000 --file data1m.json
    process = subprocess.Popen(['mongoimport', '--port',port,'--db','291db','--collection','dblp','--drop','--batchSize','10000','--file',json_file],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    subprocess.check_output("ls non_existent_file; exit 0", stderr=subprocess.STDOUT,shell=True)
    collection.update_many({}, [{"$set":{"str_year":{"$toString": "$year"}}}]) 
    #collection.aggregate([{"$addFields": {"str_year": {"$toString": "$year"}}}]) #can not create a field

    collection.create_index([("abstract",pymongo.TEXT),("title",pymongo.TEXT),("venue",pymongo.TEXT),("authors",pymongo.TEXT),("str_year",pymongo.TEXT)],default_language='none')
    collection.create_index([("id",1)])
    collection.create_index([("id","hashed")])
    collection.create_index([("references",1)])
    collection.create_index([("id",1),("references",1)])
    collection.create_index([("year",1)])
    collection.create_index([("venue",1),("references",1)])
    collection.create_index([("number_of_refs",-1)])


def main():
    global client, db, collection

    json_file = input("Please enter the name of the json file: ").strip()
    while (len(json_file)==0) or os.path.isfile(json_file) == False:
        json_file = input("Please enter a valid json file: ").strip()
    port = input("Please enter the port number: ").strip()
    while(len(port)==0 or port.isdigit() == False):
        port = input("Please enter a valid port number: ").strip()

    connect_server(port)
    construct_db()
    create_collection(json_file,port)

main()