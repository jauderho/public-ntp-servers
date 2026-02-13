#!/usr/bin/env python3
"""
ntpUpdateSources.py - Update NTP sources with AS numbers and stratum information

This script reads an ntp-sources.yml file and updates each server entry with:
- Correct AS number (using asnmap tool) in format "AS12345"
- Correct stratum (using ntpdate tool)

Usage: python3 ntpUpdateSources.py <ntp-sources.yml>
"""

import sys
import yaml
import subprocess
import json
import re
import logging
import argparse
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_required_tools():
    """Check if required external tools are available"""
    tools = ['asnmap', 'ntpdate', 'jq']
    missing_tools = []
    
    for tool in tools:
        try:
            subprocess.run([tool, '--help' if tool != 'jq' else '--version'], 
                         capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            missing_tools.append(tool)
    
    if missing_tools:
        logger.error(f"Missing required tools: {', '.join(missing_tools)}")
        logger.error("Please install the missing tools:")
        for tool in missing_tools:
            if tool == 'asnmap':
                logger.error("  asnmap: go install -v github.com/projectdiscovery/asnmap/cmd/asnmap@latest")
            elif tool == 'ntpdate':
                logger.error("  ntpdate: sudo apt-get install ntpdate (Ubuntu/Debian) or equivalent")
            elif tool == 'jq':
                logger.error("  jq: sudo apt-get install jq (Ubuntu/Debian) or equivalent")
        return False
    return True

def get_as_numbers(hostname):
    """
    Get AS numbers for a hostname using asnmap
    Returns the AS numbers in format "AS12345, AS67890" or None if not found
    """
    try:
        # Run: asnmap -d hostname -silent -j | jq -r '.as_number' | sort -u
        asnmap_cmd = ['asnmap', '-d', hostname, '-silent', '-j']
        jq_cmd = ['jq', '-r', '.as_number']
        sort_cmd = ['sort', '-u']
        
        # Chain the commands
        asnmap_proc = subprocess.Popen(asnmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        jq_proc = subprocess.Popen(jq_cmd, stdin=asnmap_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        asnmap_proc.stdout.close()
        sort_proc = subprocess.Popen(sort_cmd, stdin=jq_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        jq_proc.stdout.close()
        
        output, error = sort_proc.communicate(timeout=30)
        
        if sort_proc.returncode == 0 and output.strip():
            as_numbers = output.decode().strip().split('\n')
            # Filter out null/empty values and collect all valid AS numbers
            valid_as_numbers = []
            for as_num in as_numbers:
                if as_num and as_num != 'null' and as_num.isdigit():
                    valid_as_numbers.append(f"AS{as_num}")
            
            if valid_as_numbers:
                return ", ".join(valid_as_numbers)
        
        logger.warning(f"Could not determine AS numbers for {hostname}")
        return None
        
    except Exception as e:
        logger.error(f"Error getting AS numbers for {hostname}: {e}")
        return None

def parse_existing_as_numbers(as_string):
    """
    Parse existing AS numbers from string format
    Returns set of AS numbers for comparison
    """
    if not as_string or as_string == "Unknown":
        return set()
    
    # Split by comma and clean up
    as_numbers = set()
    for as_num in as_string.split(','):
        as_num = as_num.strip()
        if as_num.startswith('AS') and as_num[2:].isdigit():
            as_numbers.add(as_num)
    
    return as_numbers

def normalize_as_numbers(as_string):
    """
    Normalize AS numbers string to consistent format
    Returns sorted, comma-separated AS numbers
    """
    as_numbers = parse_existing_as_numbers(as_string)
    if not as_numbers:
        return None
    
    # Sort AS numbers by their numeric value
    sorted_as = sorted(as_numbers, key=lambda x: int(x[2:]))
    return ", ".join(sorted_as)

def is_unknown_value(value):
    """
    Check if a value is considered "unknown" and needs updating
    """
    if value is None or value == "":
        return True
    if isinstance(value, str) and value.lower() == "unknown":
        return True
    return False

def get_stratum(hostname):
    """
    Get stratum for a hostname using ntpdate
    Returns the stratum as integer or None if not found
    """
    try:
        # Run: ntpdate -q hostname
        cmd = ['ntpdate', '-q', hostname]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse output to find stratum
            # Example output: "2025-05-23 02:57:29.980318 (+0000) +0.000214 +/- 0.003723 time.cloudflare.com 162.159.200.1 s3 no-leap"
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and hostname in line:
                    # Look for pattern like "s3" or "s1" etc.
                    stratum_match = re.search(r'\bs(\d+)\b', line)
                    if stratum_match:
                        return int(stratum_match.group(1))
        
        # If ntpdate fails, try alternative approach with timeout
        logger.warning(f"ntpdate failed for {hostname}, trying alternative method")
        
        # Alternative: use ntpq if available
        try:
            cmd_alt = ['timeout', '10', 'ntpq', '-p', hostname]
            result_alt = subprocess.run(cmd_alt, capture_output=True, text=True)
            if result_alt.returncode == 0:
                # Parse ntpq output for stratum
                for line in result_alt.stdout.split('\n'):
                    if hostname in line or '*' in line or '+' in line:
                        parts = line.split()
                        if len(parts) >= 3 and parts[2].isdigit():
                            return int(parts[2])
        except:
            pass
        
        logger.warning(f"Could not determine stratum for {hostname}")
        return None
        
    except Exception as e:
        logger.error(f"Error getting stratum for {hostname}: {e}")
        return None

def write_yaml_with_formatting(data, filepath):
    """Write YAML with proper formatting including newlines between entries."""
    def str_presenter(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_presenter)

    yaml_str = yaml.dump(
        data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
        indent=2
    )

    lines = yaml_str.split('\n')
    formatted_lines = []
    first_hostname = True

    for i, line in enumerate(lines):
        if line.strip().startswith('- hostname:'):
            if not first_hostname:
                formatted_lines.append('')
            first_hostname = False
        formatted_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_lines))


def update_ntp_sources(yaml_file, dry_run=False):
    """
    Update NTP sources YAML file with AS numbers and stratum information
    """
    try:
        # Read the YAML file
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data or 'servers' not in data:
            logger.error("Invalid YAML structure. Expected 'servers' key.")
            return False
        
        updated = False
        changes_made = []
        
        if dry_run:
            logger.info("=== DRY RUN MODE - No changes will be made ===")
        
        # Process each server entry
        for server_entry in data['servers']:
            if 'hostname' not in server_entry:
                logger.warning("Server entry missing 'hostname' field, skipping")
                continue
            
            hostname = server_entry['hostname']
            logger.info(f"Processing {hostname}...")
            
            # Update AS numbers
            current_as = server_entry.get('AS')
            new_as = get_as_numbers(hostname)
            
            if new_as is not None:
                # Normalize both current and new AS numbers for comparison
                current_as_normalized = normalize_as_numbers(current_as) if not is_unknown_value(current_as) else None
                new_as_normalized = normalize_as_numbers(new_as)
                
                if current_as_normalized != new_as_normalized:
                    if is_unknown_value(current_as):
                        change_msg = f"  Replacing Unknown AS for {hostname}: {new_as_normalized}"
                        logger.info(change_msg)
                        changes_made.append(f"REPLACE Unknown AS for {hostname}: {new_as_normalized}")
                    elif current_as is None or current_as == "":
                        change_msg = f"  Adding AS numbers for {hostname}: {new_as_normalized}"
                        logger.info(change_msg)
                        changes_made.append(f"ADD AS for {hostname}: {new_as_normalized}")
                    else:
                        change_msg = f"  Updating AS numbers for {hostname}: {current_as} -> {new_as_normalized}"
                        logger.info(change_msg)
                        changes_made.append(f"UPDATE AS for {hostname}: {current_as} -> {new_as_normalized}")
                    
                    if not dry_run:
                        server_entry['AS'] = new_as_normalized
                    updated = True
                else:
                    logger.info(f"  AS numbers for {hostname} are correct: {new_as_normalized}")
            else:
                logger.warning(f"  Could not update AS numbers for {hostname}")
                # If we have existing AS numbers but can't verify, log them
                if current_as and not is_unknown_value(current_as):
                    logger.info(f"  Keeping existing AS numbers for {hostname}: {current_as}")
                    # Still normalize the existing format
                    normalized_existing = normalize_as_numbers(current_as)
                    if normalized_existing and normalized_existing != current_as:
                        change_msg = f"  Normalizing AS format for {hostname}: {current_as} -> {normalized_existing}"
                        logger.info(change_msg)
                        changes_made.append(f"NORMALIZE AS for {hostname}: {current_as} -> {normalized_existing}")
                        if not dry_run:
                            server_entry['AS'] = normalized_existing
                        updated = True
                elif is_unknown_value(current_as):
                    logger.warning(f"  AS remains Unknown for {hostname} (lookup failed)")
            
            # Update stratum
            current_stratum = server_entry.get('stratum')
            new_stratum = get_stratum(hostname)
            
            if new_stratum is not None:
                # Handle both numeric and string "Unknown" values
                current_stratum_unknown = is_unknown_value(current_stratum)
                
                if current_stratum != new_stratum:
                    if current_stratum_unknown:
                        change_msg = f"  Replacing Unknown stratum for {hostname}: {new_stratum}"
                        logger.info(change_msg)
                        changes_made.append(f"REPLACE Unknown stratum for {hostname}: {new_stratum}")
                    elif current_stratum is None:
                        change_msg = f"  Adding stratum for {hostname}: {new_stratum}"
                        logger.info(change_msg)
                        changes_made.append(f"ADD stratum for {hostname}: {new_stratum}")
                    else:
                        change_msg = f"  Updating stratum for {hostname}: {current_stratum} -> {new_stratum}"
                        logger.info(change_msg)
                        changes_made.append(f"UPDATE stratum for {hostname}: {current_stratum} -> {new_stratum}")
                    
                    if not dry_run:
                        server_entry['stratum'] = new_stratum
                    updated = True
                else:
                    logger.info(f"  Stratum for {hostname} is correct: {new_stratum}")
            else:
                logger.warning(f"  Could not update stratum for {hostname}")
                if is_unknown_value(current_stratum):
                    logger.warning(f"  Stratum remains Unknown for {hostname} (lookup failed)")
        
        # Summary of changes
        if dry_run:
            logger.info("\n=== DRY RUN SUMMARY ===")
            if changes_made:
                logger.info(f"Would make {len(changes_made)} changes:")
                for change in changes_made:
                    logger.info(f"  - {change}")
                logger.info(f"\nTo apply these changes, run without --dry-run flag")
            else:
                logger.info("No changes would be made")
            return True
        
        # Write back to file if any updates were made
        if updated:
            # Create backup
            backup_file = f"{yaml_file}.backup"
            subprocess.run(['cp', yaml_file, backup_file])
            logger.info(f"Created backup: {backup_file}")
            
            # Write updated data
            write_yaml_with_formatting(data, yaml_file)
            
            logger.info(f"Updated {yaml_file}")
            logger.info(f"Applied {len(changes_made)} changes:")
            for change in changes_made:
                logger.info(f"  - {change}")
        else:
            logger.info("No updates needed")
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating NTP sources: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Update NTP sources with AS numbers and stratum information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ntpUpdateSources.py ntp-sources.yml
  python3 ntpUpdateSources.py --dry-run ntp-sources.yml
  python3 ntpUpdateSources.py -n ntp-sources.yml
        """
    )
    
    parser.add_argument('yaml_file', 
                       help='Path to the ntp-sources.yml file')
    
    parser.add_argument('--dry-run', '-n', 
                       action='store_true',
                       help='Show what changes would be made without modifying the file')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not Path(args.yaml_file).exists():
        logger.error(f"File not found: {args.yaml_file}")
        sys.exit(1)
    
    # Check required tools
    if not check_required_tools():
        sys.exit(1)
    
    # Update NTP sources
    if update_ntp_sources(args.yaml_file, dry_run=args.dry_run):
        if args.dry_run:
            logger.info("Dry run completed successfully")
        else:
            logger.info("Script completed successfully")
    else:
        logger.error("Script failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
