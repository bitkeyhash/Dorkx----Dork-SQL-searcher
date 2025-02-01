#!/bin/bash

# Start the Tor service
echo "Starting Tor service..."
sudo service tor start

# Run dorkx.py using Python
echo "Running DorkX..."
python dorkx.py

# Run filter.py Filtering URl for Injection SQL Format Python
echo "Running Filtering URl for Injection SQL..."
python filter.py


