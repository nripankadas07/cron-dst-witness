# Research — cron-dst-witness

Observed 13 October 2026 on live GitHub. Demand is inferred from documented workflows and public issues, not a verified request for this product. Only the first page of each star-sorted problem search was reviewed; this is not an exhaustive global ranking. Broad unrelated results were excluded. Stars are discovery signals, not technical performance evidence.

## User and acceptance

An operator reviewing a timezone schedule before a DST transition.

Pain: Expose missing and ambiguous wall-clock cron slots with exact UTC witnesses.

Smallest useful capability and acceptance: New York 2026-03-08 02:30 has no UTC witness; 2026-11-01 01:30 has 05:30Z and 06:30Z; Lord Howe half-hour gaps/folds are correct; invalid expressions/timezones/window limits fail; ordinary folds deduplicate.

## Observed alternatives

| Repository | Stars | Last push (UTC) | Status / detected license |
| --- | ---: | --- | --- |
| [robfig/cron](https://github.com/robfig/cron) | 14193 | 2024-07-08T01:21:14Z | active repository / MIT |
| [kelektiv/node-cron](https://github.com/kelektiv/node-cron) | 8950 | 2026-10-13T02:37:57Z | active repository / MIT |
| [pallets-eco/croniter](https://github.com/pallets-eco/croniter) | 563 | 2026-10-02T09:34:28Z | active repository / MIT |

Query: `cron`; [GitHub search, Most stars](https://github.com/search?q=cron&type=repositories&s=stars&o=desc). Exact observed queries, stars and push dates are recorded above. Highest-star relevant result on that page: robfig/cron (library; larger distributed schedulers are a different deployment workflow). Other established workflow alternatives were reviewed even if they were not on that first page.

Robfig cron is a Go parser/runner with timezone support and documented DST handling in spec.go. Node cron is a Node scheduler with timeZone and Luxon semantics. Croniter already supports aware-datetime iteration and documents DST. This tool exposes both possible UTC witnesses or a missing wall slot over a bounded date window; it does not claim those libraries lack timezone handling or predict their execution behavior.

## Differentiation and discovery

Owned crontab-lite explicitly supports timezone-naive matches only; this independently implemented diagnostic addresses wall-slot ambiguity, not general cron iteration. Distinct from clock-quorum-window uncertainty intervals. Discover through DST incident explanations and cron migration examples.

## Fair comparison boundary

Docs, relevant source and accessible issue collections were inspected. No comparator was installed or timed on equivalent workloads; therefore no install-speed, reliability or performance superiority is claimed. A passing example proves our documented behavior only. No external code was reused; comparator licenses above are API-detected labels, not a legal determination. Support and licensing follow each upstream repository; this alpha offers MIT source and best-effort issue support.
