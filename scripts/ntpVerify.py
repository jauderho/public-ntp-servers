#!/usr/bin/python3
#
# Verify NTP servers with chronyd and report stratum and origin AS.
#
# Usage: scripts/ntpVerify.py <hostname> [<hostname> ...]
#
# Requires chronyd and dig. chronyd -Q does not need root.
#

import ipaddress
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile

CHRONYD = shutil.which("chronyd") or next(
    (p for p in ("/usr/local/sbin/chronyd", "/usr/sbin/chronyd", "/opt/homebrew/sbin/chronyd") if os.path.exists(p)),
    None,
)


HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)[A-Za-z0-9_]([A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?"
    r"(\.[A-Za-z0-9_]([A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?)*$"
)


def is_valid_hostname(hostname):
    """Accept only a DNS name or an IP literal."""
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return bool(HOSTNAME_RE.match(hostname))


def run(cmd, timeout):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None


def check_chronyd(hostname):
    """Query hostname once with chronyd. Returns (reachable, stratum)."""
    with tempfile.TemporaryDirectory() as logdir:
        result = run(
            [CHRONYD, "-Q", "-t", "8",
             f"server {hostname} iburst maxsamples 1", f"logdir {logdir}", "log measurements"],
            20,
        )
        reachable = result is not None and "System clock wrong" in result.stdout + result.stderr
        stratum = None
        log = os.path.join(logdir, "measurements.log")
        if os.path.exists(log):
            with open(log) as f:
                for line in f:
                    fields = line.split()
                    if len(fields) > 5 and fields[0][0].isdigit():
                        stratum = int(fields[4])
    return reachable, stratum


def origin_as(ip):
    """
    Look up the origin AS for an IP via Team Cymru DNS.
    Cymru returns one TXT record per covering prefix (e.g. a /24 and its /22),
    so keep only the most-specific prefix, which is what actually routes the address.
    """
    addr = ipaddress.ip_address(ip)
    zone = "origin.asn.cymru.com" if addr.version == 4 else "origin6.asn.cymru.com"
    rev = addr.reverse_pointer.rsplit(".", 2)[0]  # strip in-addr.arpa / ip6.arpa
    result = run(["dig", "+short", "TXT", f"{rev}.{zone}"], 10)
    records = []
    for line in result.stdout.splitlines() if result else []:
        fields = [f.strip() for f in line.strip('"').split("|")]
        if len(fields) >= 2 and "/" in fields[1]:
            records.append(fields)
    if not records:
        return set()
    best = max(records, key=lambda f: int(f[1].split("/")[1]))
    return {f"AS{asn}" for asn in best[0].split()}


def get_as_numbers(hostname):
    """Return sorted AS numbers across all IPv4/IPv6 addresses, e.g. 'AS1140, AS215088'."""
    as_numbers = set()
    try:
        ips = {info[4][0] for info in socket.getaddrinfo(hostname, 123)}
    except socket.gaierror:
        return None
    for ip in ips:
        as_numbers |= origin_as(ip)
    return ", ".join(sorted(as_numbers, key=lambda a: int(a[2:]))) or None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hostname> [<hostname> ...]")
        sys.exit(1)
    if not CHRONYD:
        print("chronyd not found")
        sys.exit(1)

    failed = False
    for hostname in sys.argv[1:]:
        if not is_valid_hostname(hostname):
            print(f"{hostname!r}: invalid hostname", flush=True)
            failed = True
            continue
        reachable, stratum = check_chronyd(hostname)
        failed |= not reachable
        print(
            f"{hostname}: chronyd={'OK' if reachable else 'FAIL'} "
            f"stratum={stratum if stratum is not None else '?'} "
            f"AS={get_as_numbers(hostname) or '?'}",
            flush=True,
        )
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
