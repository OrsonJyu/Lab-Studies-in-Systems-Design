#include <IO_Control.h>

int state = 0;
// Time targets are measured from CPU start, not from the previous message.
const ulong_t messageTime[] = {2000, 3000, 3500, 4000, 4500, 5500};
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  if (state >= 6 || _ctrl.getUpdateTime() < messageTime[state]) return;
  Serial.print("At t = ");
  Serial.print(_ctrl.getUpdateTime());
  Serial.print(", ");
  switch (state) {
    case 0: Serial.println("Hello"); break;
    case 1: Serial.println("from"); break;
    case 2: Serial.println("\"School"); break;
    case 3: Serial.println("of"); break;
    case 4: Serial.println("Design\""); break;
    case 5: Serial.println("!!!"); break;
  }
  state++; // one complete sequence, then stay idle until reset
});
void setup() {
  IO_Control.begin();
  Serial.begin(115200);
  IO_Control.enableScheduler(2000, 1, iocontrolHandler);
}
void loop() {}
