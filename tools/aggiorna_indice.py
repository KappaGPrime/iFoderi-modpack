"""Rigenera index.toml e l'hash in pack.toml (stesso formato di `packwiz refresh`).
Uso: python3 tools/aggiorna_indice.py [nuova_versione_del_pacchetto]"""
import hashlib, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# cartelle e file che finiscono nel gioco dei giocatori
CARTELLE = ['mods', 'resourcepacks', 'shaderpacks', 'config']
# impostazioni: messe solo alla prima installazione, poi non si toccano piu' (i giocatori possono cambiarle)
SOLO_LA_PRIMA_VOLTA = ['options.txt', 'servers.dat', 'config/']


def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


files = []
for c in CARTELLE:
    for base, _, names in os.walk(os.path.join(ROOT, c)):
        for n in sorted(names):
            files.append(os.path.relpath(os.path.join(base, n), ROOT).replace(os.sep, '/'))
for f in ('options.txt', 'servers.dat'):
    if os.path.exists(os.path.join(ROOT, f)):
        files.append(f)

out = ['hash-format = "sha256"', '']
for f in sorted(files):
    out += ['[[files]]', f'file = "{f}"', f'hash = "{sha256(os.path.join(ROOT, f))}"']
    if f.endswith('.pw.toml'):
        out.append('metafile = true')
    elif any(f == s or (s.endswith('/') and f.startswith(s)) for s in SOLO_LA_PRIMA_VOLTA):
        out.append('preserve = true')
    out.append('')
open(os.path.join(ROOT, 'index.toml'), 'w', newline='\n').write('\n'.join(out))

pack = open(os.path.join(ROOT, 'pack.toml')).read()
pack = re.sub(r'(\[index\][^\[]*?hash = ")[0-9a-f]*(")', r'\g<1>' + sha256(os.path.join(ROOT, 'index.toml')) + r'\2', pack, flags=re.S)
if len(sys.argv) > 1:
    pack = re.sub(r'^version = ".*"', f'version = "{sys.argv[1]}"', pack, flags=re.M)
open(os.path.join(ROOT, 'pack.toml'), 'w', newline='\n').write(pack)
print(len(files), 'file nell\'indice')
