# Week 1 Project Scope

## Project name
Rapid KL Bus Route Assistant

## Domain
Public transport information and natural-language access to structured transit schedules.

## Problem statement
Rapid KL bus information can be explored through maps and timetable datasets, but the GTFS feed separates a rider's question across route, trip, stop, and stop-time tables. A new or occasional rider may need help translating a plain-language question into the correct linked records. This project will test that need with a small set of rider tasks rather than assume that all riders experience the same difficulty.

## Evidence and data feasibility
The official Malaysia GTFS Static API documents standardized route, stop, trip, stop-time, and calendar files and provides a Prasarana `rapid-bus-kl` feed under CC BY 4.0. A live download reviewed on 18 November 2026 was a valid ZIP with 139 routes, 4,107 stops, 2,118 trips, and 88,801 stop-time records. The route, trip, stop and service references checked without orphan records, and a sample lookup linked “STESEN BRT SETIA JAYA” to route `B1000`. The feed provider also documents that approximately 2% of Rapid Bus KL trips have been removed from `stop_times.txt` because of operational issues; the prototype must disclose this coverage limitation.

Sources:

1. [Official GTFS Static API documentation](https://developer.data.gov.my/realtime-api/gtfs-static)
2. [Rapid Bus KL GTFS feed endpoint](https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl)
3. [Klang Valley Integrated Transit Map (PDF)](https://myrapid.com.my/wp-content/uploads/2025/10/Transit-Map_131025.pdf)
4. [Rapid KL service-use guide (PDF)](https://myrapid.com.my/wp-content/uploads/2024/10/Booklet_Panduan-Penggunaan-Perkhidmatan-Rapid-KL_c.pdf)

## Existing approaches

1. **Official GTFS feed and data portal:** provides structured schedule and stop data. Limitation for this project: answering rider questions requires joining multiple tables and interpreting stop or route references.
2. **Official integrated transit map:** gives a visual network overview. Limitation: map labels are not as directly searchable as structured stop records and do not provide a conversational query interface.
3. **General map or transit apps:** provide route search and navigation features. Limitation for this project: answers and source provenance may not expose the exact GTFS records or feed coverage caveats used in this coursework prototype.

## Engineering gap
A small, testable prototype can connect natural-language rider questions to exact GTFS route/stop records, state the feed date, and show its supporting source identifiers. The project makes no claim that current tools lack these features universally; the comparison will be limited to the selected tasks and sources.

## Objectives

- **O1:** Design a source-grounded assistant for answering selected Rapid KL bus route and stop questions.
- **O2:** Build a prototype that maps natural-language questions to structured GTFS records and returns traceable answers.
- **O3:** Evaluate answer correctness, grounding, scope handling, and response time on a defined question set.

## Intended users
New or occasional Rapid KL bus riders who need to look up route and stop sequence information.

## Supported tasks

- Find which listed routes serve a named stop.
- Check whether a named stop is included in a selected route or trip.
- Show the ordered stops for a selected trip where the feed contains stop-time records.
- Explain what feed date and source records support the answer.

## Explicit out-of-scope tasks

- Live arrival times, service alerts, delays, or predictions.
- Fare calculation, trip transfers, or end-to-end optimized journey planning.
- Confirming that a service is currently operating or that a stop is accessible.
- Inferring missing records or claiming complete coverage.

## Constraints and risks

- Feed data can change; each prepared snapshot must carry retrieval date and hash.
- The provider documents a missing-trips issue affecting roughly 2% of Rapid Bus KL trips in `stop_times.txt`.
- Stop names may be duplicated, abbreviated, or expressed in Malay/English variants; ambiguous queries should trigger clarification.
- Users may mistake a schedule lookup for real-time advice; every response must label the data as static.

## Evaluation focus
Can the prototype answer supported route/stop questions accurately from the selected feed, cite the relevant route/stop/trip records, abstain on unsupported or ambiguous questions, and respond within the proposed latency threshold?

