from keep_alive import keep_alive
import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Start Flask server to keep Replit alive
keep_alive()

# Authenticate with saved token
creds = Credentials.from_authorized_user_file(
    "token.json",
    ["https://www.googleapis.com/auth/youtube.force-ssl"]
)
youtube = build("youtube", "v3", credentials=creds)

# Source and target video IDs
VIDEO_SOURCE = "BxV14h0kFs0"  # Video to read title + views from
VIDEO_TARGET = "86LgJKEuo2I"  # Video to update title

# Get current title and view count from source video
def get_source_title_and_views(video_id):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()
    item = response["items"][0]
    title = item["snippet"]["title"]
    views = item["statistics"]["viewCount"]
    return title, views

# Update the title of the target video
def update_title(source_title, view_count):
    formatted_views = f"{int(view_count):,}"
    new_title = f'"{source_title}" has {formatted_views} views (I guess...)'
    youtube.videos().update(
        part="snippet",
        body={
            "id": VIDEO_TARGET,
            "snippet": {
                "title": new_title,
                "categoryId": "22"
            }
        }
    ).execute()

# Loop: fetch and update every 60 seconds
while True:
    try:
        source_title, source_views = get_source_title_and_views(VIDEO_SOURCE)
        update_title(source_title, source_views)
        print(f'Updated title to: "{source_title}" has {int(source_views):,} views (I guess...)')
    except Exception as e:
        print("Error:", e)
    time.sleep(60)
