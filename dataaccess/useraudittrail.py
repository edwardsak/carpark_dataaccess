from datalayer.models.models import UserAuditTrail

from datetime import datetime 

class UserAuditTrailDataAccess():
    def create(self, code, action, message):
        audit = UserAuditTrail()
        audit.user_code = code
        audit.date = datetime.now()
        audit.action = action
        audit.message = message
        audit.put()