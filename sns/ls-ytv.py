import requests
import json
import os
import subprocess
import time

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# Load channels from JSON file
with open("ytCh.json", "r") as file:
    channels = json.load(file)["channels"]

# Display the list of channels
print("Select a channel from the list:")
for i, channel in enumerate(channels, start=1):
    print(f"{i}. {channel['name']}")

# Get user input
choice = int(input("Enter the number of your chosen channel: ")) - 1
if choice < 0 or choice >= len(channels):
    print("Invalid choice.")
    exit()

# Get the selected channel ID
selected_channel = channels[choice]
CHANNEL_ID = selected_channel["id"]

# Step 1: Get the Uploads Playlist ID
channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={YOUTUBE_API_KEY}"
response = requests.get(channel_url).json()

if "error" in response:
    print(f"Error fetching channel data: {response['error']['message']}")
    exit()

uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Step 2: Get Videos from the Playlist
playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults=50&key={YOUTUBE_API_KEY}"
videos = []

while playlist_url:
    response = requests.get(playlist_url).json()
    if "error" in response:
        print(f"Error fetching playlist data: {response['error']['message']}")
        break

    for item in response.get('items', []):
        videos.append({
            "title": item["snippet"]["title"],
            "videoId": item["snippet"]["resourceId"]["videoId"]
        })

    playlist_url = (
        f"https://www.googleapis.com/youtube/v3/playlistItems?pageToken={response.get('nextPageToken')}&part=snippet&playlistId={uploads_playlist_id}&maxResults=50&key={YOUTUBE_API_KEY}"
        if "nextPageToken" in response
        else None
    )

# Step 3: Display video titles with index
if videos:
    print(f"\nVideos from {selected_channel['name']}:\n")
    for idx, video in enumerate(videos, start=1):
        print(f"{idx}. {video['title']}")

    # Step 4: Get user choice for video
    video_choice = int(input("\nEnter the number of the video you want to watch: ")) - 1
    if video_choice < 0 or video_choice >= len(videos):
        print("Invalid choice.")
        exit()

    # Step 5: Check if Docker container is running and start it if not
    container_name = "ubuntu"
    try:
        # Check if the container is running
        subprocess.run(['docker', 'ps', '--filter', f'name={container_name}'], check=True)
    except subprocess.CalledProcessError:
        print("Docker container is not running. Starting Docker Desktop...")
        # Open Docker Desktop if the container is not running
        subprocess.run(['open', '/Applications/Docker.app'], check=True)

        print("Waiting for Docker to start...")
        # Wait a few seconds for Docker to be ready
        time.sleep(10)  # Adjust this if needed

        # Pull and run the Docker container if it doesn't exist
        print("Setting up the Docker container...")
        subprocess.run(["docker", "pull", "ubuntu:latest"], check=True)
        subprocess.run(["docker", "run", "-d", "--name", container_name, "ubuntu:latest", "sleep", "infinity"], check=True)

        # Install necessary dependencies inside the container
        install_commands = [
            "apt-get update",
            "apt-get install -y wget curl gnupg",
            "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
            "apt install -y ./google-chrome-stable_current_amd64.deb",
            "apt-get install -y libnss3 libatk-bridge2.0-0 libxss1 libgdk-pixbuf2.0-0 libgtk-3-0"
        ]
        
        for command in install_commands:
            subprocess.run(["docker", "exec", "-it", container_name, "bash", "-c", command], check=True)

        # Now check if the container is available
        try:
            subprocess.run(['docker', 'start', container_name], check=True)
        except subprocess.CalledProcessError:
            print(f"Error: Could not start the Docker container {container_name}.")
            exit()

    # Step 6: Play the selected video
    selected_video = videos[video_choice]
    video_url = f"https://www.youtube.com/watch?v={selected_video['videoId']}"

    print(f"Opening video: {selected_video['title']}")

    # Open the video in Google Chrome inside the Docker container
    subprocess.run(['docker', 'exec', '-d', container_name, 'google-chrome', '--no-sandbox', '--incognito', video_url])

else:
    print("No videos found.")
