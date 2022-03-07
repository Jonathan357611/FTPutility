from ftplib import FTP_TLS
import ftplib
from colorama import Fore, Back, init
import pwinput
import sys, os, io
import download_dir

init(autoreset=True)


def deleteLast():  # https://stackoverflow.com/a/52590238
    "Use this function to delete the last line in the STDOUT"
    # cursor up one line
    sys.stdout.write("\x1b[1A")
    # delete last line
    sys.stdout.write("\x1b[2K")


def main(ftp):
    while True:
        CURR_PATH = ftp.pwd()

        command = input(f"{Fore.CYAN}( {Fore.BLUE}{CURR_PATH} {Fore.CYAN}) $ ")

        if command == "help":
            print(
                f"{Fore.CYAN}HELP{Fore.RESET}\nls             - List all files\ncd <dir>       - Go to dir\nrm <file>      - Remove file\nget / download - Download file/dir\nupload         - Upload local file to server\ncat <file>     - Show file contents\nCTRL+c/exit    - Logout"
            )

        elif command == "ls":
            ls_list = list()
            all_files = ftp.nlst()
            for file in all_files:
                try:
                    ftp.cwd(file)
                    ls_list.append(f"{Fore.BLUE}{file}")
                    ftp.cwd("..")
                except Exception as e:
                    ls_list.append(f"{Fore.RESET}{file}")

            for i, item in enumerate(ls_list):
                marker = ""
                if i % 5 == 0 and i != 0:
                    print()
                if " " in item:
                    marker = "'"
                print(f"{marker}{item}{marker}  ", end="")

            print()

        elif command.split(" ")[0] == "cd":
            ftp.cwd(f"{CURR_PATH}/{command.split(' ')[1]}")

        elif command.split(" ")[0] == "rm":
            ftp.delete(f"{CURR_PATH}/{command.split(' ')[1]}")

        elif command == "get" or command == "download":
            print(f"NOTE: This selection will be automated in near future!")
            filetype = input(f"{Fore.BLUE}Filetype: [F]ile / [D]irectory > ")
            server_file = input(f"{Fore.BLUE}Server file > ")
            local_file = input(f"{Fore.BLUE}Local file > ")

            if filetype.upper() == "D":
                download_dir.download_ftp_tree(ftp, server_file, local_file)
            else:
                print(f"{Fore.YELLOW}Downloading...")
                ftp.retrbinary("RETR " + server_file, open(local_file, "wb").write)
                deleteLast()
                print(f"{Fore.GREEN}File downloaded!")

        elif command == "upload":
            localfile = input(f"{Fore.BLUE}Local source file > ")
            remotefile = input(f"{Fore.BLUE}Server target file > ")

            try:
                with open(localfile, "rb") as file:
                    ftp.storbinary("STOR %s" % remotefile, file)
            except FileNotFoundError:
                print(f'{Fore.RED}File "{localfile}" not found!')
            else:
                print(f"{Fore.GREEN}File uploaded!")

        elif command.split(" ")[0] == "cat":
            output = io.StringIO()
            try:
                ftp.retrlines("RETR " + command.split(" ")[1], output.write)
            except Exception:
                print(
                    f"{Fore.RED}Seems like this file doesn't exist or is a directory!"
                )
            except UnicodeDecodeError:
                print(f"{Fore.RED}Bytefiles (Images, movies...) are not supported!")
            else:
                print(f"{Fore.RESET}{output.getvalue()}")


if __name__ == "__main__":
    host = input(f"{Fore.CYAN}Host $ {Fore.RESET}")
    user = input(f"{Fore.CYAN}User $ {Fore.RESET}")
    passwd = pwinput.pwinput(f"{Fore.CYAN}Password $ ")

    while True:
        ftp = FTP_TLS()
        try:
            print(f"{Fore.YELLOW}Connecting...")
            ftp.connect(host, 21)
            deleteLast()
            print(f"{Fore.YELLOW}Running USER command...")
            ftp.sendcmd(f"USER {user}")
            deleteLast()
            print(f"{Fore.YELLOW}Running PASS command...")
            ftp.sendcmd(f"PASS {passwd}")
            deleteLast()
        except Exception:
            print(f"{Fore.RED}Error during login. Please check host and credentials!")
            exit(1)

        try:
            main(ftp)

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nQuitting...")
            ftp.quit()
            deleteLast()
            print(f"{Fore.GREEN}Bye!")
            exit(1)
