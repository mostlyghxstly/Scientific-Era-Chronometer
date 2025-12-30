import subprocess
import sys
import os

# --- AUTO-INSTALLER LOGIC ---
def install_dependencies():
    required = {'timezonefinder', 'pytz'}
    try:
        import timezonefinder
        import pytz
    except ImportError:
        print("Calibrating Scientific Libraries... Please wait.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
        print("Calibration complete. Launching Chronometer...")
        os.execl(sys.executable, sys.executable, *sys.argv)

install_dependencies()

import tkinter as tk
import math
import datetime
from datetime import timezone
import pytz
from timezonefinder import TimezoneFinder

# --- INITIAL SETUP: USER INPUT ---
print("--- SE Chronometer Calibration ---")
try:
    USER_LAT = float(input("Enter Latitude (e.g., 40.0192): "))
    USER_LNG = float(input("Enter Longitude (e.g., -82.8782): "))
except ValueError:
    print("Invalid input. Defaulting to Gahanna, OH.")
    USER_LAT, USER_LNG = 40.0192, -82.8782

tf = TimezoneFinder()
LOCAL_TZ_NAME = tf.timezone_at(lng=USER_LNG, lat=USER_LAT) or "UTC"
LOCAL_TZ = pytz.timezone(LOCAL_TZ_NAME)

def get_solar_data():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    day_of_year = now_utc.timetuple().tm_yday
    
    # Equation of Time (EoT) - Correction for Earth's axial tilt/orbit
    B = (360 / 365) * (day_of_year - 81)
    B_rad = math.radians(B)
    eot = 9.87 * math.sin(2 * B_rad) - 7.53 * math.cos(B_rad) - 1.5 * math.sin(B_rad)
    
    # Solar Time calculation based on Longitude
    offset_minutes = (USER_LNG * 4) + eot
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute + (now_utc.second / 60)
    solar_minutes = (total_minutes_utc + offset_minutes) % 1440
    
    return solar_minutes

def calculate_se_date(solar_minutes):
    """
    Year 0 SE = 1543. 
    New Day officially begins at Solar Noon (720 minutes).
    """
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
    
    # SOLAR NOON FLIP: If before 12:00 PM True Solar Time, stay on previous day count.
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
root.title("SE Chronometer v1.2")
root.geometry("400x250")
root.configure(bg="#050505")

tk.Label(root, text="TRUE SOLAR TIME", bg="#050505", fg="#00ffcc", font=("Courier", 10)).pack(pady=(20,0))
lbl_time = tk.Label(root, text="", bg="#050505", fg="#00ffcc", font=("Courier", 45, "bold"))
lbl_time.pack()

lbl_date = tk.Label(root, text="", bg="#050505", fg="#ffffff", font=("Arial", 16, "bold"))
lbl_date.pack(pady=10)

tk.Label(root, text=f"SOLAR DAY START: NOON", bg="#050505", fg="#444444", font=("Arial", 8)).pack(side="bottom", pady=10)

update_clock()
root.mainloop()
