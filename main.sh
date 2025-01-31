#!/bin/bash

# Start the Tor service
echo "Starting Tor service..."
sudo service tor start

# Start the pip service
echo "Starting pip install..."
pip install -r requirements.txt --break-system-packages

# Run dorkx.py using Python
echo "Running DorkX..."
python dorkx.py
