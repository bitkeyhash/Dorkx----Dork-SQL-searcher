```markdown
# DorkX Scraper Searxng Ip Rotation Tor🕵️‍♂️

This script performs automated searches on Searx using dorks, extracts URLs, and saves them to a file. It leverages Tor for anonymity and includes features like IP rotation and user-agent randomization.

## Installation

### **1. Prerequisites**
Ensure you have Python 3.x and `pip` installed on your system.

### **2. Install Required Python Packages**
Run the following command to install the required Python libraries:

```
pip install -r requirements.txt
```

### **3. Install Tor**
Install Tor using the following command:

```
sudo apt update && sudo apt install tor -y
```

Make sure the Tor service is running:

```
sudo service tor start
```

## Usage

1. **Prepare Dork File**: Create a `dorks.txt` file in the same directory as the script. Add your dorks (one per line).
2. **Run the Script**: Execute the script using:
   ```
   python dorkx.py
   ```
3. Follow the prompts to specify the number of pages to scrape per dork.

## Files

- **`requirements.txt`**  
  Contains the Python dependencies:
  ```
  requests==2.31.0
  beautifulsoup4==4.12.2
  ```
- **`dorks.txt`**  
  A file containing search dorks.
- **`urls.txt`**  
  Output file where extracted URLs are saved.

## Features

- 🌐 **Tor Integration**: Ensures anonymity by routing traffic through Tor.
- 🔄 **IP Rotation**: Automatically changes IP when rate-limited.
- 🕵️‍♀️ **Customizable Headers and Cookies**: Mimics real browser behavior.
- 📂 **Output File**: Saves unique URLs to `urls.txt`.

## Notes

- Ensure Tor is installed and running for proper functionality.
- Use responsibly and adhere to legal and ethical guidelines.

