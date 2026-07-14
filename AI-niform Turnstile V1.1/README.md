# Solenoid Controller

A Python GUI application to control a solenoid via Arduino with ON/OFF buttons.

## Hardware Setup

1. Connect your MOSFET to Arduino pin 7
2. Connect the solenoid to the MOSFET circuit
3. Upload the `solenoid_arduino.ino` code to your Arduino

## Software Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Python application:
   ```bash
   python solenoid_controller.py
   ```

## Usage

1. Connect your Arduino to your computer via USB
2. Open the Python application
3. Select the correct COM port from the dropdown
4. Click "Connect" to establish serial communication
5. Use the "SOLENOID ON" and "SOLENOID OFF" buttons to control the solenoid

## Features

- **Serial Communication**: Communicates with Arduino via USB serial
- **Auto-Connect**: Automatically detects and connects to available ports
- **Visual Feedback**: Shows connection status and solenoid state
- **Safe Shutdown**: Automatically turns off solenoid when closing the application
- **Error Handling**: Displays connection errors and handles disconnections gracefully

## Arduino Code

The Arduino code has been enhanced to:
- Accept serial commands ("ON" and "OFF")
- Provide feedback via serial communication
- Handle unknown commands gracefully
- Maintain the original solenoid control functionality

## Troubleshooting

- Make sure the Arduino is connected and the correct COM port is selected
- Check that the Arduino code is uploaded and running
- Ensure the MOSFET is properly connected to pin 7
- Verify the solenoid circuit is working correctly
