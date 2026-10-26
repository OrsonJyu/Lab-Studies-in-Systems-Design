#include <IO_Control.h>

// Task 1: absolute first invocation at 1500 ms; retain the 100 ms interval.
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  Serial.print("Welcome, current time since start = ");
  Serial.println(_ctrl.getUpdateTime());
});

void setup() {
  IO_Control.begin();
  Serial.begin(115200);
  IO_Control.enableScheduler(1500, 100, iocontrolHandler);
}
void loop() {}
