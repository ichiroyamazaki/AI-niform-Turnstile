const int MOSFET_PIN = 7; // your control pin

void setup() {
  pinMode(MOSFET_PIN, OUTPUT);
  digitalWrite(MOSFET_PIN, LOW);
}

void loop() {
  digitalWrite(MOSFET_PIN, HIGH); // solenoid ON
  delay(1000);
  digitalWrite(MOSFET_PIN, LOW);  // solenoid OFF
  delay(2000);
}
