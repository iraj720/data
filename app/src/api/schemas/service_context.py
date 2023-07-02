from marshmallow import Schema, fields


class IndexResult:
    hits = {}
    name = fields.String()
    title = fields.String()
    ethnicity = fields.String()
    director = fields.String()
    cast = fields.String()
    genre = fields.String()
    plot = fields.String()
    year = fields.Int()
    wiki_page = fields.String()

class ServiceContextSchema(Schema):
    id : int
    tag_id : int

class SearchRequest(Schema):
    index=fields.String()
    title=fields.String()
    cast=fields.String()
    wiki_page=fields.String()
    director=fields.String()
    genre=fields.String()
    plot=fields.String()
    year=fields.Int()
    ethnicity=fields.String()


