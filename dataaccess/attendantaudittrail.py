from datalayer.models.models import AttendantAuditTrail

from datetime import datetime 

class AttendantAuditTrailDataAccess():
    def create(self, code, action, message):
        audit = AttendantAuditTrail()
        audit.attendant_code = code
        audit.date = datetime.now()
        audit.action = action
        audit.message = message
        audit.put()