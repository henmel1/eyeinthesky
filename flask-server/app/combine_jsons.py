import json

FILE1 = 'coords.json'
FILE2 = 'locations.json'

# Load the data from both JSON files
with open(FILE1, 'r') as file1, open(FILE2, 'r') as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# Initialize a dictionary to track unique entries by url
unique_locations = {}

# Helper function to add locations to the dictionary
def add_locations(data):
    for entry in data:
        if "url" in entry:
            url = entry["url"]
            # Add the entry if the URL is not already present
            if url not in unique_locations:
                unique_locations[url] = {
                    "url": url,
                    "lat": entry["lat"],
                    "long": entry["long"]
                }
    for entry in data:
        if "url" in entry:
            url = entry["url"]
            # Add the entry if the URL is not already present
            if url not in unique_locations:
                unique_locations[url] = {
                    "url": url,
                    "lat": entry["lat"],
                    "long": entry["long"]
                }

# Add data from both files
add_locations(data1)
add_locations(data2)

# Convert the dictionary back to a list of dictionaries
combined_locations = list(unique_locations.values())

# Optionally, write the combined data to a new JSON file
with open('combined_locations.json', 'w') as outfile:
    json.dump(combined_locations, outfile, indent=4)

# Output the combined data
print(combined_locations)
