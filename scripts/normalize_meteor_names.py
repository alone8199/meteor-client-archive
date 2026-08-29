from pathlib import Path
import hashlib
import re
import shutil

ROOT = Path('/home/ubuntu/meteor-client-archive-repo')
ARCH = ROOT / 'historical-archive'
TEMP = ROOT / '.rename-staging'
TEMP.mkdir(exist_ok=True)

# Files downloaded directly from the official API have no build number in the
# filename; give them an explicit api label. Historical files keep their original
# Meteor release/build stem after the MC version.
def mc_version(name: str) -> str:
    explicit = re.search(r'(1\.14\.4|1\.15\.2|1\.16\.1|1\.16\.2)', name)
    if explicit:
        return explicit.group(1)
    if '__' in name:
        return name.split('__', 1)[0]
    m = re.match(r'meteor-client-(\d+(?:\.\d+){1,3})\.jar$', name)
    if m:
        return m.group(1)
    # Unsuffixed early archive builds are documented as 1.14.4.
    return '1.14.4'

def target_for(path: Path) -> str:
    name = path.name
    mc = mc_version(name)
    if '__' in name:
        stem = name.split('__', 1)[1][:-4]
        stem = re.sub(r'^meteor-client-', 'meteor-', stem)
        return f'mc-{mc}__{stem}.jar'
    stem = name[:-4]
    version = stem.removeprefix('meteor-client-')
    return f'mc-{mc}__meteor-api-{version}.jar'

# First group exact duplicates and retain the already version-qualified name
# when available; otherwise retain the original API name temporarily.
files = sorted(ARCH.glob('*.jar'))
groups = {}
for p in files:
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    groups.setdefault(digest, []).append(p)
kept = []
removed = []
for digest, group in groups.items():
    preferred = sorted(group, key=lambda p: (('__' not in p.name), p.name))[0]
    kept.append(preferred)
    removed.extend(p for p in group if p != preferred)
for p in removed:
    p.unlink()

# Stage and rename to avoid collisions while moving files in place.
for p in kept:
    dest = TEMP / target_for(p)
    if dest.exists():
        # Different bytes with an identical semantic name get a short hash suffix.
        dest = TEMP / f'{dest.stem}__{hashlib.sha256(p.read_bytes()).hexdigest()[:8]}.jar'
    shutil.move(str(p), str(dest))
for p in TEMP.glob('*.jar'):
    shutil.move(str(p), str(ARCH / p.name))
TEMP.rmdir()
print(f'kept={len(kept)} removed_exact_duplicates={len(removed)} final={len(list(ARCH.glob("*.jar")))}')
