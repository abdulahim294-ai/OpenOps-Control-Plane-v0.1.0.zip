from .base import Action
class RecordEvent(Action):
 name='record-event'; rollback_supported=True
 def plan(self,p): return {**super().plan(p),'side_effects':['append a local event record']}
 def execute(self,p): return {'status':'recorded','event':p.get('event','demo')}
 def compensate(self,p): return {'status':'compensated'}
class SendNotification(Action):
 name='send-notification'; rollback_supported=False
 def plan(self,p): return {**super().plan(p),'side_effects':['simulate an outbound notification']}
 def execute(self,p):
  if p.get('force_failure'): raise RuntimeError('simulated action failure')
  return {'status':'sent','destination':p.get('destination','demo@example.invalid')}
class CreateTicket(Action):
 name='create-ticket'; rollback_supported=True
 def plan(self,p): return {**super().plan(p),'side_effects':['create a deterministic local ticket record']}
 def execute(self,p): return {'status':'created','ticket_id':p.get('ticket_id','T-DEMO')}
 def compensate(self,p): return {'status':'closed'}
class DeploymentSimulation(Action):
 name='deployment-simulation'; rollback_supported=False
 def plan(self,p): return {**super().plan(p),'side_effects':['simulate a deployment; no external system is contacted']}
 def execute(self,p): return {'status':'simulated','service':p.get('service','service-a')}
ACTIONS={x.name:x() for x in [RecordEvent,SendNotification,CreateTicket,DeploymentSimulation]}
