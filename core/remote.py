from . import common
import datetime
import shutil
import subprocess
import tarfile
import tempfile
import warnings


def push():
    remote = common.getConfig("remote_folder")
    if shutil.which("rsync") is None:
        raise Exception("No 'rsync' found. Cannot upload files. Aborting.")
    if remote is None:
        raise Exception("No remote folder configured. Aborting.")
    files_to_archive = []
    if not common.HISTORY_FILE.exists():
        raise Exception("No file containing data has been found. Aborting.")
    else:
        files_to_archive.append(common.HISTORY_FILE)
    if not common.ACTIVITIES_FILE.exists():
        warnings.warn("No activity file has been found: it will be omitted inside the archive!")
    else:
        files_to_archive.append(common.ACTIVITIES_FILE)

    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    target_name = f"{remote}/archived_{year:04d}{month:02d}{day:02d}.tgz"
    with tempfile.NamedTemporaryFile() as f:
        archive = tarfile.open(f.name, "w:gz")
        for file in files_to_archive:
            archive.add(file)
        archive.close()
        cli = ["rsync", "-a", "-z", "-P", f.name, target_name]
        print(">> {}".format(" ".join(cli)))
        proc = subprocess.run(cli)
        return proc.returncode
