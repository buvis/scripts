#!/bin/bash

# Check if the required arguments are provided
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <directory_path> <output_file>"
    exit 1
fi

# Arguments
directory_path="$1"
output_file="$2"

# Validate directory path
if [[ ! -d "$directory_path" ]]; then
    echo "Error: Directory '$directory_path' does not exist."
    exit 1
fi

# Initialize the CSV file with headers
echo "File Path,Audio Track 1 Language,Audio Track 2 Language,..." > "$output_file"

# List of common video file extensions (case-insensitive)
video_extensions="mkv|mp4|avi|mov|wmv|flv|webm|m4v"

# Function to extract language from a line of mkvinfo output
extract_language() {
    local line="$1"
    local language="und"

    # Match "Language:" key-value pair
    if [[ "$line" =~ [[:space:]]Language:[[:space:]]*([a-z]{3}) ]]; then
        language="${BASH_REMATCH[1]}"
    fi

    # Match "Language (IETF BCP 47):" key-value pair
    if [[ "$line" =~ [[:space:]]Language\ \(IETF\ BCP\ 47\):[[:space:]]*([a-zA-Z\-]+) ]]; then
        language="${BASH_REMATCH[1]}"
    fi

    echo "$language"
}

# Function to process each video file
process_video() {
    local file="$1"
    local languages=()
    local track_count=0
    local reading_audio_track=false

    echo "Scanning: $file"  # Progress feedback

    # Extract audio track information using mkvinfo with verbosity
    while IFS= read -r line; do
        if [[ "$line" =~ Track\ type:\ audio ]]; then
            track_count=$((track_count + 1))
            reading_audio_track=true # Start looking for language info in subsequent lines
        elif $reading_audio_track; then
            # Extract language from subsequent lines after "Track type: audio"
            local language
            language=$(extract_language "$line")
            if [[ "$language" != "und" ]]; then
                languages+=("$language")
                reading_audio_track=false # Stop looking after finding language info
            fi
        fi
    done < <(mkvinfo -v "$file" 2>/dev/null) # Suppress errors but scan entire file

    # Only report files with more than one audio track
    if (( track_count > 1 )); then
        echo "Found $track_count audio tracks in: $file"
        # Prepare the CSV row
        csv_row="\"$file\""
        for lang in "${languages[@]}"; do
            csv_row+=",$lang"
        done

        # Append the row to the output file
        echo "$csv_row" >> "$output_file"
    else
        echo "Skipping: $file (only $track_count audio track(s))"
    fi
}

# Export functions and variables for use with find's subprocesses
export -f process_video extract_language
export output_file

# Find all files in the specified directory and filter by extension based on the last dot in their name
find "$directory_path" -type f | while IFS= read -r file; do
    ext="${file##*.}"                # Extract extension after the last dot
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]') # Convert to lowercase using tr

    if [[ "$ext" =~ ^(${video_extensions})$ ]]; then
        process_video "$file"
    else
        echo "Skipping unsupported file: $file"
    fi
done

echo "Summary saved to $output_file"
