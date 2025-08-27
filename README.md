# Computer Usage Monitor (WS2812 LED matrix 8x8)

A **WS2812 LED matrix** 8x8 project that displays your computer’s current usage in real time.  
Controlled by an **RP2040**, which receives data from a **Python script** running on your PC.

---

## Features

- **Two display modes:**
  1. **Hexadecimal percentage display** – usage shown as a hex value.
  2. **Percentage bar display** – each LED represents **12.5%** usage.

- **Displayed system metrics:**
  - CPU usage
  - RAM usage
  - GPU usage
  - GPU VRAM usage

---

## Finished Prototype

---

<p align="center">
  <img src="images/display_hex.jpg" width="250">
  <img src="images/display_prozent.jpg" width="250">
</p>

The **left display** shows system status (CPU usage, RAM, GPU, and GPU VRAM) in **hexadecimal format**.  
The **right display** shows the same data in **percentage format**, where each LED represents **12.5%** usage.  

The display mode can be switched using a **dedicated push button**.

---

## Limitations

- The Python script **only works** with **NVIDIA GPUs** (requires NVIDIA-SMI).
- PC communicates with the RP2040 or other µC via **serial connection**.

---

---

## Finished project:
A case for the LED matrix was created using a 3D printer. Afterwards, this case was attached to the side of the monitor.

<p align="center">
  <img src="images/display_with_case.jpg" width="250">
</p>

---






