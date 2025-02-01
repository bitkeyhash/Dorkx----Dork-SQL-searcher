#!/bin/bash
echo " ____             _    __  __  _____           ";
echo "|  _ \  ___  _ __| | __\ \/ / |_   _|__  _ __  ";
echo "| | | |/ _ \| '__| |/ / \  /    | |/ _ \| '__| ";
echo "| |_| | (_) | |  |   <  /  \    | | (_) | |    ";
echo "|____/ \___/|_| _|_|\_\/_/\_\   |_|\___/|_|    ";
echo "        / ___| / _ \| |                        ";
echo "        \___ \| | | | |                        ";
echo "         ___) | |_| | |___                     ";
echo "        |____/ \__\_\_____|  by bitkeyhash°©®  ";
# Start the Tor service
echo "Starting Tor service..."
sudo service tor start

# Run dorkx.py using Python
echo "Running DorkX..."
python dorkx.py

# Run filter.py Filtering URl for Injection SQL Format Python
echo "Running Filtering URl for Injection SQL..."
python filter.py


