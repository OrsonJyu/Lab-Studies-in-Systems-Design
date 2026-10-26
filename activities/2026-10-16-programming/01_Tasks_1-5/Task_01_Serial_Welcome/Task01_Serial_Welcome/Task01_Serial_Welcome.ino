// SD5531 | In-Class Activity 6 | Task 1 | 16 Oct 2026
#include <IO_Control.h>
// First invocation at 1500ms; subsequent invocations every 100ms.
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  Serial.print("Welcome, current time since start = ");
  Serial.println(_ctrl.getUpdateTime());
});
void setup() {
  IO_Control.begin();
  Serial.begin(115200);
  Serial.println(); // Separate the output from the ESP32 boot messages.
  IO_Control.enableScheduler(1500, 100, iocontrolHandler);
}
void loop() {}
