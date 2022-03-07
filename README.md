# FTPutility 
FTPutility is a tool written by me to simple interact with a FTP-server in a 'Linux-Like-Environment' where I also tried to make a visually appearing TUI (Hope that worked!).

Please note that this tool was written for Linux! It propably wont work in Windows!

The tool isn't great, it's only written by me to learn programming!

## Installation 💿
```bash
git clone https://github.com/Jonathan357611/FTPutility.git
cd FTPutility
pip3 install -r requirements.txt
```
## Usage 🪛
Just run ```python3 main.py``` and enter your servers credentials,
The program will then try to connect to it.

The program will now open a console where you can interact with your server.
type ```help``` to see all commands on the go.

#### All valid commands:
- ls             - List all files
- cd <dir>       - Go to dir
- rm <file>      - Remove file
- get / download - Download file/dir
- upload         - Upload local file to server
- cat <file>     - Show file contents
- CTRL+c/exit    - Logout
  
## Notes 🗒️
Any contributions are very welcome so that I can learn more!

I formated my program using black, huge thanks for that handy tool :)
