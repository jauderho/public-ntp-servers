import json

def separate_servers(input_json_path, non_geo_output_path, geo_output_path):
    """
    Separates NTP server entries based on their location (geographical or non-geographical).

    Args:
        input_json_path (str): Path to the input JSON file containing the server list.
        non_geo_output_path (str): Path to save the non-geographical servers.
        geo_output_path (str): Path to save the geographical servers.
    """
    non_geographical_locations = [
        "Google NTP", "Amazon NTP", "Cloudflare NTP", "Facebook NTP", 
        "Microsoft NTP", "Apple NTP", "DEC/Compaq/HP", "NTP SERVERS", 
        "stratum1.net", "ACO.net", "Trabia-Network", "RIPE", 
        "Internet Systems Consortium", "Kantonsschule Zug", "Nat Morris", 
        "ISI", "NetBone Digital", "Microsemi/Symmetricom", "Quintex", 
        "Conectiv", "USSHC", "timegps.net", "Layer42", "Stygium", 
        "planeacion.net", "KPN International Carrier", "oar.net", "HEAnet", 
        "ona.org", "your.org", "mrow.org", "Ubuntu", "Qualcomm"
    ]

    non_geo_servers = []
    geo_servers = []

    try:
        with open(input_json_path, 'r') as f:
            servers = json.load(f)

        for server in servers:
            location = server.get("location", "") # Get location, default to empty string if not found
            if location in non_geographical_locations:
                non_geo_servers.append(server)
            else:
                geo_servers.append(server)

        with open(non_geo_output_path, 'w') as f_non_geo:
            json.dump(non_geo_servers, f_non_geo, indent=4)
        
        with open(geo_output_path, 'w') as f_geo:
            json.dump(geo_servers, f_geo, indent=4)

        print(f"Number of non-geographical servers: {len(non_geo_servers)}")
        print(f"Non-geographical servers saved to: {non_geo_output_path}")
        print(f"Number of geographical servers: {len(geo_servers)}")
        print(f"Geographical servers saved to: {geo_output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_json_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_json_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_file = "parsed_data.json"
    non_geo_file = "non_geo_servers.json"
    geo_file = "geo_servers.json"
    separate_servers(input_file, non_geo_file, geo_file)
