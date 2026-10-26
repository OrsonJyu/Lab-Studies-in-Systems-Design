// SD5531 | In-Class Activity 6 | Task 2 | 16 Oct 2026
#include <IO_Control.h>
int state = 0;
const ulong_t dueTimes[] = {2000, 3000, 3500, 4000, 4500, 5500};
// Quote characters are literal output, escaped in C++ strings.
const char *messages[] = {"Hello", "from", "\"School", "of", "Design\"", "!!!"};
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  if (state >= 6 || _ctrl.getUpdateTime() < dueTimes[state]) return;
  if (state == 0) Serial.println(); // Separate output from ESP32 ROM boot bytes.
  Serial.print("At t = ");
  Serial.print(_ctrl.getUpdateTime());
  Serial.print(", ");
  switch (state) {
    case 0: case 1: case 2: case 3: case 4: case 5:
      Serial.println(messages[state]); ++state; break;
    default: break;
  }
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  IO_Control.enableScheduler(2000, 1, iocontrolHandler);
}
void loop() {}
