import shutil
import os


def create_archive(user_dir, lst):
    files_dir = os.path.join(user_dir, "files")
    os.mkdir(files_dir)
    for num, note in enumerate(lst):
        file_name = os.path.join(files_dir, "file" + str(num) + ".txt")
        with open(file_name, 'w') as file:
            file.write(note[0])

    archive_name = os.path.join(user_dir, "export")
    shutil.make_archive(archive_name, 'zip', files_dir)
    shutil.rmtree(files_dir)
    return os.path.join(user_dir, "export.zip")
