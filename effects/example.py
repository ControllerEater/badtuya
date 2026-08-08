# Example script for building off of, flips between blue and red cop-style.
# by cupri, blah blah blah polyform noncommercial
from tinytuya import BulbDevice
from time import sleep
import customtkinter
running = True
def settings(app, setfont):
    # region making the window not look like shit
    # region fonts
    header = (setfont, 50, "bold")
    bold = (setfont, 20, "bold")
    normal = (setfont, 20)
    big = (setfont, 35)
    bigbold = (setfont, 35, "bold")
    # endregion
    settings = customtkinter.CTkToplevel(app)
    settings.title("Colorpicker")
    # Get main window position
    app.update_idletasks()
    x = app.winfo_x()
    y = app.winfo_y()
    width = app.winfo_width()
    height = app.winfo_height()
    # Center settings window
    settings_width = 500
    settings_height = 200
    pos_x = x + (width - settings_width) // 2
    pos_y = y + (height - settings_height) // 2
    settings.geometry(f"500x200+{pos_x}+{pos_y}")
    settings.transient(app)
    settings.grab_set()
    #endregion
    label = customtkinter.CTkLabel(settings, text="Example Settings", fg_color="transparent", font=header)
    label.pack(padx=20, pady=10)
def run(bulb:BulbDevice):
    global running
    running = True
    while running:
        for hue in range(360):
            if not running:
                return
            # write your code here
            print("Example")
            bulb.set_colour(255,0,0)
            sleep(5)
            bulb.set_colour(0,0,255)
            sleep(5)
def stop():
    global running
    running = False