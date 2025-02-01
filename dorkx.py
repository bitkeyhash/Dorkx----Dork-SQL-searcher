import requests
import time
import random
import subprocess
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Configuration
SEARX_URL = "https://searx.be/search"  # Replace if needed.  Make sure to include the /search endpoint
DORK_FILE = "dorks.txt"
OUTPUT_FILE = "urls.txt"
REQUEST_DELAY = 5  # Seconds
MAX_RETRIES = 3  # Not used directly, handled within the loop
RETRY_DELAY = 5 # Not used directly
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.62",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",  # Older Chrome
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",  # Older Firefox
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",  # IE 11
]
COOKIES = {
    "categories": "general",
    "language": "auto",
    "locale": "en",
    "autocomplete": "google",
    "favicon_resolver": "",
    "image_proxy": "1",
    "method": "POST",
    "safesearch": "0",
    "theme": "simple",
    "results_on_new_tab": "0",
    "doi_resolver": "oadoi.org",
    "simple_style": "auto",
    "center_alignment": "0",
    "advanced_search": "0",
    "query_in_title": "1",
    "infinite_scroll": "0",
    "search_on_category_select": "1",
    "hotkeys": "default",
    "url_formatting": "pretty",
    "disabled_engines": "",
    "enabled_engines": "duckduckgo__general,google__general,qwant__general,startpage__general,yahoo__general,brave__general,goo__general",
    "disabled_plugins": "",
    "enabled_plugins": "",
    "tokens": ""
}
HEADERS = {
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not?A_Brand";v="99", "Chromium";v="130"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "null",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"


def colored_print(text, color=COLOR_RESET, end="\n"):
    """Prints text with ANSI color codes."""
    print(f"{color}{text}{COLOR_RESET}", end=end)

def read_dorks(filename):
    """Reads dorks from a file, stripping whitespace."""
    try:
        with open(filename, "r") as f:
            dorks = [line.strip() for line in f]
        return dorks
    except FileNotFoundError:
        colored_print(f"Error: Dork file not found: {filename}", color=COLOR_RED)
        return []
    except Exception as e:
        colored_print(f"Error reading dork file: {e}", color=COLOR_RED)
        return []


def extract_urls_from_html(html):
    """Extracts URLs from HTML using BeautifulSoup.  Filters and cleans them."""
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        url = a_tag["href"]

        # Basic filtering:  Exclude internal links and common unwanted patterns.  Customize as needed.
        if url.startswith("#") or "searx.be" in url or url.startswith("javascript:"): # Adjust domain if you're not using searx.be
            continue

        # Attempt to clean up URLs if they're redirects through another site
        if "url?q=" in url:  #Google redirect URL
            try:
                url = url.split("url?q=")[1].split("&")[0]
            except:
                pass #If it fails, keep the original url
        # Add more cleaning rules as needed for other search engines.
        urls.append(url)
    return urls

def change_tor_ip():
    """Changes the Tor IP address using command-line."""
    try:
        colored_print("  - Changing Tor IP...", color=COLOR_YELLOW)
        subprocess.run(["killall", "tor"], check=True, capture_output=True)
        subprocess.run(["service", "tor", "start"], check=True, capture_output=True)
        # Basic connection check:
        result = subprocess.run(["curl", "--proxy", "socks5h://localhost:9050", "https://check.torproject.org"], capture_output=True, text=True)
        if "Congratulations" in result.stdout:
             colored_print("  - Tor IP successfully changed.", color=COLOR_GREEN)
             return True
        else:
             colored_print("  - Error checking Tor connection after IP change.", color=COLOR_RED)
             return False

    except subprocess.CalledProcessError as e:
        colored_print(f"  - Error changing Tor IP: {e}", color=COLOR_RED)
        return False
    except FileNotFoundError:
        colored_print("  - Error: curl or tor command not found. Make sure they are installed and in your PATH.", color=COLOR_RED)
        return False

def searx_search(dork, page=1):
    """Performs a search on Searx using Tor and returns the HTML content."""
    while True:  # Retry loop, no explicit retries counter needed
        try:
            # Construct the POST data
            post_data = {
                "q": dork,
                "category_general": "1",
                "pageno": str(page),
                "language": "auto",
                "time_range": "",
                "safesearch": "0",
                "theme": "simple",
            }

            # Choose a random User-Agent
            headers = HEADERS.copy()  # Make a copy to avoid modifying the original
            headers["User-Agent"] = random.choice(USER_AGENTS)
            headers["Referer"] = SEARX_URL # add referer

            proxies = {
                "http": "socks5h://localhost:9050",
                "https": "socks5h://localhost:9050"
            }

            # Send the request with POST method
            response = requests.post(SEARX_URL, data=post_data, headers=headers, cookies=COOKIES, proxies=proxies)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            return response.text
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429:
                colored_print("  - Rate limit hit (429).", color=COLOR_YELLOW)
                if not change_tor_ip(): # Change IP and check success
                    colored_print("  - Failed to change Tor IP.  Exiting this dork/page.", color=COLOR_RED)
                    return None
                else:
                    time.sleep(REQUEST_DELAY)  # Wait a bit *after* successfully changing IP
                    continue  # Retry the request with the new IP

            else:  # Handle other request errors
                colored_print(f"Request error: {e}", color=COLOR_RED)
                return


def save_urls_to_file(urls_to_save, filename, append=False):
    """Saves a set of URLs to a file.

    Args:
        urls_to_save (set): The set of URLs to save.
        filename (str): The path to the output file.
        append (bool, optional): Whether to append to the file. Defaults to False (overwrite).
    """
    try:
        mode = "a" if append else "w"
        with open(filename, mode) as f:
            for url in sorted(urls_to_save): #Sort urls for easier reading
                f.write(url + "\n")
        colored_print(f"Saved {len(urls_to_save)} URLs to {filename} ({'appended' if append else 'overwritten'}).", color=COLOR_GREEN)
    except Exception as e:
        colored_print(f"Error writing to output file: {e}", color=COLOR_RED)


def main():
    """Main function to orchestrate the scraping and URL extraction."""
    dorks = read_dorks(DORK_FILE)
    if not dorks:
        colored_print("No dorks to process. Exiting.", color=COLOR_YELLOW)
        return

    all_urls = set()  # Use a set to store unique URLs efficiently
    total_url_count = 0
    url_threshold = 200

    try:
        colored_print("How many pages to query per dork? (Enter a number):Default=0 ", color=COLOR_CYAN, end="")
        num_pages_to_query = input()
        try:
            num_pages_to_query = int(num_pages_to_query)
            if num_pages_to_query <= 0:
                colored_print("Please enter a positive number of pages.", color=COLOR_RED)
                return
        except ValueError:
            colored_print("Invalid input. Please enter a number.", color=COLOR_RED)
            return

        for dork in dorks:
            colored_print(f"Processing dork: {dork}", color=COLOR_BLUE)
            for page_number in range(1, num_pages_to_query + 1): # Loop through user defined pages
                colored_print(f"  - Scraping page: {page_number}", color=COLOR_CYAN)
                html_content = searx_search(dork, page_number)

                if not html_content:
                    colored_print("  - No content received. Skipping to next dork.", color=COLOR_YELLOW)
                    break # Break inner loop, go to next dork

                urls = extract_urls_from_html(html_content)
                if not urls:
                    colored_print("  - No URLs found on this page.  Assuming end of results.", color=COLOR_YELLOW)
                    break # Break inner loop, go to next dork

                new_urls = set(urls) - all_urls  # Find URLs not already in the set
                if not new_urls:
                    colored_print("  - No new URLs found.  Assuming end of results.", color=COLOR_YELLOW)
                    break # Break inner loop, go to next dork

                all_urls.update(new_urls) #Add to the overall set
                found_on_page = len(new_urls)
                total_url_count += found_on_page

                colored_print(f"  - Found {found_on_page} new URLs on page {page_number}. Total URLs: {total_url_count}", color=COLOR_GREEN)

                if len(all_urls) > url_threshold:
                    save_urls_to_file(all_urls, OUTPUT_FILE, append=True) # Append if file already exists from prior saves
                    all_urls = set() # Clear set to free memory

                time.sleep(REQUEST_DELAY)  # Rate limiting

    except KeyboardInterrupt:
        colored_print("\nKeyboard interrupt detected. Stopping the scraping process...", color=COLOR_YELLOW)
    except Exception as e:
        colored_print(f"An unexpected error occurred: {e}", color=COLOR_RED)

    # Save any remaining URLs after loop finishes or interrupt
    if all_urls:
        save_urls_to_file(all_urls, OUTPUT_FILE, append=True) # Append remaining URLs

    colored_print(f"Successfully wrote total {total_url_count} unique URLs to {OUTPUT_FILE}", color=COLOR_GREEN)


if __name__ == "__main__":
    main()
