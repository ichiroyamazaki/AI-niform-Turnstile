#include <IRremote.hpp>

#define IR_SEND_PIN 8  // LED strip control pin
#define MOSFET_PIN 7   // Solenoid control pin

struct IrCmd {
  uint16_t address;
  uint8_t command;
  const char *name;
};

IrCmd seq[] = {
  {0xEF00, 0x2,  "POWER OFF"},
  {0xEF00, 0x3,  "POWER ON"},
  {0xEF00, 0x4,  "RED"},
  {0xEF00, 0x5,  "GREEN"}
};

const int cmdCount = sizeof(seq) / sizeof(seq[0]);
bool systemInitialized = false;

void setup() {
  pinMode(MOSFET_PIN, OUTPUT);
  digitalWrite(MOSFET_PIN, LOW);
  
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize IR sender
  IrSender.begin(IR_SEND_PIN, ENABLE_LED_FEEDBACK);
  
  // Wait for serial connection (optional, for debugging)
  while (!Serial) {
    ; // wait for serial port to connect
  }
  
  Serial.println("Solenoid & LED Controller Ready");
  Serial.println("Commands: ON, OFF, LED_ON, LED_OFF, LED_RED, LED_GREEN");
  
  // Send initial sequence: Power On + Red
  sendInitialSequence();
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace
    
    if (command == "ON") {
      digitalWrite(MOSFET_PIN, HIGH); // solenoid ON
      sendLEDCommand("GREEN"); // Send Green when solenoid ON
      Serial.println("Solenoid: ON, LED: GREEN");
    }
    else if (command == "OFF") {
      digitalWrite(MOSFET_PIN, LOW);  // solenoid OFF
      sendLEDCommand("RED"); // Send Red when solenoid OFF
      Serial.println("Solenoid: OFF, LED: RED");
    }
    else if (command == "LED_ON") {
      sendLEDCommand("POWER_ON");
      Serial.println("LED: POWER ON");
    }
    else if (command == "LED_OFF") {
      sendLEDCommand("POWER_OFF");
      Serial.println("LED: POWER OFF");
    }
    else if (command == "LED_RED") {
      sendLEDCommand("RED");
      Serial.println("LED: RED");
    }
    else if (command == "LED_GREEN") {
      sendLEDCommand("GREEN");
      Serial.println("LED: GREEN");
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(10);
}

void sendInitialSequence() {
  // Send Power On + Red immediately on startup
  Serial.println("Sending initial sequence: POWER ON + RED");
  IrSender.sendNEC(seq[1].address, seq[1].command, 0); // POWER ON
  delay(100); // Small delay between commands
  IrSender.sendNEC(seq[2].address, seq[2].command, 0); // RED
  systemInitialized = true;
}

void sendLEDCommand(const char* command) {
  if (strcmp(command, "POWER_ON") == 0) {
    IrSender.sendNEC(seq[1].address, seq[1].command, 0);
  }
  else if (strcmp(command, "POWER_OFF") == 0) {
    IrSender.sendNEC(seq[0].address, seq[0].command, 0);
  }
  else if (strcmp(command, "RED") == 0) {
    IrSender.sendNEC(seq[2].address, seq[2].command, 0);
  }
  else if (strcmp(command, "GREEN") == 0) {
    IrSender.sendNEC(seq[3].address, seq[3].command, 0);
  }
}
