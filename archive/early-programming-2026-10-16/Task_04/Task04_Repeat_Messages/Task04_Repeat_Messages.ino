#include <IO_Control.h>
#include "InputHelpers.h"

SerialLineReader inputReader;
int state = 0;
long repeatsRemaining = 0;

DeclareHandler(printNextMessage, _ctrl, IOControl, {
  if (repeatsRemaining <= 0) return;
  switch (state) {
    case 0: Serial.println("hello"); state = 1; break;
    case 1: Serial.println("world"); state = 2; break;
    case 2:
      Serial.println("!!!"); state = 0; repeatsRemaining--; break;
  }
  if (repeatsRemaining > 0)
    _ctrl.setTimeoutByRelTime(0, printNextMessage, 1000, true);
});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (!inputReader.read(input)) return;
  long count;
  if (!parseInteger(input, count) || count < 1) {
    Serial.println("Please enter a positive integer (>=1).");
    return;
  }
  // A new valid input restarts the sequence with the requested exact count.
  _ctrl.stopTimeout(0);
  state = 0; repeatsRemaining = count;
  _ctrl.setTimeoutByRelTime(0, printNextMessage, 0, true);
});
void setup() {
  IO_Control.begin();
  Serial.begin(115200);
  // No startup banner or idle output, as required by Task 4.
  IO_Control.enableScheduler(0, 1, iocontrolHandler, 1);
}
void loop() {}
