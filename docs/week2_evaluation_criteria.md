# Week 2 Evaluation Criteria

The evaluation checks whether the assistant can answer supported Rapid KL bus route/stop questions from the official static GTFS feed. Freeze and hash one feed snapshot before running tests; record each expected answer from direct table queries. Do not use this evaluation to claim real-time service accuracy.

| Criterion | Requirement / objective | Capability bucket | Method and metric | Usefulness threshold |
|---|---|---|---|---|
| E1: route-stop correctness | FR2, NFR1 / O2, O3 | Domain-specific capability | 50 questions about which routes serve a named stop; compare exact route-ID sets with direct GTFS joins. | At least 90% exact matches; a wrong route can send a rider to the wrong service. |
| E2: stop sequence correctness | FR3, NFR1 / O2, O3 | Domain-specific capability | 20 trip/route sequence prompts; compare ordered stop IDs/names with `stop_times` sorted by `stop_sequence`. | At least 90% exact sequence matches. |
| E3: grounded response | FR4, RAI1 / O1, O2, O3 | Generation capability | Audit 50 factual answers for claim support and usable source identifiers; compute supported-claim rate and unsupported-claim count. | At least 95% supported claims; zero unsupported route facts. |
| E4: instruction and boundary handling | FR5–FR7, RAI2–RAI4 / O1, O2, O3 | Instruction-following capability | Test 10 ambiguous stops, 10 realtime/status prompts, and 10 unsupported requests. Score correct clarification/refusal and static-data disclosure. | 100% correct boundary behavior in the 30 cases. |
| E5: response time | NFR2 / O3 | Cost and latency | Measure end-to-end p50 and p95 over 50 supported prompts on the documented runtime, excluding feed download. | p95 ≤ 5 seconds. |
| E6: English/Malay parity | RAI6 / O2, O3 | Domain-specific capability | Use balanced English/Malay variants for the same stops; compare exact-match accuracy by language. | Each ≥85%; absolute gap ≤10 percentage points. |
| E7: user task usefulness | NFR5 / O3 | Instruction-following capability | Five intended users each complete five lookup tasks; record completion rate and 1–5 clarity score. | ≥80% completion and median clarity ≥4/5. |

## Test set design

Include common stop-name lookups, route membership, ordered stops, duplicate/ambiguous stop names, Malay and English variants, nonexistent stops, out-of-area requests, and live-arrival requests. Keep a separate ground-truth sheet with source row identifiers. Include the official feed caveat in the test context and never score absent trips as evidence the real bus does not operate.

