# Week 3 Data Inventory

## Source and requirement link

The selected source is the official Prasarana Rapid Bus KL static GTFS feed. It supports Topic 2 requirements FR2 (routes serving a stop), FR3 (ordered stops for a trip), FR4 (trace source identifiers), FR8 (repeatable refresh), and NFR3–NFR4 (repeatability and data integrity). The data is a structured, multi-table ZIP; no dummy data was used. The selected Topic 3 pathway is **B: structured/tabular data**.

| Source ID | File / URL | Type and purpose | Version / date / owner | Access / rights | Inspection evidence |
|---|---|---|---|---|---|
| S01 | [Rapid Bus KL GTFS endpoint](https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl) | ZIP containing comma-separated GTFS tables used to link routes, trips, stops and stop times | Retrieved 2026-11-18; provider: Prasarana Malaysia | Public API; CC BY 4.0 per [official documentation](https://developer.data.gov.my/realtime-api/gtfs-static); preserve attribution | Valid ZIP, 1697000 bytes, SHA-256 `8721e30d81a29b64dc4a64424871ec3afe8b2a0b509153ade2a32401c6c5cc61`; tables and row counts below; zero broken required references in this snapshot |
| S02 | [GTFS Static API documentation](https://developer.data.gov.my/realtime-api/gtfs-static) | Schema, endpoints, licensing and provider caveats | Accessed 2026-11-18; Malaysia Open API | Public documentation | Confirms the GTFS tables and notes approximately 2% of Rapid Bus KL trips are absent from `stop_times.txt` due to operational issues |

## Files inspected

| File | Rows | Key columns / role |
|---|---:|---|
| `routes.txt` | 139 | `route_id`, short and long names; route lookup |
| `trips.txt` | 2118 | `trip_id`, `route_id`, `service_id`, direction |
| `stops.txt` | 4107 | `stop_id`, `stop_name`, latitude/longitude |
| `stop_times.txt` | 88801 | trip, stop, arrival/departure and `stop_sequence` |
| `calendar.txt` | 2 | weekday/weekend service dates; snapshot validity |
| `agency.txt` | 1 | agency metadata; agency name is Rapid KL |

Two representative tables, `routes.txt` and `stops.txt`, were inspected with sample records; a sample stop-time join linked “STESEN BRT SETIA JAYA” to route `B1000`. The combined route-stop lookup contains 88801 rows.

## Observed limitations and handling

- The provider reports about 2% of Rapid Bus KL trips were removed from `stop_times.txt`; the feed is not complete. Do not infer that a missing trip means the real-world service does not operate.
- The downloaded snapshot’s service calendar runs from 2020-04-01 through 2027-03-31. Always check the calendar and refresh before reuse.
- `trip_headsign` and `stop_headsign` are blank for some records; they are optional, so retain IDs and stop sequence as the reliable join fields.
- Some stop descriptions/headsigns are blank. Names can be ambiguous; the assistant should ask for clarification when a stop is not unique.
- The raw ZIP is temporary under `data/raw/` in Colab and is not committed. The prepared output retains source IDs and the manifest records retrieval date, source URL, hash and processing decisions.

## Prepared output

`data/processed/route_stop_lookup.csv.gz` joins each stop-time row to its trip, route and stop. It is sorted by route, direction, trip and `stop_sequence`. This is a lookup artefact, not a validated journey planner.

