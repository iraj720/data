from src.infrastructure.models import ElasticModel
from src.config import Config

from elasticsearch import Elasticsearch
es = Elasticsearch(Config.ELASTIC_CONN)


class ElasticService:

    def update(self, data):
        return ElasticModel()

    def get(self, index, query):
            
        # we can search with all of its fields and even expose the json for user
        # to be able to use DSL directly
        resp = es.search(
            index="movies",
            query={"bool": {
                "should": [
                    {
                        "match_phrase": {
                            "title": query["title"],
                        },
                    },
                    {
                        "match_phrase": {
                            "wiki_page": query["wiki_page"],
                        },
                    }
                ],
                    "minimum_should_match" : 1
                },
            }
        )
        # also we can use ElasticModel which would be better for real project
        return resp.body["hits"]

# mappings = {
#         "properties": {
#             "title": {"type": "text", "analyzer": "english"},
#             "ethnicity": {"type": "text", "analyzer": "standard"},
#             "director": {"type": "text", "analyzer": "standard"},
#             "cast": {"type": "text", "analyzer": "standard"},
#             "genre": {"type": "text", "analyzer": "standard"},
#             "plot": {"type": "text", "analyzer": "english"},
#             "year": {"type": "integer"},
#             "wiki_page": {"type": "keyword"}
#     }
# }

# query example : 

# {
#                     "bool": {
#                         "must": {
#                             "match_phrase": {
#                                 "cast": "jack nicholson",
#                             }
#                         },
#                         "filter": {"bool": {"must_not": {"match_phrase": {"director": "roman polanski"}}}},
#                     },
#                 },