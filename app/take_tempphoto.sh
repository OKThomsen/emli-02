#!/bin/bash

take_tempphoto() {
    if rpicam-still -t 0.01 -o ./tempphotos/picture2.jpg; then
        echo "Photo captured successfully."
    else
        echo "Error: Failed to capture photo."
    fi
}
take_tempphoto
