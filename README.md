# Mobile-Controlled Light

This project showcases a light fixture that can be controlled remotely via a smartphone (using ESP32 and BLE/Wi-Fi). The device is designed for flexible operation and easy assembly, making it suitable for a wide range of DIY enthusiasts or educational projects. By incorporating a custom PCB, an LED panel, and 3D-printed parts, you can create a smart lighting system that connects seamlessly to your mobile phone.

Originally designed to help users learn about PCB assembly, soldering techniques, and microcontroller programming, this project emphasizes a hands-on approach. Whether you order your PCBs from JLCPCB and print your own stencil for the LED panel or simply 3D-print the housing at home, you’ll gain valuable experience in hardware assembly and coding for an IoT-focused device.

## Features
- **ESP32-Based Controller**: Uses two main files (`main.py` and `ble_advertising.py`) to establish a reliable Bluetooth connection for receiving commands from your smartphone.
- **LED Panel**: Powered by an optional custom PCB or a standard LED strip; easily replaceable or upgradable.
- **3D-Printable Enclosure**: Designed for FDM printing with minimal supports. Can also be adapted to various 3D printers.
- **Scalable Assembly**: Choose between ordering a stencil for solder paste application or printing your own with a standard 3D printer.
- **Easy Soldering**: Ideal for beginners; the main PCB has through-hole or straightforward SMD components, and the layout is beginner-friendly.
- **Flexible Power Input**: Operates on typical USB power or a regulated supply (e.g., 5V).  

## Getting Started
1. **Gather Materials**: Order or produce the main PCB (recommended via JLCPCB) and LED panel. If you own a 3D printer, you can create the stencil for solder paste application.  
2. **Print Enclosure**: Use your preferred 3D printer and slicer settings (e.g., minimal supports). PLA or PETG are commonly used filaments.  
3. **Solder Components**: Prepare your soldering iron (typically 320–350 °C). Follow the silkscreen labels on the PCB and reference any documentation or schematics for correct polarity and placement.  
4. **Program the ESP32**:  
   - Upload `main.py` and `ble_advertising.py` to the ESP32 board.  
   - `main.py` runs automatically on reboot.  
   - `ble_advertising.py` enables BLE connectivity so the device can receive commands.  
5. **Assemble & Power Up**: Once everything is in place, provide power (5V recommended), and check the device’s functionality by connecting with your mobile phone.

## Usage
- **Mobile App Connection**: Use a compatible app (or custom-developed one) to scan and connect via BLE.  
- **Light Control**: Toggle the light on/off or adjust brightness (if supported).  
- **Firmware Updates**: Modify `main.py` for custom behavior, color transitions, scheduling, or advanced IoT integration.

## License
- Under **GPL-3.0** license.

## Example in Action
![led-box-preview-video](https://github.com/user-attachments/assets/914f537c-5393-4c83-a25a-f0fdf2354518)
