import subprocess
import sys
import os
import json

# --- AUTO-INSTALLER & CONFIG LOGIC ---
def setup_environment():
    required = {'timezonefinder', 'pytz'}
    try:
        import timezonefinder
        import pytz
    except ImportError:
        print("Calibrating Scientific Libraries... Please wait.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
        print("Calibration complete. Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)

def load_or_create_config():
    config_file = "se_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print("--- SE Chronometer Initial Calibration ---")
        try:
            lat = float(input("Enter Latitude (e.g., 40.0192): "))
            lng = float(input("Enter Longitude (e.g., -82.8782): "))
            config = {"lat": lat, "lng": lng}
            with open(config_file, 'w') as f:
                json.dump(config, f)
            return config
        except ValueError:
            print("Invalid input. Using default (Gahanna, OH).")
            return {"lat": 40.0192, "lng": -82.8782}

setup_environment()
config = load_or_create_config()

import tkinter as tk
import math
import datetime
from datetime import timezone
import pytz
from timezonefinder import TimezoneFinder

USER_LAT = config["lat"]
USER_LNG = config["lng"]

tf = TimezoneFinder()
LOCAL_TZ_NAME = tf.timezone_at(lng=USER_LNG, lat=USER_LAT) or "UTC"
LOCAL_TZ = pytz.timezone(LOCAL_TZ_NAME)

def get_solar_data():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    day_of_year = now_utc.timetuple().tm_yday
    
    # Equation of Time (EoT) calculation
    B = (360 / 365) * (day_of_year - 81)
    B_rad = math.radians(B)
    eot = 9.87 * math.sin(2 * B_rad) - 7.53 * math.cos(B_rad) - 1.5 * math.sin(B_rad)
    
    # Solar Time Calculation
    offset_minutes = (USER_LNG * 4) + eot
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute + (now_utc.second / 60)
    solar_minutes = (total_minutes_utc + offset_minutes) % 1440
    
    return solar_minutes

def calculate_se_date(solar_minutes):
    now = datetime.datetime.now(LOCAL_TZ)
    se_start_year = 1543
    se_new_year_date = datetime.datetime(now.year, 5, 24, tzinfo=LOCAL_TZ)
    
    if now < se_new_year_date:
        current_se_year = now.year - se_start_year - 1
        reference_date = datetime.datetime(now.year - 1, 5, 24, tzinfo=LOCAL_TZ)
    else:
        current_se_year = now.year - se_start_year
        reference_date = se_new_year_date

    days_passed = (now - reference_date).days + 1
    
    # DAY FLIP AT SOLAR NOON (720 minutes)
    if solar_minutes < 720:
        display_day = days_passed - 1
    else:
        display_day = days_passed
        
    return current_se_year, display_day

def update_clock():
    solar_mins = get_solar_data()
    se_year, se_day = calculate_se_date(solar_mins)
    
    sh = int(solar_mins // 60)
    sm = int(solar_mins % 60)
    ss = int((solar_mins * 60) % 60)
    
    lbl_time.config(text=f"{sh:02d}:{sm:02d}:{ss:02d}")
    lbl_date.config(text=f"Year {se_year} SE | Day {se_day}")
    root.after(100, update_clock)

# --- GUI ---
root = tk.Tk()
root.title("SE Chronometer v1.3")
root.geometry("400x250")
root.configure(bg="#000000")

tk.Label(root, text="TRUE SOLAR TIME", bg="#000000", fg="#00ffcc", font=("Courier", 10)).pack(pady=(20,0))
lbl_time = tk.Label(root, text="", bg="#000000", fg="#00ffcc", font=("Courier", 45, "bold"))
lbl_time.pack()

lbl_date = tk.Label(root, text="", bg="#000000", fg="#ffffff", font=("Arial", 16, "bold"))
lbl_date.pack(pady=10)

tk.Label(root, text=f"LOCATION LOCKED: {USER_LAT}, {USER_LNG}", bg="#000000", fg="#333333", font=("Arial", 7)).pack(side="bottom", pady=10)

update_clock()
root.mainloop()
