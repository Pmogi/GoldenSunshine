# GoldenSunshine
A Windows 10 process written in Python that notfies the user when a new video is available from David Lynch's series of morning videos.

Python 3.6> required with commandline path set for Python.
Your own YouTube API key must also be provided in a config.py file.
Dependencies are installed with setup.py file.

- Running Setup.py with the install command will download the dependencies. `Python setup.py install` while in the main directory of the repository.
- The program is started either by starting the `__init__.py` file manually,
- or dropping a shortcut to the `__init__.py` file in \Programs\Startup\. With the startup shortcut, it'll initiate the shortcut each bootup.
