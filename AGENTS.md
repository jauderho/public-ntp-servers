# AGENTS.md

- Scan the URL provided or GitHub Issue for any relevant information
- Extract hostname and verify that the NTP server is reachable
- Place new entry in the proper location in ntp-sources.yml by alphabetical country
- Do not make direct changes to README.md, chrony.conf and ntp.toml. Run scripts/ntpServerConvertor.py to update after changes to ntp-sources.yml are completed
- Leverage logic from scripts/ntpUpdateSources.py to determine AS and stratum if information is not provided
