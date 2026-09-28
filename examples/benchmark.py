import statistics,time
from openops.storage.sqlite import Store
from openops.service import OpenOps
from openops.domain import ActionRequest
s=OpenOps(Store(':memory:')); samples=[]
for i in range(100):
 t=time.perf_counter(); s.policy.evaluate(ActionRequest('record-event',{})); samples.append((time.perf_counter()-t)*1000)
print('policy_evaluation_ms_p50=',statistics.median(samples)); print('iterations=100'); print('machine-specific benchmark; rerun locally for comparable results')
