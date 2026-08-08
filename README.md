# badtuya
A really bad script for controlling a single tuya light, features effect loading and closes to system tray, poorly written in python.
## Setup
you need the following
`pip install pillow customtkinter pystray`
you also need to edit `config.json` with the device's local key, IP, and device id. These can be grabbed from the tuya dev website.
writing effects is simple, they're written in normal python, with tinytuya. Example.py is a great place to start
