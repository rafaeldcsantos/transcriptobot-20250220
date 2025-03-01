import os
import re
import subprocess

def convert_timestamp_to_seconds(timestamp):
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", timestamp)
    if not match:
        return None
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds

def extract_srt_timestamps(srt_file):
    entries = []
    with open(srt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    temp_entry = None
    for line in lines:
        line = line.strip()
        
        if line.isdigit():
            temp_entry = {"id": line, "timestamp": ""}
        elif "-->" in line:
            if temp_entry:
                temp_entry["timestamp"] = line.split(" --> ")[0]
        elif line == "":
            if temp_entry:
                entries.append(temp_entry)
                temp_entry = None
    
    return entries

def generate_thumbnails(video_file, srt_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    timestamps = extract_srt_timestamps(srt_file)
    
    for entry in timestamps:
        seconds = convert_timestamp_to_seconds(entry["timestamp"])
        if seconds is None:
            continue
        
        output_path = os.path.join(output_folder, f"{entry['id']}.jpg")
        
        cmd = [
            "ffmpeg", "-y", "-ss", str(seconds), "-i", video_file,
            "-vf", "scale=-1:64", "-vframes", "1", output_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Generated thumbnail: {output_path}")

if __name__ == "__main__":
    video_file = "video.mp4"  # Change to your actual video file
    srt_file = "subtitles.srt"  # Change to your actual SRT file
    output_folder = "Thumbnails"
    
    generate_thumbnails(video_file, srt_file, output_folder)