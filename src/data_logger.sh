#!/bin/bash
# Data logger for Linux which adds options for real-time logging and filtering

# Check if output file is provided
output_to_file=false
output_file=""
append_mode=false

# List of error terms for filtering
errorRegEx="abort|error|warn|fail"

# Default mode to filter for errors
grep_pattern="grep -iE $errorRegEx"

# Parse user arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        # Use cat to pass through logs unfiltered
        -all) grep_pattern="cat"; shift ;;
        # Flag to capture logs in realtime
        -realtime) mode="realtime"; shift ;;
        # Output to specified filepath
        -o) output_to_file=true; output_file="$2"; shift 2 ;;
        # Append to file if it exists
        -append) append_mode=true; shift ;;
        # Warn user if flags not set correctly
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done

# Function to handle logging output
output_logs() {
    if $output_to_file; then
        if $append_mode; then
            # Use tee to append to the file while logging in console
            tee -a "$output_file"
        else
            # Use tee to overwrite the file while logging in console
            if [ -f "$output_file" ]; then
                rm "$output_file"
            fi
            tee "$output_file"
        fi
    else
        # Use cat to output unfiltered logs
        cat
    fi
}

# Check if logging in real-time
if [ "$mode" == "realtime" ]; then
    # Read most recent row from journalctl and follow updates in real-time
    journalctl -f -n 1 | $grep_pattern | output_logs
else
    # Save snapshot from journalctl to file
    journalctl | $grep_pattern | output_logs
fi