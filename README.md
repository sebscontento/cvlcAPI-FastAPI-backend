# cvlcAPI-FastAPI-backend


This project is a reimplementation of a flask API backend for CVLC 
https://github.com/sebscontento/cvlcAPI-flask-backend

This is the FastAPI backend for CVLC (Commandline VLC) API. It provides a backend for controlling VLC media player using APIs. It is designed for linux servers. 

Feel free to modify, redistribute and/or modify this project to your needs. 
Do not hesitate to reach out if you have any questions or want to contribute to this project.


## Start the server 

Navigate to directory then use command: 
uvicorn app:app --reload --host 0.0.0.0

Preferbly use the bashscript start_fastapi.sh
./start_fastapi.sh


The following examples shows how to send commands to the servers as well as configuring your linux machine. 

## Example endpoints

curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:8000/play 
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:8000/stop 
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:8000/pause
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:8000/resume 
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:8000/restart


## Modified examples for play/stop/pause/resume/restart
Make sure to change the location of the directories for videos, playlists and picutes.
Make sure to change the IP address accordingly. 

curl -X POST -H "Content-Type: application/json" -d '{"filename": "/home/seb/dev/fasttestapi/videos/1.mp4"}' http://custom-IP:8000/play
curl -X POST -H "Content-Type: application/json" -d '{"filename": "/home/seb/dev/fasttestapi/videos/1.mp4"}' http://custom-IP:8000/stop
curl -X POST -H "Content-Type: application/json" -d '{"filename": "/home/seb/dev/fasttestapi/videos/1.mp4"}' http://custom-IP:8000/pause
curl -X POST -H "Content-Type: application/json" -d '{"filename": "/home/seb/dev/fasttestapi/videos/1.mp4"}' http://custom-IP:8000/resume
curl -X POST -H "Content-Type: application/json" -d '{"filename": "/home/seb/dev/fasttestapi/videos/1.mp4"}' http://custom-IP:8000/restart


## Modified examples for playlists 
Feel free to use my bashscripts for playlists in CVLC
Make sure to change the location of the directories for videos inside the scripts. 
Make sure to change the permissions of the scripts
navigate to the directory where the playlists are located then use:
chmod +x randomplaylist1.sh

curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "randomplaylist1.sh"}' http://127.0.0.1:8000/playlist/start
curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "randomplaylist1.sh"}' http://127.0.0.1:8000/playlist/stop


## Examples for reboot 
Make sure you change the configuration for username and password. This is located inside the app.py file
curl -X POST -u user:password http://127.0.0.1:8000/reboot

Make sure you give permission on the local machine you want to reboot (!caution! this can have security implications!)
step 1:
sudo visudo 

step 2:
paste the following (remember to replace usernname to your username on your machine) 
username ALL=(ALL) NOPASSWD: /sbin/reboot



