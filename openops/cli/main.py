import argparse,json
from openops.storage.sqlite import Store
from openops.service import OpenOps
from openops.domain import ActionRequest

def main():
 p=argparse.ArgumentParser(prog='openops'); sub=p.add_subparsers(dest='cmd',required=True); 
 for c in ['list','status','audit','approve','reject','replay']: sub.add_parser(c).add_argument('id',nargs='?')
 r=sub.add_parser('run'); r.add_argument('action'); r.add_argument('--payload',default='{}'); r.add_argument('--environment',default='development'); r.add_argument('--idempotency-key'); r.add_argument('--actor',default='cli')
 d=sub.add_parser('dry-run'); d.add_argument('action'); d.add_argument('--payload',default='{}'); d.add_argument('--environment',default='development')
 sub.add_parser('serve'); sub.add_parser('demo')
 a=p.parse_args(); svc=OpenOps(Store(':memory:') if a.cmd=='demo' else Store())
 if a.cmd=='serve': from openops.api.server import serve; serve(svc); return
 if a.cmd=='list': print(json.dumps(svc.store.list(),indent=2)); return
 if a.cmd=='status': print(json.dumps(svc.store.get(a.id),indent=2)); return
 if a.cmd=='audit': print(json.dumps(svc.store.audits(a.id),indent=2)); return
 if a.cmd=='approve': print(json.dumps(svc.approve(a.id,'cli'),indent=2)); return
 if a.cmd=='reject': print(json.dumps(svc.reject(a.id,'cli'),indent=2)); return
 if a.cmd=='run' or a.cmd=='dry-run':
  e,_=svc.create(ActionRequest(a.action,json.loads(a.payload),a.actor,getattr(a,'environment','development'),idempotency_key=getattr(a,'idempotency_key',None)),a.cmd=='dry-run'); print(json.dumps(e,indent=2)); return
 if a.cmd=='replay':
  e=svc.store.get(a.id); r=ActionRequest(e['action'],e['payload'],e['actor'], 'development',idempotency_key=e.get('idempotency_key')); print(json.dumps(svc.create(r)[0],indent=2)); return
 if a.cmd=='demo':
  r=ActionRequest('send-notification',{'destination':'demo@example.invalid','message':'safe demonstration'},'demo-agent','production',idempotency_key='demo-001'); e,_=svc.create(r); print('AWAITING:',e['state'],e['id']); e=svc.approve(e['id'],'demo-operator'); print('RESULT:',e['state']); e2,_=svc.create(r); print('REPLAY SAME ID:',e2['id']==e['id']); print('AUDIT EVENTS:',len(svc.store.audits(e['id'])))

if __name__ == '__main__': main()
