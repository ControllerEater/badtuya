# Queer little rainbow effect for gay little fellows
# made by Cupri, licensed under the Polyform noncommercial license
from tinytuya import BulbDevice
import colorsys
import time
import customtkinter
running = True
cycle_speed = 10
def settings(app, setfont):
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
    global cycle_speed # get cycle speed for display
    label = customtkinter.CTkLabel(settings, text="Cycle Settings", fg_color="transparent", font=header)
    label.pack(padx=20, pady=10)
    valuelabel = customtkinter.CTkLabel(settings, text=cycle_speed, fg_color="transparent", font=big) # a cool label for the current cycle speed
    valuelabel.pack(padx=20, pady=10)
    def slider_event(new_speed):
        global cycle_speed
        cycle_speed = int(new_speed)
        valuelabel.configure(text=cycle_speed)
    slider = customtkinter.CTkSlider(settings, from_=0, to=100, command=slider_event, width=500)
    slider.pack(padx=20, pady=10)
def run(bulb:BulbDevice):
    global running
    running = True
    while running:
        for hue in range(360):
            if not running:
                return
            r, g, b = colorsys.hsv_to_rgb(hue / 360, 1, 1) # gay little colors for our favorite gay little person <3
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            bulb.set_colour(r, g, b)
            time.sleep(cycle_speed/100)
def stop():
    global running
    running = False