# Week 2 Requirements Specification

## 0. Project framing and application scope

**Project:** Rapid KL Bus Route Assistant. **Users:** new or occasional riders. **Problem:** route, trip, stop and stop-time facts are distributed across linked GTFS tables; a plain-language lookup should return an answer traceable to the underlying records. The project will test this with a curated question set and must not claim that the feed is complete.

**Evidence/data:** Official Malaysia GTFS Static API documentation; the Prasarana `rapid-bus-kl` GTFS feed; the October 2025 Klang Valley Integrated Transit Map; and the 2024 Rapid KL service-use guide. Feed licence is CC BY 4.0 per the API documentation. A snapshot fetched on 18 November 2026 yielded 139 routes, 4,107 stops, 2,118 trips, 88,801 stop-time rows and 2 service calendar records. Basic uniqueness and foreign-key checks passed. Provider caveat: approximately 2% of Rapid Bus KL trips were removed from `stop_times.txt` due to operational issues.

**Existing approaches:** official structured GTFS data (machine-readable but requires linked-table lookup); official transit map (useful overview, less directly queryable); general map/transit applications (convenient, but this project will not assume their internal data or provenance).

**Engineering gap:** evaluate a small natural-language interface that retrieves exact records from the official static feed, reports provenance/freshness and handles unsupported questions safely. This is a coursework engineering gap, not a claim of research novelty.

**Objectives:** O1 design the source-grounded assistant; O2 implement question-to-GTFS retrieval and answer generation; O3 evaluate correctness, groundedness, scope control and latency.

**Scope:** look up routes serving a named stop, whether a stop belongs to a selected route/trip, and ordered stops for a selected trip. Static scheduled data only. No live arrivals, disruptions, fare calculation, transfers, accessibility confirmation, or optimized end-to-end trip planning. Ambiguous stop names require clarification.

**Constraints:** public CC BY 4.0 feed, changing snapshots, documented missing-trip caveat, name ambiguity, single semester, and no official service status. Store source date/hash and retain attribution.

## 1. Functional requirements

| ID | Requirement | Objective | Acceptance evidence |
|---|---|---|---|
| FR1 | The system shall identify route, stop, or trip lookup intent from a supported natural-language question. | O1, O2 | Curated intent set with expected lookup type. |
| FR2 | The system shall list route identifiers and names serving a uniquely identified stop using linked GTFS records. | O2 | Compare result set against direct GTFS joins. |
| FR3 | The system shall return the ordered stops for a selected trip using `stop_times.stop_sequence`. | O2 | Compare ordered output against source records. |
| FR4 | The system shall cite the feed retrieval date and relevant source identifiers (route, stop, trip, and/or source file) for each factual answer. | O1, O2 | Inspect answer and provenance fields. |
| FR5 | The system shall ask a clarification question when a stop or route reference is ambiguous. | O1, O2 | Ambiguous-name scenarios. |
| FR6 | The system shall state that the feed is static and shall not present a scheduled time as a live arrival estimate. | O1, O2 | Realtime-query scenarios. |
| FR7 | The system shall abstain and direct users to the official provider when a request is outside the supported dataset or requires current operational status. | O1, O2 | Out-of-scope scenarios. |
| FR8 | The system shall allow the operator to refresh the GTFS snapshot and record its retrieval timestamp, source URL, file hash, and validation summary. | O2 | Refresh run manifest. |

## 2. Non-functional requirements

Thresholds below are provisional engineering targets for the coursework prototype; validate them with a small intended-user task session and revise if needed.

| ID | Quality | Requirement and measurement | Threshold |
|---|---|---|---|
| NFR1 | Correctness | On a frozen set of 50 supported lookups, measure exact match of route/stop result sets against direct GTFS queries. | At least 90% exact-match accuracy. |
| NFR2 | Latency | Measure end-to-end response time for the same 50 questions on the documented Colab/runtime setup. | p95 no more than 5 seconds, excluding feed download. |
| NFR3 | Reliability | Run the pipeline five times on the same archived feed snapshot and compare prepared-table counts, source hash and key outputs. | 5/5 runs produce identical data fingerprints and counts. |
| NFR4 | Data integrity | Count duplicate primary keys and unresolved foreign-key references across routes, trips, stops, stop_times and calendar. | Zero duplicate primary keys and zero unresolved required references, or documented stop-and-report failure. |
| NFR5 | Usability | Ask at least five intended users to complete five representative lookup tasks; collect task completion and a 1–5 clarity rating. | At least 80% task completion and median clarity rating of 4/5 or higher. |

## 3. Responsible AI requirements

| ID | Risk/control | Requirement | Measurement and threshold |
|---|---|---|---|
| RAI1 | Grounding and hallucination | The system shall only state route/stop facts supported by retrieved GTFS rows and shall show source identifiers. | Audit 50 answers: at least 95% of factual claims supported by cited rows; unsupported claim rate 0%. |
| RAI2 | Misleading real-time use | The system shall label data as static schedule information and refuse live arrival/status claims. | Test 10 realtime/status prompts: 10/10 clearly state limitation and link to official service channel. |
| RAI3 | Ambiguity | The system shall ask for clarification instead of choosing among duplicate or uncertain stop names. | Test all ambiguous cases in the evaluation set: 100% clarification before route claims. |
| RAI4 | Coverage transparency | The system shall disclose the provider's documented missing-trip caveat when describing coverage and shall not claim the feed is complete. | Review README and relevant responses: caveat appears in all project documentation and applicable responses. |
| RAI5 | Privacy | The system shall not request or store sensitive personal data; question logs used for evaluation shall be anonymized and contain no account identifiers. | Inspect log schema and sample logs: zero personal-data fields. |
| RAI6 | Language handling | The system shall handle supported English and Malay stop queries without materially worse lookup accuracy in either language. | Compare English/Malay test subsets: each at least 85% exact-match accuracy and gap no more than 10 percentage points. |

## Objective-to-requirement links

- O1: FR1, FR4–FR7, RAI2–RAI4.
- O2: FR2–FR3, FR8, NFR3–NFR4, RAI1, RAI5–RAI6.
- O3: NFR1–NFR2, NFR5, and the measurable RAI criteria.

## Source register

- GTFS API documentation: https://developer.data.gov.my/realtime-api/gtfs-static
- Rapid Bus KL feed: https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl
- Transit map (October 2025): https://myrapid.com.my/wp-content/uploads/2025/10/Transit-Map_131025.pdf
- Rapid KL guide (2024): https://myrapid.com.my/wp-content/uploads/2024/10/Booklet_Panduan-Penggunaan-Perkhidmatan-Rapid-KL_c.pdf

