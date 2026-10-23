"""Validate reviewed static source, not live domain verification."""
import base64, hashlib, json, re
from pathlib import Path
root = Path(__file__).resolve().parent
association = json.loads((root / '.well-known/assetlinks.json').read_text())
assert len(association) == 1
assert association[0]['relation'] == ['delegate_permission/common.handle_all_urls']
target = association[0]['target']
assert target['namespace'] == 'android_app'
assert target['package_name'] == 'com.joojdevs.ondafy'
assert target['sha256_cert_fingerprints'] == ['4E:3A:AC:36:76:33:C7:80:6C:0B:76:6F:F2:11:0D:CA:D7:8D:D2:4B:C8:25:25:0D:E3:32:A5:88:70:AB:AD:E2']
assert hashlib.sha1(b'blob 151\0' + (root/'index.html').read_bytes()).hexdigest() == '7153283a8659a364d61de197f438e91856ad8b88'
assert (root/'.nojekyll').exists()
html = (root/'ondafy/callback.html').read_text()
assert html == (root/'404.html').read_text()
script = re.search(r'<script>(.*?)</script>', html).group(1)
digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
assert "'sha256-" + digest + "'" in html
assert 'history.replaceState' in script and 'location.search' not in script
assert not re.search(r'\bfetch\s*\(|localStorage|sessionStorage|document.cookie|https?://|src=|href=', html)
assert not (root/'ondafy/callback').exists()
print('PASS: real association schema, original index hash, CSP, sensitive-parameter cleanup, static fallback')
