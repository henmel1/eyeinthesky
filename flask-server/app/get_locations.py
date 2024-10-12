import re
import requests
import json

# Input and output file names
input_file = "urls.txt"
output_file = "locations.json"

# Function to extract IP from the URL using regex
def extract_ip(url):
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    match = re.search(ip_pattern, url)
    return match.group(1) if match else None

# Function to get latitude and longitude from IP using the ipinfo.io API
def get_geo_location(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        if 'loc' in data:
            lat, long = data['loc'].split(',')
            return float(lat), float(long)
        else:
            return None, None
    except Exception as e:
        print(f"Error getting geolocation for {ip}: {e}")
        return None, None

# Main function to process URLs
def process_urls(input_file, output_file):
    # Read the URLs from the file and remove duplicates
    with open(input_file, 'r') as f:
        urls = list(set(f.read().splitlines()))

    ip_locations = []

    # Loop through each URL
    for url in urls:
        # Extract the IP address
        ip = extract_ip(url)
        if ip:
            # Get latitude and longitude
            lat, long = get_geo_location(ip)
            if lat is not None and long is not None:
                # Append to the list
                ip_locations.append({
                    "url": url,
                    "lat": lat,
                    "long": long
                })
    
    # Write the IP locations to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(ip_locations, json_file, indent=4)
    
    print(f"IP locations saved to {output_file}")

# Run the script
if __name__ == "__main__":
    process_urls(input_file, output_file)