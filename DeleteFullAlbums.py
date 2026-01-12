import os
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_FILENAME = "Full Album.flac"

def delete_if_match(file_path: str) -> bool:
    try:
        if os.path.basename(file_path) == TARGET_FILENAME:
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")
    return False

def collect_files(root_folder: str):
    for root, _, files in os.walk(root_folder):
        for name in files:
            if name == TARGET_FILENAME:
                yield os.path.join(root, name)

def main(music_root: str):
    deleted = 0

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        futures = [executor.submit(delete_if_match, path)
                   for path in collect_files(music_root)]

        for future in as_completed(futures):
            if future.result():
                deleted += 1

    print(f"Deleted {deleted} file(s) named '{TARGET_FILENAME}'.")

if __name__ == "__main__":
    MUSIC_FOLDER = r"P:\Soulseek Downloads\complete" 
    main(MUSIC_FOLDER)
