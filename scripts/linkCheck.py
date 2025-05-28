#!/usr/bin/env python3
"""
YAML Hostname to Markdown Converter

Processes YAML files to convert plaintext hostnames to markdown links
when the hostname has an active website (HTTP/HTTPS).
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


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Custom handler that prevents automatic redirect following."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    def http_error_301(self, req, fp, code, msg, headers):
        return fp


def test_url_connectivity(hostname, timeout=5):
    """
    Test if hostname is reachable via HTTP or HTTPS.
    Skips processing if the first response is a redirect (301/302).
    Skips processing if HTTPS has invalid or self-signed certificates.
    Prefers HTTPS over HTTP if both are available.
    
    Args:
        hostname (str): The hostname to test
        timeout (int): Connection timeout in seconds
    
    Returns:
        str or None: Returns the working URL (with protocol) or None if unreachable
    """
    # Clean hostname - remove any existing protocol
    clean_hostname = hostname.strip()
    if clean_hostname.startswith(('http://', 'https://')):
        clean_hostname = clean_hostname.split('://', 1)[1]
    
    # Remove trailing slash and path
    clean_hostname = clean_hostname.split('/')[0].lower()
    
    # Test both protocols and collect results
    working_urls = []
    protocols = ['https', 'http']
    
    for protocol in protocols:
        url = f"{protocol}://{clean_hostname}"
        try:
            # Create opener with no-redirect handler
            no_redirect_handler = NoRedirectHandler()
            
            if protocol == 'https':
                # Use default SSL context with proper certificate validation
                ssl_context = ssl.create_default_context()
                # Do NOT disable certificate verification for HTTPS
                https_handler = urllib.request.HTTPSHandler(context=ssl_context)
                opener = urllib.request.build_opener(https_handler, no_redirect_handler)
            else:
                opener = urllib.request.build_opener(no_redirect_handler)
            
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (compatible; YAML-Processor/1.0)')]
            
            # Create request
            req = urllib.request.Request(url)
            
            response = opener.open(req, timeout=timeout)
            
            if 200 <= response.status < 300:
                # Direct success (2xx status) - no redirect
                working_urls.append(url)
                print(f"Success: {url} returned {response.status}")
            elif 300 <= response.status < 400:
                # Any redirect (301/302/etc.) - skip processing
                print(f"Skipping {url} - returns redirect ({response.status})")
                continue
                        
        except ssl.SSLError as e:
            # SSL certificate errors (invalid, self-signed, expired, etc.)
            print(f"Skipping {url} - SSL certificate error: {e}")
            continue
        except ssl.CertificateError as e:
            # Certificate validation errors
            print(f"Skipping {url} - certificate validation error: {e}")
            continue
        except urllib.error.HTTPError as e:
            # Handle HTTP errors (4xx, 5xx) and redirects caught as errors
            if 300 <= e.code < 400:
                print(f"Skipping {url} - returns redirect ({e.code})")
            continue
        except (urllib.error.URLError, socket.timeout, 
                ConnectionRefusedError, OSError) as e:
            # Check if the error is SSL-related within URLError
            if isinstance(e.reason, ssl.SSLError):
                print(f"Skipping {url} - SSL error: {e.reason}")
            continue
    
    # Return preferred URL: HTTPS over HTTP
    if working_urls:
        # Sort to prefer HTTPS
        working_urls.sort(key=lambda x: (not x.startswith('https://'), x))
        return working_urls[0]
    
    return None


def create_markdown_link(hostname, url):
    """Create markdown link format."""
    return f"[{hostname}]({url})"


def process_yaml_content(content, dry_run=False):
    """
    Process YAML content to convert hostnames to markdown links.
    
    Args:
        content (dict): Parsed YAML content
        dry_run (bool): If True, only show what would be changed
    
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
            
        hostname = server['hostname']
        
        # Skip if already markdown
        if is_markdown_link(hostname):
            print(f"Skipping {hostname} (already markdown)")
            continue
        
        print(f"Testing hostname: {hostname}")
        
        # Test connectivity
        working_url = test_url_connectivity(hostname)
        
        if working_url:
            markdown_link = create_markdown_link(hostname, working_url)
            
            if dry_run:
                print(f"[DRY RUN] Would change: {hostname} -> {markdown_link}")
                changes_made.append({
                    'index': i,
                    'old': hostname,
                    'new': markdown_link,
                    'url': working_url
                })
            else:
                print(f"Converting: {hostname} -> {markdown_link}")
                server['hostname'] = markdown_link
                changes_made.append({
                    'index': i,
                    'old': hostname, 
                    'new': markdown_link,
                    'url': working_url
                })
        else:
            print(f"No working URL found for: {hostname}")
    
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
        description='Convert plaintext hostnames to markdown links in YAML files'
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
    
    # Set output path
    output_path = Path(args.output) if args.output else input_path
    
    try:
        # Load YAML content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        if content is None:
            print("Error: Empty or invalid YAML file")
            sys.exit(1)
        
        print(f"Processing {len(content.get('servers', []))} server entries...")
        
        # Process content
        modified_content, changes = process_yaml_content(content, args.dry_run)
        
        # Report results
        if changes:
            print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
            print(f"- {len(changes)} hostname(s) processed")
            
            for change in changes:
                print(f"  • {change['old']} -> {change['new']}")
        else:
            print("\nNo changes made - no plaintext hostnames with working URLs found")
        
        # Write output (unless dry run)
        if not args.dry_run and changes:
            write_yaml_with_formatting(modified_content, output_path)
            print(f"\nOutput written to: {output_path}")
        elif args.dry_run:
            print(f"\n[DRY RUN] Would write to: {output_path}")
            
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
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
