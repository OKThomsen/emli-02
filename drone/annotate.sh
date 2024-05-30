#!/bin/bash

DIRECTORY="$1"

annotate_json_file() {
    local json_file="$1"
    local image_file="${json_file%.json}.jpg"

    if grep -q '"Annotation"' "$json_file"; then
        echo "File $json_file is already annotated."
        return
    fi

    if [ ! -f "$image_file" ]; then
        echo "Image file $image_file not found for $json_file"
        return
    fi

    annotation=$(ollama run llava:7b "describe this image: $image_file")

    if [ -n "$annotation" ]; then
        jq --arg annotation "$annotation" '. + { "Annotation": { "Source": "LLaVA", "Text": $annotation } }' "$json_file" > tmp.json && mv tmp.json "$json_file"
        echo "Annotated $json_file with: $annotation"
    else
        echo "Failed to get annotation for $json_file"
    fi
}

find "$DIRECTORY" -type f -name '*.json' | while read -r json_file; do
    annotate_json_file "$json_file"
done

