#include <IRremote.hpp>

#define IR_SEND_PIN 7

struct IrCmd {
  uint16_t address;
  uint8_t command;
  const char *name;
};

IrCmd seq[] = {
  {0xEF00, 0x2,  "POWER OFF"},
  {0xEF00, 0x3,  "POWER ON"},
  {0xEF00, 0x4,  "RED"},
  {0xEF00, 0x5,  "GREEN"},
  {0xEF00, 0xB,  "FLASH MODE"},
  {0xEF00, 0x13, "FADE MODE"}
};

const int cmdCount = sizeof(seq) / sizeof(seq[0]);
const unsigned long delayMs = 5000; // 5 seconds

void setup() {
  Serial.begin(115200);
  IrSender.begin(IR_SEND_PIN, ENABLE_LED_FEEDBACK);
  Serial.println("IR sequence ready.");
}

void loop() {
  for (int i = 0; i < cmdCount; ++i) {
    Serial.print("Sending: ");
    Serial.println(seq[i].name);
    IrSender.sendNEC(seq[i].address, seq[i].command, 0); // 0 repeats
    delay(delayMs);
  }
}
