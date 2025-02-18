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

# Prevent sleep and suspend
echo "Disabling sleep and suspend modes..."
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# Start the Tor service
echo "Starting Tor service..."
sudo service tor start

# Run dorkx.py using Python
echo "Running DorkX..."
python dorkx.py

# Run filter.py Filtering URL for Injection SQL Format Python
echo "Running Filtering URL for Injection SQL..."
python filter.py


echo "Finished.Check Output Files : urls.txt=*without filtering* and sqlurl.txt=*with filtering for sql Injections like ?id=2* ®© BitKeyHash"
