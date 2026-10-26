// SD5531 | In-Class Activity 6 | Task 4 | 16 Oct 2026
#include "SerialInput.h"
int state = 0;
long remaining = 0;
ulong_t nextMessage = 0;
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (readCommand(input)) {
    long requested;
    if (!parseInteger(input, requested) || requested < 1) {
      Serial.println("Please enter a positive integer (>= 1).");
    } else {
      // A new valid command restarts the sequence with the new count.
      remaining = requested; state = 0; nextMessage = _ctrl.getUpdateTime();
    }
  }
  if (remaining == 0 || (long)(_ctrl.getUpdateTime() - nextMessage) < 0) return;
  switch (state) {
    case 0: Serial.println("Hello"); state = 1; break;
    case 1: Serial.println("world"); state = 2; break;
    case 2: Serial.println("!!!"); --remaining; state = 0; break;
  }
  nextMessage = _ctrl.getUpdateTime() + 1000;
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  // No startup text: remain silent until user input.
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
