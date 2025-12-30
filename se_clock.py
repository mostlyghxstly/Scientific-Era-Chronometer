import subprocess
import sys
import os
import json

# --- BOOTSTRAP ---
def setup_environment():
    try:
        import timezonefinder
        import pytz
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "timezonefinder", "pytz"])
        os.execl(sys.executable, sys.executable, *sys.argv)

def load_or_create_config():
    # FIXED: This finds the actual folder where your script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "se_config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    
    print("\n--- SE Chronometer Calibration ---")
    try:
        lat = float(input("Enter Latitude: "))
        lng = float(input("Enter Longitude: "))
        config = {"lat": lat, "lng": lng}
        # Save to the absolute path to avoid permission issues
        with open(config_file, 'w') as f:
            json.dump(config, f)
        return config
    except Exception as e:
        print(f"CRITICAL ERROR: Could not save config to {config_file}")
        print(f"Error detail: {e}")
        input("Press Enter to exit...")
        sys.exit()

setup_environment()
config = load_or_create_config()

import tkinter as tk
import math
import datetime
import pytz
from timezonefinder import TimezoneFinder

# --- CLOCK ENGINE ---
USER_LAT, USER_LNG = config["lat"], config["lng"]
tf = TimezoneFinder()
LOCAL_TZ = pytz.timezone(tf.timezone_at(lng=USER_LNG, lat=USER_LAT) or "UTC")

def get_data():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    day_of_year = now_utc.timetuple().tm_yday
    B = math.radians((360 / 365) * (day_of_year - 81))
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    solar_mins = ((now_utc.hour * 60) + now_utc.minute + (now_utc.second / 60) + (USER_LNG * 4) + eot) % 1440
    ref_moon = datetime.datetime(2000, 1, 6, 18, 14, 0, tzinfo=datetime.timezone.utc)
    age = ((now_utc - ref_moon).total_seconds() / 86400) % 29.53058867
    illum = 0.5 * (1 - math.cos((age / 29.53058867) * 2 * math.pi))
    return solar_mins, f"LUNAR ILLUMINATION: {int(illum * 100)}%"

def update_display():
    sm, moon_str = get_data()
    now = datetime.datetime.now(LOCAL_TZ)
    is_post_may24 = now >= datetime.datetime(now.year, 5, 24, tzinfo=LOCAL_TZ)
    se_year = now.year - 1543 if is_post_may24 else now.year - 1544
    ref_date = datetime.datetime(now.year if is_post_may24 else now.year - 1, 5, 24, tzinfo=LOCAL_TZ)
    days_diff = (now - ref_date).days + 1
    se_day = days_diff if sm >= 720 else days_diff - 1
    lbl_time.config(text=f"{int(sm//60):02d}:{int(sm%60):02d}:{int((sm*60)%60):02d}")
    lbl_date.config(text=f"Year {se_year} SE | Day {se_day}")
    lbl_moon.config(text=moon_str)
    root.after(200, update_display)

# --- GUI ---
root = tk.Tk()
root.title("SE Chronometer")
root.geometry("400x280")
root.configure(bg="#000000")
root.attributes('-topmost', True)

tk.Label(root, text="TRUE SOLAR TIME", bg="#000000", fg="#00ffcc", font=("Courier", 10)).pack(pady=(20,0))
lbl_time = tk.Label(root, text="00:00:00", bg="#000000", fg="#00ffcc", font=("Courier", 45, "bold"))
lbl_time.pack()
lbl_date = tk.Label(root, text="...", bg="#000000", fg="#ffffff", font=("Arial", 16, "bold"))
lbl_date.pack(pady=10)
lbl_moon = tk.Label(root, text="", bg="#000000", fg="#888888", font=("Arial", 10, "italic"))
lbl_moon.pack()

update_display()
root.mainloop()
