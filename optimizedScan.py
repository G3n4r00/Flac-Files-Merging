import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from fullalbumgenerator import merge_flac_with_last_track_metadata

MUSIC_ROOT = r"P:\Soulseek Downloads\complete"
MAX_WORKERS = max(1, os.cpu_count() // 2)


def looks_like_album(folder):
    """folder with at least 2 FLAC files"""
    try:
        flacs = [f for f in os.listdir(folder) if f.lower().endswith(".flac")]
        return len(flacs) >= 2
    except OSError:
        return False


def find_album_folders(root):
    albums = []

    for entry in sorted(os.listdir(root)):
        entry_path = os.path.join(root, entry)
        if not os.path.isdir(entry_path):
            continue

        # Case 1: albums directly under MUSIC_ROOT
        if looks_like_album(entry_path):
            if not os.path.exists(os.path.join(entry_path, "Full Album.flac")):
                albums.append(entry_path)
            continue

        # Case 2: artist -> album structure
        for sub in sorted(os.listdir(entry_path)):
            album_path = os.path.join(entry_path, sub)
            if not os.path.isdir(album_path):
                continue

            if not looks_like_album(album_path):
                continue

            if os.path.exists(os.path.join(album_path, "Full Album.flac")):
                continue

            albums.append(album_path)

    return albums


if __name__ == "__main__":
    album_folders = find_album_folders(MUSIC_ROOT)

    print(f"Found {len(album_folders)} albums to process")
    print(f"Using {MAX_WORKERS} parallel workers\n")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(merge_flac_with_last_track_metadata, album): album
            for album in album_folders
        }

        for future in as_completed(futures):
            album = futures[future]
            try:
                future.result()
                print(f"✓ Done: {album}")
            except Exception as e:
                print(f"✗ Failed: {album}\n  {e}")
