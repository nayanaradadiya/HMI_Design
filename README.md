# Textile Weaving Machine GUI Controller

A **Python (Tkinter)**-based graphical user interface designed for textile weaving machines.  
This application runs on a **Raspberry Pi** and communicates with an Textile controller (e.g., STM32 or LPC2148) using serial (UART) communication to send and receive real-time machine data.

---

## Features
- Real-time monitoring of weaving machine parameters (speed, pattern status, sensor position, current pick, Data setting, file selection, Store weaving pattern, etc..)
- Two-way serial communication between the Raspberry Pi and the controller for command and data exchange
- Auto-refresh of GUI values to reflect live machine updates
- Touchscreen-friendly layout for industrial operator use
- Error handling for serial disconnection or invalid data frames
- Configuration page for machine settings and diagnostics

---

## 🧩 System Architecture

Raspberry Pi (GUI) - Python 3 / Tkinter - PySerial Library - Visual Studio Environment 

communication protocol- UART / RS232 / RS485

port='/dev/ttyS0',baudrate = 336538,parity= serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0  // port settings

Embedded Controller(LPC2148)- C / C++ Firmware - Sensor & Motor Control -

## Requirement to install

pip install -r requirements.txt
