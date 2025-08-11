import os

def rotate_backups(json_file, max_versions=3):
    # Delete the oldest
    oldest = f"{json_file}.{max_versions}"
    if os.path.exists(oldest):
        os.remove(oldest)

    # Shift other versions
    for i in range(max_versions - 1, 0, -1):
        src = f"{json_file}.{i}"
        dst = f"{json_file}.{i+1}"
        if os.path.exists(src):
            os.rename(src, dst)

    # Move current to .1
    if os.path.exists(json_file):
        os.rename(json_file, f"{json_file}.1")
