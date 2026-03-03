from datetime import datetime
import random
import uuid
import pandas as pd
import os
from subprocess import Popen, PIPE

# Ensure thumbnails directory exists
THUMBNAIL_DIR = "songs/thumbnails"
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv("song.csv",sep=";")


def extract_metadata(row):

    file_path = str(row["musicName"])

    # -----------------------
    # Extract Metadata
    # -----------------------
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format_tags=artist,title,album,date",
        "-of", "default=nw=1",
        file_path
    ]

    result = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = result.communicate()

    text = stdout.decode().strip()
    lines = text.split("\n")

    data = {}

    for line in lines:
        if line.startswith("TAG:"):
            key, value = line.replace("TAG:", "").split("=", 1)
            data[key] = value

    # -----------------------
    # Date Formatting
    # -----------------------
    date_str = data.get("date")

    if date_str:
        date_str = date_str.strip()

        # Only year (yyyy)
        if len(date_str) == 4 and date_str.isdigit():
            year = int(date_str)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date_str = f"{year}{month:02d}{day:02d}"

        # Format yyyy-MM-dd
        else:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                date_str = dt.strftime("%Y%m%d")
            except:
                pass
    else:
        date_str = ""

    # -----------------------
    # Thumbnail Extraction
    # -----------------------
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    thumbnail_name = f"{base_name}.jpg"
    thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_name)

    extract_command = [
        "ffmpeg",
        "-y",
        "-i", file_path,
        "-map", "0:v:0",
        "-frames:v", "1",
        "-update", "1",
        thumbnail_path
    ]

    result = Popen(extract_command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = result.communicate()

    # If thumbnail not created (no album art), set empty
    if not os.path.exists(thumbnail_path):
        thumbnail_name = ""

    # -----------------------
    # Return Clean Series
    # -----------------------
    return pd.Series({
        "id": uuid.uuid4().hex,
        "fileName": os.path.basename(file_path),
        "title": str(data.get("title", "")).replace("_", " "),
        "artistName": data.get("artist", ""),
        "album": data.get("album", ""),
        "createdDate": date_str,
        "musicUrl": file_path,
        "musicThumbnailUrl": thumbnail_name
    })


# Apply extraction
metadata_df = df.apply(extract_metadata, axis=1)

# Save CSV
metadata_df.to_csv("song_with_metadata.csv", index=False)

# Save JSON
metadata_df.to_json(
    "song_with_metadata.json",
    orient="records",
    indent=2
)

print("✅ Metadata extraction complete.")
print("📁 CSV: song_with_metadata.csv")
print("📁 JSON: song_with_metadata.json")
