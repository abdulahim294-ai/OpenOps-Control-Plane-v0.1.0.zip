from openops.storage.sqlite import Store
from openops.service import OpenOps
from openops.domain import ActionRequest
s=OpenOps(Store(':memory:'))
r=ActionRequest('send-notification',{'destination':'demo@example.invalid','message':'hello'},'demo-agent','production',idempotency_key='demo-python')
e,_=s.create(r); print(e['state'],e['id']); print('approval required'); e=s.approve(e['id'],'demo-operator'); print(e['state']); e2,_=s.create(r); print('idempotent replay:',e2['id']==e['id']); print('audit events:',len(s.store.audits(e['id'])))
