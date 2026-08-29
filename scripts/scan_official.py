#!/usr/bin/env python3
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HOME = 'https://meteorclient.com/'
ARCHIVE = 'https://meteorclient.com/archive'
API = 'https://meteorclient.com/api/download?version={}'
ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    req = Request(url, headers={'User-Agent': 'meteor-client-archive-daily-scanner/1.0'})
    with urlopen(req, timeout=60) as r:
        return r.read(), r.headers


def versions_from_archive(text):
    return set(re.findall(r'/api/download\?version=([0-9A-Za-z._-]+)', text))


def current_version(text):
    match = re.search(r'Meteor Client\s*\[([^\]]+)', text)
    return match.group(1).split()[0] if match else None

home, _ = fetch(HOME)
archive, _ = fetch(ARCHIVE)
versions = versions_from_archive(archive.decode('utf-8', 'replace'))
current = current_version(home.decode('utf-8', 'replace'))
if current:
    versions.add(current)

items = []
for version in sorted(versions):
    try:
        data, headers = fetch(API.format(version))
        valid_jar = len(data) > 1000 and data.startswith(b'PK')
        items.append({'minecraft_version': version, 'api_url': API.format(version), 'available': valid_jar, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest() if valid_jar else None, 'content_type': headers.get_content_type()})
    except Exception as exc:
        items.append({'minecraft_version': version, 'api_url': API.format(version), 'available': False, 'error': str(exc)})

result = {'scanned_at': datetime.now(timezone.utc).isoformat(), 'sources': [HOME, ARCHIVE], 'current_version': current, 'items': items}
(ROOT / 'daily-scan.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'scanned={len(items)} available={sum(x.get("available", False) for x in items)}')
