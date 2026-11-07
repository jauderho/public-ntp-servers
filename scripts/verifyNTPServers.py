#!/usr/bin/python3

import yaml
import argparse
import subprocess
import re
import ipaddress


def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def extract_hostname(hostname_field):
    # Extract hostname from potential markdown link
    match = re.search(r"\[([^\]]+)\]", hostname_field)
    if match:
        return match.group(1)
    return hostname_field


HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)[A-Za-z0-9_]([A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?"
    r"(\.[A-Za-z0-9_]([A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?)*$"
)


def is_valid_hostname(hostname):
    """Accept only a DNS name or an IP literal (no whitespace, quotes or shell/chrony syntax)."""
    if not isinstance(hostname, str):
        return False
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return bool(HOSTNAME_RE.match(hostname))


def verify_ntp_server(hostname):
    print(f"Verifying {hostname!r} ...", end="", flush=True)
    if not is_valid_hostname(hostname):
        print(" Failed")
        print(f"Invalid hostname: {hostname!r}\n")
        return False
    # Argument list, no shell: hostname can never be interpreted as shell syntax
    command = ["chronyd", "-Q", "-t", "5", f"server {hostname} iburst maxsamples 1"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(" Good")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(" Failed")
        print(f"Error verifying {hostname}: {e}")
        print((e.output or "").strip())
        print()
        return False
    except FileNotFoundError:
        print(" Failed")
        print("chronyd not found\n")
        return False
    print()  # Add a newline for better readability
    return True


def main():
    parser = argparse.ArgumentParser(description="Verify NTP server connectivity")
    parser.add_argument("yaml_file", help="Path to the input YAML file")
    parser.add_argument("--hostname", help="Specific hostname to verify (optional)")

    args = parser.parse_args()

    data = load_yaml(args.yaml_file)

    if args.hostname:
        verify_ntp_server(args.hostname)
    else:
        hostnames = [extract_hostname(server["hostname"]) for server in data["servers"]]
        for hostname in hostnames:
            verify_ntp_server(hostname)


if __name__ == "__main__":
    main()
