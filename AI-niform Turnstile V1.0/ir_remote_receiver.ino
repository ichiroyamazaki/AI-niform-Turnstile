/*
 * Simple IR Remote Receiver
 * Receives IR codes and displays them on serial monitor
 * 
 * Hardware Setup:
 * - IR receiver module connected to pin 12
 * - Common IR receiver modules: TSOP4838, TSOP38238, etc.
 * 
 * Library Required:
 * - IRremote library by z3t0
 * - Install via Arduino IDE Library Manager
 */

#include <IRremote.h>

// Pin definitions
const int IR_RECEIVE_PIN = 12;

// Create IR receiver object
IRrecv irrecv(IR_RECEIVE_PIN);

// Create decode results object
decode_results results;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize IR receiver
  irrecv.enableIRIn();
  
  Serial.println("IR Remote Receiver Started");
  Serial.println("Press any button on your remote...");
}

void loop() {
  // Check if IR signal is received
  if (irrecv.decode(&results)) {
    // Print only the IR code
    Serial.println(results.value, HEX);
    
    // Resume receiving
    irrecv.resume();
  }
}
