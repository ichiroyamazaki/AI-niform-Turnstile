const int MOSFET_PIN = 7; // your control pin

void setup() {
  pinMode(MOSFET_PIN, OUTPUT);
  digitalWrite(MOSFET_PIN, LOW);
  
  // Initialize serial communication
  Serial.begin(9600);
  
  // Wait for serial connection (optional, for debugging)
  while (!Serial) {
    ; // wait for serial port to connect
  }
  
  Serial.println("Solenoid Controller Ready");
  Serial.println("Commands: ON, OFF");
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace
    
    if (command == "ON") {
      digitalWrite(MOSFET_PIN, HIGH); // solenoid ON
      Serial.println("Solenoid: ON");
    }
    else if (command == "OFF") {
      digitalWrite(MOSFET_PIN, LOW);  // solenoid OFF
      Serial.println("Solenoid: OFF");
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(10);
}
