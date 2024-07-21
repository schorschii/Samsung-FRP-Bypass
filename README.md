# Samsung FRP Bypass

Unlock the Google Account Factory Reset Protection on Samsung devices.

Adjusted for new Samsung firmware update - also working with 2022-2024 software. No need to run suspicious closed-source Windows tools!

## How to use

- Make sure you have all the dependencies listed in `requirements.txt` installed
  - Install via `apt install python3-usb python3-serial` or via pip `pip install -r requirements.txt`

- Tap on emergency call button and dial `*#0*#` to open factory tests page.
- Plug the samsung over USB and run `sudo python main.py`
  - Or only run a specific tool: `python3 at_utils.py`, `python3 usbswitcher.py`
