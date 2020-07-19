from mongoengine import *
                                                    # document, we create a
class Metadata(EmbeddedDocument):                   # class that inherits from
    tags = ListField(StringField())                 # Document.
    revisions = ListField(IntField())
                                                    # Fields are specified by
class Quote(Document):                              # adding field objects as
    quote = StringField()                           # class attributes to the
    author = StringField()                            # document class.
    metadata = EmbeddedDocumentField(Metadata)
