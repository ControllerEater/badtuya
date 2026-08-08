# made by cupri, licensed under the polyform noncommercial license
import threading
import tinytuya
import time
import json
from tkinter import colorchooser
import customtkinter
import os
import importlib
import pystray
from PIL import Image, ImageDraw
from sys import argv
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# region configuration load/save logic

with open("config.json", "r") as file: # open the config, make it a dictionary
    config = json.load(file)
def consave(path, value):
    with open("config.json", "r") as file:
        config = json.load(file)

    keys = path.split(".")
    current = config

    for key in keys[:-1]:
        current = current[key]

    current[keys[-1]] = value

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

# endregion
# region light setup
device_id = config["device_id"]
ip = config["ip"]
local_key = config["local_key"]

print(device_id + " Added!")

bulb = tinytuya.BulbDevice(device_id,ip,local_key)
bulb.set_version(3.3)
# endregion
# region getting effects
effects = {"solid": None}

for filename in os.listdir("effects"):
    if not filename.endswith(".py") or filename == "__init__.py":
        continue

    effect_name = filename[:-3]
    module = importlib.import_module(f"effects.{effect_name}")
    effects[effect_name] = module
print(effects)
# endregion
# region pulling variables
status = bulb.status()
last_update = 0
effect = effects[config["effect"]]
# endregion
# region GUI
app = customtkinter.CTk()
app.geometry("600x300")
# region fonts
setfont = config["font"]
header = (setfont,50,"bold")
bold = (setfont,20,"bold")
normal = (setfont,20)
big = (setfont,35)
bigbold = (setfont,35,"bold")
# endregion
print(str(bulb.status()) + " = connected")
# region onoff button logic

def onoffswitch(argument =""):
    if argument == "":
        onoffswitch.onoff = not onoffswitch.onoff
        bulb.turn_onoff(onoffswitch.onoff)
        button.configure(text="Turn Off" if onoffswitch.onoff else "Turn On")
if not hasattr(onoffswitch, "onoff"):  # grab the bulb's power state and set it in the function, making powering on/off a LOT faster.
    try:
        onoffswitch.onoff = status["dps"]["20"]  # Some bulbs (like my cheap one) use dps 20
    except:
        try:
            onoffswitch.onoff = status["dps"]["1"]  # some other lights may use different dps, this tries 1.
        except:
            onoffswitch.onoff = False  # Doing it this way wont get the light's correct state, but will be synchronized after the first press.
# endregion
# region colorpicker logic
def pickcolors(argument =""):
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
    settings_height = 250

    pos_x = x + (width - settings_width) // 2
    pos_y = y + (height - settings_height) // 2
    settings.geometry(f"500x250+{pos_x}+{pos_y}")
    settings.transient(app)
    settings.grab_set()
    # somewhere someone is probably doing this same bullshit
    def temperature(): # used for setting white shades
        settings.destroy()
        temp = customtkinter.CTkToplevel(app)
        temp.title("Temperature")
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
        temp.geometry(f"500x200+{pos_x}+{pos_y}")
        temp.transient(app)
        temp.grab_set()
        consave("effect", "solid")
        label = customtkinter.CTkLabel(temp, text="Temperature", fg_color="transparent", font=header)
        label.pack(padx=20, pady=10)
        temperature = customtkinter.CTkLabel(temp, text="", fg_color="transparent", font=normal)
        temperature.pack(padx=20, pady=10)
        def slider_event(value):
            global bulb
            global last_update
            now = time.monotonic()
            if now - last_update >= 1:
                last_update = now
                bulb.set_colourtemp_percentage(value)
            if value >= 75:
                fuzzy = "very cold"
            elif value >= 50:
                fuzzy = "cold"
            elif value >= 25:
                fuzzy = "warm"
            else:
                fuzzy = "very warm"
            text = str(int(100-value)) + ", " + fuzzy
            temperature.configure(text=text)

        slider = customtkinter.CTkSlider(temp, from_=0, to=100, command=slider_event, width=500)
        slider.pack(padx=20, pady=10)

    def color(): # set a pretty and gay color
        settings.destroy()
        color = colorchooser.askcolor()
        if color:
            print(str(color[0]) + " Chosen!")
            consave("settings", "solid")
            global bulb
            bulb.set_colour(color[0][0], color[0][1], color[0][2])
    # pack and create the ui
    label = customtkinter.CTkLabel(settings, text="Colorpicker", fg_color="transparent", font=header)
    label.pack(padx=20, pady=10)
    button = customtkinter.CTkButton(settings, text="Color", command=color, font=normal, width=500, height=50)
    button.pack(padx=20, pady=10)
    button = customtkinter.CTkButton(settings, text="Temperature", command=temperature, font=normal, width=500, height=50)
    button.pack(padx=20, pady=10)
# endregion
def combobox_callback(choice): # effect switcher
    global effect
    if effect is not None: # handle none differently (for "solid" built-in effect)
        effect.stop()
        if choice == "solid": # solid needs to be handled different both when selected and when current effect
            effect = effects["solid"]
            print("solid chosen!")
        else:
            effect = effects[choice]
            print("combobox dropdown clicked:", choice)
            threading.Thread(target=effect.run,args=(bulb,),daemon=True).start()
            print("set effect to ", effect)
    else:
        print("combobox dropdown clicked:", choice)
        effect = effects[choice]
        threading.Thread(target=effect.run,args=(bulb,),daemon=True).start()
        print("set effect to ", effect)
def effectsettings():
    global app
    global setfont
    if effect is not None:
        effect.settings(app, setfont)
    else:
        pickcolors()
combobox_var = customtkinter.StringVar(value=config["effect"])


# region Packing ui elements
label = customtkinter.CTkLabel(app, text="Controlling: " + config["lightname"], fg_color="transparent", font=header)
label.pack(padx=20, pady=10)
button = customtkinter.CTkButton(app, text="Turn Off" if onoffswitch.onoff else "Turn On", command=onoffswitch, font=normal, width=500, height=50)
button.pack(padx=20, pady=10)
combobox = customtkinter.CTkComboBox(app, values=effects, command=combobox_callback, variable=combobox_var, font=normal, width=500, height=50)
combobox.pack(padx=20, pady=10)
settingsbutton = customtkinter.CTkButton(app, text="Effect Options", command=effectsettings, font=normal, width=500, height=50)
settingsbutton.pack(padx=20, pady=10)
# endregion
# region system tray
def create_tray_icon():
    # Create a simple tray icon
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Simple light bulb-ish icon
    draw.ellipse((12, 8, 52, 48), fill=(255, 220, 80, 255))
    draw.rectangle((24, 43, 40, 56), fill=(180, 180, 180, 255))
    draw.rectangle((26, 54, 38, 58), fill=(120, 120, 120, 255))
    return image
def show_window(icon=None, item=None):
    # Tkinter must be modified from the Tk thread
    app.after(0, app.deiconify)
def hide_window(icon=None, item=None):
    app.after(0, app.withdraw)
def quit_app(icon=None, item=None):
    def shutdown():
        global effect
        # Stop currently running effect
        if effect is not None:
            try:
                effect.stop()
            except Exception as e:
                print("Error stopping effect:", e)

        # Stop tray icon
        if icon is not None:
            icon.stop()
        # Destroy GUI
        app.destroy()
    app.after(0, shutdown)
def on_window_close():
    # X button hides the app instead of exiting
    app.withdraw()
tray_menu = pystray.Menu(
    pystray.MenuItem("Show", show_window),
    pystray.MenuItem("Quit", quit_app)
)
tray_icon = pystray.Icon(
    "CupriLight",
    create_tray_icon(),
    "Cupri Light",
    tray_menu
)
argument = argv[1] if len(argv) > 1 else None
if argument is not None:
    print("Using argument:", argument)
    if argument == "--hidden":
        print("hidden")
        on_window_close()
# Don't let closing the window terminate the program
app.protocol("WM_DELETE_WINDOW", on_window_close)
# Run pystray separately
tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
tray_thread.start()
# endregion
app.mainloop()
# endregion