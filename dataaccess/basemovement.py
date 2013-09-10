from google.appengine.ext import ndb

class BaseMovement():
    def __get_key(self, kind, movement_date, person_kind, person_code=None, movement_code=None):
        date_code = movement_date.strftime('%Y%m%d')
        
        key = None
        if person_code is None:
            key = ndb.Key(kind, date_code)
        else:
            if movement_code is None:
                key = ndb.Key(
                              kind, date_code, 
                              person_kind, person_code
                              )
            else:
                key = ndb.Key(
                              kind, date_code, 
                              person_kind, person_code,
                              kind, movement_code
                              )
            
        return key