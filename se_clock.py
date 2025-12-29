import tkinter as tk
import math
import datetime
from datetime import timezone

# --- CONFIGURATION: SET YOUR LOCATION (Default: Gahanna, Ohio) ---
LATITUDE = 40.0192
LONGITUDE = -82.8782

def calculate_se_date():
    """
    Calculates the Scientific Era date.
    Year 0 SE starts on May 24, 1543 (Publication of De Revolutionibus).
    New Year's Day is May 24th.
    """
    now = datetime.datetime.now()
    
    # Check if we have passed the "Scientific New Year" (May 24)
    se_start_year = 1543
    se_new_year_date = datetime.datetime(now.year, 5, 24)
    
    if now >= se_new_year_date:
        current_se_year = now.year - se_start_year
        # Day of the SE year
        day_of_se_year = (now - se_new_year_date).days + 1
    else:
        current_se_year = now.year - se_start_year - 1
        # Days since LAST May 24th
        last_year_se_date = datetime.datetime(now.year - 1, 5, 24)
        day_of_se_year = (now - last_year_se_date).days + 1
        
    return current_se_year, day_of_se_year

def calculate_true_solar_time():
    """
    Calculates 'Apparent Solar Time' (True Time).
    12:00 PM is exactly when the sun is highest in the sky (Solar Noon).
    """
    now_utc = datetime.datetime.now(timezone.utc)
    
    # 1. Day of the Year (1-365)
    day_of_year = now_utc.timetuple().tm_yday
    
    # 2. Equation of Time (EoT) - Correction for Earth's elliptical orbit
    # Approximation formula (result in minutes)
    B = (360 / 365) * (day_of_year - 81)
    B_rad = math.radians(B)
    eot = 9.87 * math.sin(2 * B_rad) - 7.53 * math.cos(B_rad) - 1.5 * math.sin(B_rad)
    
    # 3. Solar Time Calculation
    # Solar Time = UTC + (Longitude * 4 minutes) + EoT
    offset_minutes = (LONGITUDE * 4) + eot
    
    total_minutes_utc = (now_utc.hour * 60) + now_utc.minute + (now_utc.second / 60)
    solar_minutes = total_minutes_utc + offset_minutes
    
    # Normalize to 24h format
    if solar_minutes < 0:
        solar_minutes += 1440
    if solar_minutes >= 1440:
        solar_minutes -= 1440
        
    solar_hour = int(solar_minutes // 60)
    solar_minute = int(solar_minutes % 60)
    solar_second = int((solar_minutes * 60) % 60)
    
    return f"{solar_hour:02d}:{solar_minute:02d}:{solar_second:02d}"

def get_moon_phase():
    """
    Calculates rough moon phase percentage and description.
    """
    # Known new moon reference: Jan 6, 2000
    ref_date = datetime.datetime(2000, 1, 6, 18, 14, 0)
    now = datetime.datetime.now()
    diff = now - ref_date
    days = diff.total_seconds() / 86400
    
    # Synodic month (new moon to new moon)
    lunar_cycle = 29.53058867
    current_cycle_pos = days % lunar_cycle
    
    # Calculate percentage (0% = New, 50% = Full, 100% = New)
    # Actually, we want illumination %
    phase_progress = current_cycle_pos / lunar_cycle
    illumination = 0.5 * (1 - math.cos(phase_progress * 2 * math.pi))
    
    # Determine Label
    age = current_cycle_pos
    if age < 1: phase_name = "New Moon"
    elif age < 7: phase_name = "Waxing Crescent"
    elif age < 8: phase_name = "First Quarter"
    elif age < 14: phase_name = "Waxing Gibbous"
    elif age < 16: phase_name = "Full Moon"
    elif age < 22: phase_name = "Waning Gibbous"
    elif age < 23: phase_name = "Last Quarter"
    elif age < 29: phase_name = "Waning Crescent"
    else: phase_name = "New Moon"
    
    return f"{phase_name} ({int(illumination * 100)}%)"

def update_clock():
    # Get Data
    se_year, se_day = calculate_se_date()
    solar_time = calculate_true_solar_time()
    moon_info = get_moon_phase()
    
    # Update Labels
    lbl_time.config(text=solar_time)
    lbl_date.config(text=f"Year {se_year} SE | Day {se_day}")
    lbl_moon.config(text=f"Moon: {moon_info}")
    
    # Update every 100ms (to keep seconds ticking smoothly)
    root.after(100, update_clock)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Scientific Era Clock")
root.geometry("400x250")
root.configure(bg="#1e1e1e") # Dark mode background

# Fonts
font_time = ("Courier New", 40, "bold")
font_date = ("Helvetica", 16)
font_moon = ("Helvetica", 12, "italic")

# Labels
tk.Label(root, text="TRUE SOLAR TIME", bg="#1e1e1e", fg="#888888", font=("Arial", 10)).pack(pady=(20, 0))
lbl_time = tk.Label(root, text="00:00:00", bg="#1e1e1e", fg="#00ff00", font=font_time)
lbl_time.pack(pady=5)

lbl_date = tk.Label(root, text="Year --- SE", bg="#1e1e1e", fg="#ffffff", font=font_date)
lbl_date.pack(pady=5)

lbl_moon = tk.Label(root, text="Moon Phase", bg="#1e1e1e", fg="#bbbbbb", font=font_moon)
lbl_moon.pack(pady=10)

tk.Label(root, text="Time anchored to Gahanna, OH", bg="#1e1e1e", fg="#444444", font=("Arial", 8)).pack(side="bottom", pady=10)

update_clock()
root.mainloop()