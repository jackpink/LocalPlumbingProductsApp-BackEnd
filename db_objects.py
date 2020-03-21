from mongoengine import connect, Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField

# Objects for ORM to MongoDB Database


class PhotoLink(EmbeddedDocument):
    Photo = IntField(required=True, primary_key=True)
    Link = StringField(required=True)

    def __init__(self, *args, **kwargs):
        super(PhotoLink, self).__init__(*args, **kwargs)

    '''def to_dict(self):
        return {'photo': self.Photo,
                'link': self.Link}'''


class Specification(EmbeddedDocument):
    Spec = StringField(required=True)
    Value = StringField(required=True)

    def __init__(self, *args, **kwargs):
        super(Specification, self).__init__(*args, **kwargs)


class Product(Document):
    id = IntField(required=True, primary_key=True)
    Name = StringField(required=True)
    Photos = ListField(StringField(required=True))
    Summary = StringField()
    Specifications = EmbeddedDocumentListField(Specification)
    Product = StringField()

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

    def to_dict(self):
        r = {
            'id' : self.id,
            'Name' : self.Name,
            'Summary' : self.Summary,
            'Photos' : self.Photos
        }



