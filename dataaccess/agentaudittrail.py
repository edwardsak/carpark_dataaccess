from datalayer.models.models import AgentAuditTrail

from datetime import datetime 

class AgentAuditTrailDataAccess():
    def create(self, code, action, message):
        audit = AgentAuditTrail()
        audit.user_id = code
        audit.date = datetime.now()
        audit.action = action
        audit.message = message
        audit.put()