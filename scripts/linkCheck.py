#!/usr/bin/env python3
"""
YAML Hostname to Markdown Converter

Processes YAML files to convert plaintext hostnames to markdown links
when the hostname has an active HTTPS website. Also verifies existing
markdown links and converts back to plaintext if unreachable.
"""

import argparse
import sys
import urllib.request
import urllib.error
import socket
import ssl
import re
from pathlib import Path
import yaml


def is_markdown_link(hostname):
    """Check if hostname is already in markdown format."""
    return bool(re.match(r'^\[.*\]\(.*\)$', hostname.strip()))


def extract_hostname_from_markdown(markdown_text):
    """Extract hostname from markdown link format [text](url)."""
    match = re.match(r'^\[(.*?)\]\((.*?)\)$', markdown_text.strip())
    if match:
        link_text, url = match.groups()
        # Extract hostname from URL
        if url.startswith(('http://', 'https://')):
            hostname = url.split('://', 1)[1].split('/')[0]
            return hostname, url, link_text
        else:
            # URL without protocol, assume it's just the hostname
            return url.split('/')[0], url, link_text
    return None, None, None


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Custom handler that prevents automatic redirect following."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    def http_error_301(self, req, fp, code, msg, headers):
        return fp


def test_https_connectivity(hostname, timeout=5):
    """
    Test if hostname is reachable via HTTPS only.
    Skips processing if the first response is a redirect (301/302).
    Skips processing if HTTPS has invalid or self-signed certificates.
    
    Args:
        hostname (str): The hostname to test
        timeout (int): Connection timeout in seconds
    
    Returns:
        str or None: Returns the working HTTPS URL or None if unreachable
    """
    # Clean hostname - remove any existing protocol
    clean_hostname = hostname.strip()
    if clean_hostname.startswith(('http://', 'https://')):
        clean_hostname = clean_hostname.split('://', 1)[1]
    
    # Remove trailing slash and path
    clean_hostname = clean_hostname.split('/')[0].lower()
    
    # Only test HTTPS
    url = f"https://{clean_hostname}"
    
    try:
        # Create opener with no-redirect handler
        no_redirect_handler = NoRedirectHandler()
        
        # Use default SSL context with proper certificate validation
        ssl_context = ssl.create_default_context()
        https_handler = urllib.request.HTTPSHandler(context=ssl_context)
        opener = urllib.request.build_opener(https_handler, no_redirect_handler)
        
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (compatible; YAML-Processor/1.0)')]
        
        # Create request
        req = urllib.request.Request(url)
        
        response = opener.open(req, timeout=timeout)
        
        if 200 <= response.status < 300:
            # Direct success (2xx status) - no redirect
            print(f"Success: {url} returned {response.status}")
            return url
        elif 300 <= response.status < 400:
            # Any redirect (301/302/etc.) - skip processing
            print(f"Skipping {url} - returns redirect ({response.status})")
            return None
                    
    except ssl.SSLError as e:
        # SSL certificate errors (invalid, self-signed, expired, etc.)
        print(f"Skipping {url} - SSL certificate error: {e}")
        return None
    except ssl.CertificateError as e:
        # Certificate validation errors
        print(f"Skipping {url} - certificate validation error: {e}")
        return None
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (4xx, 5xx) and redirects caught as errors
        if 300 <= e.code < 400:
            print(f"Skipping {url} - returns redirect ({e.code})")
        return None
    except (urllib.error.URLError, socket.timeout, 
            ConnectionRefusedError, OSError) as e:
        # Check if the error is SSL-related within URLError
        if isinstance(e.reason, ssl.SSLError):
            print(f"Skipping {url} - SSL error: {e.reason}")
        return None
    
    return None


def create_markdown_link(hostname, url):
    """Create markdown link format."""
    return f"[{hostname}]({url})"


def process_yaml_content(content, dry_run=False, timeout=5):
    """
    Process YAML content to convert hostnames to/from markdown links.
    
    Args:
        content (dict): Parsed YAML content
        dry_run (bool): If True, only show what would be changed
        timeout (int): Connection timeout in seconds
    
    Returns:
        tuple: (modified_content, changes_made)
    """
    changes_made = []
    
    if 'servers' not in content:
        print("Warning: No 'servers' key found in YAML")
        return content, changes_made
    
    for i, server in enumerate(content['servers']):
        if 'hostname' not in server:
            continue
            
        hostname_field = server['hostname']
        
        # Handle existing markdown links
        if is_markdown_link(hostname_field):
            extracted_hostname, original_url, link_text = extract_hostname_from_markdown(hostname_field)
            
            if extracted_hostname:
                print(f"Testing existing markdown link: {hostname_field}")
                
                # Skip NTP pool hostnames
                if extracted_hostname.lower().endswith('.pool.ntp.org'):
                    print(f"Skipping {extracted_hostname} (NTP pool hostname)")
                    continue
                
                # Test if the extracted hostname is still reachable via HTTPS
                working_url = test_https_connectivity(extracted_hostname, timeout)
                
                if not working_url:
                    # Convert back to plaintext hostname
                    if dry_run:
                        print(f"[DRY RUN] Would revert to plaintext: {hostname_field} -> {extracted_hostname}")
                        changes_made.append({
                            'index': i,
                            'old': hostname_field,
                            'new': extracted_hostname,
                            'action': 'revert_to_plaintext'
                        })
                    else:
                        print(f"Reverting to plaintext: {hostname_field} -> {extracted_hostname}")
                        server['hostname'] = extracted_hostname
                        changes_made.append({
                            'index': i,
                            'old': hostname_field,
                            'new': extracted_hostname,
                            'action': 'revert_to_plaintext'
                        })
                else:
                    print(f"Existing markdown link is valid: {hostname_field}")
            continue
        
        # Handle plaintext hostnames
        hostname = hostname_field.strip()
        
        # Skip NTP pool hostnames
        if hostname.lower().endswith('.pool.ntp.org'):
            print(f"Skipping {hostname} (NTP pool hostname)")
            continue
        
        print(f"Testing plaintext hostname: {hostname}")
        
        # Test HTTPS connectivity
        working_url = test_https_connectivity(hostname, timeout)
        
        if working_url:
            markdown_link = create_markdown_link(hostname, working_url)
            
            if dry_run:
                print(f"[DRY RUN] Would convert to markdown: {hostname} -> {markdown_link}")
                changes_made.append({
                    'index': i,
                    'old': hostname,
                    'new': markdown_link,
                    'url': working_url,
                    'action': 'convert_to_markdown'
                })
            else:
                print(f"Converting to markdown: {hostname} -> {markdown_link}")
                server['hostname'] = markdown_link
                changes_made.append({
                    'index': i,
                    'old': hostname, 
                    'new': markdown_link,
                    'url': working_url,
                    'action': 'convert_to_markdown'
                })
        else:
            print(f"No working HTTPS URL found for: {hostname}")
    
    return content, changes_made


def write_yaml_with_formatting(content, output_path):
    """
    Write YAML with proper formatting including newlines between entries.
    """
    # Custom YAML representer to handle formatting
    def str_presenter(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, str_presenter)
    
    # Write YAML with custom formatting
    yaml_str = yaml.dump(content, default_flow_style=False, sort_keys=False, 
                        allow_unicode=True, width=1000)
    
    # Add newlines between server entries for readability
    lines = yaml_str.split('\n')
    formatted_lines = []
    
    for i, line in enumerate(lines):
        formatted_lines.append(line)
        # Add blank line after 'vm: false' (end of server entry)
        if line.strip().startswith('vm:') and i < len(lines) - 1:
            if lines[i + 1].strip().startswith('- hostname:'):
                formatted_lines.append('')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_lines))


def main():
    parser = argparse.ArgumentParser(
        description='Convert plaintext hostnames to HTTPS markdown links in YAML files. '
                   'Also verifies existing markdown links and reverts to plaintext if unreachable.'
    )
    parser.add_argument('input_file', help='Input YAML file path')
    parser.add_argument('-o', '--output', help='Output file path (default: overwrite input)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without modifying files')
    parser.add_argument('--timeout', type=int, default=5,
                       help='Connection timeout in seconds (default: 5)')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"Error: '{input_path}' is not a file")
        sys.exit(1)
    
    # Set output path
    output_path = Path(args.output) if args.output else input_path
    
    # Validate output path (only if different from input)
    if args.output and output_path.exists() and output_path.is_dir():
        print(f"Error: Output path '{output_path}' is a directory")
        sys.exit(1)
    
    try:
        # Load YAML content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        if content is None:
            print("Error: Empty or invalid YAML file")
            sys.exit(1)
        
        server_count = len(content.get('servers', []))
        print(f"Processing {server_count} server entries...")
        
        if server_count == 0:
            print("Warning: No server entries found in YAML")
            return
        
        # Process content
        modified_content, changes = process_yaml_content(content, args.dry_run, args.timeout)
        
        # Report results
        if changes:
            print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
            
            convert_count = sum(1 for c in changes if c.get('action') == 'convert_to_markdown')
            revert_count = sum(1 for c in changes if c.get('action') == 'revert_to_plaintext')
            
            if convert_count > 0:
                print(f"- {convert_count} hostname(s) converted to HTTPS markdown links")
            if revert_count > 0:
                print(f"- {revert_count} markdown link(s) reverted to plaintext (unreachable)")
            
            print("\nChanges:")
            for change in changes:
                action_desc = "→ HTTPS link" if change.get('action') == 'convert_to_markdown' else "→ plaintext"
                print(f"  • {change['old']} {action_desc}")
        else:
            print("\nNo changes made - all hostnames are already in correct format")
        
        # Write output (unless dry run)
        if not args.dry_run and changes:
            write_yaml_with_formatting(modified_content, output_path)
            print(f"\nOutput written to: {output_path}")
        elif args.dry_run:
            print(f"\n[DRY RUN] Would write to: {output_path}")
            
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading/writing file: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
