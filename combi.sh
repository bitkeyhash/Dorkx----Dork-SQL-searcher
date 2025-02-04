#!/bin/bash

# Prompt for file paths
read -p "Enter the path to File 1: " file1
read -p "Enter the path to File 2: " file2

# Check if files exist
if [[ ! -f "$file1" ]]; then
  echo "File 1 does not exist. Please check the path."
  exit 1
fi

if [[ ! -f "$file2" ]]; then
  echo "File 2 does not exist. Please check the path."
  exit 1
fi

# Output file
output="dorksfinal.txt"
> "$output"

# Function to generate all combinations of lines in a file
generate_combinations() {
  local lines=("$@")
  local n=${#lines[@]}
  
  for ((i=1; i<(1<<n); i++)); do
    combo=""
    for ((j=0; j<n; j++)); do
      if ((i & (1 << j))); then
        combo+="${lines[j]} "
      fi
    done
    echo "$combo"
  done
}

# Read File 2 into an array
mapfile -t file2_lines < "$file2"

# Initialize variables
line_count=0
temp_output="temp_dorks.txt"
> "$temp_output"

# Start a background process to echo the number of lines generated every 10 seconds
(
  while true; do
    sleep 10
    echo "Lines generated so far: $line_count"
  done
) &

# Process each line in File 1
while IFS= read -r line1; do
  # Generate all combinations of lines from File 2
  combinations=$(generate_combinations "${file2_lines[@]}")
  
  # Combine each line from File 1 with the combinations of File 2
  while IFS= read -r combo; do
    echo "$line1 $combo" >> "$temp_output"
    ((line_count++))
    
    # Save to output file every 1000 lines
    if (( line_count % 1000 == 0 )); then
      cat "$temp_output" >> "$output"
      > "$temp_output"
    fi
  done <<< "$combinations"
done < "$file1"

# Save any remaining lines to the output file
cat "$temp_output" >> "$output"
rm "$temp_output"

echo "All combinations saved to $output."
