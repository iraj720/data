import threading, time

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import pandas as pd

import json


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:29092')

        df = (
            pd.read_csv("wiki_movie_plots_deduped.csv")
            .dropna()
            .sample(100, random_state=42)
            .reset_index()
        )
        print("file is read")
        for i, row in df.iterrows():
            doc = {
                "title": row["Title"],
                "ethnicity": row["Origin/Ethnicity"],
                "director": row["Director"],
                "cast": row["Cast"],
                "genre": row["Genre"],
                "plot": row["Plot"],
                "year": row["Release Year"],
                "wiki_page": row["Wiki Page"]
            }
            user_encode_data = json.dumps(doc, indent=0).encode('utf-8')
            producer.send('test', user_encode_data)
           
        producer.flush()
        print("flushed")

        producer.close()


def run():
    try:
        admin = KafkaAdminClient(bootstrap_servers='localhost:29092')
        topic = NewTopic(name='test',
                    num_partitions=1,
                    replication_factor=1) 
        admin.create_topics([topic])
    except TopicAlreadyExistsError:
        pass
    except :
        raise
    
    while True :
        try:
            time.sleep(1)
            p = Producer()
            p.start()
            time.sleep(10) # 100 mins
        except:
            continue
        


if __name__ == "__main__":
    run()

