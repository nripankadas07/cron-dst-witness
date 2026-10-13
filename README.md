# cron-dst-witness

Expose missing and ambiguous wall-clock cron slots with exact UTC witnesses.

**Alpha, offline diagnostic.** Built for an operator reviewing a timezone schedule before a DST transition.
Original implementation with AI assistance; no competitor code or prose copied.
No production impact, adoption or performance advantage is claimed.

## Install and get a useful result

Python 3.10+. Clone this repository, then:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install .
cron-dst-witness example.json
```

The bundled fixture is synthetic. `example.py` only creates its own temporary
fixture when present. Exit 0 means a report was produced with no CLI-level failure;
exit 2 reports invalid or unsupported input.
A zero exit is not an eviction or scheduler safety guarantee.

## Input

`cron-dst-witness schedule.json` accepts `expression`, IANA `zone`,
`start_date` as YYYY-MM-DD, and integer `days` from 1 to 31; see
[the fixture](example.json). Output `counts` includes all matching local slots;
`anomalies` contains only missing or ambiguous slots. An ambiguity exposes both
UTC instants, offsets and fold values. This is a wall-time audit, not a claim
about when a particular cron daemon runs or catches up.

## Capability and limits

Five numeric cron fields, lists/ranges/steps, standard DOM/DOW OR when both restricted, and Sunday 0/7. Leading-star day fields retain wildcard semantics. Reports round-trip-valid UTC instants for every matching wall-clock slot, including both folds and gaps. Window 1..31 local dates; up to 44,640 slots. Uses installed IANA tzdata. Linux CI uses system tzdata; Windows may need the official tzdata package. Not a scheduler: daemon catch-up/deduplication behavior differs. Seconds, names, L/W/#, jobs and execution are unsupported.

## Acceptance criteria

New York 2026-03-08 02:30 has no UTC witness; 2026-11-01 01:30 has 05:30Z and 06:30Z; Lord Howe half-hour gaps/folds are correct; invalid expressions/timezones/window limits fail; ordinary folds deduplicate.

## Checks and evidence

```bash
python -m unittest -v
python -m compileall -q .
```

[Validation](VALIDATION.md) documents the prepared checks and failure cases.
[Research and alternatives](RESEARCH.md) records dated observations, competing
workflows and a bounded inferred need. The [CI workflow](.github/workflows/test.yml)
builds wheels and tests installed commands outside the checkout on Linux Python
3.10/3.12/3.14. Check the actual current Actions result before relying on it.

[Contributing](CONTRIBUTING.md) · [Support](SUPPORT.md) ·
[Security](SECURITY.md) · [MIT license](LICENSE)
