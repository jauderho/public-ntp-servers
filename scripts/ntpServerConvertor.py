#!/usr/bin/python3

import yaml
import argparse
import re
import os


def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def extract_hostname(hostname_field):
    if isinstance(hostname_field, str) and hostname_field.startswith("[") and "](" in hostname_field and hostname_field.endswith(")"):
        match = re.search(r"\[([^\]]+)\]\(.*\)", hostname_field)
        if match:
            return match.group(1)
    return hostname_field


def generate_markdown(data):
    markdown = "|Hostname|AS|Stratum|Location|Owner|Notes|\n"  # Start directly with table header
    markdown += "|---|---|:---:|---|---|---|\n"
    current_location = None
    vm_servers = []

    for server in data["servers"]:
        if server.get("vm", False):
            vm_servers.append(server)
            continue
        if server["location"] != current_location:
            if current_location is not None:
                markdown += "||\n"
            current_location = server["location"]

        hostname = server["hostname"]
        asn = server.get("AS", "Unknown")
        stratum = server["stratum"]
        location = server["location"]
        owner = server["owner"]
        notes = server.get("notes", "")
        markdown += f"|{hostname}|{asn}|{stratum}|{location}|{owner}|{notes}|\n"

    if vm_servers:
        markdown += "\n\nThe following servers are known to be virtualized and may be less accurate. YMMV.\n\n"
        markdown += "|Hostname|AS|Stratum|Location|Owner|Notes|\n"
        markdown += "|---|---|:---:|---|---|---|\n"
        for server in vm_servers:
            hostname = server["hostname"]
            asn = server.get("AS", "Unknown")
            stratum = server["stratum"]
            location = server["location"]
            owner = server["owner"]
            notes = server.get("notes", "")
            markdown += f"|{hostname}|{asn}|{stratum}|{location}|{owner}|{notes}|\n"
    return markdown


def generate_chrony_conf(data):
    chrony_conf = "#\n# NTS servers in chrony format - Modified to standard NTP\n#\n\n"
    current_location = None
    vm_servers = []

    for server in data["servers"]:
        if server.get("vm", False):
            vm_servers.append(server)
            continue
        if server["location"] != current_location:
            if current_location is not None:
                chrony_conf += "\n"
            chrony_conf += f"# {server['location']}\n"
            current_location = server["location"]

        hostname = extract_hostname(server["hostname"])
        chrony_conf += f"server {hostname} iburst\n"

    if vm_servers:
        chrony_conf += "\n# Known VM servers (may be less accurate)\n"
        for server in vm_servers:
            hostname = extract_hostname(server["hostname"])
            chrony_conf += f"server {hostname} iburst\n"
    return chrony_conf


def generate_ntp_toml(data):
    ntp_toml = "#\n# NTS servers in ntpd-rs format - Modified to standard NTP server mode\n#\n\n"
    current_location = None
    vm_servers = []

    for server in data["servers"]:
        if server.get("vm", False):
            vm_servers.append(server)
            continue

        if server["location"] != current_location:
            if current_location is not None:
                ntp_toml += "\n"
            ntp_toml += f"# {server['location']}\n"
            current_location = server["location"]

        hostname = extract_hostname(server["hostname"])
        ntp_toml += f'[[source]]\nmode = "server"\naddress = "{hostname}"\n\n'

    if vm_servers:
        ntp_toml += "\n# Known VM servers (may be less accurate)\n"
        for server in vm_servers:
            hostname = extract_hostname(server["hostname"])
            ntp_toml += f'[[source]]\nmode = "server"\naddress = "{hostname}"\n\n'
    return ntp_toml


def update_readme(readme_path, new_content):
    try:
        with open(readme_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Warning: {readme_path} not found. Creating a new file with the content.")
        # Ensure new_content itself forms a valid complete document if README is missing
        full_new_content = f"## The List\n{new_content}" if not new_content.startswith("## The List") else new_content
        with open(readme_path, "w") as file:
            file.write(full_new_content)
        return

    start_marker = "## The List"
    end_marker = "## Star History"

    start_index = content.find(start_marker)

    if start_index == -1:
        print(f"Warning: Start marker '{start_marker}' not found in {readme_path}. Appending content to the end.")
        updated_content = content + "\n" + start_marker + "\n" + new_content # Ensure newlines
        with open(readme_path, "w") as file:
            file.write(updated_content)
        return

    # Content before the start marker (inclusive of the marker itself)
    before_start_marker = content[:start_index + len(start_marker)]
    
    # Find end marker after the start marker
    end_index = content.find(end_marker, start_index + len(start_marker))

    if end_index != -1:
        # Content after the new_content (from end_marker onwards)
        after_new_content = content[end_index:]
        updated_content = before_start_marker + "\n" + new_content + "\n" + after_new_content
    else:
        print(f"Warning: End marker '{end_marker}' not found after start marker in {readme_path}. Replacing content after start marker.")
        updated_content = before_start_marker + "\n" + new_content # Appends new_content, ensures a newline before it

    with open(readme_path, "w") as file:
        file.write(updated_content)


def main():
    parser = argparse.ArgumentParser(
        description="Convert NTP server data from YAML to Markdown, chrony.conf, or ntp.toml format"
    )
    parser.add_argument("input_file", default="ntp-sources.yml", nargs="?",
                        help="Path to the input YAML file (default: ntp-sources.yml)")
    args = parser.parse_args()
    
    try:
        data = load_yaml(args.input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{args.input_file}': {e}")
        return

    readme_path = "README.md" 
    chrony_path = "chrony.conf"
    toml_path = "ntp.toml"

    markdown_content = generate_markdown(data)
    update_readme(readme_path, markdown_content)
    print(f"Processed {readme_path}")

    chrony_content = generate_chrony_conf(data)
    with open(chrony_path, "w") as file:
        file.write(chrony_content)
    print(f"Written {chrony_path}")

    toml_content = generate_ntp_toml(data)
    with open(toml_path, "w") as file:
        file.write(toml_content)
    print(f"Written {toml_path}")

if __name__ == "__main__":
    main()
