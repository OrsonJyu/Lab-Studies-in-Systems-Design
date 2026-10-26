# Task 3: Serial Integer Plus15

Open `Task03_Serial_Integer_Plus15/Task03_Serial_Integer_Plus15.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Send `10`, `-20`, `0`, `123abc`, `abc` on separate lines. Expected results: 25, -5, 15, 138, 15. Arduino String::toInt() converts an initial numeric portion to long and returns 0 when no numeric conversion is possible. Use representable 32-bit long inputs; out-of-range conversion is not a validation mechanism. Required evidence: real Serial Monitor screenshot including input/result pairs. Documentation: https://docs.arduino.cc/language-reference/en/variables/data-types/stringObject/Functions/toInt/

## Submission

Upload the ZIP in this folder under the Task 3 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
