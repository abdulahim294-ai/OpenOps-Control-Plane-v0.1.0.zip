import sqlite3,json,threading
from pathlib import Path
class Store:
 def __init__(self,path='openops.db'):
  Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path,check_same_thread=False); self.db.row_factory=sqlite3.Row; self.lock=threading.RLock(); self.init()
 def init(self):
  with self.lock, self.db: self.db.executescript("CREATE TABLE IF NOT EXISTS executions(id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE, data TEXT NOT NULL); CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, execution_id TEXT, event TEXT, actor TEXT, timestamp TEXT, metadata TEXT);")
 def get_by_key(self,key):
  if not key:return None
  with self.lock:
   r=self.db.execute("SELECT data FROM executions WHERE idempotency_key=?",(key,)).fetchone(); return json.loads(r["data"]) if r else None
 def save(self,e):
  with self.lock, self.db: self.db.execute("INSERT INTO executions(id,idempotency_key,data) VALUES(?,?,?)",(e["id"],e.get("idempotency_key"),json.dumps(e)))
 def update(self,e):
  with self.lock, self.db: self.db.execute("UPDATE executions SET data=? WHERE id=?",(json.dumps(e),e["id"]))
 def get(self,i):
  with self.lock:
   r=self.db.execute("SELECT data FROM executions WHERE id=?",(i,)).fetchone(); return json.loads(r["data"]) if r else None
 def list(self):
  with self.lock: return [json.loads(r["data"]) for r in self.db.execute("SELECT data FROM executions ORDER BY rowid DESC")]
 def audit(self,eid,event,actor,ts,metadata):
  with self.lock, self.db: self.db.execute("INSERT INTO audit(execution_id,event,actor,timestamp,metadata) VALUES(?,?,?,?,?)",(eid,event,actor,ts,json.dumps(metadata)))
 def audits(self,eid):
  with self.lock: return [dict(r) for r in self.db.execute("SELECT * FROM audit WHERE execution_id=? ORDER BY id",(eid,))]
