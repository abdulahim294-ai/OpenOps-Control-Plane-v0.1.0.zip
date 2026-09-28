from openops.domain import RiskAssessment
class RiskEngine:
 def assess(self,r,p):
  score=0; factors=[]
  if r.environment=='production': score+=40; factors.append('production target')
  if r.payload.get('destructive'): score+=40; factors.append('destructive operation')
  if r.payload.get('sensitive_data'): score+=30; factors.append('sensitive data')
  if r.action=='send-notification': score+=20; factors.append('external side effect')
  if r.payload.get('large_blast_radius'): score+=30; factors.append('large blast radius')
  level='CRITICAL' if score>=80 else 'HIGH' if score>=50 else 'MEDIUM' if score>=20 else 'LOW'
  return RiskAssessment(level,score,factors or ['no elevated risk factors detected'])
