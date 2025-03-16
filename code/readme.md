# PWM-Light Firmware

This repository contains **MicroPython** files for driving a PWM-based light (LED or MOSFET output) via Bluetooth Low Energy (BLE) on **ESP32-C3** microcontrollers. It demonstrates how to advertise and receive BLE messages to control the brightness level or simple on/off actions for connected LEDs.

## Repository Contents

1. **`ble_advertising.py`**  
   - A helper library that enables the ESP32-C3 to broadcast its presence via BLE. It handles the fundamental advertising payload necessary for BLE connections.
2. **`pwm-led-ESP32_C3_SuperMini.py`**  
   - A MicroPython script optimized for the **ESP32-C3 SuperMini** board.  
   - Assigns GPIO pins specific to this board and sets up BLE-based UART to receive commands (e.g., "ON", "OFF", or brightness values).
3. **`pwm-led-Seed-Studio-C3.py`**  
   - A nearly identical MicroPython script for the **Seed-Studio ESP32-C3** board.  
   - The main difference lies in the assigned GPIO pins for the RGB LEDs, MOSFET driver, and optional buzzer.

## How It Works

### BLE Peripheral Setup
Both `pwm-led-ESP32_C3_SuperMini.py` and `pwm-led-Seed-Studio-C3.py` create a **BLESimplePeripheral** instance, which:
- Advertises itself under the name `PWM-LED`.
- Exposes two UART-like characteristics (`RX` and `TX`) so a smartphone or computer can connect via BLE and exchange data.

The advertising functionality is implemented with the help of **`ble_advertising.py`**, which constructs the BLE packets announcing the device’s presence. Once a central device (such as a phone) connects:
- **Writes** to the `RX` characteristic are received by the script (`on_write` callback).
- **Notifications** for the `TX` characteristic can be used to send data back to the central device if needed.

### Command Parsing
Incoming data is decoded in `on_rx(value)`, where text commands are expected:
- `ON` turns on the MOSFET (or LED) at either full brightness or a previously set brightness level.
- `OFF` switches the MOSFET (or LED) fully off.
- Numeric values between **0** and **100** set the duty cycle, effectively controlling brightness (`0`% = off, `100`% = maximum).

### PWM Output & Pin Definitions
- A dedicated **PWM** object controls the MOSFET pin, allowing partial or full brightness adjustments.
- Additional **PWM** objects handle an **RGB LED** (three separate channels for red, green, and blue). These enable pulse/breathing effects while advertising or responding to connection status.
- **Buzzer** feedback:
  - A short ascending tone indicates a **new connection**.
  - A short descending tone indicates a **disconnection**.

### Differences in Board Scripts
The **ESP32-C3 SuperMini** and **Seed-Studio ESP32-C3** boards share similar functionality, but differ in **GPIO pin assignments**:
- `pwm-led-ESP32_C3_SuperMini.py` uses pin constants (`buzzer_gpio`, `mosfet_gpio`, etc.) suitable for the SuperMini layout.
- `pwm-led-Seed-Studio-C3.py` adjusts these pin values for the Seed-Studio layout.

## Getting Started

1. **Set Up MicroPython**:  
   - Flash a MicroPython firmware compatible with your ESP32-C3 board.

2. **Upload Files**:  
   - Use a tool such as **Thonny**, **uPyCraft**, or the **ampy** CLI to upload:
     - `ble_advertising.py`
     - The relevant PWM script for your board:
       - `pwm-led-ESP32_C3_SuperMini.py` **or**  
       - `pwm-led-Seed-Studio-C3.py`
   - Make sure both files reside in the device’s root filesystem.  
   - You may rename the chosen script to `main.py` so it runs on startup, or manually call it from the REPL.

3. **Power the Board**:  
   - Provide a suitable 5V supply (or 3.3V if your board includes a regulator).  
   - Ensure any connected LED strip, MOSFET, or RGB LED is wired properly.

4. **Connect via BLE**:
   - On your smartphone, open a BLE UART app or a custom app.  
   - Find and connect to the device named `PWM-LED`.  
   - Once connected, send commands like `ON`, `OFF`, or a number from `0` to `100`.

5. **Test and Modify**:
   - Observe LED brightness changes and buzzer feedback on connection/disconnection.  
   - Adjust code in the script for custom effects or different pin mappings.

## Example Commands

- **`ON`**: Turn on the LED/MOSFET at the last known brightness level or full.  
- **`OFF`**: Switch off the LED/MOSFET entirely.  
- **`50`**: Set the LED brightness to 50% (half duty cycle).  

## License
- Under **GPL-3.0** license.

## Further Customizations
- **RGB Effects**: Modify `pulse()` or `blink()` methods in the `RGBleds` class for unique lighting animations.  
- **Buzzer Sounds**: Customize the tones in `sound_connect()` or `sound_disconnect()` for unique connection alerts.  
- **Pin Mapping**: Change the pin constants at the top of each script if you use different GPIO lines or want to port the code to another board.

---  

Enjoy controlling your PWM-based lighting system via BLE! Contributions and suggestions are always welcome.
