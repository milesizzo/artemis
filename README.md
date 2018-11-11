# Artemis
This repository contains Artemis SBS configuration files for each
station, as well as other miscellaneous configurations (eg. joystick,
registry).

# Installing
If installing a fresh PC, first install Artemis (eg. `Artemis_full_installer_2_0.exe`). Set the game location to `c:\games\artemis`.
Then install any upgrades needed (as of 2018, Artemis was at version 2.7.1).

Also install Python 2.7 and Git so you can clone this repository.

# Set up station
To set up a console to act as a particular station, use the `deploy.py` script. It allows you to deploy the Artemis configs for each station, as well as set up audio volumes (eg. music) and other registry settings.

For the most basic usage:
```
python deploy.py --station helm
```
This assumes the Artemis location is `c:\games\artemis`. If you specify `--help` you can see all the possible options.

# DMX
I couldn't get this working last time we played. Will need to look into it.

# PCs (specific to my setup)
These were the best PC setups last time we played:
* Dell Latitude laptop (weapons) + LG monitor (VGA only)
* Alienware laptop (engineering) + Dell touchscreen
* Main gaming desktop (helm) + old Dell HD monitor
* PIPO (science) + small Samsung monitor (DVI to HDMI)
* Lenovo Yoga laptop (comms) flipped to use the touchscreen
* Old gaming desktop (server) + SPDIF + DVI to HDMI (projector)

The stick PC barely worked; the PIPOs were much better.
