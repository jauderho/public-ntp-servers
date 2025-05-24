import json
import yaml

def write_combined_list_to_yaml(combined_json_path, output_yaml_path):
    """
    Reads a combined list of NTP servers from a JSON file, structures it
    under a 'servers' key, converts it to YAML, and writes it to a new
    YAML file, overwriting if it exists.

    Args:
        combined_json_path (str): Path to the input JSON file with the combined server list.
        output_yaml_path (str): Path to the output YAML file (e.g., ntp-sources.yml).
    """
    try:
        with open(combined_json_path, 'r') as f_json:
            combined_servers_list = json.load(f_json)

        # Structure the data as required for the YAML output
        output_data = {'servers': combined_servers_list}

        # Convert to YAML and write to the output file
        # Using Dumper=yaml.SafeDumper for safety and default_flow_style=False for block style
        with open(output_yaml_path, 'w') as f_yaml:
            yaml.dump(output_data, f_yaml, Dumper=yaml.SafeDumper, default_flow_style=False, sort_keys=False, indent=2)

        print(f"Successfully wrote {len(combined_servers_list)} servers to {output_yaml_path}")
        print(f"The file '{output_yaml_path}' has been updated with the combined and sorted server list.")

    except FileNotFoundError:
        print(f"Error: Input file not found at {combined_json_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {combined_json_path}")
    except yaml.YAMLError as e:
        print(f"Error during YAML generation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    combined_json_file = "combined_servers.json"  # From the previous step
    output_yaml_file = "ntp-sources.yml"         # The file to be overwritten
    
    write_combined_list_to_yaml(combined_json_file, output_yaml_file)
