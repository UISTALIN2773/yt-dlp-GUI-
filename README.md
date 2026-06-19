

yt-dlp GUI



A simple desktop graphical interface for yt-dlp built with Python and Tkinter.
Overview
This project provides a graphical user interface (GUI) for yt-dlp, allowing users to download videos and audio without using the command line.
The goal is to make yt-dlp easier to use for people who are not familiar with terminal commands.
 
Features
•	Download videos as MP4
•	Download audio as MP3
•	Select destination folder
•	Real-time download logs
•	Simple and intuitive interface
•	Error handling and validation
•	Built with Python and Tkinter
My Contribution
This project does not replace yt-dlp and is not a fork of the original project.
My contribution was developing a desktop GUI that acts as a bridge between the user and yt-dlp, making downloads easier through a visual interface.
The application communicates with yt-dlp using Python's subprocess module.
Requirements
yt-dlp
Official Repository:
https://github.com/yt-dlp/yt-dlp
FFmpeg
Official Repository:
https://github.com/yt-dlp/FFmpeg-Builds
FFmpeg is required for audio extraction and media processing.
Installation
1.	Clone this repository:
git clone https://github.com/TU-USUARIO/yt-dlp-gui.git
2.	Download:
•	yt-dlp.exe
•	ffmpeg.exe
•	ffprobe.exe
3.	Place them in the same directory as:
yt_dlp_gui.py
Run
python yt_dlp_gui.py
Build Executable
Install PyInstaller:
pip install pyinstaller
Generate executable:
pyinstaller --onefile --windowed yt_dlp_gui.py
Project Structure
yt-dlp-gui/
│
├── yt_dlp_gui.py
├── README.md
├── requirements.txt
└── .gitignore
Credits
All credit for the download engine belongs to the yt-dlp development team.
Official repositories:
•	https://github.com/yt-dlp/yt-dlp
•	https://github.com/yt-dlp/FFmpeg-Builds
This project only provides a graphical interface and integration layer.
License
This project depends on third-party software.
Please review the licenses of:
•	yt-dlp
•	FFmpeg
before redistributing any binaries.
antes de redistribuir binarios incluidos en este repositorio.
