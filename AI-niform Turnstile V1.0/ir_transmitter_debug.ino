/*
 * IR Remote Transmitter with Debug
 * Sends IR codes and includes debugging features
 */

#include <IRremote.h>

// Pin definitions
const int IR_TRANSMIT_PIN = 12;
const int LED_PIN = 13; // Built-in LED for visual feedback

// Create IR sender object
IRsend irsend;

// Variables for serial input
String inputString = "";
boolean stringComplete = false;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set pin modes
  pinMode(LED_PIN, OUTPUT);
  pinMode(IR_TRANSMIT_PIN, OUTPUT);
  
  // Reserve space for input string
  inputString.reserve(200);
  
  Serial.println("IR Remote Transmitter with Debug Started");
  Serial.println("Commands:");
  Serial.println("1. Send hex code (e.g., FF00FF)");
  Serial.println("2. Type 'test' to send test signal");
  Serial.println("3. Type 'blink' to test LED");
  Serial.println("----------------------------------------");
}

void loop() {
  // Check for serial input
  if (stringComplete) {
    // Remove any whitespace and convert to uppercase
    inputString.trim();
    inputString.toUpperCase();
    
    Serial.print("Received: ");
    Serial.println(inputString);
    
    // Handle special commands
    if (inputString == "TEST") {
      sendTestSignal();
    } else if (inputString == "BLINK") {
      testLED();
    } else if (isValidHex(inputString)) {
      // Convert hex string to unsigned long
      unsigned long code = strtoul(inputString.c_str(), NULL, 16);
      
      Serial.print("Transmitting: 0x");
      Serial.println(inputString);
      
      // Blink LED to show transmission
      digitalWrite(LED_PIN, HIGH);
      
      // Send the IR code (using NEC protocol as default)
      irsend.sendNEC(IR_TRANSMIT_PIN, code, 32);
      
      // Turn off LED
      digitalWrite(LED_PIN, LOW);
      
      Serial.println("Transmission complete!");
    } else {
      Serial.println("Invalid input! Try:");
      Serial.println("- Hex code (e.g., FF00FF)");
      Serial.println("- 'test' for test signal");
      Serial.println("- 'blink' for LED test");
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

// Function to send test signal
void sendTestSignal() {
  Serial.println("Sending test signal...");
  digitalWrite(LED_PIN, HIGH);
  
  // Send a simple test code
  irsend.sendNEC(IR_TRANSMIT_PIN, 0xFF00FF, 32);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("Test signal sent!");
}

// Function to test LED
void testLED() {
  Serial.println("Testing LED...");
  for (int i = 0; i < 5; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
  Serial.println("LED test complete!");
}
