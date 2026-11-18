# Week 3 Pipeline Decisions

## Requirement traceability

- **FR2 / O2:** route-to-stop lookup needs `routes.txt`, `trips.txt`, `stop_times.txt` and `stops.txt`.
- **FR3 / O2:** ordered stop sequences come from `stop_times.stop_sequence`.
- **FR4 / RAI1:** preserve route, trip and stop IDs to support answer provenance.
- **FR8 / NFR3 / NFR4:** record source URL, retrieval time, source hash, input counts, output hash and relationship.
- **RAI2 / RAI4:** use the static feed only, label it as schedule data, and disclose the provider’s incomplete-trip caveat.

## Part B preparation choice

The selected pathway is **B: structured/tabular data**. The downloaded official Rapid Bus KL GTFS feed contains multiple relational tables in CSV-compatible `.txt` files. Inspection showed 139 route rows, 2,118 trips, 4,107 stops, 88,801 stop-time rows and two calendar rows. Required route/trip/stop references were complete in the inspected snapshot. The provider notes approximately 2% of Rapid Bus KL trips have been removed from `stop_times.txt`.

The prepared artefact, `data/processed/route_stop_lookup.csv.gz`, joins stop times to trips, routes and stops; preserves source identifiers; and sorts by route, direction, trip and stop sequence. A wide joined lookup was chosen over copying all raw tables because it directly supports the project’s FR2/FR3 tasks. Raw source tables remain available from the source endpoint for audit; the raw ZIP is not committed. No dummy dataset was used.

## Alternatives and comparison

| Option | Evidence / trade-off | Decision |
|---|---|---|
| Keep each GTFS table separate | Preserves normalized source structure but every assistant lookup repeats several joins. | Keep raw in the temporary Colab raw folder; produce joined lookup for the prototype. |
| Build one route-stop table | Directly supports route membership and ordered-stop retrieval; repeats some route/trip attributes across rows. | Selected; preserve IDs and provenance to make repeats auditable. |
| Merge only the map PDF | Visual map gives broad network context but cannot reliably replace timetable rows or stop sequence records. | Not used for the executable pipeline. |

## Processing and operating choices

- **ETL:** extract source tables, inspect schema and identifiers, transform into the route-stop lookup, validate, then save prepared CSV and manifests. Transformation is performed after ingestion in Colab; this is ETL for the coursework pipeline.
- **Batch/streaming:** batch refresh is appropriate because this is a static schedule snapshot, not a real-time arrival feed. Record each retrieval date and hash; refresh before later evaluations.
- **Output locations:** Part B output: `data/processed/route_stop_lookup.csv.gz`; Part B lineage: `data/week3_manifest.json`; Part C output and manifest: `data/pipeline_v1/tabular/`.
- **Access and rights:** public Malaysia Open API; CC BY 4.0. Include attribution when redistributing prepared output. Do not commit raw downloads by default; if the instructor requires the full feed, retain the API source, license and snapshot hash.
- **Accepted limitation:** provider reports about 2% of Rapid Bus KL trips missing from `stop_times.txt`; do not infer non-operation from absent rows. The source calendar ends 2027-03-31 in the inspected snapshot.

## V1 stage contracts and failure responses

| Stage | Evidence / contract | Failure response |
|---|---|---|
| Ingest | HTTP success, valid ZIP, source URL, retrieval date and source SHA-256 recorded | Stop if request fails or ZIP CRC check fails. |
| Inspect | Required files and columns exist; row counts and representative records displayed | Stop with missing file/column name. |
| Prepare | Required joins resolve; output retains source identifiers and stop sequence | Stop if row loss or invalid keys are detected. |
| Validate | Unique primary keys, valid foreign keys, non-empty output, deterministic sort and hash | Stop with failed check and do not register a successful run. |
| Store | CSV and JSON manifest exist and are non-empty | Stop and report missing or empty artifact. |
| Record lineage | Source-to-output mapping, source/output hashes, date, license, method and caveat recorded | Stop if source-output mapping or metadata is absent. |

## Plausible failure points and response

1. API returns HTML/error page instead of a ZIP → ZIP validation fails; stop and retry only after checking the provider status.
2. Feed schema changes or required table is missing → schema contract fails; stop and update the reader only after inspecting the new schema.
3. Referential-integrity or join-row-count failure → do not export a trusted lookup; record the failing IDs/counts.
4. Feed omits some service trips → disclose the provider caveat and never interpret missing rows as proof a route is inactive.

