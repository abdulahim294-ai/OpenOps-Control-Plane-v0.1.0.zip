import tempfile,unittest,threading
from openops.storage.sqlite import Store
from openops.service import OpenOps
from openops.domain import ActionRequest,State
class T(unittest.TestCase):
 def setUp(self): self.svc=OpenOps(Store(tempfile.mktemp(suffix='.db')))
 def test_low_executes(self):
  e,_=self.svc.create(ActionRequest('record-event',{'event':'x'},idempotency_key='a')); self.assertEqual(e['state'],'SUCCEEDED')
 def test_approval(self):
  e,_=self.svc.create(ActionRequest('send-notification',{},environment='production',idempotency_key='b')); self.assertEqual(e['state'],'AWAITING_APPROVAL'); self.svc.approve(e['id'],'alice'); self.assertEqual(self.svc.store.get(e['id'])['state'],'SUCCEEDED')
 def test_expire_cancel(self):
  e,_=self.svc.create(ActionRequest('send-notification',{},environment='production',idempotency_key='ex')); e=self.svc.expire(e['id']); self.assertEqual(e['state'],'EXPIRED')
  e,_=self.svc.create(ActionRequest('send-notification',{},environment='production',idempotency_key='ca')); e=self.svc.cancel(e['id'],'alice'); self.assertEqual(e['state'],'CANCELLED')
 def test_reject(self):
  e,_=self.svc.create(ActionRequest('send-notification',{},environment='production',idempotency_key='c')); e=self.svc.reject(e['id'],'alice'); self.assertEqual(e['state'],'REJECTED')
 def test_idempotency(self):
  r=ActionRequest('record-event',{'event':'x'},idempotency_key='same'); a,_=self.svc.create(r); b,replay=self.svc.create(r); self.assertTrue(replay); self.assertEqual(a['id'],b['id']); self.assertEqual(len(self.svc.store.list()),1)
 def test_dry_run(self):
  e,_=self.svc.create(ActionRequest('send-notification',{},environment='development',idempotency_key='d'),True); self.assertEqual(e['state'],'RISK_ASSESSMENT'); self.assertEqual(len(self.svc.store.audits(e['id'])),4)
 def test_blocked(self):
  e,_=self.svc.create(ActionRequest('delete-everything',{},idempotency_key='x')); self.assertEqual(e['state'],'BLOCKED')
 def test_retry_failure(self):
  e,_=self.svc.create(ActionRequest('send-notification',{'force_failure':True},environment='production',idempotency_key='rt')); e=self.svc.approve(e['id'],'tester'); self.assertEqual(e['state'],'FAILED'); e['payload']['force_failure']=False; self.svc.store.update(e); e=self.svc.retry(e['id']); self.assertEqual(e['state'],'SUCCEEDED')
 def test_illegal_transition(self):
  e,_=self.svc.create(ActionRequest('record-event',{},idempotency_key='z')); 
  with self.assertRaises(ValueError): self.svc.transition(e,State.APPROVED)
 def test_failure(self):
  e,_=self.svc.create(ActionRequest('send-notification',{'force_failure':True},environment='production',idempotency_key='f')); e=self.svc.approve(e['id'],'tester'); self.assertEqual(e['state'],'FAILED')
 def test_concurrent_duplicates(self):
  r=ActionRequest('record-event',{'event':'x'},idempotency_key='cc'); out=[]
  def f(): out.append(self.svc.create(r)[0]['id'])
  ts=[threading.Thread(target=f) for _ in range(10)]
  [t.start() for t in ts]; [t.join() for t in ts]
  self.assertEqual(len(set(out)),1); self.assertEqual(len(self.svc.store.list()),1)
if __name__=='__main__': unittest.main()
