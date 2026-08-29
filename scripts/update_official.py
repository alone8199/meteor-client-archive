#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

API = 'https://meteorclient.com/api/download?version={}'
HOME = 'https://meteorclient.com/'
ARCHIVE = 'https://meteorclient.com/archive'
ROOT = Path(__file__).resolve().parents[1]
MODS = ROOT / 'official-api'
MODS.mkdir(parents=True, exist_ok=True)

def fetch(url):
    req = Request(url, headers={'User-Agent': 'meteor-client-archive-updater/1.0'})
    with urlopen(req, timeout=90) as r:
        return r.read()

def versions_from_archive(text):
    return set(re.findall(r'/api/download\?version=([0-9A-Za-z._-]+)', text))

def current_version(text):
    m = re.search(r'Meteor Client\s*\[([^\]]+)', text)
    if not m:
        return None
    return m.group(1).split()[0]

archive_text = fetch(ARCHIVE).decode('utf-8', 'replace')
home_text = fetch(HOME).decode('utf-8', 'replace')
versions = versions_from_archive(archive_text)
current = current_version(home_text)
if current:
    versions.add(current)
if not versions:
    raise RuntimeError('No Minecraft versions found from official sources')

records = []
for version in sorted(versions):
    data = fetch(API.format(version))
    if len(data) < 1000 or not data.startswith(b'PK'):
        raise RuntimeError(f'Invalid JAR response for {version}: {len(data)} bytes')
    target = MODS / f'meteor-client-{version}.jar'
    target.write_bytes(data)
    with ZipFile(target) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'Corrupt JAR {version}: {bad}')
    records.append({'minecraft_version': version, 'filename': str(target.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'source': API.format(version)})

(Path(ROOT / 'official-api-manifest.json')).write_text(json.dumps({'source_archive': ARCHIVE, 'source_home': HOME, 'items': records}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'updated {len(records)} official API JARs')
