import os
import subprocess

def merge_flac_with_last_track_metadata(folder_path):
    # Getting all FLAC files in order
    flac_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".flac")])
    if not flac_files:
        print("No FLAC files found.")
        return

    # Creating concat input string
    input_str = "|".join([os.path.join(folder_path, f) for f in flac_files])

    # Merging all tracks losslessly
    temp_output = os.path.join(folder_path, "temp_full_album.flac")
    merge_cmd = [
        "ffmpeg",
        "-i", f"concat:{input_str}",
        "-c:a", "flac",  # re-encode to fix timestamps
        "-vn",            # ignore album art streams
        temp_output
    ]
    subprocess.run(merge_cmd, check=True)

    # metadata from the last track
    last_track_path = os.path.join(folder_path, flac_files[-1])
    # FFmpeg command to copy all metadata but override track number
    full_album_path = os.path.join(folder_path, "Full Album.flac")
    album_number = len(flac_files) + 1
    metadata_cmd = [
        "ffmpeg",
        "-i", temp_output,
        "-i", last_track_path,
        "-map_metadata", "1", 
        "-c", "copy",
        "-metadata", f"track={album_number}",
        "-metadata", "title=Full Album",
        full_album_path
    ]
    subprocess.run(metadata_cmd, check=True)

    # Cleaning up temporary file
    os.remove(temp_output)

    print(f"Full album created: {full_album_path} (track {album_number})")

if __name__ == "__main__":
    
    album_folder = input("Enter the path to the album folder: ")
    merge_flac_with_last_track_metadata(album_folder)





