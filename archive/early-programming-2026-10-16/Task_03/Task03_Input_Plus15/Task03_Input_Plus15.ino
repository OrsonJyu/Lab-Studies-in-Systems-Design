#include <IO_Control.h>
#include "InputHelpers.h"

SerialLineReader inputReader;
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (!inputReader.read(input)) return;
  // Required by Task 3: use String.toInt(), including its documented behavior.
  long integerNumber = input.toInt();
  int64_t result = (int64_t)integerNumber + 15; // avoid signed 32-bit addition overflow
  Serial.print("Input: "); Serial.println(input);
  Serial.print("Integer: "); Serial.println(integerNumber);
  Serial.print("Result (+15): "); Serial.printf("%lld\n", (long long)result);
});
void setup() {
  IO_Control.begin();
  Serial.begin(115200);
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
