
# DorkX SQL Searcher | using Searxng + Ip Rotation Tor 
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://i.ibb.co/JW821n7m/Screenshot-2025-01-31-02-39-51-466-edit-com-termux.jpg">
  <source media="(prefers-color-scheme: light)" srcset="https://i.ibb.co/JW821n7m/Screenshot-2025-01-31-02-39-51-466-edit-com-termux.jpg">
  <img alt="DorkX in Action" src="https://i.ibb.co/JW821n7m/Screenshot-2025-01-31-02-39-51-466-edit-com-termux.jpg">
</picture>


This script performs automated searches on Searx using dorks, extracts URLs, and saves them to a file. It leverages Tor for anonymity and includes features like IP rotation and user-agent randomization.

## Installation

### **1. Prerequisites**
Ensure you have Python 3.x and `pip` installed on your system.

### **2. Install Required Python Packages**
Run the following command to install the required Python libraries:

```markdown
pip install -r requirements.txt
```

### **3. Install Tor**
Install Tor using the following command:

```markdown
sudo apt update && sudo apt tor -y
```

Make sure the Tor service is running:

```markdown
sudo service tor start
```

## Usage

1. **Prepare Dork File**: Create a `dorks.txt` file in the same directory as the script. Add your dorks (one per line).
2. **Run the Script**: Execute the script using:
   
```markdown
chmod +x main.sh && bash main.sh
```
(ps: I have add script to filter url at the end . final output file is "sqlurl.txt" )
   
4. Follow the prompts to specify the number of pages to scrape per dork.

## Files

- **`dorks.txt`**  
  Input File containing all search dorks.
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

