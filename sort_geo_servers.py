import json

def sort_geographical_servers(input_json_path, output_json_path):
    """
    Sorts a list of geographical NTP server entries by location, then by owner.

    Args:
        input_json_path (str): Path to the input JSON file containing the geo server list.
        output_json_path (str): Path to save the sorted list of geo servers.
    """
    try:
        with open(input_json_path, 'r') as f:
            geo_servers = json.load(f)

        # Sort the servers:
        # Primary key: location (case-insensitive)
        # Secondary key: owner (case-insensitive)
        # Fallback for missing keys: use an empty string to avoid errors and place them consistently.
        sorted_servers = sorted(
            geo_servers,
            key=lambda x: (
                x.get("location", "").lower(), 
                x.get("owner", "").lower()
            )
        )

        with open(output_json_path, 'w') as f_sorted:
            json.dump(sorted_servers, f_sorted, indent=4)

        print(f"Successfully sorted {len(sorted_servers)} geographical servers.")
        print(f"Sorted geographical servers saved to: {output_json_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_json_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_json_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_file = "geo_servers.json"  # From the previous step
    output_file = "geo_servers_sorted.json"
    sort_geographical_servers(input_file, output_file)
