from datalayer.models.models import Tag

from google.appengine.ext import ndb

class TagDataAccess():
    def get(self, code):
        return Tag.query(ancestor=ndb.Key('Tag', code)).get()
    
    def create(self, vm):
        # validate id
        data_validate = self.get(vm.code)
        if data_validate != None:
            raise Exception('Tag ID already exist.')
        
        data = Tag(id=vm.code)
        data.code = vm.code
        data.agent_code = ''
        data.agent = None
        data.car_reg_no = ''
        data.car = None
        data.active = True
        data.put()
        
        return data
        
    def update_agent_code(self, vm):
        # get data
        data = self.get(vm.code)
        if data == None:
            raise Exception('Tag not found.')
        
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.put()
        
        return data
    
    def update_car_reg_no(self, vm):
        # get data
        data = self.get(vm.code)
        if data == None:
            raise Exception('Tag not found.')
        
        data.car_reg_no = vm.car_reg_no
        data.car = vm.car.key
        data.put()
        
        return data
    
    @ndb.transactional(xg=True)
    def save_register(self, vm):
        tag = self.get(vm.code)
        if tag:
            # update tag car reg no
            tag.car_reg_no = vm.car_reg_no
            tag.car = vm.car.key
            tag.put()
        else:
            # create tag
            tag = self.__demo_create_register(vm)
            
        return tag
    
    
    def demo_save_register(self, vm):
        tag = self.get(vm.code)
        if tag:
            raise Exception('Tag ID already registered.')
        else:
            # create tag
            tag = self.__demo_create_register(vm)
            
        return tag
    
    def __demo_create_register(self, vm):
        # validate id
        data_validate = self.get(vm.code)
        if data_validate != None:
            raise Exception('Tag ID already exist.')
        
        data = Tag(id=vm.code)
        data.code = vm.code
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.car_reg_no = vm.car_reg_no
        data.car = vm.car.key
        data.active = True
        data.last_modified = ''
        data.put()
        
        return data