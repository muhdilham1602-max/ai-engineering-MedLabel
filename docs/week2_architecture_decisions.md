# Week 2 Architecture Decisions and Traceability

## V1 conceptual architecture

See [`week2_architecture_v1.png`](week2_architecture_v1.png). The diagram is conceptual. It names capabilities, not specific vendors or frameworks. Structured GTFS records remain the source of truth; a language model may interpret the question and phrase a response but may not supply route facts from memory.

## Architecture decision records

| Decision | Requirement / constraint | Alternatives considered | Selected option | Trade-off accepted |
|---|---|---|---|---|
| ADR1: use official static GTFS as route/stop source | FR2–FR4, RAI1; need route, stop, trip and ordered stop-time facts | General web search; manually maintained list; official GTFS | Parse and join the official Prasarana `rapid-bus-kl` feed | Reproducible structured facts and source IDs; joins and feed-quality caveats add complexity. |
| ADR2: keep structured retrieval as authority | FR2–FR4, RAI1 | Ask a language model to answer from its pretrained knowledge; generate from summaries only | Parse intent, query structured tables, pass retrieved rows to response composer | More constrained output and easier auditing; only supported query shapes can be answered. |
| ADR3: clarify duplicate stop names | FR5, RAI3 | Guess the most common match; show all matches; ask for clarification | Ask for area/context when matches are ambiguous | Adds a user turn but reduces wrong-stop answers. |
| ADR4: exclude real-time, fares and transfer planning from V1 | FR6–FR7, RAI2; static GTFS does not establish live conditions and trip coverage has a documented gap | Extend to live APIs and multi-leg routing; make schedule-only prototype | Restrict to route/stop and scheduled-sequence lookups | Smaller semester scope and lower risk of misleading riders; fewer supported tasks. |
| ADR5: preserve snapshot provenance | FR8, NFR3–NFR4, RAI4 | Always query live without a record; manually replace files | Save retrieval timestamp, URL, feed hash, table counts and validation report | Repeatable evaluation and transparent freshness; requires refresh/manifest steps. |

## Initial requirements traceability matrix

| Objective | Requirement | Evaluation criterion | Architecture element | Later evidence |
|---|---|---|---|---|
| O1 | FR4, RAI1 | E3 grounded response | Provenance formatter and source-row references | Answer audit sheet with source IDs |
| O1 | FR5, RAI3 | E4 ambiguity cases | Stop-name resolver and clarification control | Ambiguous-name test results |
| O2 | FR2, FR3 | E1 route-stop and E2 sequence correctness | GTFS relational tables / query layer | Direct-query comparison results |
| O2 | FR8, NFR3, NFR4 | Repeatability and integrity checks | Ingestion/validation stage and manifest | Feed hash, table counts and rerun logs |
| O3 | NFR1, NFR2, NFR5 | E1, E5, E7 | Evaluation harness and user task session | Accuracy, latency and task-completion results |
| O3 | RAI2, RAI4 | E4 boundary cases | Static-data scope control and feed-caveat notice | Realtime/coverage scenario results |

## Review notes

- The live Rapid Bus KL feed snapshot inspected on 18 November 2026 had internally consistent route/trip/stop references in basic checks, but the provider explicitly reports a small missing-trip issue in `stop_times.txt`.
- Do not infer real-world service absence from a missing scheduled trip in this snapshot.
- Keep raw feed downloads out of public Git history unless required; cite the CC BY 4.0 source and record the snapshot hash and date in later pipeline artefacts.

