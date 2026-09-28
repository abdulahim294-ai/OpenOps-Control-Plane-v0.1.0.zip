from openops.domain import *
from openops.policy.engine import PolicyEngine
from openops.risk.engine import RiskEngine
from openops.actions.builtin import ACTIONS
class OpenOps:
 transitions={State.RECEIVED:{State.VALIDATING},State.VALIDATING:{State.POLICY_CHECK,State.BLOCKED},State.POLICY_CHECK:{State.RISK_ASSESSMENT,State.BLOCKED},State.RISK_ASSESSMENT:{State.AWAITING_APPROVAL,State.APPROVED,State.BLOCKED},State.AWAITING_APPROVAL:{State.APPROVED,State.REJECTED,State.EXPIRED,State.CANCELLED},State.APPROVED:{State.EXECUTING},State.EXECUTING:{State.SUCCEEDED,State.FAILED,State.TIMED_OUT},State.FAILED:{State.EXECUTING,State.CANCELLED}}
 def __init__(self,store): self.store=store; self.policy=PolicyEngine(); self.risk=RiskEngine()
 def event(self,e,event,actor='system',meta=None): self.store.audit(e['id'],event,actor,now(),meta or {})
 def transition(self,e,to):
  if State(e['state']) not in self.transitions or to not in self.transitions[State(e['state'])]: raise ValueError(f'illegal transition {e["state"]} -> {to.value}')
  e['state']=to.value; e['updated_at']=now()
 def create(self,r,dry=False):
  existing=self.store.get_by_key(r.idempotency_key)
  if existing: self.event(existing,'IDEMPOTENCY_REPLAY',r.actor,{'idempotency_key':r.idempotency_key}); return existing,True
  e=Execution(actor=r.actor,action=r.action,payload=r.payload,correlation_id=r.correlation_id,idempotency_key=r.idempotency_key).json()
  try: self.store.save(e)
  except Exception:
   existing=self.store.get_by_key(r.idempotency_key)
   if existing:
    self.event(existing,'IDEMPOTENCY_REPLAY',r.actor,{'idempotency_key':r.idempotency_key,'concurrent':True}); return existing,True
   raise
  self.event(e,'REQUEST_RECEIVED',r.actor)
  self.transition(e,State.VALIDATING); self.event(e,'VALIDATED',r.actor)
  p=self.policy.evaluate(r); e['policy']=p.__dict__; self.transition(e,State.POLICY_CHECK); self.event(e,'POLICY_EVALUATED',r.actor,p.__dict__)
  if not p.allowed: self.transition(e,State.BLOCKED); self.store.update(e); return e,False
  rr=self.risk.assess(r,p); e['risk']=rr.__dict__; self.transition(e,State.RISK_ASSESSMENT); self.event(e,'RISK_ASSESSED',r.actor,rr.__dict__)
  a=ACTIONS[r.action]; plan=a.plan(r.payload); plan.update(risk=rr.level,approval_required=p.approval_required); e['plan']=plan
  if dry: self.store.update(e); return e,False
  if p.approval_required: self.transition(e,State.AWAITING_APPROVAL); self.event(e,'APPROVAL_REQUESTED',r.actor); self.store.update(e); return e,False
  self.transition(e,State.APPROVED); self.store.update(e); return self._execute(e),False
 def approve(self,i,actor):
  e=self.store.get(i)
  if not e: raise KeyError('execution not found')
  if e['state']!='AWAITING_APPROVAL': raise ValueError('execution is not awaiting approval')
  self.transition(e,State.APPROVED); self.event(e,'APPROVED',actor,{'approver':actor}); self.store.update(e); return self._execute(e)
 def cancel(self,i,actor):
  e=self.store.get(i)
  if not e: raise KeyError('execution not found')
  if e['state'] not in {'AWAITING_APPROVAL','APPROVED'}: raise ValueError('execution cannot be cancelled in current state')
  self.transition(e,State.CANCELLED); self.event(e,'CANCELLED',actor); self.store.update(e); return e
 def expire(self,i,actor='system'):
  e=self.store.get(i)
  if not e: raise KeyError('execution not found')
  if e['state']!='AWAITING_APPROVAL': raise ValueError('execution is not awaiting approval')
  self.transition(e,State.EXPIRED); self.event(e,'EXPIRED',actor); self.store.update(e); return e
 def retry(self,i,actor='system'):
  e=self.store.get(i)
  if not e: raise KeyError('execution not found')
  if e['state']!='FAILED': raise ValueError('only failed executions can be retried')
  self.transition(e,State.EXECUTING); self.event(e,'EXECUTION_RETRY',actor); self.store.update(e); return self._execute(e)
 def reject(self,i,actor,reason='rejected'):
  e=self.store.get(i)
  if not e: raise KeyError('execution not found')
  if e['state']!='AWAITING_APPROVAL': raise ValueError('execution is not awaiting approval')
  self.transition(e,State.REJECTED); e['result']={'reason':reason}; self.event(e,'REJECTED',actor,{'reason':reason}); self.store.update(e); return e
 def _execute(self,e):
  if e['state']!='EXECUTING': self.transition(e,State.EXECUTING)
  self.event(e,'EXECUTION_STARTED',e['actor']); self.event(e,'ATTEMPT_STARTED',e['actor'])
  try: e['result']=ACTIONS[e['action']].execute(e['payload']); self.transition(e,State.SUCCEEDED); self.event(e,'EXECUTION_SUCCEEDED',e['actor'],e['result'])
  except Exception as ex: e['result']={'error':str(ex)}; self.transition(e,State.FAILED); self.event(e,'EXECUTION_FAILED',e['actor'],{'error':str(ex)})
  self.store.update(e); return e
