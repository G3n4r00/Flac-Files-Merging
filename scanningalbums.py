import os
from fullalbumgenerator import merge_flac_with_last_track_metadata

# Parent folder containing all album folders
parent_folder = r"D:\Testingsss"

# Loop through each album folder
for album_name in os.listdir(parent_folder):
    album_path = os.path.join(parent_folder, album_name)
    if not os.path.isdir(album_path):
        continue  # skip files, we only want folders

    full_album_file = os.path.join(album_path, "Full Album.flac")
    if os.path.exists(full_album_file):
        print(f"Skipping '{album_name}' (Full Album already exists)")
        continue

    print(f"Generating Full Album for '{album_name}'...")
    merge_flac_with_last_track_metadata(album_path)
