"""Tiny dependency-free PEP 517 backend for this reference project."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import base64,hashlib,os
NAME='openops_control_plane'; VERSION='0.1.0'; DIST=f'{NAME}-{VERSION}'

def _wheel_name(): return f'{DIST}-py3-none-any.whl'
def _metadata(): return f'Metadata-Version: 2.1\nName: openops-control-plane\nVersion: {VERSION}\nSummary: Open-source control plane for safer automation execution\nRequires-Python: >=3.10\nLicense: Apache-2.0\n'
def _write_wheel(wheel_directory, editable=False):
 out=Path(wheel_directory); out.mkdir(parents=True,exist_ok=True); fn=_wheel_name(); path=out/fn
 files=[]
 if editable:
  files.append((f'{NAME}.pth', str(Path.cwd())+'\n'))
 else:
  for p in Path('openops').rglob('*.py'): files.append((str(p),p.read_bytes()))
 dist=f'{DIST}.dist-info'
 files += [(f'{dist}/METADATA',_metadata()),(f'{dist}/WHEEL','Wheel-Version: 1.0\nGenerator: openops-build-backend\nRoot-Is-Purelib: true\nTag: py3-none-any\n'),(f'{dist}/entry_points.txt','[console_scripts]\nopenops = openops.cli.main:main\n')]
 records=[]
 with ZipFile(path,'w',ZIP_DEFLATED) as z:
  for name,data in files:
   if isinstance(data,str): data=data.encode()
   z.writestr(name,data); h=base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode(); records.append(f'{name},sha256={h},{len(data)}')
  records.append(f'{dist}/RECORD,,'); z.writestr(f'{dist}/RECORD','\n'.join(records)+'\n')
 return fn

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None): return _write_wheel(wheel_directory,False)
def build_editable(wheel_directory, config_settings=None, metadata_directory=None): return _write_wheel(wheel_directory,True)
def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
 p=Path(metadata_directory)/f'{DIST}.dist-info'; p.mkdir(parents=True,exist_ok=True); (p/'METADATA').write_text(_metadata()); (p/'WHEEL').write_text('Wheel-Version: 1.0\nGenerator: openops-build-backend\nRoot-Is-Purelib: true\nTag: py3-none-any\n'); return p.name
def prepare_metadata_for_build_editable(metadata_directory, config_settings=None): return prepare_metadata_for_build_wheel(metadata_directory,config_settings)
