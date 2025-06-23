# AGENTS.md

- Scan the URL provided or GitHub Issue for any relevant information
- Extract hostname and verify that the NTP server is reachable
- Place new entry in the proper location in ntp-sources.yml by alphabetical country
- Leverage logic from scripts/ntpUpdateSources.py to determine AS and stratum if information is not provided
