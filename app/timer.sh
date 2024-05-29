#!/bin/bash

take_photo() {
    /home/wildlife/app/take_photo.sh timer
}

while true; do
    take_photo
    sleep 300
done
