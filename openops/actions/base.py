class Action:
 name=''
 rollback_supported=False
 def validate(self,payload): return None
 def plan(self,payload): return {'action':self.name,'target':payload.get('target'),'rollback_supported':self.rollback_supported,'side_effects':[]}
 def execute(self,payload): raise NotImplementedError
 def compensate(self,payload): raise NotImplementedError
