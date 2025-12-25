import os
from fullalbumgenerator import merge_flac_with_last_track_metadata

# Parent folder containing all artists
parent_folder = r"G:\Music"

# Loop through each artist folder
for artist_name in os.listdir(parent_folder):
    artist_path = os.path.join(parent_folder, artist_name)
    if not os.path.isdir(artist_path):
        continue  # skip files

    # Loop through each album folder inside the artist folder
    for album_name in os.listdir(artist_path):
        album_path = os.path.join(artist_path, album_name)
        if not os.path.isdir(album_path):
            continue  # skip files

        full_album_file = os.path.join(album_path, "Full Album.flac")
        if os.path.exists(full_album_file):
            print(f"Skipping '{artist_name} - {album_name}' (Full Album already exists)")
            continue

        print(f"Generating Full Album for '{artist_name} - {album_name}'...")
        merge_flac_with_last_track_metadata(album_path)
