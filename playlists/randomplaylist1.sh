#!/bin/bash

#Author: Sebastian Solórzano Holbøll
#version: 4
#THIS IS JUST A PLAYLIST PLAYS FROM LOWEST OT HIGHST 

# Set the absolute path to your video folder
video_folder="/home/seb/dev/artinstallation31maj/flasklogic/videos"

# Get a list of all video files in the folder
video_files=("$video_folder"/*.mp4)

# Check if there are any video files
if [ ${#video_files[@]} -eq 0 ]; then
    echo "No video files found in the specified folder."
    exit 1
fi

# Shuffle the video files randomly
shuffled_videos=($(shuf -e "${video_files[@]}"))

# Loop through the shuffled videos and play them in fullscreen
for video in "${shuffled_videos[@]}"; do
    echo "Playing: $video"
    #cvlc --fullscreen --play-and-exit "$video"
    cvlc --fullscreen --no-osd --play-and-exit "$video" #no tiles and informatics 
done

echo "All videos have been played."


