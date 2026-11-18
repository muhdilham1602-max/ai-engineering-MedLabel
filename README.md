# Rapid KL Bus Route Assistant

A semester AI Engineering project exploring a source-grounded assistant for public transport lookup. The current V1 scope is Rapid KL bus route and stop facts from the official static GTFS feed. A Rapid Rail KL static feed snapshot has also been collected for a possible rail lookup extension.

## Current scope

The current bus assistant prototype is intended to answer supported questions such as which listed Rapid KL bus routes serve a named stop, whether a stop appears on a route, and the stop sequence for a selected trip. Route facts must come from linked GTFS records and the assistant must not invent them.

The additional rail feed supports static station, line, and scheduled-stop lookups for the lines it contains. The assistant has not yet integrated the rail feed. Neither feed alone currently supports reliable point-to-point journey planning: explicit station transfer/pathway information is absent from the collected rail ZIP, and bus-to-rail transfer connections have not been verified. The project does not provide live arrivals, fares, accessibility guarantees, traffic-aware planning, or disruption advice. It is an educational prototype, not an official Rapid KL service.

## Project files

- `docs/week1_project_scope.md` - initial project framing and scope
- `docs/week2_requirements.md` - functional, non-functional and Responsible AI requirements
- `docs/week2_evaluation_criteria.md` - evaluation plan and thresholds
- `docs/week2_architecture_v1.png` - conceptual architecture
- `docs/week2_architecture_decisions.md` - decisions and traceability
- `notebooks/week3_pipeline.ipynb` - executable Colab pipeline for the bus GTFS feed
- `docs/week3_data_inventory.md` - bus source inventory and inspection evidence
- `docs/week3_pipeline_diagram.png` - bus pipeline workflow
- `docs/week3_pipeline_decisions.md` - bus preparation choices, contracts and trade-offs
- `data/rail_manifest.json` - provenance and inspection summary for the collected rail ZIP

## Data

### Rapid Bus KL

Primary source: [Malaysia GTFS Static API](https://developer.data.gov.my/realtime-api/gtfs-static), Prasarana category `rapid-bus-kl` at `https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl`.

The bus feed is licensed CC BY 4.0. The snapshot retrieved 18 November 2026 was a valid 1,697,000-byte ZIP containing 139 routes, 4,107 stops, 2,118 trips, and 88,801 stop-time rows. Primary-key uniqueness and route/trip/stop foreign-key checks passed. The provider notes that about 2% of Rapid Bus KL trips are absent from `stop_times.txt` due to operational data issues, so coverage is incomplete. The bus ZIP is downloaded by the notebook and is not stored in Git.

### Rapid Rail KL

Official source: [Malaysia GTFS Static API](https://developer.data.gov.my/realtime-api/gtfs-static), Prasarana category `rapid-rail-kl` at `https://api.data.gov.my/gtfs-static/prasarana?category=rapid-rail-kl`.

The rail snapshot retrieved 18 November 2026 is included at `data/raw/rapid-rail-kl-gtfs.zip` under CC BY 4.0. It is 80,673 bytes (SHA-256 `45c134f991b955eff801d35a45d9bdbeca83ae780bfc29dcac142665146c4533`) and contains 8 routes, 187 stop records, 48 trips, 1,122 stop-time rows and 8 calendar records. Key uniqueness and required foreign-key checks passed on this snapshot. This is a static feed; the API says Prasarana GTFS Static data is updated as required.

The rail snapshot has no `transfers.txt` or `pathways.txt`. Six of its eight service calendars end on 31 December 2026 and two end on 31 March 2026. Refresh and review calendar validity before relying on a date-specific timetable. It can support static line/station/trip lookups, but not a reliable automatic multi-line or bus-to-rail itinerary without validated transfer connections. The GTFS Realtime documentation also says Rapid Rail KL does not yet have a stable real-time feed.

Supplementary public sources:

- [GTFS Static API documentation](https://developer.data.gov.my/realtime-api/gtfs-static)
- [GTFS Realtime API documentation](https://developer.data.gov.my/realtime-api/gtfs-realtime)
- [Klang Valley Integrated Transit Map (October 2025, PDF)](https://myrapid.com.my/wp-content/uploads/2025/10/Transit-Map_131025.pdf)
- [Rapid KL service-use guide (PDF)](https://myrapid.com.my/wp-content/uploads/2024/10/Booklet_Panduan-Penggunaan-Perkhidmatan-Rapid-KL_c.pdf)

The bus feed snapshots are downloaded at runtime and excluded from Git. The collected rail snapshot is retained for reproducibility with its date, SHA-256 and CC BY 4.0 attribution recorded in `data/rail_manifest.json`. Re-check all feed contents and service dates before making user-facing claims.

## Status

Topics 1-3 individual artefacts are prepared. The official bus feed was downloaded, its structured pipeline was built, and a deterministic repeatability check passed on the preserved snapshot. The bus notebook was run in Google Colab. The rail feed has been downloaded and structurally inspected as a candidate next-stage data source; it has not yet been integrated into the assistant. Group observation and system-map files are retained as the student's original group evidence.

