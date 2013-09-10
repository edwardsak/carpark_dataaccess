from datalayer.models.models import CustomerAuditTrail

from sharelib.utils import DateTime

class CustomerAuditTrailDataAccess():
    def create(self, ic, action, message):
        audit = CustomerAuditTrail()
        audit.ic = ic
        audit.date = DateTime.malaysia_now()
        audit.action = action
        audit.message = message
        audit.put()