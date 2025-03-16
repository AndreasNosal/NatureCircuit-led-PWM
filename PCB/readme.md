# PWM-Light PCB

This repository contains the PCB design files and documentation for a **PWM-based light control module**. By using a dedicated PCB, you can drive LEDs or other lighting elements with precise brightness control via PWM (Pulse Width Modulation). The board is ideal for DIY projects, educational use, or as a foundation for more advanced smart-lighting solutions.
![image](https://github.com/user-attachments/assets/160079a2-fc02-40bf-a2c5-ecb0fede713f)
![image](https://github.com/user-attachments/assets/62ab89a3-0c3a-4d01-ba89-8288dd012df8)


## Overview
- **KiCad Design**: The PCB is designed in KiCad (including schematic and layout).  
- **PWM Output**: Provides efficient dimming capability for LED arrays or single LEDs with minimal flicker.  
- **ESP32 or Other Microcontrollers**: Compatible with 3.3V logic devices (e.g., ESP32, STM32, Arduino Pro Mini at 3.3V, etc.) for easy integration into IoT or custom home-automation setups.  
- **Power Handling**: Designed to be supplied from a stable 5V source (or other voltages, depending on your chosen components and regulator configuration).  
- **JLCPCB Manufacturing**: Gerber files are ready to upload to PCB manufacturers (e.g., JLCPCB).  

## Features
- **Compact Layout**: Minimal footprint for easy integration into small enclosures.  
- **Adjustable Voltage Regulation**: Option to include a regulator if powering from higher than 5V.  
- **Through-Hole & SMD Mix**: Balanced design for straightforward soldering—newcomers can assemble basic sections while advanced users can integrate SMD parts for improved performance.  
- **Expansion Headers**: Multiple I/O pins (PWM, I2C, SPI, etc.) broken out for adding sensors or additional modules.

## Getting Started

1. **Download or Clone the Repository**  
   - Access the KiCad project files and Gerber exports from this repository.

2. **Customize the Design (Optional)**  
   - If you want different connectors, pinouts, or layout modifications, edit the schematic and PCB layout in KiCad.  
   - Generate new Gerber files if you make changes.

3. **Order the PCB**  
   - Upload the provided Gerber files to a PCB manufacturer such as JLCPCB.  
   - Choose your PCB specifications (layer count, color, thickness, etc.).  
   - Wait for the boards to be manufactured and shipped.

![image](https://github.com/user-attachments/assets/dac68052-e6fd-4025-9e39-791e608f60b6)


4. **Assemble the Components**  
   - Refer to the schematic/BoM (Bill of Materials) for correct part placement.  
   - Solder the components using standard soldering techniques.  
     - For SMD parts, you may use solder paste and a reflow method (hot plate, reflow oven, or hot air gun).  
     - For through-hole parts, use a temperature of around 320–350 °C and ensure solid, shiny joints.

5. **Program & Connect**  
   - If using an ESP32 or similar microcontroller, attach it to the board’s headers or pads.  
   - Upload your firmware (e.g., Arduino, MicroPython) to control PWM signals and logic.  
   - Power the board with a stable 5V supply (or according to your regulator setup).

6. **Test & Calibrate**  
   - Connect an LED array or single LED to the PWM output pins.  
   - Vary the duty cycle in your code to confirm proper dimming functionality.  
   - Check power consumption, heat dissipation, and general performance.

## Usage Scenarios
- **Smart Lighting**: Combine with a Bluetooth or Wi-Fi module for mobile app control.  
- **DIY Projects**: Enhance desk lamps, ambient room lighting, or artistic LED installations.  
- **Educational**: Demonstrate PWM principles and advanced lighting control in classroom or workshop settings.

## License
- Licensed under the **GPL-3.0** License.
> *Feel free to share improvements or fork this project to fit your specific needs. Contributions are welcome!*
