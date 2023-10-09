import os

def create_dir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return


def run_dir_checks():
    required_dirs = ["videos", "audio", "output"]

    for dir in required_dirs:
        create_dir_if_not_exists(dir)
