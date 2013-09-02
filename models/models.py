from google.appengine.ext import ndb

class UserAuditTrail(ndb.Model):
    user_code = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class AgentAuditTrail(ndb.Model):
    agent_code = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class User(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    level = ndb.IntegerProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Agent(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Attendant(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Customer(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()