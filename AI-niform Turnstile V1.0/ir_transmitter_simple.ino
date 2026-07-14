/*
 * Simple IR Remote Transmitter
 * Transmits IR codes using the same protocol as the receiver
 * 
 * Hardware Setup:
 * - IR LED connected to pin 4 (through a resistor ~220-330 ohms)
 * - Ground connected to ground
 * 
 * This transmitter sends codes in the same format that the receiver expects
 */

const int irPin = 4;

void setup() {
  Serial.begin(115200);
  pinMode(irPin, OUTPUT);
  digitalWrite(irPin, LOW);
  
  Serial.println("IR Transmitter Ready");
  Serial.println("Enter a code to transmit:");
  Serial.println("- Decimal: 1779");
  Serial.println("- Hex: F720DF or 0xF720DF");
  Serial.println("Auto-testing red code (F720DF) every 3 seconds...");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readString();
    input.trim();
    
    if (input.length() > 0) {
      unsigned long codeToSend = 0;
      
      // Check if input is hexadecimal (starts with 0x or contains letters)
      if (input.startsWith("0x") || input.startsWith("0X")) {
        codeToSend = strtoul(input.c_str(), NULL, 16);
        Serial.print("Transmitting hex code: 0x");
        Serial.println(codeToSend, HEX);
      } else if (input.indexOf("ABCDEFabcdef") >= 0) {
        // Contains hex characters
        codeToSend = strtoul(input.c_str(), NULL, 16);
        Serial.print("Transmitting hex code: 0x");
        Serial.println(codeToSend, HEX);
      } else {
        // Decimal input
        codeToSend = input.toInt();
        Serial.print("Transmitting decimal code: ");
        Serial.println(codeToSend);
      }
      
      if (codeToSend != 0) {
        sendIrCode(codeToSend);
      }
    }
  }
  
  // Test with red code (F720DF) every 3 seconds
  static unsigned long lastTest = 0;
  if (millis() - lastTest > 3000) {
    Serial.println("Auto-testing red code (F720DF)...");
    sendIrCode(0xF720DF);
    lastTest = millis();
  }
}

void sendIrCode(int code) {
  // Send start pulse (LOW for > 5000 microseconds) - this is what the receiver looks for
  digitalWrite(irPin, LOW);
  delayMicroseconds(9000); // 9ms start pulse
  
  // Send 32 data bits - the receiver expects exactly 32 bits
  for (int i = 31; i >= 0; i--) {
    // Send HIGH pulse first
    digitalWrite(irPin, HIGH);
    delayMicroseconds(600); // 600us HIGH
    
    // Send LOW pulse (length depends on bit value)
    digitalWrite(irPin, LOW);
    if (code & (1 << i)) {
      delayMicroseconds(1600); // 1.6ms for bit '1'
    } else {
      delayMicroseconds(600);  // 600us for bit '0'
    }
  }
  
  // End with LOW
  digitalWrite(irPin, LOW);
  delayMicroseconds(600);
  
  // Add delay between transmissions
  delay(250); // Match the delay in your receiver
}

// Alternative function to send predefined codes
void sendPredefinedCode(int codeNumber) {
  int codes[] = {
    0x00000001,  // Code 1
    0x00000002,  // Code 2
    0x00000004,  // Code 3
    0x00000008,  // Code 4
    0x00000010,  // Code 5
    0x00000020,  // Code 6
    0x00000040,  // Code 7
    0x00000080,  // Code 8
    0x00000100,  // Code 9
    0x00000200,  // Code 10
  };
  
  if (codeNumber >= 1 && codeNumber <= 10) {
    Serial.print("Sending predefined code ");
    Serial.print(codeNumber);
    Serial.print(": 0x");
    Serial.println(codes[codeNumber - 1], HEX);
    sendIrCode(codes[codeNumber - 1]);
  } else {
    Serial.println("Invalid code number. Use 1-10");
  }
}
