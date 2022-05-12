# video_streaming_application
A video conferencing application that allows video, voice, and chat by text. This application enables two clients to connect to a hosted server on a local network.

## Capabilities
- Each client may mute or unmute audio
- Each client may be able to message over a text interface
- Each client can display their video camera

## Technology
1. QT Designer
2. PyQT (Python library)
3. Pickle (Python library)
4. Threading (Python library)
5. Time (Python library)
6. Socket (Python library)
7. Numpy (Python library)

## Download
The user may either choose to download the source or download a one of the selected releases. Downloading the source has advantages.
Executables for the clients and the servers.
The pre-releases may not function as intended as the user must hardcode the server or host IP in the Video_client.py file.
For this reason, please consider downloading the source instead.

## Source
1. Ensure that the Python and all of its dependencies are installed
2. Open Video_client and change `host_ip` variable to the IP of where the server will be run
3. Navigate to the Video_Application directory
4. Execute `python Video_server.py` first
5. Execute `python Video_client.py` next on one machine
6. Execute `python Video_client.py` (previous command in step 5) on preferably on another machine

## Notes
- The user must ensure that the camera of the machine works if displaying the video feed is desired
- Running the clients before the server may fail because the clients will timeout quickly if no server on the LAN is discovered
