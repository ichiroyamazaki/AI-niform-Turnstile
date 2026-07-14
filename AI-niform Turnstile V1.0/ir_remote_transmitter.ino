/*
 * IR Remote Transmitter
 * Sends IR codes received from serial monitor on pin 12
 * 
 * Hardware Setup:
 * - IR LED connected to pin 12 through a resistor (220-330 ohms)
 * - IR LED cathode to ground, anode to pin 12 through resistor
 * 
 * Library Required:
 * - IRremote library by z3t0
 * - Install via Arduino IDE Library Manager
 * 
 * Usage:
 * - Send hex codes via serial monitor (e.g., FF00FF)
 * - Code will be transmitted as IR signal
 */

#include <IRremote.h>

// Pin definitions
const int IR_TRANSMIT_PIN = 12;

// Create IR sender object
IRsend irsend;

// Variables for serial input
String inputString = "";
boolean stringComplete = false;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Reserve space for input string
  inputString.reserve(200);
  
  Serial.println("IR Remote Transmitter Started");
  Serial.println("Send hex codes via serial monitor (e.g., FF00FF)");
  Serial.println("----------------------------------------");
}

void loop() {
  // Check for serial input
  if (stringComplete) {
    // Remove any whitespace and convert to uppercase
    inputString.trim();
    inputString.toUpperCase();
    
    // Check if input is valid hex
    if (isValidHex(inputString)) {
      // Convert hex string to unsigned long
      unsigned long code = strtoul(inputString.c_str(), NULL, 16);
      
      Serial.print("Transmitting: 0x");
      Serial.println(inputString);
      
      // Send the IR code (using NEC protocol as default)
      irsend.sendNEC(IR_TRANSMIT_PIN, code, 32);
      
      Serial.println("Transmission complete!");
    } else {
      Serial.println("Invalid hex code! Please send valid hex (e.g., FF00FF)");
    }
    
    // Clear the string
    inputString = "";
    stringComplete = false;
  }
}

// Function to read serial input
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

// Function to validate hex string
boolean isValidHex(String str) {
  if (str.length() == 0) return false;
  
  for (int i = 0; i < str.length(); i++) {
    char c = str.charAt(i);
    if (!((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F'))) {
      return false;
    }
  }
  return true;
}
