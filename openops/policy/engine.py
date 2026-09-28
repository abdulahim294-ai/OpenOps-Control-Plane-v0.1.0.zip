from openops.domain import PolicyDecision
class PolicyEngine:
 def evaluate(self, r):
  reasons=[]; allowed=True
  if r.action not in {'record-event','send-notification','create-ticket','deployment-simulation'}: allowed=False; reasons.append('unknown action')
  if not r.action: allowed=False; reasons.append('action is required')
  if r.environment=='production': reasons.append('target environment is production')
  if r.payload.get('sensitive_data'): reasons.append('sensitive data declared')
  approval = r.environment=='production' or r.action=='send-notification' or bool(r.payload.get('sensitive_data'))
  risk='HIGH' if r.environment=='production' or r.payload.get('sensitive_data') else ('MEDIUM' if r.action=='send-notification' else 'LOW')
  return PolicyDecision(allowed, approval, reasons or ['request matches baseline policy'], risk)
