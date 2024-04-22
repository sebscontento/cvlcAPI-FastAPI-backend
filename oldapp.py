from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import psutil

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cvlc_process = None
current_filename = None
playlist_playing = False
playlist = []

playlists_folder = os.path.expanduser("~/dev/fasttestapi/playlists")
video_folder = os.path.expanduser("~/dev/fasttestapi/videos")
picture_folder = os.path.expanduser("~/dev/fasttestapi/pics")


@app.get("/")
async def index():
    video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
    return {"video_folder": video_folder, "video_files": video_files}


def play_video(filename):
    global cvlc_process
    cvlc_process = subprocess.Popen(['cvlc', '--fullscreen', '--no-osd', '--loop', filename])


@app.post("/play")
async def play(request: Request):
    global cvlc_process, current_filename
    data = await request.json()
    filename = data.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    if filename != current_filename:
        if cvlc_process:
            cvlc_process.terminate()
        play_video(filename)
        current_filename = filename
        return {"status": "playing", "filename": filename}
    else:
        return {"status": "video is already playing", "filename": filename}


@app.post("/stop")
async def stop():
    global cvlc_process
    if cvlc_process:
        cvlc_process.terminate()
        return {"status": "stopped"}
    else:
        return {"status": "no video is playing"}


@app.post("/pause")
async def pause():
    global cvlc_process
    if cvlc_process:
        cvlc_process.send_signal(subprocess.signal.SIGSTOP)
        return {"status": "paused"}
    else:
        return {"status": "no video is playing"}


@app.post("/resume")
async def resume():
    global cvlc_process
    if cvlc_process:
        cvlc_process.send_signal(subprocess.signal.SIGCONT)
        return {"status": "resumed"}
    else:
        return {"status": "no video is playing"}


@app.post("/restart")
async def restart():
    global current_filename, cvlc_process
    if current_filename:
        if cvlc_process and cvlc_process.poll() is None:
            cvlc_process.terminate()
        play_video(current_filename)
        return {"status": "restarted", "filename": current_filename}
    else:
        return {"status": "no video is playing"}


@app.post("/playlist/start")
async def start_playlist(request: Request):
    global playlist_playing, cvlc_process
    if playlist_playing:
        raise HTTPException(status_code=400, detail="Another playlist is already playing")

    data = await request.json()
    playlist_name = data.get("playlist_name")
    if not playlist_name:
        raise HTTPException(status_code=400, detail="Playlist name is required")

    playlist_path = os.path.join(playlists_folder, playlist_name)
    if not os.path.isfile(playlist_path):
        raise HTTPException(status_code=404, detail="Playlist not found")

    try:
        cvlc_process = subprocess.Popen([playlist_path, video_folder])
        playlist_playing = True
        return {"status": f"Playlist {playlist_name} started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/playlist/stop")
async def stop_playlist():
    global playlist_playing, cvlc_process
    if not playlist_playing:
        raise HTTPException(status_code=400, detail="No playlist is currently playing")

    if cvlc_process:
        try:
            parent = psutil.Process(cvlc_process.pid)
            children = parent.children(recursive=True)
            for process in children:
                process.kill()

            parent.kill()
            parent.wait()
            playlist_playing = False
            cvlc_process = None
            return {"status": "Playlist stopped successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="No playlist process found")


@app.get("/picture")
async def get_picture(picture_name: str):
    if not picture_name:
        raise HTTPException(status_code=400, detail="Picture name is required")

    picture_path = os.path.join(picture_folder, picture_name)
    if not os.path.isfile(picture_path):
        raise HTTPException(status_code=404, detail="Picture not found")

    subprocess.Popen(['cvlc', '--fullscreen', '--no-osd', '--loop', picture_path])
    return {"status": "Picture displayed"}


@app.post("/close_picture")
async def close_picture():
    subprocess.Popen(['killall', 'vlc'])
    return {"status": "Picture closed"}


#users = {'seb': 'psw', 'user2': 'password2'}

"""
@app.post("/shutdown")
async def shutdown(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not (auth in users and users[auth]):
        raise HTTPException(status_code=401, detail="Unauthorized")

    os.system("sudo shutdown -h now")
    return "Server is shutting down..."


@app.post("/reboot")
async def reboot(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not (auth in users and users[auth]):
        raise HTTPException(status_code=401, detail="Unauthorized")

    os.system("sudo reboot")
    return "Server is rebooting..."

"""

users = {'seb': 'psw', 'user2': 'password2'}

@app.post("/reboot")
async def reboot(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Unauthorized")

    auth_type, auth_token = auth.split(" ", 1)
    if auth_type.lower() != "basic":
        raise HTTPException(status_code=401, detail="Unauthorized")

    decoded_credentials = auth_token.encode("utf-8").decode("base64")
    username, password = decoded_credentials.split(":", 1)

    if not (username in users and users[username] == password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    os.system("sudo reboot")
    return "Server is rebooting..."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
