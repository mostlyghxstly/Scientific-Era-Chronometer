# ![SE Chronometer Logo](seclockgemini.png)
# SE Chronometer: The Scientific Era

The **SE Chronometer** is a high-precision timekeeping instrument that rejects arbitrary civil time in favor of planetary reality. It anchors the observer to the **Scientific Era (SE)**, which began in **1543** with the publication of *De revolutionibus orbium coelestium* by Nicolaus Copernicus.

---

## 🌌 Core Principles

* **Year Zero (1543):** Time is measured from the moment humanity realized the Earth orbits the Sun.
* **The Noon Epoch:** Unlike the Gregorian calendar, which flips days at the arbitrary hour of midnight, the SE Chronometer increments the day at **Solar Noon**—the exact moment the Sun reaches its highest point in your specific sky.
* **True Solar Time:** Uses the **Equation of Time** to calculate time based on Earth's elliptical orbit and axial tilt.



---

## ✨ Key Features (v1.3.4)

* **Solar Zenith Tracking:** Decouples from "Mean Time" and tracks the physical rotation of the planet relative to your exact Longitude.
* **Lunar Illumination:** Live tracking of the lunar phase based on the synodic month cycle ($29.53$ days).
* **Self-Bootstrapping:** Automatically installs required scientific libraries (`pytz`, `timezonefinder`) on the first run.
* **Persistent Calibration:** Remembers your coordinates so you only have to calibrate once.
* **Always-on-Top:** Built-in `-topmost` logic to keep your chronometer pinned to your workspace.

---

## 🚀 Getting Started

| Phase | What Happens | Action Required |
| :--- | :--- | :--- |
| **First Launch** | **Calibration Mode:** Script installs dependencies and asks for location. | Run `python se_clock.py` in terminal and enter Lat/Lon. |
| **Second Launch** | **Instant Deployment:** Script reads `se_config.json`. | Just **double-click** `se_clock.py`. |

> [!TIP]
> **Pro-Tip:** Rename the file to `se_clock.pyw` to hide the background terminal window for a cleaner "app" experience.

---

## 🔄 Managing Configuration

### **Resetting your Location**
The app saves your coordinates in a file called `se_config.json` in the same folder as the script.
If you move or want to re-calibrate:
1.  **Delete `se_config.json`**.
2.  The next time you launch the app, it will re-enter **Calibration Mode**.

---

## 🛠 Technical Deep-Dive

### **The Evolution: What's new in v1.3.4?**
While v1.3.0 introduced the concept, **v1.3.4** perfects the execution:
* **Solar Noon Day-Flip:** Officially decoupled from midnight. The day count increments at **12:00:00 True Solar Time**.
* **Permission Hardening:** Fixed a Windows bug where the app crashed on double-click. It now uses **Absolute Pathing** to ensure settings are saved safely regardless of launch method.
* **Lunar Phase Integration:** High-precision tracking relative to the J2000 epoch.

### **Requirements**
* **Python 3.x**
* Libraries: `pytz`, `timezonefinder` (Auto-installed on first run).

---

## ⚖️ License
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.
