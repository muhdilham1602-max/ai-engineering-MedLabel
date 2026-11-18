# Data directory

The project uses official Prasarana GTFS Static data from Malaysia's Open API. All feeds are licensed CC BY 4.0.

## Bus feed

The Rapid Bus KL feed (`rapid-bus-kl`) is downloaded by `notebooks/week3_pipeline.ipynb` from:

`https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl`

The downloaded source ZIP is temporary and excluded from Git. Record retrieval date, source URL, SHA-256, attribution and validation results in the generated manifest. The provider documents about 2% of Rapid Bus KL trips missing from `stop_times.txt`.

Part B's prepared table is `processed/route_stop_lookup.csv.gz`, with lineage in `week3_manifest.json`. Part C's pipeline result and manifest are in `pipeline_v1/tabular/`.

## Rail feed

A Rapid Rail KL static snapshot (`rapid-rail-kl`) retrieved 18 November 2026 is stored at `raw/rapid-rail-kl-gtfs.zip`; its attribution, SHA-256 and row counts are in `rail_manifest.json`. Source:

`https://api.data.gov.my/gtfs-static/prasarana?category=rapid-rail-kl`

This snapshot contains routes, stops, trips, stop_times, calendars, frequencies and shapes. It does not contain `transfers.txt` or `pathways.txt`; multi-line and bus-to-rail transfers require separate validated connection data. Refresh the feed and check service calendar expiry before using scheduled times. The archive is retained for reproducibility; verify against the official endpoint before deployment.

