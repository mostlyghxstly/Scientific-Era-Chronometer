![SE Chronometer Logo](seclockgemini.png)
SE Chronometer: The Scientific Era
The SE Chronometer is a high-precision timekeeping instrument that rejects arbitrary civil time in favor of planetary reality. It anchors the observer to the Scientific Era (SE), which began in 1543 with the publication of De revolutionibus orbium coelestium by Nicolaus Copernicus.

Core Principles
Year Zero (1543): Time is measured from the moment humanity realized the Earth orbits the Sun.

The Noon Epoch: Unlike the Gregorian calendar, which flips days at the arbitrary hour of midnight, the SE Chronometer increments the day at Solar Noon—the exact moment the Sun reaches its highest point in your specific sky.

True Solar Time: Uses the Equation of Time to calculate time based on Earth's elliptical orbit and axial tilt.

Key Features (v1.3.4)
Solar Zenith Tracking: Decouples from "Mean Time" and tracks the physical rotation of the planet relative to your exact Longitude.

Lunar Illumination: Live tracking of the lunar phase based on the synodic month cycle.

Self-Bootstrapping: Automatically installs required scientific libraries (pytz, timezonefinder) on the first run.

Persistent Calibration: Remembers your coordinates so you only have to calibrate once.



Installation & Setup
Step 1: First-Time Calibration
Download se_clock.py.
Open your Terminal or Command Prompt.
Navigate to the folder and run:
python se_clock.py

Enter your Latitude and Longitude when prompted. (You can find these by right-clicking your location in Google Maps).

Step 2: Daily Use
Once calibrated, you no longer need the terminal.
Double-click the se_clock.py file to launch the clock instantly.

Pro-Tip: Rename the file to se_clock.pyw to hide the background terminal window for a cleaner "app" experience.Managing Configuration

Resetting your Location - 
The app saves your coordinates in a file called se_config.json located in the same folder as the script.
If you move to a new city or want to change your coordinates: Simply delete se_config.json.
The next time you launch the app, it will enter "Calibration Mode" and ask for your Latitude and Longitude again.

Technical Requirements
Python 3.x

The script will automatically attempt to install pytz and timezonefinder via pip if they are missing.
