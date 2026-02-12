#!/usr/bin/env python3
import yaml
import ntplib
import socket
import requests
import time
import re
import sys
import os

def extract_hostname(hostname_field):
    if isinstance(hostname_field, str) and hostname_field.startswith("[") and "](" in hostname_field and hostname_field.endswith(")"):
        match = re.search(r"\[([^\]]+)\]\(.*\)", hostname_field)
        if match:
            return match.group(1)
    return hostname_field

def get_stratum(hostname):
    client = ntplib.NTPClient()
    try:
        response = client.request(hostname, version=3, timeout=2)
        return response.stratum
    except Exception:
        return None

def get_as_info(hostname):
    try:
        # Get all IP addresses for the hostname
        _, _, ip_list = socket.gethostbyname_ex(hostname)
        as_numbers = set()

        for ip in ip_list:
            # Using ip-api.com free tier. Limit is 45 requests per minute.
            # We'll do individual lookups for simplicity but keep track of time.
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}?fields=as", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if "as" in data and data["as"]:
                        # data["as"] usually looks like "AS12345 Name of AS"
                        match = re.search(r"AS(\d+)", data["as"])
                        if match:
                            as_numbers.add(f"AS{match.group(1)}")

                # Rate limiting: 45 requests per minute is ~1.33 seconds per request
                time.sleep(1.5)
            except Exception as e:
                print(f"Error looking up AS for IP {ip}: {e}")

        if as_numbers:
            return ", ".join(sorted(list(as_numbers), key=lambda x: int(x[2:])))
    except Exception as e:
        print(f"Error resolving hostname {hostname}: {e}")

    return None

def main():
    yaml_file = "ntp-sources.yml"
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found.")
        sys.exit(1)

    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    updated = False
    for server in data.get('servers', []):
        hostname_field = server.get('hostname')
        hostname = extract_hostname(hostname_field)

        as_val = server.get('AS')
        stratum_val = server.get('stratum')

        needs_as = as_val == "Unknown"
        needs_stratum = stratum_val == "Unknown"

        if needs_as or needs_stratum:
            print(f"Processing {hostname}...")

            if needs_stratum:
                new_stratum = get_stratum(hostname)
                if new_stratum:
                    print(f"  Found stratum: {new_stratum}")
                    server['stratum'] = new_stratum
                    updated = True
                else:
                    print(f"  Could not determine stratum for {hostname}")

            if needs_as:
                new_as = get_as_info(hostname)
                if new_as:
                    print(f"  Found AS: {new_as}")
                    server['AS'] = new_as
                    updated = True
                else:
                    print(f"  Could not determine AS for {hostname}")

    if updated:
        with open(yaml_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
        print(f"\nSuccessfully updated {yaml_file}")
    else:
        print("\nNo updates were made.")

if __name__ == "__main__":
    main()
