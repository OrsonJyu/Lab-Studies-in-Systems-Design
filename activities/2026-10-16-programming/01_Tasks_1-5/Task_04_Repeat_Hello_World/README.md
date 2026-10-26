# Task 4: Repeat Hello World

Open `Task04_Repeat_Hello_World/Task04_Repeat_Hello_World.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Record from reset: there must be no startup text. Send `2`: Hello / world / !!! appears twice at 1-second message intervals, then stops. Send `0`, `-1`, `2.5`, `abc`, and an empty line: each must request a positive integer without starting a new sequence. Send `1`: exactly one complete sequence. A new valid command during playback restarts at Hello using the new count; invalid commands leave any current playback running. Required evidence: a real Serial Monitor video showing silence, valid count, invalid input and stopping.

## Submission

Upload the ZIP in this folder under the Task 4 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
