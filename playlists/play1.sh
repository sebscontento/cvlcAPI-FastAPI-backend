#!/bin/bash

#Author: Sebastian Solórzano Holbøll
#version: 4
#THIS IS JUST A PLAYLIST PLAYS FROM LOWEST OT HIGHST 
#perhas a bug vids with spaces in name. solution = no spaces in names of vids

# Set the absolute path to your video folder
video_folder="/home/seb/dev/artinstallation31maj/flasklogic/videos"

# Get a list of all video files in the folder and sort them
video_files=($(ls -v "$video_folder"/*.mp4))

# Check if there are any video files
if [ ${#video_files[@]} -eq 0 ]; then
    echo "No video files found in the specified folder."
    exit 1
fi

# Loop through the sorted videos and play them in fullscreen
for video in "${video_files[@]}"; do
    echo "Playing: $video"
    #cvlc --fullscreen --play-and-exit "$video"
    cvlc --fullscreen --no-osd --play-and-exit "$video" #no tiles and informatics 
done

echo "All videos have been played."
