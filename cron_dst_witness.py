"""Enumerate zero/one/two UTC witnesses for bounded wall-clock cron slots."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import sys
from zoneinfo import ZoneInfo


def field(text, lo, hi):
    values = set()
    for term in text.split(','):
        base, slash, step_text = term.partition('/')
        if slash and (not step_text.isdecimal() or int(step_text) == 0):
            raise ValueError('invalid step')
        step = int(step_text) if slash else 1
        if base == '*':
            start, stop = lo, hi
        elif '-' in base:
            ends = base.split('-')
            if len(ends) != 2 or any(not e.isdecimal() for e in ends):
                raise ValueError('invalid range')
            start, stop = map(int, ends)
        elif base.isdecimal():
            start = int(base)
            stop = hi if slash else start
        else:
            raise ValueError('unsupported cron syntax')
        if not lo <= start <= stop <= hi:
            raise ValueError('cron field out of range')
        values.update(range(start, stop + 1, step))
    return values


def utc_witnesses(wall, zone):
    instants = {}
    for fold in (0, 1):
        local = wall.replace(tzinfo=zone, fold=fold)
        utc = local.astimezone(timezone.utc)
        back = utc.astimezone(zone)
        if back.replace(tzinfo=None) == wall:
            instants[utc] = {'utc': utc.isoformat(), 'fold': back.fold, 'offset_seconds': int(back.utcoffset().total_seconds())}
    return [instants[t] for t in sorted(instants)]


def analyze(data):
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    expr = data.get('expression')
    if not isinstance(expr, str) or len(expr.split()) != 5:
        raise ValueError('five cron fields required')
    texts = expr.split()
    minute, hour, dom, month, dow = [field(t, a, b) for t, a, b in zip(texts, (0, 0, 1, 1, 0), (59, 23, 31, 12, 7))]
    dow = {d % 7 for d in dow}
    days = data.get('days')
    if type(days) is not int or not 1 <= days <= 31:
        raise ValueError('days must be an integer from 1 to 31')
    if not isinstance(data.get('start_date'), str) or len(data['start_date']) != 10:
        raise ValueError('start_date must be YYYY-MM-DD')
    start = date.fromisoformat(data['start_date'])
    if not isinstance(data.get('zone'), str):
        raise ValueError('zone must be an IANA zone string')
    zone = ZoneInfo(data['zone'])
    counts = {'missing': 0, 'unique': 0, 'ambiguous': 0}
    anomalies = []
    # Standard cron: restricted DOM and DOW fields use OR. A leading '*' is
    # a wildcard field even with a step, matching the Vixie-style distinction.
    dom_wild, dow_wild = texts[2].startswith('*'), texts[4].startswith('*')
    for n in range(days):
        d = start + timedelta(days=n)
        dm, dw = d.day in dom, (d.weekday() + 1) % 7 in dow
        day_match = (dm and dw) if dom_wild or dow_wild else (dm or dw)
        if d.month not in month or not day_match:
            continue
        for h in sorted(hour):
            for m in sorted(minute):
                wall = datetime(d.year, d.month, d.day, h, m)
                witnesses = utc_witnesses(wall, zone)
                label = ('missing', 'unique', 'ambiguous')[len(witnesses)]
                counts[label] += 1
                if label != 'unique':
                    anomalies.append({'wall': wall.isoformat(), 'state': label, 'witnesses': witnesses})
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return {'schema': 'cron-dst-witness/v1', 'input_sha256': digest, 'expression': expr, 'zone': zone.key, 'start_date': start.isoformat(), 'days': days, 'counts': counts, 'anomalies': anomalies,
            'limits': 'Wall-clock slot audit, not a scheduler prediction; daemon catch-up/deduplication differs. Uses installed IANA tzdata; five numeric fields only, no seconds/names/L/W/#.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    args = p.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f:
            result = analyze(json.load(f))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as error:
        print('error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
