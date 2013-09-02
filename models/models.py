from google.appengine.ext import ndb

class User(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()