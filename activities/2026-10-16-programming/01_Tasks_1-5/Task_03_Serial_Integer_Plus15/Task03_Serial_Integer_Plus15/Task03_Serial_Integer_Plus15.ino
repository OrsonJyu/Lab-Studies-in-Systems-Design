// SD5531 | In-Class Activity 6 | Task 3 | 16 Oct 2026
#include "SerialInput.h"
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (!readCommand(input)) return;
  long number = input.toInt(); // Required Arduino String function.
  // Widen before addition, so even LONG_MAX + 15 is well-defined.
  long long result = (long long)number + 15LL;
  Serial.print("Input: "); Serial.println(input);
  Serial.print("Result: "); Serial.printf("%lld\n", result);
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  IO_Control.enableScheduler(0, 10, iocontrolHandler);
}
void loop() {}
