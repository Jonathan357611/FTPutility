import ftplib
import os
from colorama import Fore, Back, init

init(autoreset=True)

# Solution by Jwely: https://stackoverflow.com/a/36776584


def _is_ftp_dir(ftp_handle, name, guess_by_extension=True):
    """simply determines if an item listed on the ftp server is a valid directory or not"""

    # if the name has a "." in the fourth to last position, its probably a file extension
    # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
    if guess_by_extension is True:
        if name[-4] == ".":
            return False

    original_cwd = ftp_handle.pwd()  # remember the current working directory
    try:
        ftp_handle.cwd(name)  # try to set directory to new name
        ftp_handle.cwd(original_cwd)  # set it back to what it was
        return True
    except:
        return False


def _make_parent_dir(fpath):
    """ensures the parent directory of a filepath exists"""
    dirname = os.path.dirname(fpath)
    while not os.path.exists(dirname):
        try:
            os.mkdir(dirname)
            print(f"{Fore.GREEN}created {dirname}!")
        except:
            _make_parent_dir(dirname)


def _download_ftp_file(ftp_handle, name, dest, overwrite):
    """downloads a single file from an ftp server"""
    _make_parent_dir(dest)
    if not os.path.exists(dest) or overwrite is True:
        with open(dest, "wb") as f:
            ftp_handle.retrbinary(f"RETR {name}", f.write)
        print(f"{Fore.GREEN}downloaded {dest}")
    else:
        print(f"{Fore.RED}{dest} already exists, skipping")


def _mirror_ftp_dir(ftp_handle, name, overwrite, guess_by_extension):
    """replicates a directory on an ftp server recursively"""
    for item in ftp_handle.nlst(name):
        if _is_ftp_dir(ftp_handle, item):
            _mirror_ftp_dir(ftp_handle, item, overwrite, guess_by_extension)
        else:
            _download_ftp_file(ftp_handle, item, item, overwrite)


def download_ftp_tree(
    ftp_handle, path, destination, overwrite=False, guess_by_extension=True
):
    try:
        os.chdir(destination)
    except:
        print(f"{Fore.RED}Folder not found!")
    _mirror_ftp_dir(ftp_handle, path, overwrite, guess_by_extension)
    # print(f"{Fore.GREEN}All files downloaded!")
