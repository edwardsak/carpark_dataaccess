from datalayer.models.models import SystemSetting

from google.appengine.ext import ndb

class SystemSettingDataAccess():
    def get_key(self, key):
        return ndb.Key('SystemSetting', key)
    
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        sys = SystemSetting()
        sys.tag_sell_price = vm.tag_sell_price
        sys.user_access_lock = False
        sys.agent_access_lock = False
        sys.attendant_access_lock = False
        sys.customer_access_lock = False
        sys.announcement = ''
        sys.put()
        
    def update(self, vm):
        sys = SystemSetting.query().get()
        sys.tag_sell_price = vm.tag_sell_price
        sys.user_access_lock = vm.user_access_lock
        sys.agent_access_lock = vm.agent_access_lock
        sys.attendant_access_lock = vm.attendant_access_lock
        sys.customer_access_lock = vm.customer_access_lock
        sys.announcement = vm.announcement
        sys.put()