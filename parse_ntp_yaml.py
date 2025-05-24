import yaml
import json

def parse_ntp_sources(yaml_file_path, output_json_file_path):
    """
    Parses an NTP sources YAML file and saves the data to a JSON file.

    Args:
        yaml_file_path (str): The path to the input YAML file.
        output_json_file_path (str): The path to the output JSON file.
    """
    try:
        with open(yaml_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if data and 'servers' in data:
            servers = data['servers']
            num_servers = len(servers)
            print(f"Found {num_servers} servers.")
            
            # Print the list of dictionaries
            # print(servers) # This might be too large for direct output

            with open(output_json_file_path, 'w') as json_f:
                json.dump(servers, json_f, indent=4)
            print(f"Parsed data saved to {output_json_file_path}")
            
            # For the purpose of this task, let's print the servers list
            # if it's not excessively long.
            # As a heuristic, if it's less than, say, 20 servers, print it.
            # Otherwise, just print the count and the confirmation of saving to file.
            if num_servers < 20:
                print("\nServer list:")
                for server in servers:
                    print(server)
            else:
                print("\nServer list is too long to print directly, but it has been saved to the JSON file.")

        else:
            print("No 'servers' key found in the YAML file or the file is empty.")

    except FileNotFoundError:
        print(f"Error: File not found at {yaml_file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    yaml_file = "ntp-sources.yml"
    json_file = "parsed_data.json"
    parse_ntp_sources(yaml_file, json_file)
