#!/bin/bash

# Directory containing the JSON files
DIRECTORY="$1"

# Function to annotate a single JSON file
annotate_json_file() {
    local json_file="$1"
    local image_file="${json_file%.json}.jpg"

    # Check if the JSON file already has an annotation
    if grep -q '"Annotation"' "$json_file"; then
        echo "File $json_file is already annotated."
        return
    fi

    # Call the local API to get the custom annotation
    annotation=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"image_path\": \"$image_file\"}" http://localhost:5000/annotate | jq -r '.annotation')


    # Add the annotation to the JSON file
    if [ -n "$annotation" ]; then
        jq --arg annotation "$annotation" '. + { "Annotation": { "Source": "LLaVA", "Text": $annotation } }' "$json_file" > tmp.json && mv tmp.json "$json_file"
        echo "Annotated $json_file with: $annotation"
    else
        echo "Failed to get annotation for $json_file"
    fi
}

# Find and annotate all JSON files in the directory
find "$DIRECTORY" -type f -name '*.json' | while read json_file; do
    annotate_json_file "$json_file"
done

