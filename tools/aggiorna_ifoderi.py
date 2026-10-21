"""Mette nel pacchetto un nuovo jar di iFoderi RPG.
Uso: python3 tools/aggiorna_ifoderi.py <percorso del jar> <url di download>"""
import hashlib, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
jar, url = sys.argv[1], sys.argv[2]
h = hashlib.sha512(open(jar, 'rb').read()).hexdigest()
open(os.path.join(ROOT, 'mods', 'ifoderi-rpg.pw.toml'), 'w', newline='\n').write(f'''name = "iFoderi RPG"
filename = "{os.path.basename(jar)}"
side = "both"

[download]
url = "{url}"
hash-format = "sha512"
hash = "{h}"
''')
print('iFoderi RPG ->', os.path.basename(jar))
