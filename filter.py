import re

def process_urls(input_file, output_file):
    # Set to store unique URLs
    unique_urls = set()

    # Read URLs from the input file
    with open(input_file, 'r') as file:
        for line in file:
            url = line.strip()

            # Skip lines that don't start with http or https
            if not (url.startswith("http://") or url.startswith("https://")):
                continue

            # Remove "https://web.archive.org/web/" if present
            url = url.replace("https://web.archive.org/web/", "")

            # Add URL to the set (to ensure uniqueness)
            unique_urls.add(url)

    # Filter URLs containing both '?' and '='
    filtered_urls = [url for url in unique_urls if '?' in url and '=' in url]

    # Write the filtered URLs to the output file
    with open(output_file, 'w') as file:
        for url in filtered_urls:
            file.write(url + '\n')

    # Print the count of extracted URLs
    print(f"Total URLs extracted: {len(filtered_urls)}")

# Input and output file names
input_file = 'urls.txt'
output_file = 'sqlurl.txt'

# Process the URLs
process_urls(input_file, output_file)
