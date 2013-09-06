from datalayer.models.models import AgentAuditTrail

from sharelib.utils import DateTime

class AgentAuditTrailDataAccess():
    def create(self, code, action, message):
        audit = AgentAuditTrail()
        audit.agent_code = code
        audit.date = DateTime.malaysia_now()
        audit.action = action
        audit.message = message
        audit.put()