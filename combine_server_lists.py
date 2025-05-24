import json

def combine_ntp_server_lists(non_geo_file_path, geo_sorted_file_path, output_combined_file_path):
    """
    Combines a list of non-geographical NTP servers with a sorted list of 
    geographical NTP servers. The non-geographical servers appear first, 
    followed by the geographical servers.

    Args:
        non_geo_file_path (str): Path to the JSON file with non-geographical servers.
        geo_sorted_file_path (str): Path to the JSON file with sorted geographical servers.
        output_combined_file_path (str): Path to save the combined list of servers.
    """
    try:
        with open(non_geo_file_path, 'r') as f_non_geo:
            non_geo_servers = json.load(f_non_geo)

        with open(geo_sorted_file_path, 'r') as f_geo_sorted:
            geo_servers_sorted = json.load(f_geo_sorted)

        # Combine the lists: non-geographical first, then sorted geographical
        combined_servers = non_geo_servers + geo_servers_sorted

        with open(output_combined_file_path, 'w') as f_combined:
            json.dump(combined_servers, f_combined, indent=4)

        total_servers = len(combined_servers)
        print(f"Successfully combined server lists.")
        print(f"Total number of servers in the combined list: {total_servers}")
        print(f"Combined server list saved to: {output_combined_file_path}")

    except FileNotFoundError as e:
        print(f"Error: Input file not found. Details: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from an input file. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    non_geo_file = "non_geo_servers.json"       # From subtask 2
    geo_sorted_file = "geo_servers_sorted.json" # From subtask 3
    combined_file = "combined_servers.json"
    
    combine_ntp_server_lists(non_geo_file, geo_sorted_file, combined_file)
