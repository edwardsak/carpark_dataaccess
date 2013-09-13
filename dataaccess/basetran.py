from google.appengine.ext import ndb

class BaseTranDataAccess():
    """ return ndb key for transaction such as Buy, Deposit, etc.
    person_kind = Agent or Attendant
    person_code = agent_code or attendant_code
    """
    def __get_key(self, kind, tran_date, person_kind, person_code=None, tran_code=None):
        date_code = tran_date.strftime('%Y%m%d')
        
        key = None
        if person_code is None:
            key = ndb.Key(kind, date_code)
        else:
            if tran_code is None:
                key = ndb.Key(
                              kind, date_code, 
                              person_kind, person_code
                              )
            else:
                key = ndb.Key(
                              kind, date_code, 
                              person_kind, person_code,
                              kind, tran_code
                              )
            
        return key