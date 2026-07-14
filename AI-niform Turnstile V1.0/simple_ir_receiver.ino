/*
 * Simple IR Remote Receiver (No Library Required)
 * Receives IR signals from remote control on pin 12
 * 
 * Hardware Setup:
 * - IR receiver module connected to pin 12
 * - Common IR receiver modules: TSOP4838, TSOP38238, etc.
 */

const int IR_RECEIVE_PIN = 12;
const int LED_PIN = 13; // Built-in LED

// Variables for timing
unsigned long lastTime = 0;
unsigned long currentTime = 0;
unsigned long pulseTime = 0;

// Variables for signal detection
bool signalDetected = false;
int signalCount = 0;
unsigned long signalStart = 0;
unsigned long signalEnd = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set pin modes
  pinMode(IR_RECEIVE_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("Simple IR Remote Receiver Started");
  Serial.println("Point your remote at the receiver and press a button...");
  Serial.println("----------------------------------------");
}

void loop() {
  // Read the IR receiver pin
  int irValue = digitalRead(IR_RECEIVE_PIN);
  
  // Detect falling edge (start of signal)
  if (irValue == LOW && !signalDetected) {
    signalDetected = true;
    signalStart = micros();
    signalCount = 0;
    digitalWrite(LED_PIN, HIGH); // Turn on LED when signal detected
  }
  
  // Count pulses while signal is active
  if (signalDetected && irValue == LOW) {
    signalCount++;
  }
  
  // Detect rising edge (end of signal)
  if (irValue == HIGH && signalDetected) {
    signalDetected = false;
    signalEnd = micros();
    pulseTime = signalEnd - signalStart;
    
    // Print signal information
    Serial.print("Signal detected! ");
    Serial.print("Duration: ");
    Serial.print(pulseTime);
    Serial.print(" microseconds, ");
    Serial.print("Pulses: ");
    Serial.println(signalCount);
    
    digitalWrite(LED_PIN, LOW); // Turn off LED
  }
  
  // Small delay to prevent overwhelming the system
  delayMicroseconds(100);
}

