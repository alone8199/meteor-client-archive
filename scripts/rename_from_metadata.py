from pathlib import Path
from zipfile import ZipFile
import hashlib, json, re, shutil

ROOT=Path('/home/ubuntu/meteor-client-archive-repo')
ARCH=ROOT/'historical-archive'
STAGE=ROOT/'.rename-metadata-staging'
STAGE.mkdir(exist_ok=True)

def metadata(p):
    with ZipFile(p) as z:
        obj=json.loads(z.read('fabric.mod.json'))
    return obj.get('id'), str(obj.get('version'))

def mc_from_name(name):
    # Early builds can encode the target MC version in the Meteor filename suffix.
    # Check that suffix before the existing prefix, because the prefix may be from
    # an earlier imperfect rename.
    tail = name.split('__', 1)[1] if '__' in name else name
    explicit = re.search(r'(1\.14\.4|1\.15\.2|1\.16\.1|1\.16\.2)', tail)
    if explicit:
        return explicit.group(1)
    if '__' in name:
        return name.split('__',1)[0].removeprefix('mc-')
    return 'unknown'

rows=[]
for p in sorted(ARCH.glob('*.jar')):
    mod_id, mod_version=metadata(p)
    mc=mc_from_name(p.name)
    if not mc or mc=='unknown':
        raise RuntimeError(f'Cannot determine Minecraft version from {p.name}')
    dest=STAGE/f'mc-{mc}__meteor-{mod_version}.jar'
    rows.append((p,dest,mod_id,mod_version,mc))
# Detect non-identical collisions before modifying anything.
by_name={}
for p,d,*_ in rows:
    if d.name in by_name and hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(by_name[d.name].read_bytes()).digest():
        raise RuntimeError(f'Non-identical filename collision: {d.name}')
    by_name[d.name]=p
# Stage only one copy for exact duplicates.
seen=set()
for p,d,*_ in rows:
    if d.name in seen: continue
    seen.add(d.name)
    shutil.move(str(p),str(d))
for p in STAGE.glob('*.jar'):
    shutil.move(str(p),str(ARCH/p.name))
STAGE.rmdir()
report=[{'filename':d.name,'minecraft_version':mc,'meteor_version':ver,'mod_id':mid,'sha256':hashlib.sha256((ARCH/d.name).read_bytes()).hexdigest()} for _,d,mid,ver,mc in rows if d.name in seen]
(ROOT/'metadata_name_inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'renamed={len(report)} final_files={len(list(ARCH.glob("*.jar")))}')
