# Rapid KL Bus Route Assistant

A semester AI Engineering project proposal for a source-grounded assistant that helps new and occasional riders find Rapid KL bus route and stop information from the official static GTFS feed.

## Scope

The V1 assistant answers questions such as which listed Rapid KL bus routes serve a named stop, whether a stop appears on a route, and what the stop sequence is for a selected trip. Natural-language query interpretation is an AI capability; route facts come from structured GTFS records and must not be invented by the model.

V1 does not provide real-time arrivals, fares, accessibility guarantees, traffic-aware trip planning, transfers, or service disruption advice. It is an educational prototype, not an official Rapid KL service.

## Project files

- `docs/week1_project_scope.md` — initial project framing and scope
- `docs/week2_requirements.md` — functional, non-functional and Responsible AI requirements
- `docs/week2_evaluation_criteria.md` — evaluation plan and thresholds
- `docs/week2_architecture_v1.png` — conceptual architecture
- `docs/week2_architecture_decisions.md` — decisions and traceability

## Data

Primary source: [Malaysia GTFS Static API](https://developer.data.gov.my/realtime-api/gtfs-static), Prasarana feed category `rapid-bus-kl` at `https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl`.

The feed is CC BY 4.0. Its documentation describes `routes`, `stops`, `trips`, `stop_times`, and service calendar files. At the time of the initial project review (18 November 2026), a downloaded feed was a valid 1,697,000-byte ZIP containing 139 routes, 4,107 stops, 2,118 trips, and 88,801 stop-time rows. Primary-key uniqueness and route/trip/stop foreign-key checks passed. These are a one-time snapshot, not a promise about future feed contents. The provider notes that about 2% of Rapid Bus KL trips have been removed from `stop_times.txt` due to operational data issues; coverage is therefore not complete.

Supplementary public sources:

- [GTFS Static API documentation](https://developer.data.gov.my/realtime-api/gtfs-static)
- [Klang Valley Integrated Transit Map (October 2025, PDF)](https://myrapid.com.my/wp-content/uploads/2025/10/Transit-Map_131025.pdf)
- [Rapid KL service-use guide (PDF)](https://myrapid.com.my/wp-content/uploads/2024/10/Booklet_Panduan-Penggunaan-Perkhidmatan-Rapid-KL_c.pdf)

Do not commit downloaded feed snapshots unless their date and CC BY 4.0 attribution are recorded. Re-check the current feed before making user-facing claims.

## Status

Topics 1 and 2 planning draft. Group observation and system-map evidence should remain the student's actual group work; do not replace it with fabricated observations. Topic 3 implementation and execution evidence are not included in this planning package.

