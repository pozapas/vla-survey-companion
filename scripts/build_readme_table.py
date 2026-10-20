"""Regenerate the systems table in README.md from data/systems.csv.

Usage:
    python scripts/build_readme_table.py          # rewrite README.md in place
    python scripts/build_readme_table.py --check  # exit 1 if README.md is out of date

The table sits between the two marker comments in README.md. Rows are grouped
by architecture class and sorted by year and name within each class, which is
the order of Table 2 in the survey. Paper links come from data/system_links.csv.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = ROOT / 'data' / 'systems.csv'
LINKS = ROOT / 'data' / 'system_links.csv'
README = ROOT / 'README.md'

BEGIN = '<!-- BEGIN SYSTEMS TABLE -->'
END = '<!-- END SYSTEMS TABLE -->'

ARCH_ORDER = ['E2E', 'B+E', 'B+E (no LLM)', 'H', 'DS', 'M']
ARCH_BAND = {'E2E': 'End-to-end (E2E)', 'B+E': 'Backbone plus action expert (B+E)',
             'B+E (no LLM)': 'Action transformer without a language model (B+E, no LLM)',
             'H': 'Hierarchical with a readable interface (H)',
             'DS': 'Dual-system with a latent interface (DS)', 'M': 'Modular (M)'}
DISPLAY = {'pi0': 'π<sub>0</sub>', 'pi0.5': 'π<sub>0.5</sub>', 'pi*0.6': 'π\\*<sub>0.6</sub>'}
HEAD = ['System (year)', 'Backbone; size', 'Action representation', 'Arch.',
        'Decoder; passes per chunk', 'Training data', 'Learn.', 'Deployment objective', 'Dep.', 'Open']


def read(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def arch_base(code):
    if code.startswith('B+E (no LLM)'):
        return 'B+E (no LLM)'
    for b in ['B+E', 'E2E', 'DS', 'H', 'M']:
        if code.startswith(b):
            return b
    raise ValueError(f'unknown architecture code: {code}')


def open_mark(v):
    v = v.strip()
    if v.startswith('yes'):
        return 'yes'
    if v.startswith('code'):
        return 'code'
    if v.startswith('promised'):
        return 'prom.'
    return 'n.s.'


def cell(text):
    text = ' '.join(text.split())
    for a, b in [('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('|', '\\|'),
                 ('~', '\\~'), ('*', '\\*'), ('_', '\\_')]:
        text = text.replace(a, b)
    return text


def build():
    rows = read(SYSTEMS)
    links = {r['key']: r['link'] for r in read(LINKS)}
    missing = [r['key'] for r in rows if not links.get(r['key'])]
    if missing:
        raise SystemExit('no link in data/system_links.csv for: ' + ', '.join(missing))
    for r in rows:
        r['_base'] = arch_base(r['arch_code'])
    rows.sort(key=lambda r: (ARCH_ORDER.index(r['_base']), r['year'], r['name'].lower()))

    out, base = [], None
    for r in rows:
        if r['_base'] != base:
            base = r['_base']
            n = sum(x['_base'] == base for x in rows)
            out += ['', f'#### {ARCH_BAND[base]}, {n} systems', '',
                    '| ' + ' | '.join(HEAD) + ' |', '|' + ' --- |' * len(HEAD)]
        name = DISPLAY.get(r['name'], cell(r['name']))
        dec = r['decoder'] + ('; ' + r['passes_per_chunk'] if r['passes_per_chunk'].strip() else '')
        back = r['backbone'] + ('; ' + r['params'] if r['params'].strip() else '')
        cells = [f"[{name}]({links[r['key']]}) ({r['year']})", cell(back), cell(r['action_rep_class']),
                 cell(r['arch_code']), cell(dec), cell(r['training_data']), cell(r['learning_class']),
                 cell(r['deployment_objective']), cell(r['deployment_class']), open_mark(r['open_weights'])]
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out).strip('\n'), len(rows)


def main():
    table, n = build()
    text = README.read_text(encoding='utf-8')
    if BEGIN not in text or END not in text:
        raise SystemExit('README.md has no table markers')
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = head + BEGIN + '\n' + table + '\n' + END + tail
    if '--check' in sys.argv:
        if new != text:
            print('README.md table is out of date; run python scripts/build_readme_table.py')
            sys.exit(1)
        print(f'README.md table is up to date ({n} systems)')
        return
    README.write_text(new, encoding='utf-8', newline='\n')
    print(f'wrote {n} systems to README.md')


if __name__ == '__main__':
    main()
