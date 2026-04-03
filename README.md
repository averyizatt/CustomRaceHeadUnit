# Custom Race Head Unit

A custom-built automotive head unit based on a Raspberry Pi, designed for use in a race or performance vehicle. The system provides media playback, a digital dashboard, and vehicle integration — originally powered by [OpenAuto Pro](https://bluewavestudio.io/shop/openauto-pro-car-head-unit-solution/), which has since been discontinued.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware](#hardware)
- [Software & Dependencies](#software--dependencies)
- [Project Structure](#project-structure)
- [Scripts](#scripts)
- [OpenAuto Pro](#openauto-pro)
- [Setup & Usage](#setup--usage)
- [License Keys](#license-keys)
- [Notes](#notes)

---

## Overview

This project documents the build, configuration, and supporting scripts for a custom Raspberry Pi head unit installed in a race vehicle. The unit replaces a factory head unit and provides:

- Music playback via Android Auto (OpenAuto Pro)
- A configurable digital dashboard with vehicle data (OBD-II / CAN bus integration)
- Automatic power management tied to the vehicle's ACC (accessory) circuit
- CarPlay support via the AutoBox plugin

OpenAuto Pro, the primary software platform this build was based on, has been officially shut down by its developer. This repository preserves the configuration, scripts, and integration notes used in the working build.

---

## Features

- **Music & Media Playback** — Full Android Auto and CarPlay support through OpenAuto Pro and the AutoBox plugin.
- **Digital Dashboard** — Configurable gauge overlays and vehicle telemetry display.
- **ACC Power Management** — GPIO-based monitoring of the vehicle's ACC line; the Pi automatically powers down after a configurable delay when the ignition is turned off.
- **Relay Control** — Relay output keeps the Pi powered during the shutdown grace period, then cuts power cleanly.
- **Race-Focused Design** — Built to run in a performance vehicle environment with boot-to-app reliability.

---

## Hardware

| Component | Details |
|---|---|
| Single-board Computer | Raspberry Pi 4 (or Pi 3B+) |
| Display | Touchscreen display (HDMI or DSI) |
| Power Management | Relay module wired to ACC circuit |
| GPIO Wiring | ACC signal on GPIO 23 (BCM); relay control on GPIO 24 (BCM) |
| OBD / CAN Interface | USB or UART OBD-II adapter (vehicle dependent) |

> **Wiring note:** The ACC pin is pulled LOW when the ignition/accessory is active (active-low logic via relay pin 30). Adjust `ACC_PIN` logic in `CarPowerMonitor.py` if your relay is wired differently.

---

## Software & Dependencies

- **OS:** Raspberry Pi OS (Bullseye or Buster, 32-bit recommended for OpenAuto Pro compatibility)
- **OpenAuto Pro 16.1** — Automotive head unit software (discontinued; see [OpenAuto Pro](#openauto-pro))
- **AutoBox Plugin** — Adds Apple CarPlay support to OpenAuto Pro
- **Python 3** with `RPi.GPIO` library
- **`sudo` / systemd** — Required for GPIO access and shutdown commands

Install Python dependency:

```bash
pip3 install RPi.GPIO
```

---

## Project Structure

```
CustomRaceHeadUnit/
├── OpenAutoPro/
│   ├── key.txt                  # License keys for OpenAuto Pro and AutoBox
│   └── openauto_userguide.pdf   # Official OpenAuto Pro user guide
├── Scripts/
│   └── CarPowerMonitor.py       # ACC power monitoring and auto-shutdown daemon
└── README.md
```

---

## Scripts

### `Scripts/CarPowerMonitor.py`

A Python daemon that runs at boot and monitors the vehicle's ACC (accessory) circuit via a GPIO input pin. When the ignition is turned off, it starts a countdown timer and then gracefully shuts down the Raspberry Pi and cuts relay power.

**Key configuration constants:**

| Constant | Default | Description |
|---|---|---|
| `ACC_PIN` | `23` | BCM GPIO pin connected to the ACC relay signal |
| `RELAY_PIN` | `24` | BCM GPIO pin controlling the power relay output |
| `SHUTDOWN_DELAY` | `60` | Seconds to wait after ACC-off before initiating shutdown |

**To run manually:**

```bash
sudo python3 Scripts/CarPowerMonitor.py
```

**To run at boot (recommended):** Create a systemd service unit:

```ini
# /etc/systemd/system/carpowermonitor.service
[Unit]
Description=Car Power Monitor
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/CustomRaceHeadUnit/Scripts/CarPowerMonitor.py
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl enable carpowermonitor
sudo systemctl start carpowermonitor
```

---

## OpenAuto Pro

[OpenAuto Pro](https://bluewavestudio.io/shop/openauto-pro-car-head-unit-solution/) was a commercial Raspberry Pi automotive head unit solution by Bluewave Studio. It provided a polished Android Auto interface, CarPlay support (via the AutoBox plugin), dashboard overlays, and deep hardware integration.

**OpenAuto Pro has been discontinued.** The developer shut down the service and license servers. This repository preserves the user guide and license keys used in this specific build for archival and reference purposes.

The `OpenAutoPro/openauto_userguide.pdf` contains full setup, configuration, and wiring documentation from the original software.

---

## Setup & Usage

1. Flash Raspberry Pi OS to a microSD card.
2. Install OpenAuto Pro per the user guide (`OpenAutoPro/openauto_userguide.pdf`).
3. Apply your license keys from `OpenAutoPro/key.txt` in the OpenAuto Pro settings.
4. Wire the ACC relay signal and power relay to the GPIO pins defined in `CarPowerMonitor.py`.
5. Install the `carpowermonitor` systemd service (see [Scripts](#scripts) above).
6. Configure display, audio output, and OBD adapter in OpenAuto Pro settings.
7. Boot the Pi in the vehicle — OpenAuto Pro will launch automatically on startup.

---

## License Keys

The `OpenAutoPro/key.txt` file contains the activation keys for:
- **OpenAuto Pro 16.1**
- **AutoBox Plugin (CarPlay)**

These are single-device licenses tied to the original build. Since OpenAuto Pro servers are offline, these keys are preserved here for reference only.

---

## Notes

- OpenAuto Pro is no longer available for purchase or activation on new devices. This build was set up before the shutdown.
- Community alternatives being explored for future versions include [OpenAuto CE](https://github.com/openautomotive/openautomotive-ce) and other open-source Android Auto / CarPlay implementations.
- Always test ACC wiring and shutdown behavior with the vehicle stationary before driving.
