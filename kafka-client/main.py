#!/usr/bin/env python
import threading, time

from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import ast

es = Elasticsearch("http://localhost:9200")
print("connected")

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:29092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['test'])
        mappings = {
                "properties": {
                    "title": {"type": "text", "analyzer": "english"},
                    "ethnicity": {"type": "text", "analyzer": "standard"},
                    "director": {"type": "text", "analyzer": "standard"},
                    "cast": {"type": "text", "analyzer": "standard"},
                    "genre": {"type": "text", "analyzer": "standard"},
                    "plot": {"type": "text", "analyzer": "english"},
                    "year": {"type": "integer"},
                    "wiki_page": {"type": "keyword"}
            }
        }
        try :
            es.indices.create(index="movies", mappings=mappings)
            print("index mappings created")
        except: 
            pass
        while not self.stop_event.is_set():
            for message in consumer:
                print("recieved")
                dict_str = message.value.decode("UTF-8")
                mydata = ast.literal_eval(dict_str)
                print(mydata)
                es.index(index="movies", document=mydata)
                print("sent to elastic")
                if self.stop_event.is_set():
                    break

        consumer.close()


def main():
    c = Consumer()
    c.start()
    while c.is_alive():
        time.sleep(1)



if __name__ == "__main__":
    main()