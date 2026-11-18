# Data directory

The project uses the official Rapid Bus KL static GTFS feed (`rapid-bus-kl`) from Malaysia's Open API, licensed CC BY 4.0. Retrieve the feed from https://api.data.gov.my/gtfs-static/prasarana?category=rapid-bus-kl and record its retrieval date, SHA-256 hash, source attribution and validation results in a manifest. The provider documents a missing-trip caveat affecting approximately 2% of trips in `stop_times.txt`.

Part B's prepared table is `processed/route_stop_lookup.csv.gz`, with lineage in `week3_manifest.json`. Part C's executable pipeline result and manifest are in `pipeline_v1/tabular/`. The compressed CSV is gzip-compressed UTF-8 CSV and is readable with `pandas.read_csv(path)` or standard gzip tools. Raw downloads are temporary and excluded from Git.

