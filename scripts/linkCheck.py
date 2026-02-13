#!/usr/bin/env python3
"""
YAML Hostname to Markdown Converter

Processes YAML files to convert plaintext hostnames to markdown links
when the hostname has an active HTTPS website. Also verifies existing
markdown links and converts back to plaintext if unreachable.

Requires Python 3.13+ for modern async features and type hints.
"""

import argparse
import asyncio
import sys
import re
from pathlib import Path
from typing import NamedTuple, Optional, TypedDict
from collections.abc import Sequence

import aiohttp
import yaml


class HostnameInfo(NamedTuple):
    """Information about a hostname entry."""
    index: int
    original_value: str
    hostname: str
    is_markdown: bool
    original_url: Optional[str] = None
    link_text: Optional[str] = None


class ProcessingResult(TypedDict):
    """Result of hostname processing."""
    index: int
    old: str
    new: str
    action: str
    url: Optional[str]


def is_markdown_link(hostname: str) -> bool:
    """Check if hostname is already in markdown format."""
    return bool(re.match(r'^\[.*\]\(.*\)$', hostname.strip()))


def extract_hostname_from_markdown(markdown_text: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract hostname from markdown link format [text](url)."""
    if match := re.match(r'^\[(.*?)\]\((.*?)\)$', markdown_text.strip()):
        link_text, url = match.groups()
        # Extract hostname from URL
        if url.startswith(('http://', 'https://')):
            hostname = url.split('://', 1)[1].split('/')[0]
            return hostname, url, link_text
        else:
            # URL without protocol, assume it's just the hostname
            return url.split('/')[0], url, link_text
    return None, None, None


def create_markdown_link(hostname: str, url: str) -> str:
    """Create markdown link format."""
    return f"[{hostname}]({url})"


def clean_hostname(hostname: str) -> str:
    """Clean hostname - remove protocol and path."""
    clean = hostname.strip()
    if clean.startswith(('http://', 'https://')):
        clean = clean.split('://', 1)[1]
    return clean.split('/')[0].lower()


def should_skip_hostname(hostname: str) -> bool:
    """Check if hostname should be skipped (e.g., NTP pools)."""
    return hostname.lower().endswith('.pool.ntp.org')


async def test_https_connectivity(
    session: aiohttp.ClientSession, 
    hostname: str, 
    timeout: float = 5.0
) -> Optional[str]:
    """
    Test if hostname is reachable via HTTPS only.
    
    Args:
        session: aiohttp ClientSession
        hostname: The hostname to test
        timeout: Connection timeout in seconds
    
    Returns:
        The working HTTPS URL or None if unreachable
    """
    clean = clean_hostname(hostname)
    url = f"https://{clean}"
    
    try:
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        
        async with session.get(
            url, 
            timeout=timeout_obj,
            allow_redirects=False,  # Don't follow redirects
            ssl=True  # Enforce SSL verification
        ) as response:
            if 200 <= response.status < 300:
                print(f"✓ Success: {url} returned {response.status}")
                return url
            elif 300 <= response.status < 400:
                print(f"⚠ Skipping {url} - returns redirect ({response.status})")
                return None
            else:
                print(f"✗ Failed: {url} returned {response.status}")
                return None
                
    except aiohttp.ClientSSLError as e:
        print(f"✗ SSL error for {url}: {e}")
        return None
    except aiohttp.ClientConnectorError as e:
        print(f"✗ Connection error for {url}: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"✗ Timeout for {url}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error for {url}: {e}")
        return None


async def process_hostname(
    session: aiohttp.ClientSession,
    hostname_info: HostnameInfo,
    timeout: float
) -> Optional[ProcessingResult]:
    """
    Process a single hostname asynchronously.
    
    Args:
        session: aiohttp ClientSession
        hostname_info: Information about the hostname to process
        timeout: Connection timeout
    
    Returns:
        ProcessingResult if changes needed, None otherwise
    """
    if should_skip_hostname(hostname_info.hostname):
        print(f"⊘ Skipping {hostname_info.hostname} (NTP pool hostname)")
        return None
    
    print(f"🔍 Testing {'markdown link' if hostname_info.is_markdown else 'plaintext'}: {hostname_info.original_value}")
    
    working_url = await test_https_connectivity(session, hostname_info.hostname, timeout)
    
    if hostname_info.is_markdown:
        # Existing markdown link
        if not working_url:
            # Convert back to plaintext hostname
            return ProcessingResult(
                index=hostname_info.index,
                old=hostname_info.original_value,
                new=hostname_info.hostname,
                action='revert_to_plaintext',
                url=None
            )
        else:
            # Markdown link is still valid
            print(f"✓ Existing markdown link is valid: {hostname_info.original_value}")
            return None
    else:
        # Plaintext hostname
        if working_url:
            # Convert to markdown
            markdown_link = create_markdown_link(hostname_info.hostname, working_url)
            return ProcessingResult(
                index=hostname_info.index,
                old=hostname_info.original_value,
                new=markdown_link,
                action='convert_to_markdown',
                url=working_url
            )
        else:
            print(f"✗ No working HTTPS URL found for: {hostname_info.hostname}")
            return None


def extract_hostname_info(content: dict) -> list[HostnameInfo]:
    """Extract hostname information from YAML content."""
    hostname_infos: list[HostnameInfo] = []
    
    if 'servers' not in content:
        print("⚠ Warning: No 'servers' key found in YAML")
        return hostname_infos
    
    for i, server in enumerate(content['servers']):
        if 'hostname' not in server:
            continue
            
        hostname_field = server['hostname']
        
        if is_markdown_link(hostname_field):
            # Existing markdown link
            extracted_hostname, original_url, link_text = extract_hostname_from_markdown(hostname_field)
            if extracted_hostname:
                hostname_infos.append(HostnameInfo(
                    index=i,
                    original_value=hostname_field,
                    hostname=extracted_hostname,
                    is_markdown=True,
                    original_url=original_url,
                    link_text=link_text
                ))
        else:
            # Plaintext hostname
            hostname_infos.append(HostnameInfo(
                index=i,
                original_value=hostname_field.strip(),
                hostname=hostname_field.strip(),
                is_markdown=False
            ))
    
    return hostname_infos


async def process_all_hostnames(
    hostname_infos: Sequence[HostnameInfo],
    timeout: float,
    max_concurrent: int = 20
) -> list[ProcessingResult]:
    """
    Process all hostnames asynchronously with concurrency control.
    
    Args:
        hostname_infos: List of hostname information
        timeout: Connection timeout
        max_concurrent: Maximum concurrent connections
    
    Returns:
        List of processing results in original order
    """
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        limit_per_host=5,
        ssl=True,
        enable_cleanup_closed=True
    )
    
    timeout_obj = aiohttp.ClientTimeout(total=timeout * 2)  # Overall session timeout
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout_obj,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; YAML-Processor/2.0)'}
    ) as session:
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(hostname_info: HostnameInfo) -> Optional[ProcessingResult]:
            async with semaphore:
                return await process_hostname(session, hostname_info, timeout)
        
        # Process all hostnames concurrently
        tasks = [process_with_semaphore(info) for info in hostname_infos]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None results and exceptions, maintain order
        processed_results: list[ProcessingResult] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"✗ Error processing hostname at index {hostname_infos[i].index}: {result}")
            elif result is not None:
                processed_results.append(result)
        
        return processed_results


def apply_changes_to_content(
    content: dict, 
    results: Sequence[ProcessingResult]
) -> dict:
    """Apply processing results to YAML content."""
    # Create a mapping of index to new value
    changes_by_index = {result['index']: result['new'] for result in results}
    
    # Apply changes
    for i, server in enumerate(content['servers']):
        if i in changes_by_index:
            server['hostname'] = changes_by_index[i]
    
    return content


def write_yaml_with_formatting(content: dict, output_path: Path) -> None:
    """Write YAML with proper formatting including newlines between entries."""
    # Custom YAML representer to handle formatting
    def str_presenter(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, str_presenter)
    
    # Write YAML with custom formatting
    yaml_str = yaml.dump(
        content, 
        default_flow_style=False, 
        sort_keys=False, 
        allow_unicode=True, 
        width=1000
    )
    
    # Add newlines between server entries for readability
    lines = yaml_str.split('\n')
    formatted_lines = []
    first_hostname = True

    for i, line in enumerate(lines):
        if line.strip().startswith('- hostname:'):
            if not first_hostname:
                formatted_lines.append('')
            first_hostname = False
        formatted_lines.append(line)
    
    output_path.write_text('\n'.join(formatted_lines), encoding='utf-8')


async def main() -> None:
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Convert plaintext hostnames to HTTPS markdown links in YAML files. '
                   'Also verifies existing markdown links and reverts to plaintext if unreachable.'
    )
    parser.add_argument('input_file', help='Input YAML file path')
    parser.add_argument('-o', '--output', help='Output file path (default: overwrite input)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without modifying files')
    parser.add_argument('--timeout', type=float, default=5.0,
                       help='Connection timeout in seconds (default: 5.0)')
    parser.add_argument('--max-concurrent', type=int, default=20,
                       help='Maximum concurrent connections (default: 20)')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"✗ Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"✗ Error: '{input_path}' is not a file")
        sys.exit(1)
    
    # Set output path
    output_path = Path(args.output) if args.output else input_path
    
    # Validate output path (only if different from input)
    if args.output and output_path.exists() and output_path.is_dir():
        print(f"✗ Error: Output path '{output_path}' is a directory")
        sys.exit(1)
    
    try:
        # Load YAML content
        content = yaml.safe_load(input_path.read_text(encoding='utf-8'))
        
        if content is None:
            print("✗ Error: Empty or invalid YAML file")
            sys.exit(1)
        
        # Extract hostname information
        hostname_infos = extract_hostname_info(content)
        server_count = len(content.get('servers', []))
        hostname_count = len(hostname_infos)
        
        print(f"📊 Processing {hostname_count} hostnames from {server_count} server entries...")
        
        if hostname_count == 0:
            print("⚠ Warning: No hostname entries found in YAML")
            return
        
        # Process all hostnames asynchronously
        print(f"🚀 Starting async processing with max {args.max_concurrent} concurrent connections...")
        results = await process_all_hostnames(hostname_infos, args.timeout, args.max_concurrent)
        
        # Report results
        if results:
            print(f"\n{'🔄 [DRY RUN] ' if args.dry_run else '📝 '}Summary:")
            
            convert_count = sum(1 for r in results if r['action'] == 'convert_to_markdown')
            revert_count = sum(1 for r in results if r['action'] == 'revert_to_plaintext')
            
            if convert_count > 0:
                print(f"  ↗️  {convert_count} hostname(s) converted to HTTPS markdown links")
            if revert_count > 0:
                print(f"  ↙️  {revert_count} markdown link(s) reverted to plaintext (unreachable)")
            
            print("\n📋 Changes:")
            # Sort results by index to maintain original order
            sorted_results = sorted(results, key=lambda x: x['index'])
            for result in sorted_results:
                action_icon = "→ 🔗" if result['action'] == 'convert_to_markdown' else "→ 📝"
                print(f"  {action_icon} {result['old']} → {result['new']}")
        else:
            print("\n✅ No changes made - all hostnames are already in correct format")
        
        # Apply changes and write output (unless dry run)
        if not args.dry_run and results:
            modified_content = apply_changes_to_content(content, results)
            write_yaml_with_formatting(modified_content, output_path)
            print(f"\n💾 Output written to: {output_path}")
        elif args.dry_run and results:
            print(f"\n🔄 [DRY RUN] Would write to: {output_path}")
            
    except yaml.YAMLError as e:
        print(f"✗ Error parsing YAML: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"✗ Error: Permission denied - {e}")
        sys.exit(1)
    except OSError as e:
        print(f"✗ Error reading/writing file: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
