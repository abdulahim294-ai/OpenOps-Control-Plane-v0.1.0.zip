import json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from openops.domain import ActionRequest
class Handler(BaseHTTPRequestHandler):
 service=None
 def _out(self,status,obj):
  b=json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def _body(self):
  n=int(self.headers.get('Content-Length','0')); 
  if n>1_000_000: raise ValueError('payload too large')
  return json.loads(self.rfile.read(n) or '{}')
 def do_GET(self):
  try:
   if self.path=='/health': return self._out(200,{'status':'ok'})
   if self.path=='/runs': return self._out(200,self.service.store.list())
   if self.path.startswith('/runs/'):
    p=self.path.split('/'); eid=p[2]; e=self.service.store.get(eid)
    if not e:return self._out(404,{'error':{'code':'NOT_FOUND','message':'execution not found'}})
    if len(p)>3 and p[3]=='audit':return self._out(200,self.service.store.audits(eid))
    return self._out(200,e)
   return self._out(404,{'error':{'code':'NOT_FOUND','message':'route not found'}})
  except Exception as x:return self._out(400,{'error':{'code':'BAD_REQUEST','message':str(x)}})
 def do_POST(self):
  try:
   if self.path=='/dry-runs': return self._run(True)
   if self.path=='/runs': return self._run(False)
   if self.path.startswith('/runs/') and self.path.endswith('/approve'):
    e=self.service.approve(self.path.split('/')[2],self.headers.get('X-Actor','operator')); return self._out(200,e)
   if self.path.startswith('/runs/') and self.path.endswith('/reject'):
    d=self._body(); e=self.service.reject(self.path.split('/')[2],self.headers.get('X-Actor','operator'),d.get('reason','rejected')); return self._out(200,e)
   if self.path.startswith('/runs/') and self.path.endswith('/cancel'):
    e=self.service.cancel(self.path.split('/')[2],self.headers.get('X-Actor','operator')); return self._out(200,e)
   if self.path.startswith('/runs/') and self.path.endswith('/retry'):
    e=self.service.retry(self.path.split('/')[2],self.headers.get('X-Actor','operator')); return self._out(200,e)
   return self._out(404,{'error':{'code':'NOT_FOUND','message':'route not found'}})
  except KeyError as x:return self._out(404,{'error':{'code':'NOT_FOUND','message':str(x)}})
  except Exception as x:return self._out(400,{'error':{'code':'BAD_REQUEST','message':str(x)}})
 def _run(self,dry):
  d=self._body(); r=ActionRequest(d['action'],d.get('payload',{}),d.get('actor',self.headers.get('X-Actor','anonymous')),d.get('environment','development'),d.get('source','api'),d.get('source_event_id'),d.get('automation'),d.get('parent_execution_id'),d.get('correlation_id') or __import__('uuid').uuid4().__str__(),self.headers.get('Idempotency-Key') or d.get('idempotency_key')); e,replay=self.service.create(r,dry); return self._out(200 if replay or dry else 201,e)
def serve(service,host='127.0.0.1',port=8080): Handler.service=service; s=ThreadingHTTPServer((host,port),Handler); s.serve_forever()
